# 後端程式規範（Python / FastAPI）

> 適用範圍：`P1-code/backend/`
> 格式與 import 排序由 **ruff** 自動管理，本文件只涵蓋 ruff 管不到的架構、命名、禁用模式。

---

## 一、命名速查表

### 1-1 檔案命名

資料夾即類型，檔名只寫 domain，不加後綴。

| 類型 | 位置 | 範例 |
|------|------|------|
| Router | `app/api/{domain}.py` | `app/api/events.py` |
| Schema | `app/schemas/{domain}.py` | `app/schemas/security_event.py` |
| SQLAlchemy Model | `app/db/models/{domain}.py` | `app/db/models/user.py` |
| Service（外部整合）| `app/services/{domain}.py` | `app/services/claude_flash.py` |
| 測試 | `tests/test_{domain}_{動作}.py` | `tests/test_user_create.py` |

### 1-2 Pydantic Schema 命名

**資源型（CRUD）：**

| 用途 | 格式 | 範例 |
|------|------|------|
| 建立輸入 | `{Domain}Create` | `UserCreate` |
| 更新輸入 | `{Domain}Update` | `UserUpdate` |
| 單筆輸出 | `{Domain}Out` | `HistoryOut` |
| 詳細輸出 | `{Domain}Detail` | `EventDetail` |
| 列表單項 | `{Domain}Item` | `EventItem` |
| 列表回應 | `{Domain}ListResponse` | `EventListResponse` |

**動作型（非 CRUD，如 auth）：**

| 用途 | 格式 | 範例 |
|------|------|------|
| 輸入 | `{Action}Request` | `LoginRequest` |
| 輸出 | `{Action}Response` | `TokenResponse` |

ORM 對應的 schema 加：`model_config = {"from_attributes": True}`

### 1-3 函式與變數命名

| 情境 | 格式 | 範例 |
|------|------|------|
| 資源型 endpoint | `{action}_{domain}` | `list_events`, `get_event` |
| 動作型 endpoint | 動詞即可 | `login`, `logout` |
| DB session 參數 | `db` | `db: Session = Depends(get_db)` |
| 當前使用者參數 | `current_user` | `current_user: User = Depends(get_current_user)` |

### 1-4 Router prefix

```
/api/{domain}
```

無版本號。是否複數視語意而定（`/api/events`、`/api/auth`）。

---

## 二、架構規則

### 2-1 分層結構

```
Request
  ↓
app/api/{domain}.py          ← Router：接收、驗證、DB 操作、回傳
  ↓ Depends()
app/core/deps.py             ← 注入：get_db、get_current_user
  ↓
app/db/models/{domain}.py    ← SQLAlchemy ORM model
app/schemas/{domain}.py      ← Pydantic 輸入/輸出驗證

app/services/{domain}.py     ← 外部整合專用（Claude、Email 等）
app/core/security.py         ← JWT、密碼 hash 等安全工具
app/core/config.py           ← pydantic-settings 設定
```

### 2-2 各層職責

| 層 | 做什麼 | 不做什麼 |
|----|--------|---------|
| **Router** (`app/api/`) | 讀參數、呼叫 Depends、查 DB、回傳 response / HTTPException | 呼叫其他 router、放業務邏輯函式 |
| **Deps** (`app/core/deps.py`) | 提供可被 `Depends()` 注入的函式 | 查詢與當前請求上下文無關的資料 |
| **Service** (`app/services/`) | 包裝外部 API（Claude、Email 等） | 寫 CRUD、查業務資料 |
| **Schema** (`app/schemas/`) | 定義 Pydantic model | 放業務邏輯 |
| **Model** (`app/db/models/`) | 定義 SQLAlchemy table mapping | 放業務邏輯 |

---

## 三、禁用模式

### ✗ 1 deps 查詢業務資料

```python
# ✗ deps 查非 auth 的業務資料
def get_user_list(db: Session = Depends(get_db)):
    return db.query(User).all()

# ✓ deps 只做 current user / permission check
def get_current_user(db: Session = Depends(get_db)) -> User:
    return db.query(User).filter(User.id == ...).first()
```

### ✗ 2 service 寫 CRUD

```python
# ✗
class UserService:
    def create_user(self, db, data): ...

# ✓ service 只包外部 API
class ClaudeFlashService:
    def analyze_logs(self, logs: list[str]): ...
```

### ✗ 3 hardcode 設定值

```python
# ✗
SECRET_KEY = "my-secret-key-123"

# ✓
from app.core.config import settings
settings.SECRET_KEY
```

### ✗ 4 函式內 import settings

```python
# ✗
@router.post("/login")
def login():
    from app.core.config import settings  # 函式內才 import
    ...

# ✓ module 頂層 import
from app.core.config import settings
```

### ✗ 5 吞掉例外

```python
# ✗
try:
    db.commit()
except:
    pass

# ✓
try:
    db.commit()
except SQLAlchemyError:
    db.rollback()
    raise HTTPException(status_code=500, detail="資料庫錯誤")
```

### ✗ 6 把內部錯誤回傳給 client

```python
# ✗ 洩漏 stack trace 或內部訊息
raise HTTPException(status_code=500, detail=str(e))

# ✓
raise HTTPException(status_code=500, detail="伺服器錯誤")
```

### ✗ 7 用裸 dict 當 API 參數

```python
# ✗
def create_user(data: dict): ...

# ✓
def create_user(data: UserCreate): ...
```

### ✗ 8 明碼儲存密碼

```python
# ✗
user.hashed_password = data.password

# ✓ 統一從 app/core/security.py 取 hash 工具
from app.core.security import get_password_hash
user.hashed_password = get_password_hash(data.password)
```

---

## 四、測試慣例

### 4-1 命名

```
test_{描述行為}_{預期結果}

範例：
  test_create_user_returns_201
  test_login_wrong_password_returns_401
  test_delete_user_self_returns_400
```

### 4-2 TestSpec ID 標注（必填）

每個 test function 的 docstring 標注對應 `_test_api.md` 的測試案例 ID：

```python
def test_create_user_returns_201(client):
    """對應 T1"""
    resp = client.post("/api/users", json={...}, headers={...})
    assert resp.status_code == 201
```

### 4-3 數量下限

pytest 數量 **≥** `_test_api.md` 測試案例數。

### 4-4 外部依賴隔離

```python
# ✓ mock 外部 service，不讓測試依賴 Claude API 或 DB seed 狀態
with patch("app.api.ingest._process_ingest", return_value={"batch_id": 1}):
    resp = client.post("/api/ingest", json=payload)
```

### 4-5 測行為，不測實作

```python
# ✗
assert user_service.create_user.called

# ✓
assert resp.status_code == 201
assert "id" in resp.json()
```
