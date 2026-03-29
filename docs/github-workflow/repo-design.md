# GitHub Repo 設計規範

## Repo 總覽

```
P1-project    產品管理（Epic、技術研究、規範文件）← PM 大本營
P1-analysis   需求分析（A-Repo）
P1-design     系統設計（D-Repo）
P1-code       系統開發（C-Repo）
```

---

## 各 Repo 目錄結構

### P1-project（PM 大本營）

```
P1-project/
├── README.md
├── issue-1/               ← Epic Issue，選擇性建立資料夾
│   └── 背景說明.md
├── issue-2/
│   └── ...
└── docs/
    └── github-workflow/   ← 本規範文件所在位置
```

**Epic Issue body 格式：**

```markdown
## 功能說明
<!-- 這個功能要解決什麼問題？ -->

## 驗收條件
<!-- 完成的定義是什麼？ -->

## 關聯 Issue
<!-- 由系統自動填入，勿手動編輯 -->
- SA Issue：P1-analysis #
- SD Issue：P1-design #
- PG Issue：P1-code #
```

> Issue Template 已設定（`.github/ISSUE_TEMPLATE/epic.md`）。開立 Epic 時選擇 **Epic** template；空白 Issue 已停用。

---

### P1-analysis（A-Repo）

```
P1-analysis/
├── README.md              ← Issue 索引（每次 merge 後手動更新一行）
├── issue-4/               ← 必須建立，以 Issue 編號命名
│   ├── business-logic.md     ← Use Case、Use Case Description、流程圖、Class Diagram、ER 示意
│   └── SD-WBS.md          ← 列出 SD 需完成的工作項目清單（格式見下方）
├── issue-5/
│   └── ...
```

**README.md 格式（Issue 索引）：**

```markdown
# P1-analysis Issue 索引

| Issue | 功能名稱 | 關鍵字 | Epic | 完成日期 |
|-------|---------|--------|------|---------|
| #4 | 請假申請 | 請假、leave、請假申請、leave_balance | P1-project #1 | 2026-03-01 |
| #5 | 使用者管理 | 用戶、user、帳號、權限 | P1-project #2 | 2026-03-15 |
```

SA 每次 merge 後手動在 README.md 新增一行。查閱歷史需求時，先搜尋 README.md 找到 Issue 編號，再進入對應資料夾。

> **注意：** README.md 更新是 merge 後的收尾動作，容易在忙碌時忘記。建議 SA 在 PR checklist 完成後立即更新，不要留到之後補。

**原則：**
- 每個 Issue 對應一個資料夾，資料夾本身就是這個 Issue 的完整 delta record
- business-logic.md 格式不限，以清楚說明商業邏輯為目標
- SD-WBS.md 需符合最低格式要求（見下方）

**SD-WBS.md 最低格式要求：**

每個工作項目需標明類型與說明，類型限定為：`Schema`、`API`、`畫面`、`其他`。

```markdown
# SD WBS：{功能名稱}

## 工作項目
| # | 類型 | 說明 |
|---|------|------|
| 1 | Schema | 新增 Leave Table |
| 2 | Schema | 修改 User Table，加入 leave_balance 欄位 |
| 3 | API | POST /api/leaves（建立請假申請） |
| 4 | API | GET /api/leaves（查詢請假清單） |
| 5 | 畫面 | 請假申請頁（含表單驗證） |

## 備註
<!-- 有無特殊限制、相依關係、需 SD 決策的設計點 -->
```

審查人員依本格式要求驗收，不符格式者退回。

**SA Issue body 格式（結構化，供 AI 讀取）：**

```markdown
## 功能說明

## 關聯項目
- Epic：P1-project #1
- SA Issue：P1-analysis #4（本 Issue）
- SD Issue：P1-design #（merge 後自動填入）
- 階段：SA
```

---

### P1-design（D-Repo）

```
P1-design/
├── README.md
├── TechStacks.md          ← 技術棧選型文件
├── Schema.md              ← 資料庫 Schema 全覽（User、Company...）
├── FunctionList.md        ← 系統功能清單
│
├── Prototype/             ← 畫面原型（HTML，活文件）
│   ├── 01A.html           ← 登入畫面
│   ├── 01B.html           ← 忘記密碼畫面
│   ├── 02A.html           ← 首頁畫面
│   ├── 03A.html           ← 使用者查詢畫面
│   ├── 03B.html           ← 使用者新增畫面
│   └── ...
│
├── Spec/                  ← 規格文件（活文件，永遠反映最新狀態）
│   ├── 01LoginAPI.md
│   ├── 01LoginPage.md     ← 前端規格（畫面邏輯、API 呼叫關係）
│   ├── 02HomeAPI.md
│   ├── 02HomePage.md
│   ├── 03UserAPI.md
│   ├── 03UserPage.md
│   ├── UserAPI.md
│   ├── CompanyAPI.md
│   └── ...
│
├── TestPlan/              ← 測試計劃（以 Issue 為單位的 delta record）
│   ├── issue-5.md         ← SD 人工填寫（測試案例）
│   ├── issue-5-diff.md    ← 系統自動產生（修改項目 + 關聯項目，勿手動編輯）
│   ├── issue-6.md
│   ├── issue-6-diff.md
│   └── ...
│
└── SD測試報告/
    └── issue-5.md
```

**活文件 vs Delta Record：**

| 類型 | 位置 | 說明 |
|------|------|------|
| 活文件 | `Spec/`、`Prototype/`、`Schema.md` | 永遠反映最新狀態 |
| Delta Record | `TestPlan/issue-N.md` | 記錄「這個 Issue 改了什麼」+ 測試案例 |

