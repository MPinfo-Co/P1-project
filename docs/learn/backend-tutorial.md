# P1-code 後端程式碼教學

> 假設你完全不懂後端，從頭解釋每一個概念。

---

## 第一章：程式是怎麼啟動的？

### `main.py` — 程式的大門

```python
app = create_app()
```

執行 `uvicorn app.main:app` 時，Python 跑這支檔案，建立 FastAPI 應用程式。

`create_app()` 做了三件事：

**① 掛上 Middleware**

```python
server.add_middleware(RequestResponseHandlerMiddleware)
```

Middleware 是「每個 HTTP 請求都必須先通過的關卡」，負責記錄 log 和身份解析（詳見第六章）。

**② 掛上所有 Router**

```python
server.include_router(auth_router)
server.include_router(user_router)
# ...
```

每個 router 是一組 API，分別放在不同檔案，這裡統一組裝進來。

**③ 設定 Lifespan（生命週期）**

```python
@asynccontextmanager
async def lifespan(app):
    # 伺服器啟動時執行
    yield
    # 伺服器關閉時執行
```

這裡只是用 logger 記錄啟動/關閉時間，讓你知道服務什麼時候上線。

---

## 第二章：設定值從哪裡來？

### `config/settings.py`

```python
class Settings(BaseSettings):
    database_url: str = Field(..., alias="DATABASE_URL")
    jwt_secret_key: str = Field(..., alias="JWT_SECRET_KEY")
    jwt_expire_minutes: int = Field(60, alias="JWT_EXPIRE_MINUTES")
    jwt_algorithm: str = "HS256"

settings = Settings()
```

所有「不能寫死在程式碼裡」的東西都放在 `.env` 檔案，例如資料庫密碼。`Settings` 類別自動讀取這些值。

> **小白理解：** `.env` 是記事本，裡面寫 `DATABASE_URL=postgresql://...`。程式啟動時自動讀進來。

整個後端只有一個 `settings` 物件，任何地方 `from app.config.settings import settings` 就能用。

---

## 第三章：資料庫是怎麼連的？

### `db/connector.py`

```python
engine = create_engine(settings.database_url, pool_pre_ping=True, future=True)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, ...)

def get_db() -> Iterator[Session]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

- **engine**：資料庫的「連線工廠」，`pool_pre_ping=True` 表示每次用連線前先 ping 一下，確保連線還活著。
- **SessionLocal**：每次操作資料庫，就從這裡開一個 Session（工作視窗），`commit()` 才真正寫入。
- **`get_db()`**：FastAPI 的依賴注入函式。每個 API 呼叫時自動產生一個 db，結束後自動關閉。

> **小白理解：** 就像借圖書館電腦——進館借一台，離館還回去，不會一直佔用。

---

## 第四章：資料表長什麼樣子？

### `db/models/` — 以功能模組命名的 Model 檔案

每個 model 檔案名稱都有 `fn_` 前綴，代表對應的功能模組：

| 檔案 | 包含的 Model |
|------|-------------|
| `fn_user_role.py` | User, Role, UserRole, TokenBlacklist |
| `fn_expert_security_event.py` | SecurityEvent, EventHistory |
| `fn_expert_ssb_pipeline.py` | LogBatch, FlashResult 等 |
| `fn_notice.py` | Notice |
| `fn_km.py` | 知識庫相關 |
| `fn_partner.py` | AI 夥伴相關 |

所有 model 都繼承自 `base.py` 的 `Base`：

```python
class Base(DeclarativeBase):
    """Project-wide declarative base."""
```

### 使用者相關（`fn_user_role.py`）

```python
class User(Base):
    __tablename__ = "tb_users"   # ← 資料表名稱加 tb_ 前綴

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    updated_by: Mapped[int | None] = mapped_column(Integer, ForeignKey("tb_users.id"), ...)
    updated_at: Mapped[datetime] = ...
```

> 注意 `Mapped[int]` 這種新寫法是 SQLAlchemy 2.0 的語法，比舊版更清楚地表達「這個欄位的型別是 int」。

### 角色權限（boolean flag 設計）

```python
class Role(Base):
    __tablename__ = "tb_roles"

    id: ...
    name: ...
    can_access_ai: Mapped[bool] = ...        # 可使用 AI 功能
    can_use_kb: Mapped[bool] = ...           # 可使用知識庫
    can_manage_accounts: Mapped[bool] = ...  # 可管理使用者
    can_manage_roles: Mapped[bool] = ...     # 可管理角色
    can_edit_ai: Mapped[bool] = ...
    can_manage_kb: Mapped[bool] = ...
    can_manage_notices: Mapped[bool] = ...   # 可發布公告
