# 工作流程

## 開立工作時所填寫的表單 - GitHub Issue Template 設定

| 工作類型   | 動作            | Repo       | yml檔案                                                                                                                                                                                                                                                                                                             | 開立後觸發...                           |
| ------ | ------------- | ---------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------- |
| 系統功能修改 | 開立 Epic 表單    | P1-project | [epic.yml](https://github.com/MPinfo-Co/P1-project/blob/main/.github/ISSUE_TEMPLATE/epic.yml)                                                                                                                                                                                                                     | p-workflow.yml<br>**見「Epic自動化流程」** |
| 行政事務   | 行政 Chore 表單   | ALL        | [a-chore](https://github.com/MPinfo-Co/P1-analysis/blob/main/.github/workflows/a-chore-workflow.yml)  <br>[d-chore](https://github.com/MPinfo-Co/P1-design/blob/main/.github/workflows/d-chore-workflow.yml) <br>[c-chore](https://github.com/MPinfo-Co/P1-code/blob/main/.github/workflows/c-chore-workflow.yml) | chore-workflow.yml<br>**開立Branch** |
| 其他工作   | 開立Draft Issue | ALL        |                                                                                                                                                                                                                                                                                                                   |                                    |

> 統一透過專案看板[MP-BOX](https://github.com/orgs/MPinfo-Co/projects/4)開立工作
> 設定禁止開立空白 Issue(設定檔：[config.yml](https://github.com/MPinfo-Co/P1-project/blob/main/.github/ISSUE_TEMPLATE/config.yml))

##  Epic自動化流程

WF-P = [p-workflow.yml](https://github.com/MPinfo-Co/P1-project/blob/main/.github/workflows/p-workflow.yml) in P1-project
WF-A = [a-workflow.yml](https://github.com/MPinfo-Co/P1-analysis/blob/main/.github/workflows/a-workflow.yml) in P1-analysis
WF-D = [d-workflow.yml](https://github.com/MPinfo-Co/P1-design/blob/main/.github/workflows/d-workflow.yml) in P1-design
WF-C = [c-workflow.yml](https://github.com/MPinfo-Co/P1-code/blob/main/.github/workflows/c-workflow.yml) in P1-code

```
PM 開立 Epic（透過填寫範本）
└─ [WF-P 自動建立] SA Issue + SA-Branch + Draft PR
└─ [WF-P 自動產生] P1-analysis:issue-{SA#}/business-logic.md
  └─ SA merge PR
    └─ [WF-A 自動建立] SD Issue + SD-Branch + Draft PR
    └─ [WF-A 自動產生] P1-design:TDD/issue-{SD#}.md
      └─ SD merge PR
        └─ [WF-D 自動產生] P1-design:SpecDiff/issue-{SD#}.md
        └─ [WF-D 自動建立] PG Issue + PG-Branch + Draft PR
        └─ [WF-D 自動產生] P1-code:TestReport/issue-{SD#}.md
          └─ PG merge PR
            └─ [WF-C 自動產生] P1-code:VersionDiff/issue-{PG#}.md
            └─ [WF-C 自動關閉] Epic、PG Issue
```

> 產生各階段issue時，會自動在issue body產生與該issue相關的所有項目連結
> 如需了解 workflow 細節，直接向AI詢問指定文件內涵即可。


---

# 品質把關

## 程式審查機制(自動＋人工)

### Repo：P1-analysis / P1-design / P1-code
- **PR**：各階段審查人確認品質，需逐行確認細節
### Repo：P1-code
- **Local(commit時)**：pre-commit（ruff）+ husky lint-staged（ESLint、Prettier）+ commitlint
- **Github(push時)**：ruff lint/format、ESLint、Prettier check、pytest

---

## 文件自動審查機制

每天台灣時間 **凌晨 2:00** 自動執行，由 Claude Code Remote Agent 在雲端運作。

| 任務名稱              | 說明                                                     |
| ----------------- | ------------------------------------------------------ |
| Daily Docs Review | 讀取 `docs/ai-review/AI-review-prompt.md`，審查四個 Repo 文件狀況 |

管理介面：https://claude.ai/code/scheduled

---