**SD Issue body 格式（結構化，供 AI 讀取）：**

```markdown
## 設計範圍
<!-- 由系統自動從 SA Issue 對應的 SD-WBS.md 複製工作項目清單，勿手動編輯 -->

## 關聯項目
- Epic：P1-project #1
- SA Issue：P1-analysis #4
- SD Issue：P1-design #5（本 Issue）
- PG Issue：P1-code #（merge 後自動填入）
- 階段：SD

## 若為拆分 Issue
- 父 Epic：P1-project #1
- 原始 SD Issue：P1-design #5
- 本拆分標記：[1b]
```

**TestPlan/issue-N.md 格式（SD 人工填寫）：**

```markdown
# TestPlan：Issue #N 標題

## 測試案例
| ID | 類型 | 前置條件 | 操作 | 預期結果 |
|----|------|---------|------|---------|
| T1 | 整合 | 登入 Tenant A | POST /api/leaves | 201，回傳 leave_id |
| T2 | 單元 | 無 | calculate_leave_days(2025-01-06, 2025-01-10) | 5 |
```

**TestPlan 最低要求：**
- 每個 API 至少需要一個正常案例（預期 2xx）+ 一個錯誤案例（預期 4xx/5xx）
- 每個畫面至少需要一個主要操作流程的正常案例
- 測試案例數量不得少於 SD-WBS.md 工作項目數量

> 說明：「案例數 ≥ 工作項目數」是最低安全線，確保每個 WBS 項目都有對應的測試。若遵循「每個 API 正常 + 錯誤各一個案例」規則，案例數通常會自然超過 WBS 項目數，不需刻意湊數。

**TestPlan/issue-N-diff.md 格式（系統自動產生，勿手動編輯）：**

```markdown
# TestPlan Diff：Issue #N 標題

## 修改項目及內容
- 02HomeAPI.md：新增 getHomeInfo() API
- 03B.html：加入備註欄位，姓名欄位由 3 碼改為 8 碼

## 關聯項目
- Epic：P1-project #1
- SA Issue：P1-analysis #4
- SD Issue：P1-design #5
- 上一個 commit：{前一個 commit hash}
- 本次 commit：{本次 commit hash}
```

---

### P1-code（C-Repo）

```
P1-code/
├── frontend/              ← React + TypeScript
├── backend/               ← Python + FastAPI
├── tests/
│   ├── unit/              ← 單元測試
│   └── integration/       ← 整合測試
│
├── VersionDiff/           ← Merge 時自動產生
│   ├── issue-7_Rex_20260326.md
│   └── ...
│
└── PG測試報告/
    └── issue-7.md
```

**PG Issue body 格式（結構化，供 AI 讀取）：**

```markdown
## 實作範圍
<!-- 由系統自動填入 SD 異動的 Spec/Prototype 清單 -->

## 關聯項目
- Epic：P1-project #1
- SA Issue：P1-analysis #4
- SD Issue：P1-design #5
- PG Issue：P1-code #7（本 Issue）
- 階段：PG
```

**VersionDiff/issue-N_author_date.md 格式：**

```markdown
# VersionDiff：Issue #N 標題

## 修改項目及內容
<!-- 由 GitHub Actions 自動產生 -->
- backend/routers/leaves.py：新增 POST /api/leaves endpoint
- backend/models/leave.py：新增 Leave model
- frontend/src/pages/LeavePage.tsx：新增請假申請頁面

## 關聯項目
- Epic：P1-project #1
- SA Issue：P1-analysis #4
- SD Issue：P1-design #5
- PG Issue：P1-code #7（本 Issue）
- 上一個 commit：{前一個 commit hash}
- 本次 commit：{本次 commit hash}
```

---

## 命名規則

### Branch 命名
```
issue-{編號}-{簡短說明}
```
範例：`issue-4-leave-request`、`issue-12-user-profile`

由 GitHub Actions 自動建立，**不手動建立分支**。

> **跨 Repo 辨識說明：** 四個 Repo 各有獨立的 Issue 編號系統，`issue-4-leave-request` 在 P1-analysis 和 P1-design 可能代表不同的 Issue。分支本身屬於各自的 Repo，不會跨 Repo 混淆；但在跨 Repo 溝通（如 PR 留言、Slack 討論）時，需加上 Repo 前綴明確指定，例如：`A-issue-4`（P1-analysis）、`D-issue-5`（P1-design）、`C-issue-7`（P1-code）。

### Commit Message 格式
```
{type}({scope}): {說明}
```

| Type | 用途 |
|------|------|
| `feat` | 新功能 |
| `fix` | 修復 bug |
| `docs` | 文件變更 |
| `refactor` | 重構 |
| `test` | 測試相關 |
| `chore` | 建置、設定 |

範例：
```
feat(leaves): 新增請假申請 API
docs(schema): 更新 Leave table 欄位說明
test(leaves): 新增 POST /api/leaves 整合測試
```

格式由 `commitlint + pre-commit` 強制執行，不符合格式的 commit 會被擋下。

### 檔案命名
- Spec 文件：`{畫面編號}{功能名稱}{類型}.md`，例：`03UserAPI.md`、`03UserPage.md`
- Prototype：`{畫面編號}{子頁面}.html`，例：`03A.html`、`03B.html`
- TestPlan：`issue-{編號}.md`
- VersionDiff：`issue-{N}_{author}_{date}.md`