```

> **設計亮點：** 舊版需要 `functions` + `role_functions` 兩張關聯表才能表達「角色有哪些權限」。新版直接在 `Role` 上放 boolean 欄位，查詢更直接，不需要 JOIN。
>
> **查詢比較：**
> - 舊：`role → role_functions → functions`（需要兩次 JOIN）
> - 新：`role.can_manage_accounts`（直接讀欄位）

---

## 第五章：身份驗證怎麼運作？

### `utils/util_store.py` — 驗證工具箱

這個檔案把 JWT 產生、密碼比對、身份驗證全部放在一起。

**密碼雜湊（SHA-256）：**

```python
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def verify_password(hashed: str, password: str) -> bool:
    return hmac.compare_digest(hashed, hash_password(password))
```

`hmac.compare_digest` 做「常數時間比對」，避免攻擊者透過回應時間差異猜出密碼。

**產生 JWT：**

```python
def create_access_token(user_id: int) -> str:
    payload = {
        "sub": str(user_id),   # 誰的 token
        "jti": uuid4().hex,    # 唯一識別碼（用於登出撤銷）
        "iat": now,            # 發行時間
        "exp": now + timedelta(minutes=60),  # 過期時間
    }
    return jwt.encode(payload, settings.jwt_secret_key, algorithm="HS256")
```

**`jti`（JWT ID）是新版的關鍵設計：** 舊版登出是把整個 token 字串存入黑名單，token 很長。新版只存 `jti`（32 個字元的 UUID），節省空間也更語意清晰。

**驗證身份（FastAPI 依賴注入）：**

```python
@dataclass(frozen=True)
class AuthContext:
    user_id: int
    token: str

def authenticate(
    credentials = Depends(oauth2_scheme),
    db = Depends(get_db),
) -> AuthContext:
    token = credentials.credentials
    payload = jwt.decode(token, settings.jwt_secret_key, ...)
    jti = payload.get("jti")

    # 檢查 jti 是否被登出過
    if db.query(TokenBlacklist).filter(TokenBlacklist.token_jti == jti).first():
        raise HTTPException(401, ...)

    return AuthContext(user_id=int(payload["sub"]), token=token)
```

任何 API 只要加上 `auth: AuthContext = Depends(authenticate)`，FastAPI 就自動執行這段驗證。驗證失敗直接回 401，不進主邏輯。

> **`AuthContext` 是什麼？** 一個小的資料物件，裝著「誰在呼叫」（user_id）和「他的 token」。API 函式透過這個物件知道操作者是誰。

---

## 第六章：Middleware 是怎麼運作的？

### `middlewares/request_response_handler.py`

每一個 HTTP 請求都會先經過這裡：

```python
class RequestResponseHandlerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        # 1. 記錄 Request log
        _resolve_logger(request).info(
            f"Request: {request.method} {request.url.path}"
        )

        # 2. 解析 token → 填入 request.state.user_id
        auth_header = request.headers.get('authorization') or ''
        if auth_header.lower().startswith('bearer '):
            # 驗證 token，把 user_id 存進 request.state
            request.state.user_id = authenticate(...).user_id

        # 3. 轉交給實際的路由處理
        response = await call_next(request)

        # 4. 4xx 正規化
        if 400 <= response.status_code < 500 and response.status_code not in {400, 401, 403, 404}:
            response = JSONResponse(400, {"detail": "Bad Request"})

        # 5. 記錄 Response log
        _resolve_logger(request).info(
            f"Response: {request.method} {request.url.path} -> {response.status_code}"
        )
        return response
```

> **為什麼要做 4xx 正規化？** 假設後端發出 `422 Unprocessable Entity`（通常是輸入格式錯誤），攻擊者可以透過這個細節猜測欄位結構。統一改成 400 可以減少洩漏的資訊。

**`_resolve_logger` 的設計：**

```python
def _resolve_logger(request):
    user_id = getattr(request.state, "user_id", None)
    if user_id is not None:
        return get_user_logger(user_id)   # 已登入 → 寫到使用者自己的 log 檔
    return get_system_logger()             # 未登入 → 寫到系統 log
```

每個使用者的操作記錄在自己專屬的 log 檔，方便事後追蹤是誰做了什麼。

---

## 第七章：API 端點怎麼寫？

### `api/user.py` — 使用者管理

以「建立使用者」為例：

```python
@router.post("", response_model=UserCreateResponse, status_code=201)
def create_user(
    payload: UserCreateRequest,           # Pydantic 自動驗證輸入格式
    db: Session = Depends(get_db),        # 自動取得資料庫連線
    auth: AuthContext = Depends(authenticate),  # 自動驗證登入
) -> UserCreateResponse:
    # 檢查 email 是否重複
    if db.query(User).filter(User.email == payload.email).first():
        raise HTTPException(409, "Email already registered.")

    # 建立 User 物件
    user = User(name=payload.name, email=payload.email, password_hash=hash_password(payload.password), ...)
    db.add(user)
    db.flush()   # ← 取得 user.id（還沒真正寫入）

    # 建立角色關聯
    for rid in payload.role_ids:
        db.add(UserRole(user_id=user.id, role_id=rid))

    db.commit()  # ← 全部一起寫入
    return UserCreateResponse(id=user.id, name=user.name, email=user.email)
