# P1 缺口與孤立文件掃描任務

> [← 回到總導覽](../../README.md)

## 任務目標
掃描四個 Repo 的實際檔案，找出：
- **孤立文件**：存在於 Repo 中但未被任何索引文件覆蓋
- **缺口**：系統中實際運作的功能或機制，但無對應文件說明

## 限制
- 唯讀分析，不修改任何檔案

---

## Phase 1 — 環境準備

若本任務緊接在 [AI-review-prompt.md](AI-review-prompt.md) 之後執行，對話中已有最新文件內容，**跳過此 Phase**。

若獨立執行：四個 Repo **平行** git pull：
- P1-project / P1-analysis / P1-design / P1-code

---

## Phase 2 — 掃描與比對

### Step 1 — 掃描 .md 檔案
平行掃描四個 Repo，排除以下目錄：
- `node_modules/`、`.git/`、`__pycache__/`、`.pytest_cache/` 等非專案目錄
- `P1-analysis/issue-{N}/`（SA Delta Record，以 Issue 為單位產生）
- `P1-design/TDD/`（SD Delta Record，以 Issue 為單位產生）
- `P1-code/VersionDiff/`（自動產生的版本異動紀錄）

### Step 2 — 識別孤立文件
**索引文件**定義：各 Repo 的 `README.md`、`CLAUDE.md` 中的目錄結構描述、`AI-review-doclist.md`。

判斷：若一份 `.md` 檔案未出現在任何索引文件的目錄描述或連結中 → 孤立文件。

以下類別設計上不需被索引，排除：
- `P1-analysis/references/`（全域參考文件，不追蹤索引）
- 自動產生的報告（`AI-review-report.md`、`AI-review-gap-report.md`）

### Step 3 — 識別缺口
比對以下面向，找出無文件覆蓋的主題：
- 系統功能（對照 `FunctionList.md`）
- Workflow 機制（對照 `workflow_guide.md` 流程）
- 部署與維運操作
- 跨 Repo 協作規則

**缺口標準**：實際運作中存在的機制或流程，找不到任何文件說明。「可以補充但非必要」不列為缺口。

---

## Phase 3 — 收尾

1. 將報告寫入 `docs/ai-review/AI-review-gap-report.md`（prepend，保留歷史）
2. Commit & Push P1-project
3. 輸出報告連結：[AI-review-gap-report.md](https://github.com/MPinfo-Co/P1-project/blob/main/docs/ai-review/AI-review-gap-report.md)

---

## 報告格式
> - 每次執行為獨立區塊，以 `## YYYY-MM-DD` 標題分隔
> - 最新一次插入檔案最上方（既有內容往下推）
> - 僅保留最近 3 次（完整歷史由 git 追溯）

### 孤立文件清單
> 存在於 Repo 中但未被任何索引文件覆蓋，供後續人工判斷處置。

| # | 文件路徑 | 備註 |
|---|---------|------|

### 缺口清單
> 實際運作中存在但缺乏文件說明的主題。

| # | 風險 | 缺口描述 | 建議處理方式 |
|---|------|---------|------------|

> 風險等級：`低`（單點補充）/`中`（影響多處）/`高`（牽動跨文件結構）

### 摘要
> 發現孤立文件 {N} 個，缺口 {M} 個。
