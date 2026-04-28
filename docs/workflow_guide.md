# 一.工作流程

## 開立工作時所填寫的表單 - GitHub Issue Template 設定

| 工作類型   | 動作            | Repo       | yml檔案                                                                                                                                                                                                                                                                                                             | 開立後觸發...                           |
| ------ | ------------- | ---------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------- |
| 系統功能修改 | 開立 Epic 表單    | P1-project | [epic.yml](https://github.com/MPinfo-Co/P1-project/blob/main/.github/ISSUE_TEMPLATE/epic.yml)                                                                                                                                                                                                                     | wf_epic_to_sa.yml<br>**見「Epic自動化流程」** |
| 行政事務   | 行政 Chore 表單   | ALL        | [d-chore](https://github.com/MPinfo-Co/P1-design/blob/main/.github/workflows/wf_chore_branch.yml) <br>[c-chore](https://github.com/MPinfo-Co/P1-code/blob/main/.github/workflows/wf_chore_branch.yml) | wf_chore_branch.yml<br>**開立Branch** |
| 其他工作   | 開立Draft Issue | ALL        |                                                                                                                                                                                                                                                                                                                   |                                    |

> 統一透過專案看板[MP-BOX](https://github.com/orgs/MPinfo-Co/projects/4)開立工作
> 設定禁止開立空白 Issue(設定檔：[config.yml](https://github.com/MPinfo-Co/P1-project/blob/main/.github/ISSUE_TEMPLATE/config.yml))

##  1.1 Epic自動化流程

```
PM 開立 Epic（透過填寫範本）-> 觸發 [wf_epic_to_sa]
└─ 建立 SA Issue + SA-Branch + Draft PR
└─ 產生 P1-design:SA/sa-{SA#}-logic.md
  └─ SA merge PR -> 觸發 [wf_sa_to_sd]
    └─ 建立 SD Issue + SD-Branch + Draft PR
    └─ 產生 P1-design:SD/sd-{SD#}-TDD.md
      └─ SD merge PR -> 觸發 [wf_sd_to_pg]
        └─ 產生 P1-design:SD/sd-{SD#}-Diff.md
        └─ 建立 PG Issue + PG-Branch + Draft PR
        └─ 產生 P1-code:TestReport/issue-{SD#}.md
          └─ PG merge PR -> 觸發 [wf_pg_close]
            └─ 關閉 Epic、PG Issue
```

## 1.2 workflows

| # | Repo | 檔名 | 觸發時點 | 執行內容 |
|---|------|------|---------|---------|
| 1 | P1-project | [wf_epic_to_sa.yml](https://github.com/MPinfo-Co/P1-project/blob/main/.github/workflows/wf_epic_to_sa.yml) | Issue 加上 `epic` label | 建立 SA Issue + SA Branch + Draft PR → SA agent 產出 logic.md |
| 2 | P1-design | [wf_sa_to_sd.yml](https://github.com/MPinfo-Co/P1-design/blob/main/.github/workflows/wf_sa_to_sd.yml) | SA PR merged to main | 建立 SD Issue + SD Branch + Draft PR → SD agent 產出 TDD.md |
| 3 | P1-design | [wf_sd_to_pg.yml](https://github.com/MPinfo-Co/P1-design/blob/main/.github/workflows/wf_sd_to_pg.yml) | SD PR merged to main | 產生 Diff.md + 建立 PG Issue + PG Branch + Draft PR → PG agent 產出 code + TestReport |
| 4 | P1-code | [wf_pg_ci.yml](https://github.com/MPinfo-Co/P1-code/blob/main/.github/workflows/wf_pg_ci.yml) | push 到 `pg-*` branch | Backend CI（Ruff + Pytest）+ Frontend CI（ESLint + Prettier） |
| 5 | P1-code | [wf_pg_close.yml](https://github.com/MPinfo-Co/P1-code/blob/main/.github/workflows/wf_pg_close.yml) | PG PR merged to main | 關閉 PG Issue + Epic Issue |
| — | P1-design | [wf_chore_branch.yml](https://github.com/MPinfo-Co/P1-design/blob/main/.github/workflows/wf_chore_branch.yml) | Issue 加上 `chore` label | 建立 chore branch |
| — | P1-code | [wf_chore_branch.yml](https://github.com/MPinfo-Co/P1-code/blob/main/.github/workflows/wf_chore_branch.yml) | Issue 加上 `chore` label | 建立 chore branch |
| — | P1-project | [archive-done-items.yml](https://github.com/MPinfo-Co/P1-project/blob/main/.github/workflows/archive-done-items.yml) | 每週一 03:00 UTC + 手動 | 封存看板上 2 週以上的 Done 項目 |
| — | P1-project | [stale-cleanup.yml](https://github.com/MPinfo-Co/P1-project/blob/main/.github/workflows/stale-cleanup.yml) | 每週一 02:00 UTC + 手動 | 標記並關閉過期 issue（跨三 repo） |

> 如需了解 workflow 細節，直接向AI詢問指定文件內涵即可。

## 1.3 Issue body 格式

- 產生各階段issue時，會自動在issue body產生與該issue相關的所有項目連結
- 各階段 Issue body 格式詳見：[issue-body-spec.md](issue-body-spec.md)

## 1.4 自動產生的 md 文件格式

各階段自動產生文件格式詳見：[auto-file-format.md](auto-file-format.md)



---

# 二.品質把關

## 2.1 程式審查機制(自動＋人工)

### Repo：P1-design / P1-code
- **PR**：各階段審查人確認品質，需逐行確認細節
### Repo：P1-code
- **Local(commit時)**：pre-commit（ruff）+ husky lint-staged（ESLint、Prettier）+ commitlint
- **Github(push時)**：ruff lint/format、ESLint、Prettier check、pytest

---

## 2.2 文件自動審查機制

每天台灣時間 **凌晨 2:00** 自動執行，由 Claude Code Remote Agent 在雲端運作。

| 任務名稱              | 說明                                                     |
| ----------------- | ------------------------------------------------------ |
| Daily Docs Review | 讀取 `docs/ai-review/AI-review-prompt.md`，審查三個 Repo 文件狀況 |

管理介面：https://claude.ai/code/scheduled

---

## 2.3 AI Skills（手動觸發）

詳見 [claude_skill_spec.md](claude_skill_spec.md)。

---
