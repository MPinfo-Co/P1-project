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
├── issue-4/              
│   └── business-logic.md  ← 系統自動產生，SA 人工填寫（需求說明、商業邏輯…）
├── issue-5/
│   └── ...
└── references/            ← 全域參考文件（架構圖、命名規則、API Schema 等）
```

>文件 business-logic.md 格式，請參考[workflow_guide.md](workflow_guide.md)[自動產生的md文件格式]段

---

### P1-design（D-Repo）

```
P1-design/
├── README.md              ← 無內文，透過連結導引到「MP-Box 專案總導覽」
├── TechStack.md           ← 技術棧選型文件
├── FunctionList.md        ← 系統功能清單
├── schema/
│   └── schema.md          ← 資料庫 Schema 全覽（User、Company...，活文件）
├── Prototype/             ← 畫面原型（HTML，活文件）
├── Spec/                  ← API 規格文件（活文件）
│   ├── xxx.md
│   └── ...
├── TDD/                   ← 技術設計文件（以 Issue 為單位）
│   ├── issue-5.md         ← 系統自動產生，SD 人工填寫（工作項目＋測試案例）
│   ├── issue-6.md
│   └── ...
│
└── SpecDiff/              ← 系統自動產生，勿手動編輯（修改項目 + 修改內容）
    ├── issue-5.md
    ├── issue-6.md
    └── ...
 
```


>文件 TDD/issue-{N}.md 及 SpecDiff/issue-{N}.md 格式
>請參考[workflow_guide.md](workflow_guide.md)[自動產生的md文件格式]段

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

