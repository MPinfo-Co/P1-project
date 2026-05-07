# PG 命名規範統一設計

> 日期：2026-05-07
> 目標：建立後端檔案、API endpoint、前端路由的一致命名規則，並修正「schema」跨文件的術語歧義

---

## 背景

目前系統在三個層面存在命名不一致或術語混淆問題：

1. **後端檔案命名**：Router / Pydantic Schema / SQLAlchemy Model 的 `fn_` 前綴使用不統一（有些有、有些無）
2. **API Endpoint**：有 `/api/skill`（單數）也有 `/api/roles`（複數），無一致規則
3. **術語歧義**："schema" 在 TDD 文件中指 DB table 異動，在程式碼中卻指 Pydantic 類別，導致 agent 理解混淆
4. **前端路由**：路由路徑由 SD 自由命名（如 `/settings/account`），與功能模組名稱無對應關係

本設計目的是讓 GitHub Actions workflow 和 local AI agent 都能依循一致規範，減少歧義帶來的實作錯誤。

---

## 設計決定

### Rule 1：後端檔案統一使用 `fn_` 前綴

資料夾即類型，檔名以 `fn_{domain}` 命名：

| 類型 | 位置 | 格式 | 範例 |
|------|------|------|------|
| Router | `app/api/` | `fn_{domain}.py` | `fn_skill.py`, `fn_user.py`, `fn_role.py` |
| Pydantic Schema | `app/api/schema/` | `fn_{domain}.py` | `fn_skill.py`, `fn_user.py` |
| SQLAlchemy Model | `app/db/models/` | `fn_{domain}.py` | `fn_skill.py`, `fn_user.py` |
| 測試 | `tests/` | `test_fn_{domain}_{動作}.py` | `test_fn_user_create.py` |

**例外**：`auth`、`health` 等基礎設施層不加 `fn_` 前綴，因其不屬於業務功能模組。

### Rule 2：API Endpoint 統一單數，對齊 fn_ 模組名

格式：`/api/{domain}`，domain 為 fn_ 模組名去除 `fn_` 前綴，一律單數。

```
fn_skill  → /api/skill
fn_user   → /api/user
fn_role   → /api/role
```

刪除原本「是否複數視語意而定」的規定，改為強制單數。`auth`、`health` 等基礎設施 endpoint 照舊不受此規則限制。

### Rule 3：術語統一——"Schema" 改為 "Model"，schema.md 改名為 model.md

**問題根源**：TDD 工作項目的「Schema 類型」指 DB table 異動（對應 SQLAlchemy model），但 FastAPI / Python 生態系的慣例中「schema」指 Pydantic 驗證類別。兩者用詞相同造成 agent 混淆。

**解決方案**：
- TDD 工作項目類型欄：`Schema` → `Model`
- `P1-design/SD/schema.md` 實際改名為 `model.md`
- `coding-rule-backend.md` 新增說明段落，明確區分：
  - **Model 層**（`app/db/models/`）= SQLAlchemy ORM，對應 DB table
  - **Schema 層**（`app/api/schema/`）= Pydantic，負責 API 輸入/輸出驗證

### Rule 4：前端路由命名對齊 fn_ 模組名，不加 fn_ 前綴

格式：`/{domain}`，domain 為 fn_ 模組名去除 `fn_` 前綴。

```
fn_user  → /user
fn_skill → /skill
fn_role  → /role
```

**不加 fn_ 前綴的原因**：路由是使用者在瀏覽器看到的 URL，技術性前綴不應出現在使用者介面。  
Dialog 型畫面（無獨立 URL）不受此規則影響，路由路徑欄留空。

---

## 影響文件清單（共 14 份，17 處改動）

> `coding-rule-backend.md` 跨 Rule 1、2、3 皆有改動；`pg-backend-writer-prompt.md` 跨 Rule 1、3 皆有改動。實作時需在同一份文件中一次套用所有對應 Rule 的修改。

### Rule 1（後端 fn_ 前綴）

| 文件 | 改動內容 |
|------|---------|
| `P1-project/docs/coding-rule-backend.md` | §1-1 命名速查表：Router / Schema / Model / Test 檔名全面加 `fn_` 前綴 |
| `P1-design/prompts/pg-backend-writer-prompt.md` | Step 3 各類型工作項目命名指引更新 |

