# P1-code 後端學習指南

> 目標讀者：有程式基礎（例如寫過 JavaScript）、第一次接觸 Python / FastAPI 的新團隊成員。
>
> 這份文件以「**一個用戶從登入到登出**」的完整旅程為主軸，帶你走過後端每一層。
> 架構速查表請見 [backend-architecture.md](backend-architecture.md)

---

## 第 0 章｜先看整體，建立地圖

學一個陌生的程式庫，最忌讀到哪算到哪。先把地圖記下來，後面每章就知道自己在哪個位置。

後端分成六層，由上到下：

```
HTTP 請求進來
      │
      ▼
  進入點 (main.py)         ← 組裝整個 app
      │
      ▼
  中介層 (middlewares/)    ← 每個請求都先到這，記 log、擋錯誤
      │
      ▼
  API 路由 (api/)          ← 決定這個請求由哪個函式處理
  Schema (api/schema/)    ← 驗證傳進來的資料格式
      │
      ▼
  工具函式 (utils/)        ← 驗 token、雜湊密碼等共用工具
      │
      ▼
  資料庫層 (db/)           ← 連線、ORM Model、讀寫資料
```

另外有三個「全域支援」模組，任何層都可以呼叫：
- `config/settings.py` — 讀設定
- `logger_utils/` — 寫 log
- `bpBoxAlembic/` — 管理資料庫 schema 版本

---

## 第 1 章｜app 是怎麼啟動的

**檔案：`app/main.py`**

```python
def create_app():
    server = FastAPI(lifespan=lifespan)

    server.add_middleware(RequestResponseHandlerMiddleware)  # 掛上中介層

    server.include_router(auth_router)    # 掛上 /auth 路由
    server.include_router(user_router)    # 掛上 /user 路由
    server.include_router(notice_router)  # 掛上 /api/notices 路由
    # … 其他 router

    return server

app = create_app()
```

如果你用過 Express.js，這個模式你很熟：

| Express.js | FastAPI |
|-----------|---------|
| `const app = express()` | `server = FastAPI()` |
| `app.use(middleware)` | `server.add_middleware(...)` |
| `app.use('/auth', authRouter)` | `server.include_router(auth_router)` |

**`lifespan` 是什麼？**

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    system_logger.info("⚡ Systems initialized")   # 伺服器啟動時執行
    yield                                          # ← 在這裡等待，處理所有請求
    system_logger.info("⚡ Systems Stopped")       # 伺服器關閉時執行
```

`yield` 前是「啟動鉤子」，`yield` 後是「關閉鉤子」。目前只用來記 log，以後可以在這裡做初始化（例如預熱快取）。

---

## 第 2 章｜設定從哪裡來

**檔案：`app/config/settings.py`** 和 **`backend/.env`**

`.env` 檔長這樣（實際值保密，不進版控）：
```
DATABASE_URL=postgresql://user:password@localhost:5432/p1db
JWT_SECRET_KEY=your-very-secret-key
JWT_EXPIRE_MINUTES=60
```

`settings.py` 負責把它讀進來：
```python
class Settings(BaseSettings):
    database_url: str = Field(..., alias="DATABASE_URL")
    jwt_secret_key: str = Field(..., alias="JWT_SECRET_KEY")
    jwt_expire_minutes: int = Field(60, alias="JWT_EXPIRE_MINUTES")

settings = Settings()
```

這樣其他地方要用設定時，只要：
```python
from app.config.settings import settings

settings.database_url      # 資料庫連線字串
settings.jwt_secret_key    # JWT 簽名金鑰
settings.jwt_expire_minutes  # token 有效分鐘數
```

**為什麼不直接寫死在 code 裡？**
因為開發環境和正式環境的設定不同（不同資料庫、不同 secret key）。用 `.env` 可以每個環境各自設定，又不會把機密資訊上傳到 GitHub。

---

## 第 3 章｜請求進門的第一關：Middleware

**檔案：`app/middlewares/request_response_handler.py`**

每個 HTTP 請求，不管是登入還是查用戶，都先經過這裡。

```python
class RequestResponseHandlerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        # ── 請求進來時 ──
        logger.info(f"Request: {request.method} {request.url.path}")

        # 嘗試從 Authorization header 解出 user_id，存到 request.state
        # （成功就能在 log 裡記是哪個用戶操作的）

        # ── 把請求往下傳給真正的 route handler ──
        response = await call_next(request)

        # ── 回應要出去時 ──
        # 4xx 錯誤碼標準化：除了 400/401/403/404，其他 4xx 一律改成 400
        # （避免洩漏伺服器細節給外部）

        logger.info(f"Response: {request.method} {request.url.path} -> {response.status_code}")
        return response
