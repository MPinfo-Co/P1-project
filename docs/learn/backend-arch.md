# P1-code 後端架構說明

## 系統是做什麼的？

這個後端是一套「**資安事件自動偵測平台**」。它會：
1. 接收來自外部的 syslog 資料（防火牆 FortiGate、Windows 事件日誌）
2. 用 AI（Claude Haiku）把 log 分析成「資安事件」
3. 每天凌晨用另一個 AI（Claude Sonnet）做最終彙整、去重
4. 把結果存進資料庫，提供前端查詢

---

## 技術棧一覽

| 元件 | 用途 | 選型 |
|------|------|------|
| Web API | 接收 HTTP 請求 | FastAPI (Python) |
| 資料庫 | 儲存資料 | PostgreSQL 15 |
| 訊息佇列 | 工作排程 | Redis 7 |
| 背景任務 | 定時執行 AI 分析 | Celery |
| AI 快速分析 | 分析原始 log | Claude Haiku |
| AI 深度彙整 | 每日最終事件 | Claude Sonnet |

---

## 目錄結構

```
backend/
├── app/
│   ├── main.py            # 程式入口，組裝所有 API
│   ├── api/               # 對外的 HTTP 端點
│   │   ├── auth.py        # 登入 / 登出
│   │   ├── users.py       # 使用者管理
│   │   ├── roles.py       # 角色管理
│   │   ├── events.py      # 查詢資安事件
│   │   ├── ingest.py      # 接收外部 log 資料
│   │   ├── functions.py   # 功能權限管理
│   │   └── health.py      # 健康檢查
│   ├── core/              # 核心設定
│   │   ├── config.py      # 從 .env 讀取設定值
│   │   ├── security.py    # 密碼加密、JWT Token 產生/驗證
│   │   └── deps.py        # 「誰在呼叫？」依賴注入
│   ├── db/                # 資料庫層
│   │   ├── session.py     # 建立資料庫連線
│   │   └── models/        # 資料表定義
│   │       ├── user.py    # User, Role, UserRole, Function, RoleFunction
│   │       ├── security_event.py  # LogBatch, FlashResult, SecurityEvent, 等
│   │       └── token_blacklist.py # 登出的 Token 黑名單
│   ├── schemas/           # 資料格式驗證（輸入/輸出的形狀）
│   ├── services/          # 呼叫 AI 的邏輯
│   │   ├── claude_flash.py  # 呼叫 Haiku 分析 log
│   │   └── claude_pro.py    # 呼叫 Sonnet 做每日彙整
│   ├── tasks/             # 背景工作
│   │   ├── flash_task.py  # 接到 log → 切 chunk → 送 Haiku
│   │   └── pro_task.py    # 每天凌晨的 Sonnet 任務
│   ├── worker.py          # Celery App 設定（定時排程在這裡）
│   └── logger_utils/      # 日誌系統（system / user / service 三種頻道）
├── alembic/               # 資料庫版本管理（Schema 異動歷史）
└── tests/                 # 自動化測試
```

---

## 層次架構

```
HTTP 請求
    │
    ▼
[api/]          ← 接收請求、驗證身份、呼叫下一層
    │
    ▼
[tasks/]        ← 處理複雜邏輯（切 chunk、合併事件）
    │
    ▼
[services/]     ← 呼叫外部 AI API（Anthropic）
    │
    ▼
[db/]           ← 讀寫 PostgreSQL
```

---

## 資料庫 Schema 關係

### 使用者 & 權限系統

```
users ──┬──< user_roles >──── roles ──< role_functions >── functions
        │
        └── token_blacklist（登出的 token 記錄）
```

- 一個 user 可以有多個 role（角色）
- 一個 role 可以有多個 function（功能權限）
- 功能權限名稱範例：`fn_user`（管理使用者）、`fn_role`（管理角色）

### 資安事件流水線

```
LogBatch（一次 ingest 為一個 batch）
    └──< FlashResult（每個 chunk 的 Haiku 分析結果）
            │  chunk_index = -1 → 當天累計匯總
            │  chunk_index = 999 → 一個 batch 的合併結果
            └── events（JSONB 欄位，存 AI 輸出的事件陣列）

SecurityEvent（最終確認的資安事件）
    └──< EventHistory（每次狀態變更 / 備註記錄）
DailyAnalysis（每日 Pro Task 執行紀錄）
```

---

## 核心流程：Log 進來到事件產生

```
外部 adapter
    │  POST /api/ingest（帶 X-Ingest-Key 驗證）
    ▼
ingest.py
    │
    ▼
flash_task._process_ingest()
    ├── 建立 LogBatch 記錄
    ├── 依 analysis_mode 切 chunk（每批最多 300 筆）
    │       ├── full 模式：FortiGate 彙總摘要 + Windows log
    │       └── windows_only 模式：只有 Windows，不切 chunk
    ├── 每個 chunk → _process_chunk()
    │       ├── 建 FlashResult（status=pending）
    │       ├── 呼叫 claude_flash.analyze_chunk()（Haiku 分析）
    │       ├── _override_match_keys()（程式產的 match_key 覆蓋 AI 的）
    │       └── _attach_raw_logs()（帶原始 log 溯源）
    ├── _merge_events()（同 match_key 的事件合併）
    └── _update_daily_accumulator()（更新當天累計 FlashResult）

每天凌晨 02:00（Celery beat 觸發）
    │
    ▼
pro_task.run_pro_task()
    ├── 讀取當天 chunk_index=-1 的累計 FlashResult
    ├── 呼叫 claude_pro.aggregate_daily()（Sonnet 最終彙整）
    └── 寫入 security_events 資料表
            ├── 同 match_key 且未結案 → UPDATE（延續事件）
            └── 否則 → INSERT（新事件）
```

---

## 身份驗證機制

```
登入 POST /api/auth/login
    → 驗證 email + password（bcrypt）
    → 產生 JWT Token（有效期 60 分鐘，預設）
    → 回傳 { access_token: "..." }

後續每個需要登入的請求
    → Header: Authorization: Bearer <token>
    → deps.get_current_user()
        ├── 檢查 token 是否在黑名單（token_blacklist）
        ├── 解析 JWT，取出 user_id
        └── 查詢 users 資料表確認帳號存在且 is_active=true

登出 POST /api/auth/logout
    → 把當前 token 記入 token_blacklist（下次帶這個 token 就會被擋）
```

---

## 部署架構（Docker Compose）

```
┌─────────────────────────────────────┐
│  docker-compose                     │
│                                     │
│  ┌─────────┐   ┌─────────────────┐  │
│  │   db    │   │      api        │  │
│  │Postgres │   │ FastAPI:8000    │  │
│  └────┬────┘   └────────┬────────┘  │
│       │                 │           │
│  ┌────┴────┐   ┌────────┴────────┐  │
│  │  redis  │   │    worker       │  │
│  │ :6379   │   │ Celery Worker   │  │
│  └────┬────┘   └─────────────────┘  │
│       │                             │
│  ┌────┴────────────────────────┐    │
│  │         beat                │    │
│  │  Celery Beat（定時觸發）    │    │
│  └─────────────────────────────┘    │
└─────────────────────────────────────┘
```

- **api**：處理 HTTP 請求
- **worker**：執行背景任務（Pro Task 就在這裡跑）
- **beat**：每天凌晨 02:00 觸發 Pro Task
- **db**：資料永久儲存
- **redis**：api / beat / worker 三者的溝通橋梁
