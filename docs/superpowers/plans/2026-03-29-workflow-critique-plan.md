# 開發流程規範批判優化計劃

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 從八個不同角度系統性批判現有開發流程規範，找出盲點與缺陷，逐步優化至接近完善。

**Architecture:** 每個任務代表一個批判角度，獨立審查後提出具體修改建議，再更新文件。每個角度完成後 commit 一次，確保每一輪優化都有紀錄。

**Target files:**
- `docs/github-workflow/overview.md`
- `docs/github-workflow/repo-design.md`
- `docs/github-workflow/workflow.md`

---

## Task 1：PM 視角

**問題清單（逐一檢視）：**

- [ ] PM 如何知道目前有多少 Epic 在進行中？看板設計夠嗎？
- [ ] PM 開立 Epic 的資訊量是否足夠驅動 SA？驗收條件是否可量化？
- [ ] Epic 關閉條件是否合理？「所有 PG Issue merge」就算完成嗎？還是需要 PM 確認驗收？
- [ ] SA 拆分 Issue 後，PM 如何被通知？通知機制有沒有說清楚？
- [ ] 若 PM 想介入某個階段（如 SA 分析方向有誤），流程有沒有讓 PM 能即時介入的管道？
- [ ] 依據以上發現，修改 `workflow.md` 與 `overview.md` 相關段落
- [ ] Commit：`docs: PM視角批判優化`

---

## Task 2：SA 視角

**問題清單（逐一檢視）：**

- [ ] SA 的輸出文件（商業邏輯說明 + SD WBS）格式是否有足夠的規範，還是太自由導致品質不一？
- [ ] SD WBS 若寫得不夠清楚，SD 要怎麼辦？有沒有退回機制？
- [ ] 需求在 SA merge 後才被 SD 發現有問題，怎麼處理？流程有沒有「需求變更」的路徑？
- [ ] SA 自己也需要查閱歷史需求嗎？P1-analysis 的資料夾結構是否便於查找？
- [ ] 依據以上發現，修改相關文件段落
- [ ] Commit：`docs: SA視角批判優化`

---

## Task 3：SD 視角

**問題清單（逐一檢視）：**

- [ ] SD 收到 SA 通知後，如何快速理解需要修改哪些 Spec/Prototype？現有資訊是否足夠？
- [ ] 活文件（Spec/Prototype）被多個 Issue 同時修改時，會有 branch conflict 嗎？如何處理？
- [ ] SD 拆分 Issue 的判斷標準是什麼？太主觀嗎？需要規範嗎？
- [ ] TestPlan 測試案例的品質如何保證？有沒有最低要求（如每個 API 至少一個正常案例 + 一個錯誤案例）？
- [ ] 依據以上發現，修改相關文件段落
- [ ] Commit：`docs: SD視角批判優化`

---

## Task 4：PG／AI 視角

**問題清單（逐一檢視）：**

- [ ] AI 讀取 PG Issue 時，能取得的資訊是否真的足夠自主實作？逐一列出 AI 需要的資訊，確認每一項都有對應的來源
- [ ] VersionDiff 的「上一個 commit」是否足夠讓 AI 理解現有程式碼狀態？還是需要更多上下文？
- [ ] PG 依據 TestPlan 寫測試，但 TestPlan 是 SD 寫的，若測試案例不夠精確，PG 如何處理？
- [ ] AI 實作偏離 Spec 時，PR template 的「實作說明」欄位是否能有效捕捉這個資訊？
- [ ] 人類 PG 與 AI PG 的工作流程是否一樣？有沒有需要分開處理的地方？
- [ ] 依據以上發現，修改相關文件段落
- [ ] Commit：`docs: PG/AI視角批判優化`

---

## Task 5：失敗情境視角

**問題清單（逐一檢視）：**

- [ ] **Hotfix**：線上出現緊急 bug，需要跳過 SA/SD 直接修程式碼，現有流程支援嗎？
- [ ] **需求變更**：SA 已 merge，SD 進行到一半，PM 說需求要改，怎麼處理？
- [ ] **CI 失敗**：PG push 後 CI 一直過不了，流程有沒有指引？
- [ ] **審查人員不可用**：指定的審查人員請假，PR 卡住，有沒有備案？
- [ ] **錯誤的 merge**：不小心把半成品 merge 進 main，怎麼回滾？
- [ ] **跨 Issue 相依**：PG Issue A 依賴 PG Issue B 的程式碼，流程有沒有處理相依關係？
- [ ] 依據以上發現，新增「例外處理」段落至 `workflow.md`
- [ ] Commit：`docs: 失敗情境批判優化`

---

## Task 6：規模化視角

**問題清單（逐一檢視）：**

- [ ] 團隊從 2 人擴展到 10 人時，流程的哪些地方會變成瓶頸？
- [ ] 多個 Epic 同時進行時，Issue 編號、分支、TestPlan 的命名是否還能清楚辨識？
- [ ] 多個 SD 同時修改同一份活文件（如 Schema.md），衝突如何處理？
- [ ] PM 同時追蹤 5 個以上 Epic 時，GitHub Projects 的看板設計是否還夠用？
- [ ] 新成員加入時，這套流程的學習曲線合理嗎？有沒有需要簡化的地方？
- [ ] 依據以上發現，修改相關文件段落
- [ ] Commit：`docs: 規模化視角批判優化`

---

## Task 7：自動化可行性視角

**問題清單（逐一檢視）：**

- [ ] 逐一列出所有「系統自動」的項目，評估實作難度（簡單／中等／複雜）
- [ ] 哪些自動化項目若沒做，流程會完全卡住？（關鍵路徑）
- [ ] 哪些自動化項目若沒做，只是不方便但流程仍可運作？（錦上添花）
- [ ] GitHub Actions 的 token 權限能否支援跨 repo 操作？需要什麼設定？
- [ ] 自動化失敗時（如 workflow 出錯），人工應急方案是什麼？文件裡有說嗎？
- [ ] 依據以上發現，在 `workflow.md` 加入自動化優先級與應急方案說明
- [ ] Commit：`docs: 自動化可行性批判優化`

---

## Task 8：採用難度視角

**問題清單（逐一檢視）：**

- [ ] 一個新成員看完三份文件，能在第一天就上手嗎？哪裡最容易卡關？
- [ ] 日常操作中，哪些步驟最繁瑣、最容易被跳過？
- [ ] 有沒有哪些規範設計得太嚴格，反而讓人想繞過？
- [ ] 文件本身的可讀性：非技術的 PM 讀 overview.md 能理解嗎？
- [ ] 需不需要一份「快速上手 Cheat Sheet」讓成員貼在桌上？
- [ ] 依據以上發現，修改文件或新增 `quick-start.md`
- [ ] Commit：`docs: 採用難度批判優化`

---

## 最終整合

- [ ] 回顧八個任務的所有修改，檢查文件之間是否一致（overview / repo-design / workflow 不互相矛盾）
- [ ] 更新 `overview.md` 的版本說明（加入最後更新日期）
- [ ] Commit：`docs: 批判優化整合完成`
