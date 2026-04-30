# P1-code 後端架構說明

> 快速查詢用。詳細說明與流程解析請見 [backend-tutorial.md](backend-tutorial.md)

---

## 技術選型

| 工具 | 用途 |
|------|------|
| **FastAPI** | Python Web 框架，自動產生 API 文件（/docs） |
| **SQLAlchemy** | ORM，用 Python class 操作資料庫，不用寫 SQL |
| **Pydantic** | 資料格式驗證，定義 API 的 request / response 結構 |
| **Loguru** | 日誌系統，依用途分 channel 寫到不同 log 檔 |
| **Alembic** | 資料庫版本控制，追蹤 schema 的變更歷史 |
| **python-jose** | JWT（JSON Web Token）簽發與驗證 |
| **pydantic-settings** | 從 `.env` 檔讀取環境變數 |

---

## 分層架構

```
HTTP Request
     │
     ▼
┌─────────────────────────────┐
│  進入點  app/main.py         │  組裝 FastAPI app、掛上所有 router 和 middleware
└─────────────────────────────┘
     │
     ▼
┌─────────────────────────────┐
│  中介層  app/middlewares/    │  每個請求進門後的第一關：記 log、標準化錯誤碼
└─────────────────────────────┘
     │
     ▼
┌─────────────────────────────┐
│  API 層  app/api/            │  各功能的路由（auth / user / notice / events…）
│  Schema   app/api/schema/   │  Pydantic 驗證 request body 與 response 格式
└─────────────────────────────┘
     │
     ▼
┌─────────────────────────────┐
│  工具層  app/utils/          │  JWT 驗證、密碼雜湊等共用函式
└─────────────────────────────┘
     │
     ▼
┌─────────────────────────────┐
│  資料庫層  app/db/           │  connector.py 管連線；models/ 定義資料表 ORM
└─────────────────────────────┘

全域支援（任何層都可呼叫）
  app/config/settings.py   — 讀取 .env 設定
  app/logger_utils/        — 日誌 channel 管理
  bpBoxAlembic/            — 資料庫 migration
```

---

## 目錄結構

```
backend/
├── app/
│   ├── main.py                        # 進入點，建立 FastAPI app
│   ├── config/
│   │   └── settings.py                # 環境變數（DATABASE_URL, JWT_SECRET_KEY…）
│   ├── middlewares/
│   │   └── request_response_handler.py # 請求/回應 log + 4xx 錯誤碼標準化
│   ├── api/
│   │   ├── auth.py                    # POST /auth/login、/auth/logout
│   │   ├── user.py                    # GET/POST/PATCH/DELETE /user
│   │   ├── notice.py                  # GET/POST /api/notices
│   │   ├── events.py                  # /events（預留）
│   │   ├── ingest.py                  # /ingest（預留）
│   │   ├── health.py                  # GET /health → {"status": "ok"}
│   │   └── schema/                    # Pydantic request/response 定義
│   │       ├── auth.py
│   │       ├── user.py
│   │       ├── notice.py
│   │       └── …
│   ├── db/
│   │   ├── connector.py               # engine、SessionLocal、get_db()
│   │   └── models/
│   │       ├── base.py                # SQLAlchemy DeclarativeBase
│   │       ├── fn_user_role.py        # User, Role, UserRole, TokenBlacklist
│   │       ├── fn_notice.py           # Notice
│   │       └── fn_*.py                # 其他功能的 model
│   ├── utils/
│   │   └── util_store.py              # authenticate(), hash_password(), create_access_token()
│   └── logger_utils/
│       ├── log_channels.py            # get_system_logger(), get_user_logger()…
│       └── logger_config.json         # log 格式、rotation、retention 設定
├── bpBoxAlembic/                      # Alembic migration 設定與版本檔
├── logs/                              # 執行時產生的 log 檔
├── tests/                             # pytest 測試
├── .env                               # 環境變數（不進版控）
├── pyproject.toml                     # 專案設定、依賴管理
└── dockerfile                         # 容器化部署設定
```

---

## API 端點一覽

| Method | Path | 說明 | 需要登入 |
|--------|------|------|---------|
| POST | `/auth/login` | 登入，回傳 JWT token | ✗ |
| POST | `/auth/logout` | 登出，token 加入黑名單 | ✓ |
| GET | `/user` | 查詢用戶列表（可過濾） | ✓ |
| POST | `/user` | 建立新用戶 | ✓ |
| PATCH | `/user/{user_id}` | 更新用戶資料 | ✓ |
| DELETE | `/user/{user_id}` | 停用用戶（soft delete） | ✓ |
| GET | `/api/notices` | 查詢有效公告 | ✓ |
| POST | `/api/notices` | 新增公告（需 can_manage_notices 權限） | ✓ |
| GET | `/health` | 健康檢查 | ✗ |

---

## 資料庫 Tables

| Table | Model class | 說明 |
|-------|-------------|------|
| `tb_users` | `User` | 系統帳號 |
| `tb_roles` | `Role` | 角色與權限旗標 |
| `tb_user_roles` | `UserRole` | 用戶↔角色 多對多關聯 |
| `tb_token_blacklist` | `TokenBlacklist` | 已登出的 JWT（靠 jti 識別） |
| `tb_notices` | `Notice` | 系統公告 |

---

## 關鍵概念速查

| 術語 | 一句話說明 |
|------|-----------|
| **JWT** | 登入後伺服器簽發的數位通行證，每次請求帶著它證明身份 |
| **jti** | JWT 的唯一 ID，登出時把這個 ID 存到黑名單，讓 token 失效 |
| **ORM** | 用 Python class 代替寫 SQL，`User` class 對應 `tb_users` 資料表 |
| **Pydantic** | 自動檢查 API 傳進來的資料格式是否正確，不對就直接回 422 |
| **Dependency Injection** | FastAPI 的 `Depends(xxx)`，讓函式自動拿到需要的物件（如 db session） |
| **Middleware** | 在每個請求到達 route 之前/之後執行的攔截層 |
| **Soft delete** | 不實際刪除資料庫紀錄，只把 `is_active` 設為 `false` |
| **Migration** | 資料庫 schema 的版本變更記錄，Alembic 負責執行和回滾 |
