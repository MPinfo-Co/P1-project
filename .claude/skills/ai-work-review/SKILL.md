---
name: ai-work-review
description: Use when user wants to review SA/SD/PG work output - auto-detects context from git branch name or files and dispatches the correct reviewer agent (sa-reviewer, sd-reviewer, or pg-reviewer)
---

# AI Work Review

自動判斷當前情境，dispatch 對應的 reviewer agent。

## 判斷流程

1. 執行 `git branch --show-current` 取得 branch 名稱
2. 依 branch 名稱判斷類型：
   - 含 `sa/` → dispatch **sa-reviewer**
   - 含 `sd/` → dispatch **sd-reviewer**
   - 含 `pg/` → dispatch **pg-reviewer**
3. 若 branch 無法判斷，偵測檔案：
   - 有 `business-logic.md`（無 TDD/）→ **sa-reviewer**
   - 有 `TDD/issue-N.md`（無 TestReport/）→ **sd-reviewer**
   - 有 `TestReport/issue-N.md` → **pg-reviewer**
4. 仍無法判斷時，詢問用戶一個問題：「這是哪個階段？SA / SD / PG？」

## 各 Agent 對應情境

| 類型 | Branch 特徵 | Agent |
|------|------------|-------|
| SA | 含 `sa/` | `sa-reviewer` |
| SD | 含 `sd/` | `sd-reviewer` |
| PG | 含 `pg/` | `pg-reviewer` |

## 執行方式

確認類型後，從 branch 名稱或 issue body 取得 issue 編號，
以 issue 編號作為 context dispatch 對應 agent。
