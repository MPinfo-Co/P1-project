# fn_feedback 用戶回饋收集 — 測試 Epic 設計文件

**日期：** 2026-05-11
**目的：** 以 fn_feedback 功能作為測試 Epic，完整執行 Epic → SA → SD → PG 流程，驗證 pg-orchestrator 實作穩定性。

---

## 目標與策略

用一個真實但完全獨立的功能（用戶回饋收集）走一次完整四階段 pipeline。

- SA/SD 走真實流程並 merge 至 P1-design main（確保 workflow 觸發鏈正確）
- PG 實作後**不 merge** P1-code main，由人類審查
- 功能本身有留用價值，可視審查結果決定是否正式引入

---

## Epic 內容（PM 填寫）

**標題：** `[PM] fn_feedback 用戶回饋收集`

**需求說明：**
用戶可在系統中提交使用回饋，包含評分（1–5 星）與文字留言，讓管理員了解用戶體驗現況。管理員可在後台查看所有回饋列表，並依評分篩選。

**驗收條件：**
- 用戶能提交一筆回饋（rating 1–5 + comment 選填）
- 管理員可查看回饋列表，支援依 rating 篩選
- 回饋列表顯示：用戶名、rating、留言摘要、提交時間

---

## 預期工作範圍（SD 產出 TDD 參考）

| # | 類型 | 工作內容 |
|---|------|---------|
| 1 | Model | 建立 `tb_feedback`（user_id, rating int 1–5, comment text nullable, created_at） |
| 2 | API | 建立 `POST /feedback`（用戶提交，需登入） |
| 3 | API | 建立 `GET /feedback`（管理員列表，支援 rating query param 篩選） |
| 4 | API | 建立 `GET /feedback/{id}`（管理員查看單筆） |
| 5 | 畫面 | 用戶：回饋表單頁（評分星星 + 留言文字框 + 送出按鈕） |
| 6 | 畫面 | 管理員：回饋列表頁（篩選下拉 + 表格呈現） |
| 7 | Test | pytest ≥ test_api.md 測試案例數 |

---

## Merge 策略

| 階段 | 動作 |
|------|------|
| SA PR | 審查後 merge → 觸發 SD workflow |
| SD PR | 審查後 merge → 觸發 PG workflow |
| PG PR | **不 merge** — 由人類審查後決定 |

---

## 清理策略（視測試結果選擇）

| 情境 | 操作 |
|------|------|
| 功能決定留用 | PG PR 正常 review + merge，無需清理 |
| 功能捨棄 | 關閉 PG PR + 刪 branch；P1-design revert 2 個 merge commit；關閉所有相關 Issue |
| 先擱置 | 關閉 PG PR（不刪 branch），隨時可重開 |

---

## 成功標準

- wf_epic_to_sa → wf_sa_to_sd → wf_sd_to_pg 三條 workflow 均正確觸發且完成
- pg-orchestrator 產出：後端 migration + API + pytest；前端表單頁 + 列表頁
- pytest 數量 ≥ test_api.md 測試案例數
- wf_pg_ci（Ruff + Pytest + ESLint + Prettier）全部通過
