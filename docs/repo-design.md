# GitHub Repo 設計規範

> [← 回到總導覽](../README.md)

## Repo 總覽

| Repo            | 職責                                   | 角色 | Merge 方式          |
| --------------- | ------------------------------------ | -- | ----------------- |
| **P1-project**  | Epic、規範文件                            | PM | 直接 push to main   |
| **P1-design**   | SA 分析 + SD 設計（含 sdPrototype / sdSpec）| SA / SD | PR + Review |
| **P1-code**     | React/TypeScript + Python/FastAPI 實作 | PG | PR + SA/PM Review |

---

## 各 Repo 目錄結構


```
P1-project/
├── README.md              ← MP-Box 專案總導覽
├── CLAUDE.md              ← AI agent 工作指引
└── docs/
    ├── repo-design.md     ← Repo 結構（本文件）
    ├── workflow_guide.md  ← 工作流程
    ├── issue-body-spec.md ← Issue body 內文格式規範
    ├── auto-file-format.md ← 系統自動產生檔案格式說明
    ├── spec-guide.md      ← Spec 目錄結構、命名規則、各檔案格式與撰寫規範
    ├── techStack.md       ← 技術棧選型文件
    └── ai-review/         ← AI 文件審查相關檔案
        ├── AI-review-prompt.md ← AI 文件審查任務 Prompt
        ├── AI-review-doclist.md ← AI 文件審查範圍清單
        └── AI-review-report.md ← 文件審查報告（自動產出）
```



---

### P1-design

```
P1-design/
├── README.md              ← 無內文，透過連結導引到「MP-Box 專案總導覽」
├── SA/                         ← SA 分析產出
│   ├── saLogic/
│   │   └── sa-{N}-logic.md     ← 原 business-logic.md
│   └── saPrototype/            ← SA 主責的畫面雛形（所有功能共用一份）
└── SD/                         ← SD 設計產出
    ├── functionList.md    ← 系統功能清單
    ├── schema.md          ← 資料庫 Schema 全覽（User、Company...，活文件）
    ├── TDD/
    │   └── sd-{N}-TDD.md       ← 原 TDD/issue-{N}.md
    ├── sdDiff/
    │   └── sd-{N}-Diff.md      ← 原 SpecDiff/issue-{N}.md
    ├── sdPrototype/            ← SD 設計稿（SD 主責）
    └── sdSpec/                 ← 原 Spec/（API 規格文件，活文件）
        └── {fn_xxx}/
            ├── {fn_xxx}_00_overview.md
            ├── {fn_xxx}_01_xxx.md
            └── Api/
                ├── _{fn_xxx}_test_api.md
                └── {fn_xxx}_xxx_api.md
```


>文件 SA/saLogic/sa-{N}-logic.md、SD/TDD/sd-{N}-TDD.md 及 SD/sdDiff/sd-{N}-Diff.md 格式，請參考 [auto-file-format.md](auto-file-format.md)

---

### P1-code

```
P1-code/
├── README.md              ← 無內文，透過連結導引到「MP-Box 專案總導覽」
├── docker-compose.yml     ← 本地開發容器設定
├── frontend/              ← React + TypeScript
├── backend/               ← Python + FastAPI
│   └── tests/             ← pytest 測試
├── TestReport/            ← PG 填寫測試結果（以 SD Issue 編號命名）
│   ├── issue-5.md         ← 檔名用 SD Issue 編號（與 TDD、SpecDiff 一致）
│   └── ...
```

