# Spec：backend-syntax-guide.md 設計文件

## 目標

為「會基本 Python、但未接觸 FastAPI 生態系」的初學者，撰寫一份語法說明文件，讓讀者能看懂 `docs/learn/backend-guide.md` 中出現的所有程式碼片段。

不求包山包海，以「看懂 backend-guide.md」為終點。

---

## 文件位置

`docs/learn/backend-syntax-guide.md`

---

## 文件結構

### 開頭：語法索引表

表格欄位：語法名稱 | 簡易說明 | 出現章節 | anchor 連結

讓讀者遇到不懂的語法時，查表跳到對應說明。

---

### 本體：章節順序對應 backend-guide.md 有程式碼的章節

#### 4.1 應用程式啟動
說明對象：
- `app.include_router(router, prefix="...")` — 把路由器掛載到 FastAPI 應用
- `CORSMiddleware` — 設定跨域存取允許規則

#### 4.2 使用者登入與 JWT 認證
說明對象：
- `@router.post("/path")` — 路由裝飾器，宣告 HTTP 方法與路徑
- `Depends(func)` — FastAPI 依賴注入，自動執行並傳入結果
- `bcrypt.checkpw()` / `bcrypt.hashpw()` — 密碼雜湊比對與建立
- `jwt.encode()` / `jwt.decode()` — JWT token 簽署與驗證
- `db.query(Model).filter(...).first()` — SQLAlchemy 查詢資料庫

#### 4.3 排程任務（Flash Task）
說明對象：
- `@celery_app.task` — 宣告 Celery 非同步任務
- `beat_schedule` — 設定 Celery 排程（執行頻率與時間）
- `httpx.AsyncClient` — 非同步 HTTP 請求（呼叫外部 API）
- list slicing `logs[i:i+300]` — 切片分批處理

#### 4.4 AI 快速分析（Claude Haiku）
說明對象：
- `client.messages.create(model=..., messages=[...])` — Anthropic SDK 呼叫 Claude
- system / user messages 結構 — prompt 的角色設定格式
- `json.loads(response.content[0].text)` — 解析 AI 回傳的 JSON 字串

#### 4.5 AI 日報彙整（Claude Sonnet）
說明對象：
- `db.add(obj)` — 新增資料庫記錄（INSERT）
- `db.merge(obj)` — 存在就更新、不存在就新增（UPSERT）
- `db.commit()` / `db.refresh(obj)` — 提交交易與重新讀取最新狀態

#### 4.6 前端查詢事件
說明對象：
- `@router.get("/path")` 搭配 `Query(...)` — 宣告查詢參數
- `class EventSchema(BaseModel)` — Pydantic Schema 定義 API 格式
- `response_model=EventSchema` — 自動序列化回應為指定格式
- `Optional[str] = None` — 可選參數型別標注

#### 6. 配置管理
說明對象：
- `class Settings(BaseSettings)` — Pydantic Settings 讀取環境變數
- `settings = Settings()` / `settings.DATABASE_URL` — 全域取用設定值
- `.env` 檔案讀取機制與 `Field(...)` 預設值設定

#### 7. 測試架構
說明對象：
- `@pytest.fixture` — 宣告 pytest 測試固件
- `conftest.py` — 共用固件的集中位置
- `TestClient(app)` — FastAPI 測試用 HTTP 客戶端
- `app.dependency_overrides[get_db] = override_get_db` — 替換依賴注入（換成測試 DB）
- `assert response.status_code == 200` — pytest 斷言

---

## 每個語法條目的固定格式

```
### `語法名稱`
**是什麼：** 一句話定義
**專案範例：** 引用 backend-guide.md 的程式碼片段
**白話解釋：** 口語說明（可用比喻）
**常見錯誤：** 初學者最容易踩的坑（1-2 條）
```

---

## 讀者假設

- 懂 Python 基礎：`def`、`class`、`async/await`、型別標注基礎
- 未接觸過：FastAPI、SQLAlchemy、Pydantic、Celery、Anthropic SDK、pytest fixture
- 閱讀目的：看懂 backend-guide.md，不是成為後端專家

---

## 不在範圍內

- 完整 FastAPI 教學
- SQL 語法說明
- Docker / 部署相關
- 前端語法（另見 frontend-syntax-guide.md）
- backend-guide.md 未出現的語法
- §3 目錄結構（純文字，無程式碼語法）
- §5 資料庫設計（表格與關係圖，無程式碼語法）
- §8 技術框架速查表（摘要性質，syntax-guide 本身即更詳細版本）
