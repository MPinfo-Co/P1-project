---
name: plan-go-check-report
description: Use when executing implementation tasks that touch multiple files or repos, require scope verification before acting, and need post-execution validation and reporting — especially for config, workflow, and prompt file changes
---

# Plan-Go-Check-Report

七步驟執行流程，確保多檔案異動任務從確認範圍到報告結果均有完整覆蓋。

## 七步驟

### Step 1：再確認影響範圍
讀取所有受影響的實際檔案（不依賴記憶），列出完整清單：
- 哪些檔案、哪些行、哪種異動類型
- 跨 repo 的依賴順序

### Step 2：評估執行計畫
依影響範圍擬定分步驟計畫：
- 每個 Task 對應一個檔案或一類變更
- 確認執行順序（有依賴的先做）
- 確認 commit 分組（同 repo 一個 commit）

### Step 3：檢查及優化計畫
計畫自我審查，優先確認：
- 有無漏改的路徑或欄位
- 每個步驟是否有可驗證的結果
- commit message 是否清楚

### Step 4：執行
依計畫逐步實作，每個 Task 完成後標記。

### Step 5：檢查執行結果及排除問題
對照 Step 1 的影響範圍清單，逐項確認每項變更均已落地：
- 用 grep 或 Read 驗證實際內容
- 發現遺漏立即修正

### Step 6：測試及排除問題
觸發實際驗證：
- 可自動測試：跑測試套件，確認通過
- 無法自動測試（如 workflow/config）：列出手動驗證步驟，請用戶確認或自行說明預期行為
- 發現問題立即修正

### Step 7：報告執行結果及建議
輸出執行摘要：
- 完成項目（每個 Task 的狀態）
- 已知限制或未驗證項目
- 建議後續行動（如：手動觸發 workflow 確認）

## 使用時機

- 影響多個檔案或跨 repo 的修改任務
- Workflow / prompt / config 類型的修正
- 需要在執行後驗證成效的變更

## 注意事項

- Step 1 必須讀取實際檔案，不依賴對話中的先前摘要
- Step 5 要對照 Step 1 的清單逐項確認，不跳過
- Step 6 若無法自動測試，明確列出手動驗證步驟而非略過
- 若測試發現問題，回到 Step 4 修正後再重跑 Step 5–6