### Rule 2（API Endpoint 單數）

| 文件 | 改動內容 |
|------|---------|
| `P1-project/docs/coding-rule-backend.md` | §1-4 Router prefix：刪除「視語意而定」，改為「統一單數，對齊 fn_ 模組名去前綴」 |

### Rule 3（Schema → Model 術語）

| 文件 | 改動內容 |
|------|---------|
| `P1-design/SD/schema.md` | **實際改名為 model.md** |
| `P1-project/docs/repo-design.md` | 目錄結構圖 `schema.md` → `model.md` |
| `P1-project/docs/workflow_guide.md` | 流程說明 `schema` → `model` |
| `P1-project/CLAUDE.md` | 檔案路徑對照表 `schema.md` → `model.md` |
| `P1-project/docs/auto-file-format.md` | TDD 類型限定：`Schema` → `Model` |
| `P1-design/prompts/sd-writer-prompt.md` | 讀取路徑、類型名稱、輸出限制：schema.md → model.md；Schema → Model |
| `P1-design/prompts/sd-reviewer-prompt.md` | 檢核 1 允許類型、檢核 9 參照：Schema → Model；schema.md → model.md |
| `P1-design/prompts/pg-backend-writer-prompt.md` | 讀取路徑、類型名稱：schema.md → model.md；Schema → Model |
| `P1-design/prompts/pg-backend-verifier-prompt.md` | 讀取路徑、類型名稱：schema.md → model.md；Schema → Model |
| `P1-project/docs/coding-rule-backend.md` | 新增 Model（SQLAlchemy）vs Schema（Pydantic）區分說明段落 |

### Rule 4（前端路由命名）

| 文件 | 改動內容 |
|------|---------|
| `P1-project/docs/spec-guide.md` | 路由路徑格式範例：`/settings/account` → `/{domain}` 格式 |
| `P1-project/docs/coding-rule-frontend.md` | 新增路由命名規則段落 |
| `P1-design/prompts/pg-frontend-writer-prompt.md` | Step 2.8 路由命名規則更新 |
| `P1-design/prompts/pg-frontend-verifier-prompt.md` | 新增路由路徑格式驗證規則 |

---

## 確認程序

實作完成後，執行以下確認步驟確保品質：

### Step 1：殘留術語掃描（grep）

```bash
# 確認所有 prompt / rule 文件中不再有舊術語
grep -rn "schema\.md" P1-project/docs/ P1-design/prompts/
grep -rn "類型限定.*Schema" P1-project/docs/ P1-design/prompts/
grep -rn "類型：Schema\b" P1-project/docs/ P1-design/prompts/
grep -rn "Schema 類型" P1-project/docs/ P1-design/prompts/

# 確認路由範例不再有 fn_ 前綴
grep -rn "路由路徑.*fn_" P1-project/docs/ P1-design/prompts/

# 確認 model.md 已存在、schema.md 已不存在
ls P1-design/SD/model.md
ls P1-design/SD/schema.md  # 應回傳 No such file
```

### Step 2：一致性交叉比對

對照本文件的「影響文件清單」，逐一確認 14 份文件皆已完成改動：
- 每份文件的改動內容與設計一致
- 沒有遺漏的文件

### Step 3：關鍵詞正確性驗證

| 驗證項目 | 預期結果 |
|---------|---------|
| `auto-file-format.md` 中的 TDD 類型限定列表 | 包含 `Model`，不含 `Schema` |
| `sd-reviewer-prompt.md` 檢核 1 的允許類型 | 包含 `Model`，不含 `Schema` |
| `coding-rule-backend.md` §1-1 的 Router 範例 | 含 `fn_skill.py`, `fn_user.py` |
| `coding-rule-backend.md` §1-4 | 含「統一單數」字樣 |
| `coding-rule-frontend.md` | 含路由命名規則段落，含 `/{domain}` 格式說明 |
| `spec-guide.md` 路由格式範例 | 路由格式更新，不再顯示 `/settings/account` 為標準格式 |

---

## 範圍說明

**不在本次異動範圍內**：
- 現有 sdSpec 畫面規格中的路由路徑（如 fn_user 的 `/settings/account`）— 這些是活文件，下次 SD 改版時依新規則自然對齊
- 現有 P1-code 中已命名的 Router / Model 檔案 — 漸進式遷移，不在本次規範改版範圍
