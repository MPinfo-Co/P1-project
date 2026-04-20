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

### `@router.post()` / `@router.get()`

**是什麼：** 路由裝飾器，宣告「這個函式處理指定 HTTP 方法與路徑的請求」。

**專案範例：**
```python
@router.post("/login")
def login(email: str, password: str, db: Session = Depends(get_db)):
    ...
```

**白話解釋：** 像門牌，`@router.post("/login")` 就是「有人寄 POST 信到 /login，就交給這個函式處理」。搭配 `app.include_router(auth_router, prefix="/api/auth")`，完整路徑是 `/api/auth/login`。`@router.get` 處理 GET、`@router.patch` 處理 PATCH，以此類推。

**常見錯誤：**
- 路由路徑是相對於 router，不是完整路徑；忘記這點會導致路由註冊到錯誤的 URL

---

### `Depends()`

**是什麼：** FastAPI 依賴注入，自動執行指定函式並把結果傳進路由函式。

**專案範例：**
```python
@router.get("/")
def list_events(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # current_user 和 db 都由 FastAPI 自動注入
    ...
```

**白話解釋：** 不需要在每個路由裡重複寫「驗證 token、拿資料庫連線」，`Depends(get_current_user)` 告訴 FastAPI「先幫我跑 get_current_user()，把結果塞進 current_user」。類似 middleware，但更精確——每個函式可以聲明自己需要哪些依賴。

**常見錯誤：**
- `Depends` 裡傳的是函式本身（`Depends(get_db)`），不是呼叫結果；不要寫成 `Depends(get_db())`（多了括號）

---

### `bcrypt.checkpw()` / `bcrypt.hashpw()`

**是什麼：** bcrypt 密碼雜湊庫，`hashpw` 把密碼加密存進資料庫，`checkpw` 驗證密碼是否正確。

**專案範例：**
```python
# 建立雜湊（註冊時）
password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

# 驗證密碼（登入時）
bcrypt.checkpw(password.encode(), user.password_hash)
```

**白話解釋：** 密碼不能明文存資料庫，bcrypt 把密碼「磨碎」成固定長度的雜湊值（不可逆）。驗證時 `checkpw` 把輸入的密碼用同樣方式磨碎，比對結果是否一致，而非比對原始密碼。

**常見錯誤：**
- `checkpw` 的第一個參數要是 bytes（`password.encode()`），傳 str 會報 TypeError

---

### `jwt.encode()` / `jwt.decode()`

**是什麼：** python-jose 的 JWT 操作函式，encode 產生 token，decode 驗證並解析 token 內容。

**專案範例：**
```python
# 產生 token
token = jwt.encode(
    {"sub": str(user.id), "exp": expire},
    settings.JWT_SECRET_KEY,
    algorithm="HS256"
)

# 驗證並解析 token
payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=["HS256"])
user_id = payload.get("sub")
```

**白話解釋：** JWT 是一個加密的字串，裡面藏著使用者 ID（sub）和過期時間（exp）。encode 用 secret key 簽署產生 token，decode 用同樣的 secret key 驗證簽名並取出裡面的資料。

**常見錯誤：**
- decode 要捕捉 `JWTError` exception，否則 token 過期或被竄改時會直接 crash；`algorithms=` 參數是 list，不是字串

---

### `db.query().filter().first()`

**是什麼：** SQLAlchemy ORM 查詢語法，從資料庫查一筆符合條件的記錄。

**專案範例：**
```python
user = db.query(User).filter(User.email == email).first()
```

**白話解釋：** 等同 SQL `SELECT * FROM users WHERE email = 'xxx' LIMIT 1`。`.query(User)` 指定查哪個表，`.filter(...)` 是 WHERE 條件，`.first()` 取第一筆（找不到回傳 None）。

**常見錯誤：**
- `filter(User.email == email)` 的 `==` 是 ORM 的比較運算（回傳條件物件），不是 Python 的相等比較，這是正確的寫法
- `.first()` 找不到回傳 None，記得做 `if user is None` 的檢查

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
