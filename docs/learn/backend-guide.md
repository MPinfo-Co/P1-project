# MP-Box 後端說明文件

> 本文以「一個資安事件從日誌到畫面」的完整旅程為主線，帶你了解 P1-code 後端各檔案如何串連，以及每個技術框架為什麼在這裡出現。

---

## 目錄

1. [這份文件怎麼讀](#1-這份文件怎麼讀)
2. [技術選型一覽](#2-技術選型一覽)
3. [目錄結構導覽](#3-目錄結構導覽)
4. [主流程走讀](#4-主流程走讀)
   - [4.1 應用程式啟動](#41-應用程式啟動)
   - [4.2 使用者登入與 JWT 認證](#42-使用者登入與-jwt-認證)
   - [4.3 排程任務：拉取日誌（Flash Task）](#43-排程任務拉取日誌flash-task)
   - [4.4 AI 快速分析（Claude Haiku）](#44-ai-快速分析claude-haiku)
   - [4.5 AI 日報彙整（Claude Sonnet）](#45-ai-日報彙整claude-sonnet)
   - [4.6 前端查詢事件](#46-前端查詢事件)
5. [資料庫設計](#5-資料庫設計)
6. [配置管理](#6-配置管理)
7. [測試架構](#7-測試架構)
8. [技術框架速查表](#8-技術框架速查表)

---

## 1. 這份文件怎麼讀

**目標讀者：** 剛接觸 P1-code 後端的開發者，不論是個人學習或新進同事皆適用。

**建議閱讀順序：**
1. 先看「技術選型一覽」，對齊框架認知（5 分鐘）
2. 再看「目錄結構導覽」，建立整體空間感（5 分鐘）
3. 從 4.1 開始按順序走讀主流程（核心，40 分鐘）
4. 讀完後看「資料庫設計」，理解資料如何儲存與關聯
5. 遇到不熟悉的框架，去「技術框架速查表」補充細節

**搭配對照的原始碼：**

| 本文章節 | 對應檔案 |
| --- | --- |
| 4.1 應用程式啟動 | `backend/app/main.py`、`backend/app/worker.py` |
| 4.2 登入認證 | `backend/app/api/auth.py`、`backend/app/core/security.py`、`backend/app/core/deps.py` |
| 4.3 Flash Task | `backend/app/tasks/flash_task.py`、`backend/app/services/ssb_client.py`、`backend/app/services/log_preaggregator.py` |
| 4.4 AI 快速分析 | `backend/app/services/claude_flash.py` |
| 4.5 AI 日報彙整 | `backend/app/services/claude_pro.py` |
| 4.6 事件查詢 | `backend/app/api/events.py` |
| 5. 資料庫 | `backend/app/models/`、`backend/alembic/versions/` |
| 6. 配置 | `backend/app/core/config.py`、`backend/.env.example` |
| 7. 測試 | `backend/tests/conftest.py`、`backend/pyproject.toml` |

> 所有檔案路徑皆相對於 `P1-code/` 根目錄。

---

## 2. 技術選型一覽

| 框架／工具                    | 解決什麼問題                                          |
| ------------------------ | ----------------------------------------------- |
| **FastAPI**              | Web 框架：處理 HTTP 請求、自動產生 API 文件、依賴注入              |
| **SQLAlchemy 2.0**       | ORM：用 Python class 操作資料庫，不用手寫 SQL               |
| **Alembic**              | 資料庫版本控制：追蹤 schema 變更歷史，像 git 一樣管理               |
| **PostgreSQL**           | 主要資料庫：存使用者、事件、日誌分析結果                            |
| **Pydantic v2**          | 資料驗證：確保 API 輸入/輸出格式正確，自動型別轉換                    |
| **python-jose + bcrypt** | 安全性：JWT token 簽署驗證、密碼雜湊                         |
| **Celery + Redis**       | 非同步任務：背景定時執行日誌拉取與 AI 分析，不阻塞 API                 |
| **Anthropic SDK**        | AI 整合：呼叫 Claude Haiku（快速分析）與 Sonnet（日報彙整）       |
| **httpx**                | HTTP 客戶端：非同步方式呼叫 SSB 外部 API                     |
| **pytest + pytest-cov**  | 測試：單元測試與覆蓋率報告                                   |
| **Ruff**                 | 程式碼品質：Python linter + formatter，取代 flake8/black |

---

## 3. 目錄結構導覽

```
backend/
├── app/
│   ├── main.py          ← FastAPI 應用入口，組裝路由器與中間件
│   ├── worker.py        ← Celery 設定與排程定義
│   ├── api/             ← HTTP 路由層（接收請求、回傳回應）
│   │   ├── auth.py      ← 登入 / 登出
│   │   ├── events.py    ← 事件查詢 / 更新
│   │   └── health.py    ← 健康檢查
│   ├── core/            ← 應用程式核心工具
│   │   ├── config.py    ← 環境變數設定（Pydantic Settings）
│   │   ├── security.py  ← JWT 建立 / 驗證、密碼雜湊
│   │   └── deps.py      ← FastAPI 依賴注入（get_db、get_current_user）
│   ├── db/
│   │   └── session.py   ← SQLAlchemy engine 與 SessionLocal
│   ├── models/          ← ORM 模型（對應資料庫 table）
│   ├── schemas/         ← Pydantic schema（API 輸入輸出格式）
│   ├── services/        ← 業務邏輯與外部整合
│   │   ├── ssb_client.py         ← 向 SSB 平台拉取日誌
│   │   ├── log_preaggregator.py  ← 日誌預彙總（減少 token 用量）
│   │   ├── claude_flash.py       ← Haiku 快速分析
│   │   └── claude_pro.py         ← Sonnet 日報彙整
│   └── tasks/           ← Celery 非同步任務
│       ├── flash_task.py ← 每 20 分鐘執行的日誌分析
│       └── pro_task.py   ← 每日凌晨 02:00 的日報彙整
├── alembic/             ← 資料庫遷移腳本
├── tests/               ← 測試套件
├── requirements.txt
└── .env.example
```

**分層邏輯：**
- `api/` 只負責接收請求與回傳結果，不寫業務邏輯
- `services/` 負責所有業務邏輯與外部 API 呼叫
- `models/` 定義資料結構（資料庫層）
- `schemas/` 定義 API 格式（HTTP 層）
- `core/` 提供應用程式共用工具

---

## 4. 主流程走讀

### 4.1 應用程式啟動

**檔案：** `app/main.py`

FastAPI 應用啟動時做兩件事：

1. **組裝路由器**：把三個路由器掛載到不同路徑
   ```python
   app.include_router(auth_router, prefix="/api/auth")
   app.include_router(events_router, prefix="/api/events")
   app.include_router(health_router)
   ```

2. **設定 CORS**：允許前端（localhost:5173、Vercel）跨域存取

**Celery Worker（`app/worker.py`）** 是另一個獨立啟動的程序，負責排程任務：

```
Flash Task：每 20 分鐘執行一次
Pro Task：每天凌晨 02:00 執行
```

> 啟動方式：FastAPI 用 `uvicorn` 啟動，Celery Worker 另開一個終端機啟動。兩者透過 Redis 溝通。

---

### 4.2 使用者登入與 JWT 認證

**檔案：** `app/api/auth.py`、`app/core/security.py`、`app/core/deps.py`

**登入流程：**

```
POST /api/auth/login
  → auth.py 接收 email + password
  → 查詢資料庫找 User
  → security.py: bcrypt.checkpw(password, user.password_hash)
  → 驗證成功 → create_access_token({"sub": str(user.id)})
  → 回傳 {"access_token": "...", "token_type": "bearer"}
```

**後續請求的認證流程（依賴注入）：**

```
請求 Header: Authorization: Bearer <token>
  → deps.py: get_current_user()
  → 檢查 TokenBlacklist（這個 token 有沒有登出過？）
  → python-jose: 解碼 JWT，取出 user_id
  → 查詢資料庫確認使用者存在且 is_active=True
  → 回傳 User 物件給路由函式使用
```

**依賴注入是什麼？**

FastAPI 用 `Depends()` 來共用邏輯。路由函式只需要宣告「我需要當前使用者」，框架自動執行 `get_current_user()` 並把結果傳進來：

```python
@router.get("/api/events")
def list_events(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # 這裡的 current_user 和 db 都由 FastAPI 自動注入
    ...
```

**登出流程：**

JWT 無法「撤銷」，所以用黑名單解決——把 token 存進 `token_blacklist` 資料表。之後每次驗證都先查黑名單。

---

### 4.3 排程任務：拉取日誌（Flash Task）

**檔案：** `app/tasks/flash_task.py`、`app/services/ssb_client.py`、`app/services/log_preaggregator.py`

每 20 分鐘，Flash Task 自動執行：

```
1. 確認上次執行的時間範圍（time_to）
2. 建立新的 LogBatch 記錄（status: running）
3. ssb_client.fetch_logs() 從 SSB 平台拉取這段時間的日誌
4. 如果 ANALYSIS_MODE=full：log_preaggregator 彙總 FortiGate 日誌
5. 把日誌切成每批 300 筆（chunk）
6. 逐 chunk 送給 Claude Haiku 分析（詳見 4.4）
7. 程式層合併同 match_key 的事件
8. 儲存結果到 FlashResult（chunk_index=-1 代表當天累計）
```

**SSB 客戶端（`ssb_client.py`）** 負責與 SSB 日誌平台（類 Splunk）溝通，支援：
- Windows AD 事件（登入失敗 4625、密碼變更 4720 等）
- FortiGate 防火牆日誌（允許/阻擋的連線）

**日誌預彙總（`log_preaggregator.py`）**：FortiGate 一次可能有上千筆「同一 IP 被擋」的重複日誌。預彙總把 ~1,500 筆壓縮成 ~20-50 筆摘要，大幅節省送給 AI 的 token 數量。

---

### 4.4 AI 快速分析（Claude Haiku）

**檔案：** `app/services/claude_flash.py`

每個 chunk（最多 300 筆日誌）送給 Claude Haiku 4.5 分析：

```python
# 送出的 prompt 大意：
# 「以下是一批資安日誌，請分析出值得關注的事件，
#   用 JSON 陣列回傳，每筆包含：
#   star_rank(1-5), title, affected_summary,
#   match_key, log_ids, ioc_list, mitre_tags, suggests」
```

**match_key** 是事件的唯一識別鍵，用來做去重與合併：
- Windows 事件：`{event_id}_{username}`（例如 `4625_john`）
- FortiGate 彙總摘要：直接用預彙總的 `group_key`

同一個 `match_key` 的事件會在程式層合併（log_ids 合併，star_rank 取最高值）。

---

### 4.5 AI 日報彙整（Claude Sonnet）

**檔案：** `app/services/claude_pro.py`

每天凌晨 02:00，Pro Task 執行：

```
1. 讀取當天 Flash Task 累計的合併事件（FlashResult chunk_index=-1）
2. 讀取昨天已確認的事件（用來判斷是否為延續事件）
3. 送給 Claude Sonnet 4.6 進行最終彙整：
   - 語意層面合併（同類現象、同根因）
   - 判斷是否為昨天事件的延續
   - 補充最終處置建議
4. 寫入 security_events 資料表
   - 新事件：INSERT
   - 延續事件：UPDATE（累加 detection_count，延長 date_end）
```

**為什麼需要兩層 AI？**

| | Flash（Haiku） | Pro（Sonnet） |
| --- | --- | --- |
| 頻率 | 每 20 分鐘 | 每天一次 |
| 目的 | 快速萃取事件 | 去重合併、跨日關聯 |
| 特點 | 便宜、速度快 | 推理能力強 |
| 輸入 | 單一 chunk 日誌 | 當天所有 Flash 結果 |

---

### 4.6 前端查詢事件

**檔案：** `app/api/events.py`

前端畫面需要的四個端點：

```
GET    /api/events           列表（支援分頁、狀態篩選、關鍵字、日期範圍）
GET    /api/events/{id}      單一事件詳情
PATCH  /api/events/{id}      更新狀態 / 指派人員
POST   /api/events/{id}/history  新增歷史記錄或操作備註
```

**查詢參數範例：**
```
GET /api/events?status=pending,investigating&keyword=john&page=1&page_size=20
```

**Pydantic Schema 的角色：**

`app/schemas/security_event.py` 定義了 API 格式：
- 請求進來時，Pydantic 自動驗證欄位型別與必填項目
- 回應出去時，Pydantic 自動序列化（把 Python 物件轉成 JSON）
- ORM model（`models/`）和 API schema（`schemas/`）分開維護，讓兩者可以各自演進

---

## 5. 資料庫設計

### 資料表關係圖

```
User ──┬── UserRole ── Role
       │
       └── EventHistory ── SecurityEvent ──── EventHistory
                                │
                    LogBatch ── FlashResult
                                │
                            DailyAnalysis
```

### 核心資料表

| 資料表 | 用途 |
| --- | --- |
| `users` | 使用者帳號（name, email, password_hash） |
| `roles` | 角色與權限（can_access_ai, can_manage_* 等 6 種權限） |
| `user_roles` | 使用者↔角色多對多關聯 |
| `token_blacklist` | 已登出的 JWT token |
| `security_events` | 資安事件主表（最重要的資料） |
| `event_history` | 事件操作紀錄（狀態變更、指派、備註） |
| `log_batches` | 每次日誌拉取的批次追蹤 |
| `flash_results` | Haiku 分析結果（chunk 級別暫存） |
| `daily_analyses` | Pro Task 每日執行統計 |

### SecurityEvent 重要欄位說明

| 欄位 | 說明 |
| --- | --- |
| `match_key` | 事件唯一識別鍵，用來跨日合併同類事件 |
| `star_rank` | 嚴重程度 1-5 星，由 AI 評分 |
| `current_status` | 事件狀態：pending / investigating / resolved 等 |
| `detection_count` | 累計偵測次數（同 match_key 事件合併後累加）|
| `continued_from` | 指向前一天的同類事件 ID（延續關係）|
| `ioc_list` | IOC 指標（可疑 IP、帳號）以 JSON 儲存 |
| `mitre_tags` | MITRE ATT&CK 技術標籤 |
| `logs` | 觸發此事件的原始日誌片段（JSONB）|

### Alembic 遷移

資料庫 schema 的變更歷史存在 `alembic/versions/`，執行順序：
1. 建立使用者 / 角色表
2. 新增 Token 黑名單表
3. 新增資安事件相關表
4. 種子資料（預設角色與管理員帳號）

---

## 6. 配置管理

**檔案：** `app/core/config.py`、`.env.example`

所有環境變數用 Pydantic Settings 統一管理，有型別檢查且支援從 `.env` 讀取：

```python
# 使用方式（任何地方都可以 import）
from app.core.config import settings
print(settings.DATABASE_URL)
```

**主要設定分類：**

| 類別 | 變數 |
| --- | --- |
| 資料庫 | `DATABASE_URL` |
| JWT | `JWT_SECRET_KEY`、`JWT_EXPIRE_MINUTES` |
| SSB | `SSB_HOST`、`SSB_USERNAME`、`SSB_PASSWORD` |
| Anthropic | `ANTHROPIC_API_KEY` |
| Celery | `CELERY_BROKER_URL`、`CELERY_RESULT_BACKEND` |
| 分析模式 | `ANALYSIS_MODE`（full / windows_only）|
| 排程 | `FLASH_INTERVAL_MINUTES`、`PRO_TASK_HOUR` |

---

## 7. 測試架構

**檔案：** `tests/conftest.py`、`pyproject.toml`

**測試用資料庫：** 使用 SQLite 記憶體資料庫（`sqlite:///:memory:`），不需要真實的 PostgreSQL 環境，測試結束自動清除。

**測試固件（Fixture）運作方式：**

```python
# conftest.py 提供兩個固件
engine   → 建立 SQLite 記憶體資料庫，自動建表
client   → FastAPI TestClient，將 get_db 依賴替換成測試 DB
```

**每個 test function 都要標注對應的 TDD ID：**

```python
def test_login_success(client):
    """對應 TDD T1"""
    response = client.post("/api/auth/login", json={"email": "...", "password": "..."})
    assert response.status_code == 200
```

**執行測試：**
```bash
cd backend
pytest  # 自動計算覆蓋率並顯示未覆蓋行
```

---

## 8. 技術框架速查表

| 框架 | 在哪裡用 | 最常見的用法 |
| --- | --- | --- |
| **FastAPI** | `api/*.py`、`main.py` | `@router.get()`、`Depends()` |
| **SQLAlchemy** | `models/*.py`、`db/session.py` | `db.query(Model).filter(...).all()` |
| **Alembic** | `alembic/` | `alembic revision --autogenerate`、`alembic upgrade head` |
| **Pydantic** | `schemas/*.py`、`core/config.py` | `class MySchema(BaseModel)`、`settings.XXX` |
| **python-jose** | `core/security.py` | `jwt.encode()`、`jwt.decode()` |
| **bcrypt** | `core/security.py` | `bcrypt.hashpw()`、`bcrypt.checkpw()` |
| **Celery** | `worker.py`、`tasks/*.py` | `@celery_app.task`、`beat_schedule` |
| **Anthropic SDK** | `services/claude_*.py` | `client.messages.create(model=..., messages=[...])` |
| **pytest** | `tests/` | `def test_xxx(client):`、`assert` |
