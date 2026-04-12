# P1 開發指南

> [← 回到總導覽](../../README.md)

> 本文件說明 P1 的設計理念與整體流程。
> 第一天操作請看 [quick-start.md](quick-start.md)。
> Repo 結構與格式規範請看 [repo-design.md](../repo-design.md)。

---

## 為什麼這樣設計

兩個核心目標：

**人類協作層面：**
- **可追蹤**：每一行程式碼都能追溯到設計規格，每一份規格都能追溯到需求分析
- **可驗證**：每個階段都有明確的品質把關，不符合標準的工作無法進入下一階段
- **自動化**：重複性的文書工作（建立分支、記錄變更、通知下游）由系統自動完成

**AI 協作層面：**
- AI 接到 PG Issue 後，能沿著 Issue 關聯鏈自主讀取商業邏輯、設計規格、歷史異動，不需要人工交接，直接產出可交付的程式碼

**終極目標：人負責決策，AI 負責執行。**

---

## 流程總覽

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

SD 若發現工作量太大，可拆分為多個 SD Issue 平行開發；所有 PG Issue 完成後，PM 手動驗收並關閉 Epic。

### 2. Delta Record（變更追蹤）

每個階段都有「這次改了什麼」的紀錄：

| 階段 | Delta 位置 | 說明 |
|------|-----------|------|
| SA | `P1-analysis/issue-{N}/` | 資料夾本身就是 delta |
| SD | `P1-design/TDD/issue-{N}-diff.md` | 系統自動產生 |
| PG | `P1-code/VersionDiff/issue-{N}.md` | merge 時自動產生 |

### 3. Issue Body 結構化（AI 可讀）

每個 Issue body 包含標準化關聯欄位，AI 讀取 PG Issue 後可沿關聯鏈往上取得完整脈絡自主實作。格式定義見 [repo-design.md](../repo-design.md)。

### 4. 品質把關

- **本地**：pre-commit（ruff）+ husky lint-staged（ESLint、Prettier）+ commitlint
- **CI**：ruff lint/format、ESLint、Prettier check、pytest（P1-code）
- **PR**：各階段有審查人確認品質，不符標準退回

---

## GitHub Actions 自動化

各 workflow 的詳細觸發條件與行為見 `spec/`：

| Workflow | 規格文件 | 觸發 | 優先級 |
|----------|---------|------|--------|
| p-workflow | [spec/p-workflow.md](spec/p-workflow.md) | Epic 加上 `epic` label | P0 |
| a-workflow | [spec/a-workflow.md](spec/a-workflow.md) | A-Branch merge | P0 |
| d-workflow | [spec/d-workflow.md](spec/d-workflow.md) | D-Branch merge | P0 |
| c-workflow | [spec/c-workflow.md](spec/c-workflow.md) | Push / PR / merge | P0 |
| chore-workflow | [spec/chore-workflow.md](spec/chore-workflow.md) | Issue 加上 `chore` label | P1 |

### Token 權限

跨 Repo 操作需要 token：

| 方案 | 適用階段 |
|------|---------|
| PAT（Personal Access Token） | MVP 階段，快速可用 |
| GitHub App Token | 人員穩定後，權限更精確 |

Token 以 Org-level Secret 集中管理，各 Repo workflow 直接引用。

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
[p-workflow.md](spec/p-workflow.md)、[a-workflow.md](spec/a-workflow.md)、[d-workflow.md](spec/d-workflow.md)、[c-workflow.md](spec/c-workflow.md)
