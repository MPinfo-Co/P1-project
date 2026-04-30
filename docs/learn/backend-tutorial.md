# P1-code 後端程式碼教學

> 假設你完全不懂後端，從頭解釋每一個概念。

---

## 第一章：程式是怎麼啟動的？

### `main.py` — 程式的大門

```python
# app/main.py
app = start_server()
```

當你執行 `uvicorn app.main:app` 時，Python 會執行這支檔案，建立一個叫做 `app` 的 FastAPI 應用程式。

`start_server()` 做了三件事：

**① 設定 CORS（跨來源資源共享）**

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", ...],
    ...
)
```

這是告訴瀏覽器「哪些網址的前端可以呼叫這個 API」。因為瀏覽器有安全限制，前端（在 localhost:5173 跑）不能隨便呼叫其他網址的 API，除非對方明確允許。

**② 掛上所有 Router（路由）**

```python
app.include_router(auth_router)
app.include_router(users_router)
# ...
```

每個 `router` 都是一組 API 端點，分別放在不同的檔案裡，這裡統一註冊進來。就像餐廳把「飲料菜單」和「主餐菜單」都放進同一本菜單一樣。

**③ 設定 Lifespan（生命週期）**

```python
@asynccontextmanager
async def lifespan(app):
    # 這裡的程式碼在伺服器「啟動時」執行
    yield
    # yield 之後的程式碼在伺服器「關閉時」執行
```

這裡只是印出啟動/關閉的 log，讓你知道伺服器什麼時候上線、跑了多久。

---

## 第二章：設定值從哪裡來？

### `core/config.py` — 環境變數管理

```python
class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET_KEY: str
    ANTHROPIC_API_KEY: str = ""
    # ...

settings = Settings()
```

所有「不能寫死在程式碼裡」的東西都放在 `.env` 檔案，例如資料庫密碼、API Key。`Settings` 類別用 `pydantic_settings` 自動讀取這些值。

> **小白理解：** `.env` 就像記事本，裡面寫 `DATABASE_URL=...`。程式啟動時，`Settings` 自動去讀這張記事本。

整個後端只有一個 `settings` 物件（在 module 層級建立），任何地方 `from app.core.config import settings` 就能用。

---

## 第三章：資料庫是怎麼連的？

### `db/session.py` — 資料庫連線

```python
engine = create_engine(settings.DATABASE_URL, pool_size=5)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
```

**engine** = 資料庫的「連線工廠」，負責實際的 TCP 連線。`pool_size=5` 表示最多同時保持 5 條連線（避免每次請求都重新連線，浪費時間）。

**SessionLocal** = 每次要操作資料庫，就開一個 Session。Session 就像一個「工作視窗」，你在裡面做的所有操作（新增、修改），要 `commit()` 才會真正寫進資料庫。

```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

這個函式是「依賴注入（Dependency Injection）」的核心。FastAPI 每收到一個 HTTP 請求，就會自動呼叫 `get_db()` 產生一個 db 物件，用完之後自動關閉。

> **小白理解：** `get_db` 就像借圖書館的電腦——進館時借一台，離館時還回去，不會一直佔用。

---

## 第四章：資料表長什麼樣子？

### `db/models/user.py` — 使用者相關資料表

SQLAlchemy 的 Model 是「Python 類別 ↔ 資料庫資料表」的對應。

```python
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)  # 密碼不明文存，存雜湊值
    is_active = Column(Boolean, nullable=False, default=True)
    updated_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    updated_at = Column(TIMESTAMP, ...)
```

> **為什麼不存明文密碼？** 萬一資料庫外洩，攻擊者拿到的是看不懂的雜湊值（例如 `$2b$12$...`），無法反推原始密碼。

**權限系統的五張表：**

```
users        ← 使用者帳號
roles        ← 角色（例如：管理員、分析師）
user_roles   ← 哪個 user 有哪個 role（多對多關係）
functions    ← 功能權限（例如：fn_user、fn_role）
role_functions ← 哪個 role 有哪個 function（多對多關係）
```

以圖示理解：

```
使用者 Rex  →  [管理員角色]  →  fn_user 權限（可以管理使用者）
                            →  fn_role 權限（可以管理角色）

使用者 Amy  →  [分析師角色]  →  （沒有 fn_user / fn_role）
```

---

## 第五章：身份驗證怎麼運作？

