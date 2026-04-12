# CLAUDE.md

> **維護說明：** 正式來源為 `MPinfo-Co/P1-project` 根目錄的 `CLAUDE.md`。
> 各開發者將此內容複製到本機 P1 工作目錄。內容有更動時，兩處同步更新。
> P1-analysis、P1-design、P1-code 不再各自維護 CLAUDE.md。

## 專案架構

P1 由四個 Repo 組成，對應四個開發階段：

| Repo            | 職責                                   | 角色 | Merge 方式               |
| --------------- | ------------------------------------ | ---- | ----------------------- |
| **P1-project**  | Epic、規範文件                            | PM   | 直接 push to main         |
| **P1-analysis** | 商業邏輯分析、SD-WBS                        | SA   | 直接 merge（無需 PR）         |
| **P1-design**   | Prototype、API Spec、Schema、TDD        | SD   | PR + SA/PM Review       |
| **P1-code**     | React/TypeScript + Python/FastAPI 實作 | PG   | PR + SA/PM Review       |

---

## 起手式

當人類成員說「我們來處理 PG Issue #99」這類的指示時，
涉及 SA / SD / PG issue 的任務，開始實作前：

1. 先讀取對應的 issue body，需要的資訊及相關連結都在 body 之中，請以其中的資訊為主，不要發散，遇到問題詢問人類成員
2. 從 issue body 的「分支」欄位取得 branch 名稱，切換到該 branch 並執行 `git pull`（P1-project 例外，PM 可直接在 main 上操作）
3. 各階段請依照下列的工作流程進行工作

**SA 階段**
1. 讀取上層 Epic Issue body 中的需求描述（由 PM 填寫）
2. 撰寫 `business-logic.md` + `SD-WBS.md` 供 SD 參照

**SD 階段**
1. 讀取 `business-logic.md` — 商業邏輯背景（由 SA 填寫）
2. 讀取 `SD-WBS.md` — SD 工作範圍（由 SA 填寫）
3. 撰寫 `TDD/issue-{N}.md` — 填寫技術設計說明與測試案例供 PG 參照

**PG 階段**
1. 讀取 `business-logic.md` — 商業邏輯背景（由 SA 填寫）
2. 讀取 `SpecDiff/issue-{N}.md` — SD 活文件差異（由 workflow 及 AI 撰寫）
3. 讀取 `TDD/issue-{N}.md` — 技術設計說明與測試標準（由 SD 填寫）
4. 撰寫 code + `TestReport/issue-{N}.md` — 填寫測試結果與備註

---

## SA 指引

### 產出標準

**business-logic.md** 需涵蓋：Use Case、流程圖、Class Diagram、ER 示意

**SD-WBS.md** 格式要求：

```markdown
## 工作項目
| # | 類型 | 說明 |
|---|------|------|
```

- 類型限定：`Schema`、`API`、`畫面`、`其他`
- 工作項目須完整涵蓋本次功能所需的所有 Schema / API / 畫面變更

---

## SD 指引

> **TDD（Technical Design Document）**：SD 階段產出的技術設計文件，包含設計說明與測試案例，作為 PG 實作依據。

### 產出標準

依「設計範圍」完成：`Prototype/`、`Spec/`、`schema/`（如有異動）、`TDD/issue-{N}.md`

**活文件原則：** `Spec/`、`Prototype/`、`schema/` 永遠反映最新狀態，直接修改，不保留舊版。
`TDD/issue-{N}.md` 是 delta record，以 Issue 為單位保存。

**TDD 最低要求：**
- 每個 API：至少 1 個成功案例（2xx）+ 1 個失敗案例（4xx/5xx）
- 每個畫面：至少 1 個主要操作流程的正常案例
- 測試案例總數 ≥ SD-WBS.md 工作項目數

---

## PG 指引

### 產出標準

- pytest 數量 ≥ TDD 案例數
- 每個 test function 標注對應 TDD ID：

```python
def test_create_user(client, db_session):
    """對應 TDD T1"""
```

- 前端新檔案一律使用 `.tsx`（舊 `.jsx` 漸進式遷移，不強制）

### 技術棧

| 層級 | 選型 |
|------|------|
| **前端** | React 19 + Vite + React Router v7（TypeScript，舊 .jsx 漸進遷移）|
| **樣式** | Tailwind CSS v3 + MUI |
| **State** | Zustand（Client）+ TanStack Query（Server）|
| **HTTP** | Axios |
| **後端** | Python 3.12 + FastAPI + Pydantic |
| **ORM** | SQLAlchemy + Alembic（Migration）|
| **資料庫** | PostgreSQL |
| **認證** | 自建 JWT（bcrypt 密碼 hash）|
| **檔案儲存** | Cloudflare R2（S3 相容 API）|
| **Email** | Resend |
| **測試** | pytest |
| **Linter** | Ruff（Python）/ ESLint + Prettier（前端）|
| **部署** | Docker + Railway（後端）+ Vercel（前端）|

完整技術選型說明見 [TechStack.md](https://github.com/MPinfo-Co/P1-design/blob/main/TechStack.md)。

---

## Branch 與 Commit 規範

- Branch：`issue-{N}-{slug}`，由 GitHub Actions 自動建立，**不手動建立**
- Commit：`{type}({scope}): 說明`，由 commitlint 強制執行
  - 常用 type：`feat` / `fix` / `docs` / `refactor` / `test` / `chore`

每次 commit 自動執行：
- **Python**：`ruff check` + `ruff format`
- **前端**：ESLint + Prettier（僅對暫存檔案）

## 語言

所有文件與 Issue template 使用繁體中文（zh-TW）。
