# Backend 語法說明文件

> 本文配合 [backend-guide.md](./backend-guide.md) 使用。
> 閱讀方式：在 backend-guide.md 遇到不懂的語法 → 查下方索引 → 跳到對應說明。

**讀者假設：** 熟悉 Python 基礎（def、class、async/await），未接觸 FastAPI 生態系。

---

## 語法索引表

| 語法 | 簡易說明 | 出現章節 | 跳到說明 |
|------|----------|----------|----------|
| `app.include_router()` | 把路由器掛載到 FastAPI 應用 | 4.1 應用程式啟動 | [連結](#appinclude_router) |
| `CORSMiddleware` | 允許前端跨域存取 API | 4.1 應用程式啟動 | [連結](#corsmiddleware) |
| `@router.post()` / `@router.get()` | 宣告 HTTP 方法與路徑的路由裝飾器 | 4.2 登入認證 | [連結](#routerpost--routerget) |
| `Depends()` | 依賴注入，自動執行共用邏輯 | 4.2 登入認證 | [連結](#depends) |
| `bcrypt.checkpw()` / `bcrypt.hashpw()` | 密碼雜湊比對與建立 | 4.2 登入認證 | [連結](#bcryptcheckpw--bcrypthashpw) |
| `jwt.encode()` / `jwt.decode()` | JWT token 簽署與驗證 | 4.2 登入認證 | [連結](#jwtencode--jwtdecode) |
| `db.query().filter().first()` | SQLAlchemy 查詢資料庫 | 4.2 登入認證 | [連結](#dbqueryfiltersfirst) |
| `@celery_app.task` | 宣告 Celery 非同步背景任務 | 4.3 Flash Task | [連結](#celery_apptask) |
| `beat_schedule` | 設定 Celery 定時排程 | 4.3 Flash Task | [連結](#beat_schedule) |
| `httpx.AsyncClient` | 非同步 HTTP 客戶端，呼叫外部 API | 4.3 Flash Task | [連結](#httpxasyncclient) |
| list slicing `logs[i:i+300]` | 把 list 切成固定大小的批次 | 4.3 Flash Task | [連結](#list-slicing-logsi300) |
| `client.messages.create()` | Anthropic SDK 呼叫 Claude | 4.4 AI 快速分析 | [連結](#clientmessagescreate) |
| system / user message 結構 | Claude prompt 的角色設定格式 | 4.4 AI 快速分析 | [連結](#system--user-message-結構) |
| `json.loads()` | 把 JSON 字串解析成 Python 物件 | 4.4 AI 快速分析 | [連結](#jsonloads) |
| `db.add()` / `db.merge()` | 新增記錄 / 存在更新不存在新增 | 4.5 AI 日報彙整 | [連結](#dbadd--dbmerge) |
| `db.commit()` / `db.refresh()` | 提交交易並同步最新資料庫狀態 | 4.5 AI 日報彙整 | [連結](#dbcommit--dbrefresh) |
| `Query(...)` | 宣告 URL 查詢參數與預設值 | 4.6 事件查詢 | [連結](#query) |
| `class Schema(BaseModel)` | Pydantic Schema 定義 API 格式 | 4.6 事件查詢 | [連結](#class-schemabasemodel) |
| `response_model=` | 路由回應自動序列化為指定格式 | 4.6 事件查詢 | [連結](#response_model) |
| `Optional[str] = None` | 可選參數型別標注 | 4.6 事件查詢 | [連結](#optionalstr--none) |
| `class Settings(BaseSettings)` | 從環境變數讀取設定，有型別驗證 | 6. 配置管理 | [連結](#class-settingsbasesettings) |
| `settings.DATABASE_URL` | 全域取用設定值 | 6. 配置管理 | [連結](#settingsdatabase_url) |
| `.env` + `Field(...)` | 環境變數檔案與欄位預設值設定 | 6. 配置管理 | [連結](#env--field) |
| `@pytest.fixture` | 宣告 pytest 測試固件 | 7. 測試架構 | [連結](#pytestfixture) |
| `conftest.py` | 共用固件的集中位置 | 7. 測試架構 | [連結](#conftestpy) |
| `TestClient(app)` | FastAPI 測試用 HTTP 客戶端 | 7. 測試架構 | [連結](#testclientapp) |
| `app.dependency_overrides` | 替換依賴注入（換成測試 DB） | 7. 測試架構 | [連結](#appdependency_overrides) |
| `assert response.status_code` | pytest 斷言驗證回應 | 7. 測試架構 | [連結](#assert-responsestatus_code) |

---

## 4.1 應用程式啟動

### `app.include_router()`

**是什麼：** 把一個路由器（router）的所有路由掛載到 FastAPI 應用，並加上統一的 URL 前綴。

**專案範例：**
```python
app.include_router(auth_router, prefix="/api/auth")
app.include_router(events_router, prefix="/api/events")
app.include_router(health_router)
```

**白話解釋：** router 是一組路由的集合，`include_router` 把它「接」進主應用。加了 `prefix="/api/auth"` 後，auth_router 裡的 `/login` 路由完整路徑就變成 `/api/auth/login`。這樣不同模組的路由可以各自管理，main.py 只負責組裝。

**常見錯誤：**
- prefix 末尾加斜線（`"/api/auth/"`），路由路徑前也有斜線，導致雙斜線（`/api/auth//login`）

---

### `CORSMiddleware`

**是什麼：** 允許瀏覽器從不同網域（如前端 localhost:5173）存取這個 API。

**專案範例：**
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**白話解釋：** 瀏覽器的安全機制會阻擋「跨域請求」（前端 localhost:5173 打後端 localhost:8000）。`CORSMiddleware` 告訴瀏覽器「這個來源是被允許的，放行」。`allow_methods=["*"]` 表示所有 HTTP 方法都允許。

**常見錯誤：**
- `allow_origins=["*"]` 開發方便，但正式環境要改成指定網域，否則任何網站都能呼叫你的 API

---

## 4.2 使用者登入與 JWT 認證

---

## 4.3 排程任務：Flash Task

---

## 4.4 AI 快速分析（Claude Haiku）

---

## 4.5 AI 日報彙整（Claude Sonnet）

---

## 4.6 前端查詢事件

---

## 6. 配置管理

---

## 7. 測試架構

---
