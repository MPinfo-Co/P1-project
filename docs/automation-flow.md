# 自動化流程設計

## 概述

本文件描述 P1 各開發階段的 AI Agent 自動化流程架構。
設計原則：**AI 負責初稿與驗證，人負責判斷與授權。**

---

## 完整流程

```
PM 開立 Epic Issue
│
├─ SA Agent 撰寫 business-logic.md
│   └─ SA Review Agent 審查（加 review comment）
│       ├─ 不通過 → 打回 SA Agent（retry，超過次數升級人工）
│       └─ 通過 → P1 審查優化 + 開 PR → P2 Approve + Merge
│
├─ SD Agent 撰寫 TDD + 更新 Spec/Prototype/Schema
│   └─ SD Review Agent 審查（加 review comment）
│       ├─ 不通過 → 打回 SD Agent（retry，超過次數升級人工）
│       └─ 通過 → P1 審查優化 + 開 PR → P2 Approve + Merge
│
└─ PG Agent 撰寫 Code
    ├─ PG SpecDiff Agent（TDD 覆蓋率核對）
    │   └─ 不通過 → 打回 PG Agent
    ├─ PG Review Agent（靜態審查）
    │   └─ 不通過 → 打回 PG Agent
    ├─ PG Test Agent（pytest 動態測試）
    │   └─ 不通過 → 打回 PG Agent
    └─ 全通過 → P1 審查 + Local Test + 開 PR → P2 Approve + Merge
```

---

## 各 Agent 職責說明

### SA 階段

| Agent | 職責 |
|---|---|
| **SA Agent** | 依 Epic 需求撰寫 `business-logic.md`（需求說明、商業邏輯、資料模型示意、SD 注意事項、畫面示意） |
| **SA Review Agent** | 審查文件完整性與品質，以 review comment 形式回饋；不通過則打回 SA Agent 修改 |

### SD 階段

| Agent | 職責 |
|---|---|
| **SD Agent** | 依 `business-logic.md` 撰寫 TDD，並同步更新 `Spec/`、`Prototype/`、`schema/` |
| **SD Review Agent** | 審查 TDD 完整性（工作項目、測試案例覆蓋率等），以 review comment 形式回饋；不通過則打回 SD Agent 修改 |

### PG 階段

| Agent | 職責 | 執行順序 |
|---|---|---|
| **PG Agent** | 依 TDD 撰寫實作 code 與 TestReport | 初稿 |
| **PG SpecDiff Agent** | 核對實作是否覆蓋 TDD 所有工作項目（T1～Tn），確認「有沒有做」 | 1st |
| **PG Review Agent** | 靜態程式碼審查（style、pattern、security），確認「做得好不好」 | 2nd |
| **PG Test Agent** | 執行 pytest 動態測試，確認「跑起來對不對」 | 3rd |

> PG 三個驗證 Agent 依序執行，任一不通過即打回 PG Agent 修改。

---

## Retry 機制

- SA / SD Agent：不通過時打回修改，**超過次數上限則升級為人工處理**（次數上限待定）
- PG Agent：三個驗證 Agent 任一不通過即打回，無次數上限（由 Test/Review 結果決定終止條件）

---

## 人工審查角色

| 角色 | 職責 | 指派方式 |
|---|---|---|
| **P1** | 審查並優化 AI 產出內容、開 PR | PM 指派 |
| **P2** | 最終審查、Approve PR、Merge | PM 指派 |

---

## 待定事項

- [ ] 各 Review Agent 獨立審查標準（prompt）定義
- [ ] SA / SD retry 次數上限
- [ ] Agent 觸發機制技術實作（Remote Trigger / GitHub Actions 串接）
