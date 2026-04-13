# GitHub Repo 設計規範

> [← 回到總導覽](../README.md)

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
├── CLAUDE.md              ← AI agent 工作指引
└── docs/
    ├── repo-design.md     ← Repo 結構與格式規範（本文件）
    ├── AI-review-prompt.md ← AI 文件審查任務 Prompt
    ├── AI-review-gap-prompt.md ← AI 缺口與孤立文件掃描 Prompt
    ├── AI-review-doclist.md ← AI 文件審查範圍清單
    ├── workflow_guide.md  ← 設計理念、整體流程、關鍵機制
    ├── quick-start.md     ← 各角色第一天操作指南
    └── project-board-guide.md ← GitHub Projects 看板用法
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

> Issue Template 已設定（`.github/ISSUE_TEMPLATE/epic.yml`）。建立 Epic 時選擇 **Epic** template，`epic` label 自動套用，P-workflow 自動建立 SA Issue 並填入關聯 Issue；空白 Issue 已停用。

**P-workflow 自動化（Epic 開立觸發）：**

當 Epic Issue 被加上 `epic` label 時自動執行：
1. 在 P1-analysis 建立 SA Issue（含 Epic 編號、分支名稱）
2. 建立 A-branch：`issue-{saNum}-{epicTitle-slug}`，並 scaffold `business-logic.md` + `SD-WBS.md`
3. 在 P1-analysis 開立 SA Draft PR（body 預填關聯項目 + `Closes #N`）
4. 回填 Epic body 的關聯 Issue 區塊（SA Issue 編號）
5. 在 Epic Issue 留言通知

**Chore Issue（PM 行政事務）：**

P1-project 的 Chore Issue 用於追蹤與功能開發無關的 PM 日常事務，包含學習筆記、文件整理、環境維護等。選擇類型：學習 / 文件 / 環境維護 / 其他。

> 不觸發任何自動化流程，純手動追蹤。其他三個 Repo（P1-analysis / P1-design / P1-code）的 Chore Issue 會自動建立 `chore-{N}-{slug}` 分支，用於 repo 內部維護。

---

### P1-analysis（A-Repo）

```
P1-analysis/
├── README.md              ← Issue 索引（每次 merge 後手動更新一行）
├── issue-4/               ← 必須建立，以 Issue 編號命名
│   ├── business-logic.md  ← Designer需要知道的最小必要資訊。
│   └── SD-WBS.md          ← 列出 SD 需完成的工作項目清單（格式見下方）
├── issue-5/
│   └── ...
└── references/            ← 全域參考文件（架構圖、命名規則、API Schema 等）
```


**原則：**
- 每個 Issue 對應一個資料夾，資料夾本身就是這個 Issue 的完整 delta record
- business-logic.md（背景與目的、需求說明為必填，其餘選填）
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

> SA Issue 由 **P-workflow 自動建立**，不可手動建立。Issue body 由系統自動填入，包含 Epic 編號與 SA Issue 編號。

---

### P1-design（D-Repo）

```
P1-design/
├── README.md
├── TechStack.md           ← 技術棧選型文件
├── schema/
│   └── schema.md          ← 資料庫 Schema 全覽（User、Company...）
├── FunctionList.md        ← 系統功能清單
│
├── Prototype/             ← 畫面原型（HTML，活文件）
│
├── Spec/                  ← 轉寫規範設計中...請等待（活文件)
│   ├── xxx.md
│   └── ...
│
├── TDD/                   ← 技術設計文件（以 Issue 為單位）
│   ├── issue-5.md         ← SD 填寫（設計說明＋測試案例）
│   ├── issue-6.md
│   └── ...
│
├── SpecDiff/              ← 系統自動產生（修改項目 + 修改內容，勿手動編輯）
│   ├── issue-5.md
│   ├── issue-6.md
│   └── ...
│
```

**活文件 vs Delta Record：**

| 類型 | 位置 | 說明 |
|------|------|------|
| 活文件 | `Spec/`、`Prototype/`、`schema/schema.md` | 永遠反映最新狀態 |
| Delta Record（設計） | `TDD/issue-{N}.md` | SD 填寫：設計說明＋測試案例 |
| Delta Record（變更摘要） | `SpecDiff/issue-{N}.md` | 系統自動產生：修改項目 + 修改內容 |

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

**TDD/issue-N.md 格式（SD 人工填寫）：**

```markdown
# TDD：Issue #N 標題

## 測試案例
| ID | 類型 | 前置條件 | 操作 | 預期結果 |
|----|------|---------|------|---------|
| T1 | 整合 | 登入 Tenant A | POST /api/leaves | 201，回傳 leave_id |
| T2 | 單元 | 無 | calculate_leave_days(2025-01-06, 2025-01-10) | 5 |
```

**TDD 最低要求：**
- 每個 API 至少需要一個正常案例（預期 2xx）+ 一個錯誤案例（預期 4xx/5xx）
- 每個畫面至少需要一個主要操作流程的正常案例
- 測試案例數量不得少於 SD-WBS.md 工作項目數量

> 說明：「案例數 ≥ 工作項目數」是最低安全線，確保每個 WBS 項目都有對應的測試。若遵循「每個 API 正常 + 錯誤各一個案例」規則，案例數通常會自然超過 WBS 項目數，不需刻意湊數。

**SpecDiff/issue-{N}.md 格式（系統自動產生，勿手動編輯）：**

```markdown
# SpecDiff：Issue #N 標題

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
│   └── tests/             ← pytest 測試
├── API/                   ← 外部 API 參考文件（PDF，唯讀）
├── SYSTEM.md              ← 系統架構與資料流說明
├── docker-compose.yml     ← 本地開發環境
└── VersionDiff/           ← Merge 時自動產生
    ├── issue-7_Rex_20260326.md
    └── ...
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

格式由 `commitlint + husky` 強制執行，不符合格式的 commit 會被擋下。Type 說明見 [quick-start.md — Commit Message 格式速查](quick-start.md#commit-message-格式速查)。

### 檔案命名
- Spec 文件：`{畫面編號}{功能名稱}{類型}.md`，例：`03UserAPI.md`、`03UserPage.md`
  > 舊版 Spec 文件（無數字前綴，如 `UserAPI.md`）為歷史遺留，新建文件需使用數字前綴格式。
- Prototype：`{畫面編號}{子頁面}.html`，例：`03A.html`、`03B.html`
- TDD：`issue-{編號}.md`
- VersionDiff：`issue-{N}_{author}_{date}.md`