### `core/security.py` — 密碼與 JWT

**密碼加密：**

```python
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())
```

bcrypt 是一種特殊的雜湊演算法，特點是「刻意設計得很慢」，讓攻擊者即使拿到雜湊值，暴力破解也很費時。

**JWT Token：**

```python
def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=60)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm="HS256")
```

JWT（JSON Web Token）是一個「加密的通行證」。登入成功後，伺服器產生一個 token 給前端，前端之後的每個請求都帶上這個 token，伺服器驗證 token 是否有效。

Token 的內容：`{"sub": "1", "exp": 1746000000}` → `sub` 是 user_id，`exp` 是過期時間。

> **小白理解：** 就像遊樂園的入場手環——進場時換手環，之後進出設施都刷手環，不需要每次重新買票。

### `api/auth.py` — 登入 / 登出 API

**登入流程：**

```python
@router.post("/api/auth/login")
def login(api_request: LoginRequest, db: Session = Depends(get_db)):
    # 1. 用 email 找 user
    user = db.query(User).filter(User.email == api_request.email).first()
    # 2. 驗證密碼
    if not verify_password(api_request.password, user.password_hash):
        raise HTTPException(401, "帳號或密碼錯誤")
    # 3. 產生 JWT
    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token}
```

**登出流程（Token 黑名單）：**

JWT 本身無法「撤銷」——一旦發出去，到期前都有效。解決辦法是把登出的 token 記在 `token_blacklist` 表，每次請求都檢查一下。

```python
@router.post("/api/auth/logout")
def logout(credentials=Depends(bearer_scheme), db=Depends(get_db)):
    token = credentials.credentials
    # 記入黑名單
    db.add(TokenBlacklist(token=token, expired_at=...))
    db.commit()
```

### `core/deps.py` — 「誰在呼叫？」

```python
def get_current_user(
    credentials=Depends(bearer_scheme),
    db=Depends(get_db),
) -> User:
    token = credentials.credentials
    # 1. 檢查黑名單
    if db.query(TokenBlacklist).filter(TokenBlacklist.token == token).first():
        raise HTTPException(401, "Token 已登出")
    # 2. 解析 JWT
    payload = decode_access_token(token)
    # 3. 查 user
    user = db.query(User).filter(User.id == int(payload["sub"])).first()
    return user
```

在任何需要登入的 API 裡，只要寫 `current_user: User = Depends(get_current_user)`，FastAPI 就會自動執行這段驗證，驗證失敗直接回傳 401，不進入主邏輯。

---

## 第六章：API 端點怎麼寫？

### `api/users.py` — 使用者管理 API

以「查詢使用者列表」為例：

```python
@router.get("/api/users", status_code=200)
def list_users(
    role_id: Optional[int] = Query(None),   # URL 參數：?role_id=1
    keyword: Optional[str] = Query(None),   # URL 參數：?keyword=rex
    db: Session = Depends(get_db),          # 自動取得資料庫連線
    current_user: User = Depends(get_current_user),  # 自動驗證登入
):
    _check_fn_user(db, current_user)  # 再檢查有沒有 fn_user 權限

    q = db.query(User).outerjoin(UserRole, ...)

    if role_id:
        q = q.filter(UserRole.role_id == role_id)
    if keyword:
        q = q.filter(User.name.ilike(f"%{keyword}%"))  # ilike = 不分大小寫的 LIKE

    users = q.distinct().order_by(User.id.asc()).all()
    return {"message": "查詢成功", "data": result}
```

**權限檢查：**

```python
def _check_fn_user(db, current_user):
    has_perm = (
        db.query(RoleFunction)
        .join(UserRole, RoleFunction.role_id == UserRole.role_id)
        .join(Function, RoleFunction.function_id == Function.function_id)
        .filter(UserRole.user_id == current_user.id)
        .filter(Function.function_name == "fn_user")
        .first()
    )
    if not has_perm:
        raise HTTPException(403, "您沒有執行此操作的權限")
```

這段查詢的意思：「沿著 user → user_roles → role_functions → functions 這條關係鏈，看有沒有 function_name = 'fn_user' 的記錄」。

> **小白理解：** 就像問「Rex 是不是有『人事管理』這個通行證？」，先查 Rex 的角色是什麼，再查那個角色有哪些通行證。

---

## 第七章：Log 進來之後怎麼處理？