```

Express.js 的類比：這就是 `app.use((req, res, next) => { ... next(); })`，只是寫法是 Python 的 `async/await`。

---

## 第 4 章｜登入流程完整追蹤

這是整份指南的核心章節。我們跟著 `POST /auth/login` 這個請求，一步一步看程式怎麼執行。

---

### 4-1. 請求長什麼樣子

用戶在前端填完帳號密碼後，瀏覽器送出：

```
POST /auth/login
Content-Type: application/json

{
  "email": "alice@example.com",
  "password": "secret123"
}
```

---

### 4-2. Schema：先驗格式

**檔案：`app/api/schema/auth.py`**

```python
class LoginRequest(BaseModel):
    email: EmailStr   # 必填，且格式必須是合法 email
    password: str     # 必填，非空字串
```

FastAPI 收到請求後，**自動**把 JSON body 對照 `LoginRequest`。如果 `email` 格式不對，或缺少欄位，FastAPI 直接回 **422 Unprocessable Entity**，連 route 函式都不會進去。

這就是 Pydantic 的核心功能：**你只要定義「格式長什麼樣」，驗證自動發生。**

---

### 4-3. Route 函式

**檔案：`app/api/auth.py`**

```python
@router.post("/login", response_model=LoginResponse)
def login(login_req: LoginRequest, db: Session = Depends(get_db)) -> LoginResponse:
    ...
```

這裡有幾個關鍵點：

**`login_req: LoginRequest`**
FastAPI 自動把驗過格式的 JSON 注入進來，你直接用 `login_req.email`、`login_req.password`。

**`db: Session = Depends(get_db)`**
這是 FastAPI 的「依賴注入」（Dependency Injection）。`Depends(get_db)` 意思是：「請去呼叫 `get_db()` 函式，把它回傳的東西給我」。`get_db()` 會給你一個資料庫 session，讓你可以查資料。

如果你寫過 Express.js，這就像 middleware 幫你在 `req` 上掛好了 `req.db`，讓你在 handler 裡直接取用。

---

### 4-4. get_db()：資料庫連線怎麼來的

**檔案：`app/db/connector.py`**

```python
# 建立資料庫引擎（只建一次，在模組載入時）
engine = create_engine(settings.database_url, pool_pre_ping=True)

# Session 工廠
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def get_db():
    db = SessionLocal()   # 建立這個請求專用的 session
    try:
        yield db           # 把 session 給 route 函式用
    finally:
        db.close()         # 請求結束後關閉，不管成功或出錯
```

`yield` 讓 `get_db` 變成「生成器」，FastAPI 在請求開始時拿到 session，請求結束後自動執行 `finally` 關掉 session。這樣每個請求都有自己的 session，不會互相干擾。

---

### 4-5. ORM Model：User 長什麼樣

**檔案：`app/db/models/fn_user_role.py`**

```python
class User(Base):
    __tablename__ = "tb_users"   # 對應資料庫的 tb_users 資料表

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(255), unique=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    updated_by: Mapped[int | None] = mapped_column(Integer, ForeignKey("tb_users.id"))
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
```

ORM（Object-Relational Mapping）讓你用 Python 物件操作資料庫，不用寫 SQL。`User` class 的每個屬性對應資料表的一個欄位。

查詢的寫法：
```python
user = db.query(User).filter(User.email == login_req.email).first()
# 等同於 SQL：SELECT * FROM tb_users WHERE email = ? LIMIT 1
```

---

### 4-6. 驗證密碼

**檔案：`app/utils/util_store.py`**

```python
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def verify_password(hashed: str, password: str) -> bool:
    return hmac.compare_digest(hashed, hash_password(password))
