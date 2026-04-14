
# 自動化流程核心目標

## 人類協作層面

- **可追蹤**：每一行程式碼都能追溯到設計規格，每一份規格都能追溯到需求分析
- **可驗證**：每個階段都有明確的品質把關，不符合標準的工作無法進入下一階段
- **自動化**：重複性的文書工作（建立分支、記錄變更、通知下游）由系統自動完成

## AI 協作層面

- AI 接到 Issue 後，能沿著 Issue 關聯(PM>SA>SD>PG)自主讀取商業邏輯、設計規格、歷史異動，不需要人工交接，直接產出可交付的程式碼

---

# 流程總覽

## 人工流程

| 負責人 | 階段   | Repo        | 產出                   |
| --- | ---- | ----------- | -------------------- |
| PM  | 工作分派 | P1-project  | SA Issue + SA-Branch |
| SA  | 系統分析 | P1-analysis | business-logic.md    |
| SD  | 系統設計 | P1-design   | Spec、Prototype、TDD   |
| PG  | 系統開發 | P1-code     | 程式碼、測試、VersionDiff   |

## 自動化流程

```
WF-P = p-workflow.yml in P1-project
WF-A = a-workflow.yml in P1-analysis
WF-D = d-workflow.yml in P1-design
WF-C = c-workflow.yml in P1-code

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

> 產生issue時，會自動在issue body產生與該issue相關的所有項目連結

## GitHub Actions 自動化設定檔(yml 檔)

| Workflow       | yml 檔                                                                                                                                                                                                                                                                                                        | 觸發                     | 優先級 |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------- | --- |
| p-workflow     | [p-workflow.yml](../.github/workflows/p-workflow.yml)                                                                                                                                                                                                                                                    | Epic issue開立           | P0  |
| a-workflow     | [a-workflow.yml](https://github.com/MPinfo-Co/P1-analysis/blob/main/.github/workflows/a-workflow.yml)                                                                                                                                                                                                        | A-Branch merge         | P0  |
| d-workflow     | [d-workflow.yml](https://github.com/MPinfo-Co/P1-design/blob/main/.github/workflows/d-workflow.yml)                                                                                                                                                                                                          | D-Branch merge         | P0  |
| c-workflow     | [c-workflow.yml](https://github.com/MPinfo-Co/P1-code/blob/main/.github/workflows/c-workflow.yml)                                                                                                                                                                                                            | Push / PR / merge      | P0  |
| chore-workflow | [a-chore](https://github.com/MPinfo-Co/P1-analysis/blob/main/.github/workflows/a-chore-workflow.yml) / [d-chore](https://github.com/MPinfo-Co/P1-design/blob/main/.github/workflows/d-chore-workflow.yml) / [c-chore](https://github.com/MPinfo-Co/P1-code/blob/main/.github/workflows/c-chore-workflow.yml) | Issue 加上 `chore` label | P1  |

> 如需了解 workflow 細節，直接向AI詢問指定文件內涵即可。

---

# 品質把關

## 程式審查機制(自動＋人工)

- **本地(commit時)**：pre-commit（ruff）+ husky lint-staged（ESLint、Prettier）+ commitlint
- **CI(push時)**：ruff lint/format、ESLint、Prettier check、pytest（P1-code）
- **PR**：各階段審查人確認品質，需逐行確認細節

---

## 文件自動審查機制

每天台灣時間 **凌晨 2:00** 自動執行，由 Claude Code Remote Agent 在雲端運作。

| 任務名稱              | 說明                                                     |
| ----------------- | ------------------------------------------------------ |
| Daily Docs Review | 讀取 `docs/ai-review/AI-review-prompt.md`，審查四個 Repo 文件狀況 |

管理介面：https://claude.ai/code/scheduled

---