### `api/ingest.py` — 接收 Log 資料

```python
@router.post("/api/ingest")
def ingest_logs(
    payload: IngestPayload,
    x_ingest_key: str = Header(default=""),  # 從 HTTP Header 取 key
    db: Session = Depends(get_db),
):
    # 驗證 INGEST_SECRET（只有 adapter 才知道這個 secret）
    if settings.INGEST_SECRET and x_ingest_key != settings.INGEST_SECRET:
        raise HTTPException(403, "Invalid ingest key")

    result = _process_ingest(db, payload)
    return result
```

這個端點沒有用 `get_current_user`，因為呼叫者是「外部 log adapter」，不是一般使用者，改用 `X-Ingest-Key` Header 做驗證。

### `tasks/flash_task.py` — Flash Task（Haiku 分析）

**切 chunk：**

```python
chunks = [
    logs[i : i + settings.FLASH_CHUNK_SIZE]
    for i in range(0, len(logs), settings.FLASH_CHUNK_SIZE)
]
```

一次 ingest 可能有幾千筆 log，但 AI 每次只能處理有限的資料（token 限制），所以要切成小塊（預設每塊 300 筆）。

**match_key 是什麼？**

match_key 是用來「辨認同一種事件」的識別碼。例如：
- `deny_external_192.168.1` → 外部 IP 對 192.168.1.x 網段的攻擊
- `4625_administrator` → administrator 帳號登入失敗（Windows event 4625）

程式自己根據 log 的內容計算 match_key（`_generate_group_key()`），再**覆蓋** AI 產生的 match_key，確保一致性。

**為什麼要覆蓋 AI 的 match_key？**

AI 每次分析同一類事件，可能用不同的 match_key（例如今天叫 `admin_login_fail`，明天叫 `failed_login_admin`）。程式用固定規則產生 match_key，確保跨批次的事件能正確合併。

**合併事件（`_merge_events()`）：**

```python
def _merge_events(all_events):
    grouped = defaultdict(list)
    for ev in all_events:
        grouped[ev["match_key"]].append(ev)

    merged = []
    for match_key, events in grouped.items():
        base = dict(events[0])
        base["star_rank"] = max(...)    # 嚴重度取最高
        base["detection_count"] = ...   # 偵測次數加總
        base["ioc_list"] = list(set(...))  # IOC 取聯集（去重）
        merged.append(base)
    return merged
```

多個 chunk 分析完，可能都偵測到「外部掃描」這個事件，用 match_key 把它們合在一起，不要重複報告。

**當天累計（`_update_daily_accumulator()`）：**

每次 ingest 處理完，把結果「累加」進一個特殊的 FlashResult（`chunk_index = -1`）。這個累計記錄代表「今天到目前為止，所有 batch 合併後的事件總覽」，給晚上的 Pro Task 讀取。

---

## 第八章：每天凌晨的 AI 彙整

### `tasks/pro_task.py` — Pro Task（Sonnet 最終彙整）

```python
@celery_app.task(name="app.tasks.pro_task.run_pro_task")
def run_pro_task():
    # 1. 讀取今天的累計 FlashResult（chunk_index=-1）
    accumulator = db.query(FlashResult).filter(..., chunk_index == -1).first()

    # 2. 讀取昨天的事件（判斷是否延續）
    prev_events = db.query(SecurityEvent).filter(event_date == yesterday).all()

    # 3. 送 Sonnet 做最終彙整
    final_events = aggregate_daily(grouped, prev_summary, today)

    # 4. 寫入 security_events
    for ev in final_events:
        existing = db.query(SecurityEvent).filter(match_key == ev["match_key"], status in ["pending", "investigating"]).first()
        if existing:
            # 延續事件 → 更新，date_end 延伸到今天
            existing.detection_count += ev["detection_count"]
        else:
            # 新事件 → 新增
            db.add(SecurityEvent(...))
```

**Sonnet 做什麼？**

Haiku 分析的是「原始 log 片段」，可能產生很多重複或類似的事件（例如 20 個不同 IP 的廣播，Haiku 各報了一筆）。Sonnet 拿到 Haiku 彙整後的結果，做二次去重合併，輸出一份「今日最終資安事件清單」。

> **小白理解：** Haiku 像是值班的資安人員，快速把每一批 log 標記出可疑事項。Sonnet 像是隔天早上的資深主管，把昨天所有標記彙整一遍，去掉重複，產出正式報告。