```

資料庫裡存的是密碼的 **SHA-256 雜湊值**，不是明文。驗證時，把用戶送來的密碼雜湊一次，再跟資料庫存的值比對。

`hmac.compare_digest` 是做常數時間比較（constant-time comparison），確保即使字串不匹配，比對時間也相同，防止攻擊者透過測量回應時間來猜測密碼。

---

### 4-7. 簽發 JWT Token

**檔案：`app/utils/util_store.py`**

```python
def create_access_token(user_id: int) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(user_id),    # subject：這個 token 代表哪個用戶
        "jti": uuid4().hex,     # JWT ID：這個 token 的唯一識別碼
        "iat": now,             # issued at：何時簽發
        "exp": now + timedelta(minutes=settings.jwt_expire_minutes),  # 到期時間
    }
    return jwt.encode(payload, settings.jwt_secret_key, algorithm="HS256")
```

JWT（JSON Web Token）是一種**數位通行證**。伺服器用 `jwt_secret_key` 簽名，確保 token 沒被竄改。用戶之後每次請求都帶著它，伺服器驗簽就能知道是誰發出的請求。

`jti`（JWT ID）是每個 token 的唯一碼，登出時靠它來讓 token 失效（見第 6 章）。

---

### 4-8. 登入回傳

```python
return LoginResponse(access_token=create_access_token(user.id), user_id=user.id)
```

成功後回傳：
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user_id": 42
}
```

前端拿到 `access_token` 後，往後每次請求都要放在 Header：
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

---

## 第 5 章｜帶著 token 操作

登入成功後，用戶要查用戶列表：`GET /user`。這次的關鍵是「伺服器怎麼確認這個請求是合法的已登入用戶」。

---

### 5-1. `authenticate()`：驗 token 的工具函式

**檔案：`app/utils/util_store.py`**

```python
@dataclass(frozen=True)
class AuthContext:
    user_id: int
    token: str

def authenticate(
    credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> AuthContext:
    token = credentials.credentials  # 從 Authorization header 取出 token 字串

    # 1. 解碼並驗簽（金鑰不對 or 已過期 → 拋 401）
    payload = jwt.decode(token, settings.jwt_secret_key, algorithms=["HS256"])
    sub = payload.get("sub")  # user_id
    jti = payload.get("jti")  # token 的唯一 ID

    # 2. 查黑名單（這個 token 有沒有被登出過）
    if db.query(TokenBlacklist).filter(TokenBlacklist.token_jti == jti).first():
        raise HTTPException(status_code=401, ...)

    return AuthContext(user_id=int(sub), token=token)
```

---

### 5-2. Route 函式如何使用

**檔案：`app/api/user.py`**

```python
@router.get("", response_model=UserListResponse)
def get_user_list(
    role_id: int | None = Query(None),
    keyword: str | None = Query(None),
    db: Session = Depends(get_db),
    auth: AuthContext = Depends(authenticate),   # ← 驗 token，取得身份
) -> UserListResponse:
    ...
```

`Depends(authenticate)` 讓 FastAPI 在進入這個函式之前，先執行 `authenticate()`。如果 token 無效，`authenticate()` 會拋出 401，用戶根本進不來。如果 token 有效，`auth` 就是驗完的 `AuthContext(user_id=42, token="...")`。

---

### 5-3. 查詢邏輯

```python
query = db.query(User)

if role_id is not None:
    # 找有這個 role 的 user_id 清單，再過濾
    sub = db.query(UserRole.user_id).filter(UserRole.role_id == role_id).subquery()
    query = query.filter(User.id.in_(sub))

if keyword:
    like = f"%{keyword}%"
    query = query.filter(or_(User.name.ilike(like), User.email.ilike(like)))

rows = query.order_by(User.id.asc()).all()
```

`.ilike()` 是大小寫不敏感的 LIKE 搜尋，`%keyword%` 表示「keyword 出現在任何位置」。

---

## 第 6 章｜登出：JWT 黑名單機制

**檔案：`app/api/auth.py`**

JWT 本身是**無狀態**的，一旦簽發就無法「撤銷」（除非等它到期）。這個專案用「黑名單」來解決：登出時把 token 的 `jti` 存到 `tb_token_blacklist`，之後每次 `authenticate()` 都會查一次黑名單。

