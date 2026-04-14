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


```
P1-project/
├── README.md              ← MP-Box 專案總導覽
├── CLAUDE.md              ← AI agent 工作指引
└── docs/
    ├── repo-design.md     ← Repo 結構（本文件）
    ├── workflow_guide.md  ← 工作流程
    ├── project-board-guide.md ← GitHub Projects 看板用法
    └── ai-review/         ← AI 文件審查相關檔案
        ├── AI-review-prompt.md ← AI 文件審查任務 Prompt
        ├── AI-review-gap-prompt.md ← AI 缺口與孤立文件掃描 Prompt
        ├── AI-review-doclist.md ← AI 文件審查範圍清單
        ├── AI-review-report.md ← 文件審查報告（自動產出）
        └── AI-review-gap-report.md ← 缺口掃描報告（自動產出）
```



---

### P1-analysis（A-Repo）

```
P1-analysis/
├── README.md              ← 無內文，透過連結導引到「MP-Box 專案總導覽」
├── issue-4/               ← 必須建立，以 Issue 編號命名
│   └── business-logic.md  ← Designer需要知道的最小必要資訊。
├── issue-5/
│   └── ...
└── references/            ← 全域參考文件（架構圖、命名規則、API Schema 等）
```


**原則：**
- 每個 Issue 對應一個資料夾，資料夾本身就是這個 Issue 的完整 delta record
- business-logic.md（背景與目的、需求說明為必填，其餘選填）


---

### P1-design（D-Repo）

```
P1-design/
├── README.md              ← 無內文，透過連結導引到「MP-Box 專案總導覽」
├── TechStack.md           ← 技術棧選型文件
├── FunctionList.md        ← 系統功能清單
├── schema/
│   └── schema.md          ← 資料庫 Schema 全覽（User、Company...）
├── Prototype/             ← 畫面原型（HTML，活文件）
├── Spec/                  ← API 規格文件（活文件）
│   ├── xxx.md
│   └── ...
├── TDD/                   ← 技術設計文件（以 Issue 為單位）
│   ├── issue-5.md         ← SD 填寫（設計說明＋測試案例）
│   ├── issue-6.md
│   └── ...
│
└── SpecDiff/              ← 系統自動產生（修改項目 + 修改內容，勿手動編輯）
    ├── issue-5.md
    ├── issue-6.md
    └── ...
 
```



**TDD/issue-N.md 格式（SD 人工填寫）：**

```markdown
# TDD：Issue #N 標題

## 本次工作範圍
| # | 類型 | 說明 |
|---|------|------|
| 1 | API  | POST /api/leaves（建立請假申請） |

## 測試案例
| ID | 類型 | 前置條件 | 操作 | 預期結果 |
|----|------|---------|------|---------|
| T1 | 整合 | 登入 Tenant A | POST /api/leaves | 201，回傳 leave_id |
| T2 | 單元 | 無 | calculate_leave_days(2025-01-06, 2025-01-10) | 5 |
```


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
├── README.md              ← 無內文，透過連結導引到「MP-Box 專案總導覽」
├── SYSTEM.md              ← 系統架構與資料流說明
├── SETUP.md               ← 本地環境建置說明
├── frontend/              ← React + TypeScript
├── backend/               ← Python + FastAPI
│   └── tests/             ← pytest 測試
├── TestReport/            ← PG 填寫測試結果（以 SD Issue 編號命名）
│   ├── issue-5.md         ← 檔名用 SD Issue 編號（與 TDD、SpecDiff 一致）
│   └── ...
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

格式：`{type}(scope?): 說明`，常用 type：`feat` / `fix` / `docs` / `refactor` / `test` / `chore`。

### 檔案命名
- Spec 文件：`{畫面編號}{功能名稱}{類型}.md`，例：`03UserAPI.md`、`03UserPage.md`
  > 舊版 Spec 文件（無數字前綴，如 `UserAPI.md`）為歷史遺留，新建文件需使用數字前綴格式。
- Prototype：`{畫面編號}{子頁面}.html`，例：`03A.html`、`03B.html`
- TDD：`issue-{編號}.md`
