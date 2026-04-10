# CLAUDE.md

> **維護說明：** 正式來源為 `MPinfo-Co/P1-project` 根目錄的 `CLAUDE.md`。
> 各開發者將此內容複製到本機 P1 工作目錄。內容有更動時，兩處同步更新。
> P1-analysis、P1-design、P1-code 不再各自維護 CLAUDE.md。

## 專案簡介

MP-BOX 是一套面向企業用戶的 AI 應用平台，協助企業解決各類作業難題。
核心功能包含：資安日誌解讀與風險處置、專家知識管理、企業技能管理（如 ERP 操作自動化）、
以及企業營運狀況解讀（財務、營運、工作執行）。

## 專案架構

P1 由四個 Repo 組成，對應四個開發階段：

| Repo | 職責 | 角色 |
|------|------|------|
| **P1-project** | Epic、規範文件 | PM |
| **P1-analysis** | 商業邏輯分析、SD-WBS | SA |
| **P1-design** | Prototype、API Spec、Schema、TestPlan | SD |
| **P1-code** | React/TypeScript + Python/FastAPI 實作 | PG／AI |

開發流程：Epic → SA Issue → SD Issue → PG Issue
每個階段由上游 merge 後 GitHub Actions 自動建立下游 Issue 與 Branch。

---

## 起手式

任何涉及 SA / SD / PG issue 的任務，開始實作前：

1. 呼叫 `get_issue` 取得該 issue 的完整 body
2. 找到 `### 關聯檔案`，逐一讀取每個連結文件
3. 如需更多背景，從 `### 關聯 Issue` 取得上游編號，重複步驟 1–2

---

## SA 指引

### 關聯檔案語義

| 檔案 | 說明 |
|------|------|
| `business-logic.md` | 商業邏輯分析文件。第一個 section 已由系統從 Epic 複製問題描述，在此基礎上填寫 |
| `SD-WBS.md` | SD 工作清單，決定下游設計範圍 |

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

### 關聯檔案語義

| 檔案 | 說明 |
|------|------|
| `business-logic.md` | SA 完成的商業邏輯。Issue body「功能說明」已內嵌完整內容，不需另外開啟 |
| `SD-WBS.md` | 本次設計範圍清單。Issue body「設計範圍」已內嵌，對照執行 |
| `TestPlan/issue-{N}.md` | 測試案例定義（SD 填寫）。merge 後由系統派生為 P1-code 的 TestReport |

### 產出標準

依「設計範圍」完成：`Prototype/`、`Spec/`、`schema/`（如有異動）、`TestPlan/issue-{N}.md`

**活文件原則：** `Spec/`、`Prototype/`、`schema/` 永遠反映最新狀態，直接修改，不保留舊版。
`TestPlan/issue-{N}.md` 是 delta record，以 Issue 為單位保存。

**TestPlan 最低要求：**
- 每個 API：至少 1 個成功案例（2xx）+ 1 個失敗案例（4xx/5xx）
- 每個畫面：至少 1 個主要操作流程的正常案例
- 測試案例總數 ≥ SD-WBS.md 工作項目數

---

## PG 指引

### 關聯檔案語義

| 檔案 | 說明 |
|------|------|
| `business-logic.md` | 商業邏輯背景，了解功能目的 |
| `SpecDiff` | 本次 SD PR 異動的 Spec/Prototype/Schema diff，確認本次實作範圍 |
| `TestPlan` | 測試標準，pytest 數量須 ≥ 案例數 |
| `TestReport` | 填寫「結果」「備註」兩欄，對應 TestPlan 案例 ID |

### 產出標準

- pytest 數量 ≥ TestPlan 案例數
- 每個 test function 標注對應 TestPlan ID：

```python
def test_create_user(client, db_session):
    """對應 TestPlan T1"""
```

- 前端新檔案一律使用 `.tsx`（舊 `.jsx` 漸進式遷移，不強制）

---

## Branch 與 Commit 規範

- Branch：`issue-{N}-{slug}`，由 GitHub Actions 自動建立，**不手動建立**
- Commit：`{type}({scope}): 說明`，由 commitlint 強制執行
  - 常用 type：`feat` / `fix` / `docs` / `refactor` / `test` / `chore`

每次 commit 自動執行：
- **Python**：`ruff check` + `ruff format`
- **前端**：ESLint + Prettier（僅對暫存檔案）

---

## 技術棧

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

## 語言

所有文件與 Issue template 使用繁體中文（zh-TW）。
