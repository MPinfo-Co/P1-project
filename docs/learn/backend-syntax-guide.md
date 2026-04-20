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

### `@celery_app.task`

**是什麼：** 把函式宣告為 Celery 非同步任務，可以交給 Worker 在背景執行，不阻塞 API server。

**專案範例：**
```python
@celery_app.task(name="flash_task")
def run_flash_task():
    # 拉取日誌、送 AI 分析...
    ...
```

**白話解釋：** `@celery_app.task` 讓這個函式可以被「丟進佇列」交給另一個程序執行。API server 丟完就繼續處理其他請求，不用等任務完成。類似「把工作單交給倉庫，倉庫慢慢處理，你繼續接客」。

**常見錯誤：**
- 直接呼叫 `run_flash_task()` 是同步執行；要用 `run_flash_task.delay()` 才是非同步丟進佇列

---

### `beat_schedule`

**是什麼：** Celery Beat 的排程設定，定義哪個任務在什麼時間自動執行。

**專案範例：**
```python
beat_schedule = {
    "flash-task-every-20-min": {
        "task": "flash_task",
        "schedule": crontab(minute="*/20"),
    },
    "pro-task-daily": {
        "task": "pro_task",
        "schedule": crontab(hour=2, minute=0),
    },
}
```

**白話解釋：** 像設定手機鬧鐘，`crontab(minute="*/20")` 是「每 20 分鐘響一次」，`crontab(hour=2, minute=0)` 是「每天凌晨 02:00」。Celery Beat 是一個獨立程序，按時把任務丟進佇列。

**常見錯誤：**
- `beat_schedule` 需要 Celery Beat 程序獨立啟動（`celery -A worker beat`），光啟動 Worker 不會執行排程

---

### `httpx.AsyncClient`

**是什麼：** 非同步 HTTP 客戶端，用 `async/await` 方式呼叫外部 API，不阻塞程式。

**專案範例：**
```python
async with httpx.AsyncClient() as client:
    response = await client.get(
        url,
        headers={"Authorization": f"Bearer {token}"}
    )
    data = response.json()
```

**白話解釋：** 類似 Python 的 `requests` 庫，但支援非同步。`async with` 確保用完自動關閉連線（類似 `with open()` 處理檔案）。`await client.get()` 等待回應時不會卡住其他程式碼。

**常見錯誤：**
- 在同步函式裡用 `await httpx` 會報錯；忘記 `async with`，手動建立的 `AsyncClient` 需要呼叫 `.aclose()` 關閉

---

### list slicing `logs[i:i+300]`

**是什麼：** Python list 切片，取出指定索引範圍的元素。

**專案範例：**
```python
for i in range(0, len(logs), 300):
    chunk = logs[i:i+300]
    # 把這批 300 筆送給 AI 分析
    await analyze_chunk(chunk)
```

**白話解釋：** `logs[i:i+300]` 取出從 index i 開始的 300 筆。`range(0, len(logs), 300)` 以 300 為步伐走過整個 list：第一次 i=0（取 0-299），第二次 i=300（取 300-599），以此類推。

**常見錯誤：**
- 最後一批不足 300 筆時 Python 自動取到結尾，不會報錯，不需要特別處理邊界

---

## 4.4 AI 快速分析（Claude Haiku）

### `client.messages.create()`

**是什麼：** Anthropic SDK 呼叫 Claude 的核心函式，傳入模型名稱與對話訊息，回傳 AI 分析結果。

**專案範例：**
```python
response = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=4096,
    system="你是資安事件分析師，請用 JSON 格式回傳分析結果。",
    messages=[{"role": "user", "content": log_text}]
)
```

**白話解釋：** `messages` 是一個對話陣列，每筆有 `role`（user 或 assistant）和 `content`（訊息內容）。`max_tokens` 限制回應長度，避免 token 費用失控。`model` 指定要用哪個 Claude 版本。

**常見錯誤：**
- 忘記設 `max_tokens` 可能超出 API 限制；`model` 名稱拼錯或使用已退役的模型 ID 會直接拋出 API 錯誤

---

### system / user message 結構

**是什麼：** Claude API 的 prompt 格式，`system` 設定 AI 的角色與回應規範，`messages` 是對話內容。

**專案範例：**
```python
# system 告訴 AI 它的角色和輸出格式
system = """你是資安事件分析師。分析以下日誌，回傳 JSON 陣列，
每筆包含：star_rank(1-5), title, match_key, suggests"""

# messages 是實際輸入的日誌內容
messages = [{"role": "user", "content": f"日誌資料：\n{log_text}"}]
```

**白話解釋：** `system` 是「背景設定」（告訴 AI 它的角色、輸出格式要求），`messages` 是「每次的實際輸入」。分開設定讓 `system` 部分可以享受 Anthropic 的 Prompt Cache，重複呼叫時只有 `messages` 計費。

**常見錯誤：**
- 把所有指令塞進 `messages` 的 user content 而不用 `system` 參數，每次都全量計費，無法享受快取優惠

---

### `json.loads()`

**是什麼：** 把 JSON 字串解析成 Python dict 或 list。

**專案範例：**
```python
result_text = response.content[0].text
events = json.loads(result_text)
# events 現在是 Python list，可以用 for 迴圈處理
for event in events:
    print(event["title"])
```

**白話解釋：** Claude 回傳的是文字字串，`json.loads()` 把 `'[{"title": "可疑登入"}]'` 這樣的字串轉成 Python 可以操作的 list。`json.dumps()` 是反方向（Python 物件轉 JSON 字串）。

**常見錯誤：**
- AI 有時回傳的 JSON 外面包了 markdown code block（` ```json...``` `），直接 `json.loads` 會失敗，需要先用字串處理或正則清掉包裝

---

## 4.5 AI 日報彙整（Claude Sonnet）

### `db.add()` / `db.merge()`

**是什麼：** `db.add` 新增記錄（INSERT），`db.merge` 存在就更新、不存在就新增（UPSERT）。

**專案範例：**
```python
# 全新事件：INSERT
new_event = SecurityEvent(title="可疑登入", match_key="4625_john")
db.add(new_event)

# 延續事件：更新已存在的記錄
existing_event.detection_count += 1
existing_event.date_end = today
db.merge(existing_event)

db.commit()
```

**白話解釋：** `db.add` 永遠新增一筆，適合第一次建立。`db.merge` 根據主鍵判斷——主鍵已存在就 UPDATE，不存在就 INSERT，適合「建立或更新」的場景（如延續事件累加計數）。

**常見錯誤：**
- 用 `db.add` 插入主鍵重複的記錄會拋出 `IntegrityError`；`db.add` 和 `db.merge` 都需要後續 `db.commit()` 才真正寫進資料庫

---

### `db.commit()` / `db.refresh()`

**是什麼：** `commit` 把交易提交到資料庫，`refresh` 重新從資料庫讀取物件的最新狀態。

**專案範例：**
```python
db.add(new_event)
db.commit()
db.refresh(new_event)
# 現在 new_event.id 有值了（資料庫自動產生的）
print(new_event.id)
```

**白話解釋：** `db.add(obj)` 只是把修改放在暫存區，`db.commit()` 才真正送進資料庫。`db.refresh(obj)` 讓 Python 物件同步資料庫的最新值，最常用在取得資料庫自動產生的欄位（如 id、created_at）。

**常見錯誤：**
- commit 後忘記 refresh，讀取 `new_event.id` 可能還是 None；如果在 commit 後繼續操作同一個 session，也要注意 SQLAlchemy 的 lazy loading 行為

---

## 4.6 前端查詢事件

---

## 6. 配置管理

---

## 7. 測試架構

---
