# P1-code 後端架構說明

## 系統是做什麼的？

這個後端是一套「**資安事件管理平台**」的 API 服務。它提供：
- 帳號登入 / 登出（JWT 驗證）
- 使用者與角色管理
- 資安事件查詢與處理
- 系統公告管理
- Log 資料接收（ingest）

---

## 技術棧一覽

| 元件 | 用途 | 選型 |
|------|------|------|
| Web API | 接收 HTTP 請求 | FastAPI (Python) |
| 資料庫 | 儲存資料 | PostgreSQL |
| ORM | Python ↔ 資料庫 | SQLAlchemy |
| Migration | 資料庫版本管理 | Alembic（bpBoxAlembic） |
| 環境變數 | 設定管理 | pydantic-settings |
| JWT | 身份驗證 | python-jose |

---

## 目錄結構

```
backend/
├── app/
│   ├── main.py                        # 程式入口，組裝 app + middleware + routers
│   ├── api/                           # 對外的 HTTP 端點
│   │   ├── auth.py                    # 登入 / 登出
│   │   ├── user.py                    # 使用者管理（CRUD）
│   │   ├── events.py                  # 資安事件查詢與處理
│   │   ├── notice.py                  # 系統公告
│   │   ├── ingest.py                  # 接收外部 log（目前 stub）
│   │   ├── health.py                  # 健康檢查
│   │   └── schema/                    # Pydantic 資料格式定義（與路由並排）
│   │       ├── auth.py
│   │       ├── user.py
│   │       ├── events.py
│   │       ├── notice.py
│   │       └── ingest.py
│   ├── config/
│   │   └── settings.py                # 從 .env 讀取設定值
│   ├── db/
│   │   ├── connector.py               # 資料庫連線與 get_db 依賴
│   │   └── models/
│   │       ├── base.py                # SQLAlchemy DeclarativeBase
│   │       ├── fn_user_role.py        # User, Role, UserRole, TokenBlacklist
│   │       ├── fn_expert_security_event.py  # SecurityEvent, EventHistory
│   │       ├── fn_expert_ssb_pipeline.py    # LogBatch, FlashResult 等
│   │       ├── fn_notice.py           # Notice
│   │       ├── fn_km.py               # 知識庫相關
│   │       └── fn_partner.py          # AI 夥伴相關
│   ├── utils/
│   │   └── util_store.py              # JWT 產生/驗證、密碼、authenticate()
│   ├── middlewares/
│   │   └── request_response_handler.py  # 請求/回應 log + 4xx 正規化
│   └── logger_utils/                  # 日誌系統（system / user / error 頻道）
├── bpBoxAlembic/                      # 資料庫版本管理
│   └── versions/
│       └── 31cf8ba73762_recreate_tables.py
├── tests/                             # 自動化測試
└── requirements.txt
```

---

## 層次架構

```
HTTP 請求
    │
    ▼
[middlewares/]      ← 每個請求都先過這裡：記 log、驗身份、正規化 4xx
    │
    ▼
[api/]              ← 接收請求、呼叫 authenticate()、執行業務邏輯
    │
    ├── [api/schema/]   ← 驗證輸入格式、定義回應格式
    │
    ├── [utils/]        ← JWT 驗證、密碼比對（authenticate 在這裡）
    │
    └── [db/]           ← 讀寫 PostgreSQL
         ├── connector.py   ← 連線管理
         └── models/        ← 資料表定義
```

---

## 資料庫 Schema 關係

### 使用者 & 權限系統

```
tb_users ──< tb_user_roles >── tb_roles
tb_users ──< tb_token_blacklist（登出記錄，存 jti）
```

**權限設計（boolean flag 模式）：**  
角色本身帶有功能旗標，不需要額外的 functions / role_functions 表。

| tb_roles 欄位 | 說明 |
|---|---|
| `can_access_ai` | 可使用 AI 功能 |
| `can_use_kb` | 可使用知識庫 |
| `can_manage_accounts` | 可管理使用者帳號 |
| `can_manage_roles` | 可管理角色 |
| `can_edit_ai` | 可編輯 AI 設定 |
| `can_manage_kb` | 可管理知識庫 |
| `can_manage_notices` | 可發布系統公告 |

### 資安事件

```
tb_security_events（最終事件）
    └──< tb_event_history（每次狀態變更記錄）

tb_log_batches（一次 ingest 批次）
    └──< tb_flash_results（每個 chunk 的 AI 分析結果）
```

---

## 核心機制：身份驗證

```
登入 POST /auth/login
    → 驗證 email + password（SHA-256）
    → 產生 JWT（含 sub=user_id、jti=唯一識別碼）
    → 回傳 access_token

每個需要登入的 API
    → Header: Authorization: Bearer <token>
    → Middleware 解析 token，填入 request.state.user_id
    → API 透過 Depends(authenticate) 取得 AuthContext(user_id, token)
    → 若 jti 在 tb_token_blacklist 中 → 401

登出 POST /auth/logout
    → 把 jti 記入 tb_token_blacklist
```

---

## 核心機制：Middleware

`request_response_handler.py` 每個請求都會執行：

1. **記錄 Request log**（路徑、方法、client IP）
2. **解析 Bearer token**（若有）→ 填入 `request.state.user_id`
3. 轉交路由處理
4. **4xx 正規化**：除 400 / 401 / 403 / 404 之外的 4xx 一律改成 400（避免洩漏細節）
5. **記錄 Response log**（狀態碼）

---

## API 端點總覽

| 路由前綴 | 說明 | 權限 |
|----------|------|------|
| `POST /auth/login` | 登入取得 JWT | 無需登入 |
| `POST /auth/logout` | 登出（撤銷 JWT） | 需登入 |
| `GET/POST/PATCH/DELETE /user` | 使用者 CRUD | 需登入 |
| `GET/PATCH /events` | 資安事件查詢與更新 | 需登入 |
| `GET/POST /events/{id}/history` | 事件歷程 | 需登入 |
| `GET/POST /api/notices` | 系統公告 | GET 需登入；POST 需 `can_manage_notices` |
| `GET /health` | 健康檢查 | 無需登入 |

---

## 部署（docker-compose）

```
┌──────────────────────────────────────┐
│  docker-compose                      │
│                                      │
│  ┌──────────┐   ┌──────────────────┐ │
│  │    db    │   │       api        │ │
│  │ Postgres │   │  FastAPI :8000   │ │
│  └──────────┘   └──────────────────┘ │
└──────────────────────────────────────┘
```

（重構後移除了 Redis / Celery Worker / Beat，後端僅剩 db + api 兩個服務。）
