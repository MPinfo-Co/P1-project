# P1 開發規範概覽

## 為什麼這樣設計

傳統開發流程中，需求分析、系統設計、程式開發三個階段往往各自為政，文件散落、追蹤困難、下游不清楚上游改了什麼。

本規範有兩個核心目標：

**人類協作層面：**
- **可追蹤**：每一行程式碼都能追溯到設計規格，每一份規格都能追溯到需求分析
- **可驗證**：每個階段都有明確的品質把關，不符合標準的工作無法進入下一階段
- **自動化**：重複性的文書工作（建立分支、記錄變更、通知下游）由系統自動完成

**AI 協作層面：**
- **AI 可自主實作**：AI 接到 PG Issue 後，能沿著 Issue 關聯鏈自主讀取商業邏輯、設計規格、歷史異動，不需要人工交接，直接產出可交付的程式碼

這套規範的終極目標是：**人負責決策，AI 負責執行。**

---

## 四個 Repo 的職責

| Repo | 層級 | 職責 | 負責角色 |
|------|------|------|---------|
| **P1-project** | 產品管理 | Epic 管理、技術研究、規範文件 | PM |
| **P1-analysis** | 需求分析 | 商業邏輯、Use Case、流程圖、SD WBS | SA |
| **P1-design** | 系統設計 | 畫面原型、API 規格、資料庫 Schema、測試計劃 | SD |
| **P1-code** | 系統開發 | 前後端程式碼、自動化測試 | PG／AI |

---

## 四個角色與工作流程

```
PM（P1-project）開立 Epic
 └─ 觸發 SA Issue（P1-analysis）
     └─ SA merge ──→ 觸發 SD Issue（P1-design）
         └─ SD merge ──→ 觸發 PG Issue（P1-code）
             └─ PG／AI 實作 ──→ 版本完成
```

每個階段：
1. 由上游 merge 後自動建立分支與 Issue
2. 在自己的 Repo 完成工作
3. 開 PR 經審查後 merge
4. Merge 後自動通知下游

---

## 四個關鍵機制

### 1. Epic 串聯（跨 Repo 全局追蹤）

一個功能從需求到上線，由一個 Epic 串起四個 Repo 的 Issue：

```
P1-project Epic #1（PM）
└── P1-analysis SA Issue #4
    ├── P1-design SD Issue #5（正常）
    │   └── P1-code PG Issue #7
    └── P1-design SD Issue #6（拆分）
        └── P1-code PG Issue #8
```

PM 在 P1-project 開立 Epic 後，系統自動在下游 Repo 建立對應 Issue 並記錄關聯。SD 若發現工作量太大，可手動拆分為多個 SD Issue，各自觸發對應的 PG Issue 平行開發；拆分時系統自動通知 PM 確認工時分配。所有 PG Issue 完成後，系統通知 PM 驗收，由 PM 手動關閉 Epic。

### 2. Delta Record（變更追蹤）

每個階段都有一份「這次改了什麼」的紀錄：

- **P1-analysis**：`issue#N/` 資料夾本身就是 delta（一個 Issue 一個資料夾）
- **P1-design**：`TestPlan/issue#N.md` 自動記錄修改了哪些規格文件，SD 人工補充測試案例
- **P1-code**：`VersionDiff/issue#N.md` merge 時自動產生，記錄程式碼異動與完整 Issue 關聯鏈

### 3. Issue Body 結構化（AI 可讀）

每個 Issue 的 body 包含標準化的關聯欄位：

```
Epic：P1-project #1
上游 Issue：P1-analysis #4（或 P1-design #5）
下游 Issue：P1-design #5（或 P1-code #7）
階段：SA / SD / PG
```

AI 讀取 PG Issue 時，可沿著關聯鏈往上追，取得完整脈絡後自主實作。

### 4. 品質把關（Branch Protection）

每個 Repo 的 `main` 分支設有保護規則：

- PR 必須通過自動化 check 才能 merge
- SA／SD PR：必填關聯項目與對下游的影響說明
- PG PR：本地測試與 CI 測試必須全數通過

---

## 預期效益

| 問題 | 解法 |
|------|------|
| PM 無法一眼看到功能全局進度 | GitHub Projects 聚合四個 Repo 的 Issue，以 Epic 為單位分組；Board view 顯示各 Epic 進行中／完成狀態 |
| 下游不知道上游改了什麼 | Merge 時自動在下游 Issue 留言，附上異動清單 |
| PR 內容空洞、難以審查 | PR template 強制填寫，workflow 自動驗證 |
| 程式碼無法追溯到需求 | Issue 關聯鏈 + VersionDiff 記錄完整脈絡 |
| 文件與程式碼脫節 | SD merge 才觸發 PG 分支，確保 PG 依最新規格開發 |
| AI 需要人工交接才能實作 | 結構化 Issue + TestPlan + VersionDiff 讓 AI 自主讀取脈絡 |
| 手動流程容易遺漏 | GitHub Actions 自動化分支建立、通知、測試、部署 |