```python
@router.post("/logout")
def logout(auth: AuthContext = Depends(authenticate), db: Session = Depends(get_db)):
    # 解碼 token，取出 jti 和到期時間
    payload = jwt.decode(auth.token, settings.jwt_secret_key, algorithms=["HS256"])
    jti = payload["jti"]
    exp = payload["exp"]

    # 已經在黑名單裡（重複登出）
    if db.query(TokenBlacklist).filter(TokenBlacklist.token_jti == jti).first():
        return LogoutResponse(detail="JWT expired")

    # 寫入黑名單
    db.add(TokenBlacklist(
        token_jti=jti,
        expired_at=datetime.fromtimestamp(exp, tz=timezone.utc),
        updated_by=auth.user_id,
    ))
    db.commit()
    return LogoutResponse(detail="Logged out")
```

**為什麼要存 `expired_at`？**
黑名單裡的舊紀錄可以在到期後清掉，避免無限累積。`expired_at` 就是清除的依據。

---

## 第 7 章｜日誌系統

**檔案：`app/logger_utils/log_channels.py`**、`logger_config.json`

這個後端的 log 依用途分成四個 channel，各自寫到不同的檔案：

| Channel | 儲存路徑 | 什麼情況寫 |
|---------|---------|-----------|
| `system` | `logs/system/system.log` | 伺服器啟動/關閉、登入登出、一般操作 |
| `user` | `logs/user/{user_id}/{日期}.log` | 每個已驗證用戶的操作記錄（一人一檔） |
| `error` | `logs/error/error.log` | 未捕捉的例外錯誤，附完整 traceback |
| `service` | `logs/service/service.log` | 排程任務輸出（預留） |

**怎麼使用：**

```python
from app.logger_utils import get_system_logger

system_logger = get_system_logger()
system_logger.info(f"User {user_id} logged in")
```

每個 logger 都是「懶初始化」（lazy init）：第一次呼叫 `get_system_logger()` 時才建立 log 檔和 sink，之後都重用同一個。

**user channel 的設計：**
```python
get_user_logger(user_id=42).info("Queried user list")
# 寫到 logs/user/42/2026-04-30.log
```
每個用戶的行為記在自己的 log 檔裡，調查問題時直接找那個 user_id 的檔案。

**rotation 和 retention：**
- `rotation: "00:00"` — 每天午夜自動開新檔
- `retention: "1 month"` — 超過一個月的 log 自動刪除
- error channel 的 retention 是「1 year」，保留更久

---

## 第 8 章｜資料庫怎麼長出來的（Alembic）

**目錄：`bpBoxAlembic/`**

Alembic 是資料庫的「版本控制」工具，功能類似 git 之於程式碼。

**為什麼需要它？**

開發過程中，資料表的欄位會一直變動（新增欄位、改型別、加資料表）。如果直接手動改資料庫，其他開發者和正式環境就很難同步。Alembic 把每次變更記成一個「migration 版本檔」，所有人只要執行同一份版本檔就能同步。

**常用指令：**

```bash
# 執行所有未套用的 migration（把 DB 更新到最新）
alembic upgrade head

# 回滾到上一個版本
alembic downgrade -1

# 查看目前套用到哪個版本
alembic current
```

**這個專案的 migration 檔：**

```
bpBoxAlembic/versions/31cf8ba73762_recreate_tables.py
```

這個版本檔建立了所有資料表（`tb_users`、`tb_roles`、`tb_user_roles`、`tb_token_blacklist`、`tb_notices` 等）。新加入的成員跑一次 `alembic upgrade head`，本地資料庫就會有完整的 schema。

---

## 附錄｜新人第一天 Checklist

1. **複製 `.env.example`** 為 `.env`，填入資料庫連線字串和 JWT secret key
2. **安裝依賴**：`uv sync`（或 `pip install -r requirements.txt`）
3. **建立資料庫**：`alembic upgrade head`
4. **啟動伺服器**：`uvicorn app.main:app --reload`
5. **開啟 API 文件**：瀏覽器前往 `http://localhost:8000/docs`
6. **跑測試**：`pytest`

---

## 附錄｜讀 Code 的順序建議

如果你想深入了解某個功能，建議按這個順序讀：

```
schema/xxx.py        ← 先看資料格式（輸入什麼、輸出什麼）
    │
api/xxx.py           ← 再看 route 函式怎麼處理
    │
db/models/xxx.py     ← 搞清楚資料存在哪個 table 的哪些欄位
    │
utils/util_store.py  ← 如果有驗 token 或密碼相關，看這裡
```

這樣你對每個 API 都能從外到內建立完整的心智模型。
