
# 自動化流程核心目標

## 人類協作層面
- **可追蹤**：每一行程式碼都能追溯到設計規格，每一份規格都能追溯到需求分析
- **可驗證**：每個階段都有明確的品質把關，不符合標準的工作無法進入下一階段
- **自動化**：重複性的文書工作（建立分支、記錄變更、通知下游）由系統自動完成

## AI 協作層面
- AI 接到 Issue 後，能沿著 Issue 關聯(PM>SA>PG>PG)自主讀取商業邏輯、設計規格、歷史異動，不需要人工交接，直接產出可交付的程式碼

---

# 流程總覽

```
PM（P1-project）開立 Epic
 └─ p-workflow 自動建立 SA Issue + A-Branch（P1-analysis）
     └─ SA merge → a-workflow 自動建立 SD Issue + D-Branch（P1-design）
         └─ SD merge → d-workflow 自動建立 PG Issue + C-Branch（P1-code）
             └─ PG merge → 版本完成，VersionDiff 自動產生
```

| 階段 | 負責人 | Repo | 產出 |
|------|--------|------|------|
| 工作分派 | PM | P1-project | SA Issue + A-Branch |
| 系統分析 | SA | P1-analysis | business-logic.md、SD-WBS.md |
| 系統設計 | SD | P1-design | Spec、Prototype、TDD |
| 系統開發 | PG／AI | P1-code | 程式碼、測試、VersionDiff |

**關鍵原則：下游分支在上游 merge 後才建立，確保 PG 永遠依據最新規格開發。**

---

## 四個關鍵機制

### 1. Epic 串聯（跨 Repo 全局追蹤）

一個功能從需求到上線，由一個 Epic 串起四個 Repo 的 Issue：

```
P1-project Epic #1（PM）
└── P1-analysis SA Issue #4
    └── P1-design SD Issue #5
        └── P1-code PG Issue #7
```

SD 若發現工作量太大，可拆分為多個 SD Issue 平行開發；PG merge 後，c-workflow 自動關閉 Epic。

### 2. Delta Record（變更追蹤）

每個階段都有「這次改了什麼」的紀錄：

| 階段 | Delta 位置 | 說明 |
|------|-----------|------|
| SA | `P1-analysis/issue-{N}/` | 資料夾本身就是 delta |
| SD | `P1-design/SpecDiff/issue-{N}.md` | 系統自動產生 |
| PG | `P1-code/VersionDiff/issue-{N}.md` | merge 時自動產生 |

### 3. Issue Body 結構化（AI 可讀）

每個 Issue body 包含標準化關聯欄位，AI 讀取 PG Issue 後可沿關聯鏈往上取得完整脈絡自主實作。格式定義見 [repo-design.md](repo-design.md)。

### 4. 品質把關

- **本地**：pre-commit（ruff）+ husky lint-staged（ESLint、Prettier）+ commitlint
- **CI**：ruff lint/format、ESLint、Prettier check、pytest（P1-code）
- **PR**：各階段有審查人確認品質，不符標準退回

---

## GitHub Actions 自動化

各 workflow 的 yml 檔如下：

| Workflow | yml 檔 | 觸發 | 優先級 |
|----------|--------|------|--------|
| p-workflow | [p-workflow.yml](../.github/workflows/p-workflow.yml) | Epic 加上 `epic` label | P0 |
| a-workflow | [a-workflow.yml](https://github.com/MPinfo-Co/P1-analysis/blob/main/.github/workflows/a-workflow.yml) | A-Branch merge | P0 |
| d-workflow | [d-workflow.yml](https://github.com/MPinfo-Co/P1-design/blob/main/.github/workflows/d-workflow.yml) | D-Branch merge | P0 |
| c-workflow | [c-workflow.yml](https://github.com/MPinfo-Co/P1-code/blob/main/.github/workflows/c-workflow.yml) | Push / PR / merge | P0 |
| chore-workflow | [a-chore](https://github.com/MPinfo-Co/P1-analysis/blob/main/.github/workflows/a-chore-workflow.yml) / [d-chore](https://github.com/MPinfo-Co/P1-design/blob/main/.github/workflows/d-chore-workflow.yml) / [c-chore](https://github.com/MPinfo-Co/P1-code/blob/main/.github/workflows/c-chore-workflow.yml) | Issue 加上 `chore` label | P1 |

> 如需了解 workflow 細節，直接詢問 AI 即可。

### Token 權限

跨 Repo 操作需要 token：

| 方案 | 適用階段 |
|------|---------|
| PAT（Personal Access Token） | MVP 階段，快速可用 |
| GitHub App Token | 人員穩定後，權限更精確 |

Token 以 Org-level Secret 集中管理，各 Repo workflow 直接引用。

---

## 排程 AI 任務

每天台灣時間 **凌晨 2:00** 自動執行，由 Claude Code Remote Agent 在雲端運作。

| 任務 | 說明 |
|------|------|
| Daily Docs Review | 讀取 `docs/ai-review/AI-review-prompt.md`，審查四個 Repo 文件狀況，結果寫入 `docs/ai-review/AI-review-report.md`（直接 push main） |

管理介面：https://claude.ai/code/scheduled

---

## 例外處理

### Hotfix（線上緊急 bug）
不走正常 Epic 流程。直接在 P1-code 開 Chore Issue，手動建立 `chore-{N}-hotfix` 分支，修完 PR merge。VersionDiff 由 c-workflow 在 merge 時自動產生；事後需手動補 Epic 關聯記錄（在對應 Epic Issue 留言說明 hotfix 範圍）。

### 需求變更（SA 已 merge，SD 進行中）
SD 在 PR 留言說明影響範圍，PM 決定：繼續（SD 在現有 PR 更新）或開新 Epic。

### CI 持續失敗
第 3 次仍失敗：在 Issue 留言 @SD @PM，說明錯誤訊息與已嘗試的方向，等待指示。

### workflow 自動化失敗（分支未自動建立）
15 分鐘內未看到下游 Issue，查閱對應 workflow 的規格文件，依其「應急方案」手動處理：
[p-workflow.yml](../.github/workflows/p-workflow.yml)、[a-workflow.yml](https://github.com/MPinfo-Co/P1-analysis/blob/main/.github/workflows/a-workflow.yml)、[d-workflow.yml](https://github.com/MPinfo-Co/P1-design/blob/main/.github/workflows/d-workflow.yml)、[c-workflow.yml](https://github.com/MPinfo-Co/P1-code/blob/main/.github/workflows/c-workflow.yml)
