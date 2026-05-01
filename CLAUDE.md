# 專案Repo 設計

專案由三個 Repo 組成，對應三個開發階段

| Repo            | 職責                                   | 角色 | Merge 方式          |
| --------------- | ------------------------------------ | -- | ----------------- |
| **P1-project**  | Epic、規範文件                            | PM | 直接 push to main   |
| **P1-design**   | SA 分析 + SD 設計（含 sdPrototype）         | SA / SD | PR + Review |
| **P1-code**     | React/TypeScript + Python/FastAPI 實作 | PG | PR + SA/PM Review |

> 「Repo 結構細節」，請參考：[repo-design.md](docs/repo-design.md)

---
# 專案限制

- Branch 由 GitHub Actions 自動建立，**不手動建立**。
- 所有文件產出使用繁體中文（zh-TW）
- Commit 格式：`{type}(scope?): 說明`，常用 type：`feat` / `fix` / `docs` / `refactor` / `test` / `chore`

---
# 執行Github Issue 工作時

## 工作所需檔案路徑

> 先知道路徑，再依據下述各流程讀取邏輯，按需加載

| 檔案/目錄名稱                 | 完整路徑                                                     |
| ----------------------- | -------------------------------------------------------- |
| `sa-{N}-logic.md`       | `P1-design/SA/saLogic/sa-{N}-logic.md`                   |
| `sd-{N}-TDD.md`         | `P1-design/SD/TDD/sd-{N}-TDD.md`                         |
| `sd-{N}-Diff.md`        | `P1-design/SD/sdDiff/sd-{N}-Diff.md`                     |
| `spec-guide.md`         | `P1-project/docs/spec-guide.md`                          |
| `sdSpec/`               | `P1-design/SD/sdSpec/`                                   |
| `schema.md`             | `P1-design/SD/schema.md`                                 |
| `sdPrototype/`          | `P1-design/SD/sdPrototype/`                              |
| `_{fn_xxx}_test_api.md` | `P1-design/SD/sdSpec/{fn_xxx}/Api/_{fn_xxx}_test_api.md` |
| `issue-{N}.md`          | `P1-code/TestReport/issue-{N}.md`                        |
| `techStack.md`          | `P1-project/docs/techStack.md`                           |

---
## 讀取 Issue body 上的資訊

1. 工作需要的資訊及實際位置都在 Issue body 之中
2. 以Issue body的資訊為主，不要發散，遇到問題詢問人類成員
3. 從 issue body 的「分支」欄位取得 branch 名稱，切換到該 branch 並執行 `git pull`。
4. Issue 標題中會標示[SA],[SD]或[PG]，執行對應流程：

> 「Issue body內文」，請參考：[issue-body-spec.md](docs/issue-body-spec.md)
> 「自動產生檔案的內文格式」，請參考：[auto-file-format.md](docs/auto-file-format.md)
---
## SA 流程

### 讀取邏輯
1. `sa-{N}-logic.md` 的 `需求說明`：預設值為 PM 填寫的需求描述

### 產出
1. `sa-{N}-logic.md` — 填寫 `畫面/操作邏輯示意`
2. `SA/saPrototype/fn_xxx/` — 若需求涉及畫面，新增或更新對應功能的雛形頁面（依 `docs/prototype-guide.md` SA 特則）

---

## SD 流程

### 讀取邏輯
1. `sa-{N}-logic.md`：商業邏輯背景（由 SA 填寫）
2. `sd-{N}-TDD.md`：（由 Github Action 填寫，SD 審查確認）
	1. 按需讀取 TDD 對應的 `sdSpec/*`、`schema.md`、`sdPrototype/*` 檔案
	2. 涉及修改既有 API 時，按需讀取對應的 `_{fn_xxx}_test_api.md`
3. `spec-guide.md`： Spec 撰寫規範

###  產出

1. `sd-{N}-TDD.md`： PG 實作依據
	+ 若文件已有內容（正常狀況由 Github Action 先填寫），跳過此步驟
	+ 若文件是空的，依下列規格填寫：
		1. 填寫「工作項目」表格，欄位：`| # | 類型 | 工作內容 | 參照規格 |`
		2.  類型限定：`Schema`、`API`、`畫面`、`Test`、`其他`
		3. 工作內容格式：建立 `{對象}` / 調整 `{對象}：{異動內容}` / 刪除 `{對象}`
		4. 設計決定只寫結論與理由，不寫曾考慮過的替代方案

2. 依 TDD「工作項目」內容調整：`sdPrototype/*`、`sdSpec/*`、`schema.md`（如有異動）
	+ **活文件原則：** `sdSpec/`、`sdPrototype/`、`schema.md` 永遠反映最新狀態，直接修改，不保留舊版。

3. 有 API 新增或修改時，同步更新對應的 `_{fn_xxx}_test_api.md`（活文件）
	+ 新增 API → 新增測試案例，ID 接續上一筆
	+ 修改 API 行為 → 更新對應測試案例
	+ 刪除 API → 移除對應測試案例，ID 不補號
	+ 若修改影響其他功能的 API（如跨功能改了權限機制），一併更新那些功能的 `_{fn_xxx}_test_api.md`
	

---

## PG 流程

### 讀取邏輯
1. `sa-{N}-logic.md`：商業邏輯背景（由 SA 填寫）
2. `sd-{N}-Diff.md`：本次 SD 對 Schema / Spec / Prototype 的變更摘要
3. `sd-{N}-TDD.md`：工作項目清單（由 GitHub Actions 生成，SD 審查確認）
	1. 按需讀取 TDD 對應的 `sdSpec/*`、`schema.md`、`sdPrototype/*` 檔案
	2. 涉及修改既有 API 時，按需讀取對應的 `_{fn_xxx}_test_api.md`
4. `techStack.md`：確認本次相關技術選型

### 產出
1. 依據TDD工作項目，實作 code
	1. TDD工作項目中，Schema 類型的異動要一併考慮 model與遷移程式
2. pytest實作
	- pytest 數量 ≥ `_test_api.md` 測試案例數
	- 每個 test function 標注對應 TestSpec ID：
```python
def test_create_user(client, db_session):
    """對應 T3"""
```

3. `issue-{N}.md` — 填寫測試結果與備註
4. 前端新檔案一律使用 `.tsx`（舊 `.jsx` 漸進式遷移，不強制）

---

> **維護說明：** 正式來源為 `MPinfo-Co/P1-project` 根目錄的 `CLAUDE.md`。
> 各開發者將此內容複製到本機 P1 工作目錄。內容有更動時，兩處同步更新。
> P1-design、P1-code 不再各自維護 CLAUDE.md。

---
# 涉及 Workflow 或 Prompt 的工作

凡工作內容涉及 GitHub Actions workflow（`.yml`）、AI Agent prompt（`prompts/*.md`）或兩者串接關係，**動手前先讀** [workflow_guide.md](docs/workflow_guide.md)，確認 yml → prompt 對應結構後再執行。