```

> **`flush()` vs `commit()` 有什麼差？**
> - `flush()`：把操作送進資料庫但還沒確認，可以取得自動產生的 id，但還可以 rollback。
> - `commit()`：確認寫入，無法撤回。
>
> 這裡先 `flush()` 取得 `user.id`，再用 id 建立 `UserRole`，最後一次 `commit()` 確認。

**刪除 = 軟刪除：**

```python
@router.delete("/{user_id}", response_model=UserDeleteResponse)
def delete_user(user_id: int, ...):
    user = db.get(User, user_id)
    user.is_active = False   # ← 不真正刪除，只是停用
    db.commit()
```

> **為什麼不真正刪除？** 保留歷史記錄，避免關聯資料孤立（例如這個 user 曾處理的事件記錄）。

---

## 第八章：Pydantic Schema 怎麼用？

### `api/schema/` — 資料格式定義

Schema 和路由放在同一個資料夾，方便對照。

```python
# api/schema/user.py
class UserCreateRequest(BaseModel):
    name: str
    email: EmailStr      # 自動驗證 email 格式
    password: str
    role_ids: list[int]

class UserCreateResponse(BaseModel):
    id: int
    name: str
    email: str
```

FastAPI 自動用這些 schema：
- **輸入**：驗證請求 body，格式錯誤直接回 400（再被 middleware 改成 400）
- **輸出**：只把 schema 裡定義的欄位回傳給前端（不會不小心洩漏 `password_hash`）

---

## 第九章：權限怎麼判斷？

### `notice.py` — 以系統公告為例

```python
def _has_notice_permission(user_id: int, db: Session) -> bool:
    return (
        db.query(Role)
        .join(UserRole, Role.id == UserRole.role_id)
        .filter(UserRole.user_id == user_id, Role.can_manage_notices.is_(True))
        .first()
        is not None
    )

@router.post("")
def create_notice(payload, db, auth):
    if not _has_notice_permission(auth.user_id, db):
        raise HTTPException(403, "您沒有執行此操作的權限")
    ...
```

查詢邏輯：「`auth.user_id` 所屬的角色中，有沒有任何一個 `can_manage_notices = True`？」

> **與舊版設計的差異：** 舊版要沿著 `user → user_roles → role_functions → functions` 這條鏈查詢。新版只需要 user → user_roles → roles，直接讀 role 上的 boolean 欄位。

---

## 第十章：資安事件怎麼管？

### `api/events.py` — 事件查詢與處理

事件有兩層資料：

**`tb_security_events`（主表）：** 每個已偵測的資安事件，有星級（`star_rank`）、狀態（`current_status`）、影響範圍等欄位。

**`tb_event_history`（歷程表）：** 每次有人更新事件的狀態或留言，都在這裡記一筆。

```python
@router.post("/{event_id}/history", status_code=201)
def add_history(event_id, payload, db, auth):
    entry = EventHistory(
        event_id=event_id,
        user_id=auth.user_id,   # ← 誰留的記錄
        action=payload.action,
        note=payload.note,
        ...
    )
    db.add(entry)
    db.commit()
```

---

## 第十一章：Log 系統

### `logger_utils/` — 三種頻道

```python
get_system_logger()        # 伺服器啟動、無法識別的請求
get_user_logger(user_id)   # 每個 user 一支 log 檔，記錄操作行為
get_error_logger()         # 未捕捉的例外錯誤
```

Middleware 根據請求是否已驗證，自動選擇寫到哪個頻道。

---

## 第十二章：資料庫版本管理

### `bpBoxAlembic/` — Schema Migration

重構後改用全新的 `bpBoxAlembic/` 目錄，裡面只有一個 migration：

```
bpBoxAlembic/versions/31cf8ba73762_recreate_tables.py
```

這個 migration 是「把所有資料表清掉重建」的版本，代表這次重構是一次乾淨的 schema 重設。

> **小白理解：** 就像搬家時把所有家具重新排列，而不是一件一件挪動。新的 migration 體現了新的 schema 設計（`tb_` 前綴、boolean 權限旗標等）。

---

## 整體流程回顧

```
前端使用者
    │ POST /auth/login（帶 email + password）
    ▼
① Middleware 記錄 request log
    ▼
② auth.py 驗證帳密（SHA-256），產生 JWT（含 jti）
    ▼
③ 回傳 access_token

後續每個 API 請求
    │ Header: Authorization: Bearer <token>
    ▼
④ Middleware 解析 token → request.state.user_id
    ▼
⑤ API 透過 Depends(authenticate) 取得 AuthContext
    ▼
⑥ 執行業務邏輯（查詢 / 新增 / 更新）
    ▼
⑦ Middleware 記錄 response log，若 4xx 非標準則正規化
    ▼
⑧ 回傳結果給前端
```