---

## 第九章：背景任務怎麼執行？

### `worker.py` — Celery 設定

```python
celery_app = Celery(
    "mpbox",
    broker=settings.CELERY_BROKER_URL,   # redis://redis:6379/0
    backend=settings.CELERY_RESULT_BACKEND,
)

celery_app.conf.beat_schedule = {
    "pro-task": {
        "task": "app.tasks.pro_task.run_pro_task",
        "schedule": crontab(hour=2, minute=0),  # 每天凌晨 02:00
    },
}
```

**Celery 的三個角色：**

| 角色 | 說明 |
|------|------|
| Beat | 鬧鐘，到了時間就往 Redis 放一個「請執行 pro_task」的訊息 |
| Redis | 訊息佇列，中間人，存放待執行的任務 |
| Worker | 真正執行任務的程式，一直盯著 Redis，有任務就撿起來跑 |

```
Beat ──(每天02:00)──> Redis ──> Worker ──> run_pro_task() ──> 寫資料庫
```

> **小白理解：** Beat 是定時鬧鐘，Redis 是公佈欄，Worker 是看到公佈欄就去執行任務的員工。

---

## 第十章：Log 系統

### `logger_utils/log_channels.py` — 三種 Log 頻道

系統日誌分三個「頻道」，各自寫到不同的檔案：

| 頻道 | 用途 | 呼叫方式 |
|------|------|------|
| `system` | 伺服器啟動/關閉等系統事件 | `get_system_logger().info("...")` |
| `service` | Celery 背景任務的執行記錄 | `get_service_logger().info("...")` |
| `user` | 每個 user 各一支 log 檔，記錄操作行為 | `get_user_logger(user_id).info("...")` |

這裡用的是 `loguru` 套件，比 Python 內建的 `logging` 更方便。「Sink」是 loguru 的術語，代表「log 要寫到哪裡」（這裡是寫到檔案）。

---

## 第十一章：資料格式驗證（Schema）

### `schemas/` 目錄 — Pydantic Models

每個 API 的輸入/輸出都需要定義格式，用 Pydantic 的 BaseModel：

```python
# schemas/auth.py
class LoginRequest(BaseModel):
    email: EmailStr    # 自動驗證格式是否為合法 email
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"  # 有預設值
```

FastAPI 自動用這些 Schema 驗證請求、序列化回應。如果前端送了一個格式錯誤的 email，FastAPI 會自動回傳 422 錯誤，不進入主邏輯。

> **小白理解：** Schema 就像表單的填寫規範，格式不對就退件。

---

## 第十二章：資料庫版本管理

### `alembic/` — Schema Migration

Alembic 管理資料庫結構的版本歷史，每次修改 Schema 都建立一個 migration 檔案：

```
alembic/versions/
    5db1ff7f746b_create_users_roles_user_roles.py   ← 最早，建立基本表
    538d0579a48c_seed_initial_roles_and_admin.py    ← 初始化資料
    c1d2e3f4a5b6_refactor_roles_add_functions.py    ← 新增 functions 表
    ...
```

每個版本檔案有 `upgrade()` 和 `downgrade()`，可以往前升版或回滾。

> **小白理解：** 就像 git commit 一樣，每次改資料表結構都留一筆記錄，可以隨時回到任何版本。

---

## 整體流程回顧

```
外部 adapter
    │ POST /api/ingest
    ▼
① 接收 log 資料，驗證 INGEST_SECRET
    ▼
② 建立 LogBatch，切成 chunk（每批 ≤300 筆）
    ▼
③ 每個 chunk 送 Claude Haiku 分析
   Haiku 輸出：[{ star_rank, title, match_key, log_ids, ... }]
    ▼
④ 程式覆蓋 match_key，撈回原始 log 做溯源
    ▼
⑤ 同 match_key 的事件合併，累計到當天的 FlashResult
    ▼
  （每天凌晨 02:00）
    ▼
⑥ Celery Beat 觸發 Pro Task
    ▼
⑦ 讀取當天所有累計事件，送 Claude Sonnet 做最終彙整
    ▼
⑧ Sonnet 去重、判斷延續事件、產出最終清單
    ▼
⑨ 寫入 security_events 資料表

前端使用者
    │ GET /api/events
    ▼
查詢 security_events，回傳事件列表
```
