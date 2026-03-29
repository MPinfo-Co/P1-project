# 開發工作流程

## 流程總覽

| 階段 | 負責人 | Repo | 觸發條件 | 產出 |
|------|--------|------|---------|------|
| 工作分派 | PM | P1-project | PM 手動開立 Epic | SA Issue + A-Branch 自動建立 |
| 系統分析 | SA | P1-analysis | A-Branch 建立後 | 商業邏輯文件、SD WBS |
| 系統設計 | SD | P1-design | SA merge 後自動觸發 | Spec、Prototype、TestPlan |
| 系統開發 | PG／AI | P1-code | SD merge 後自動觸發 | 程式碼、測試、VersionDiff |

**關鍵原則：下游分支在上游 merge 後才建立，確保 PG 永遠依據最新規格開發。**

---

## 一、工作分派（PM）

```
PM 在 P1-project 使用 Epic Issue 範本開立 Epic
    └─ 觸發 P-workflow
        ├─ 在 P1-analysis 開立 SA Issue（關聯 Epic）
        ├─ 自動建立 A-Branch（issue-{N}-{slug}）
        └─ 自動 assign SA
PM 手動 assign Issue 給 SA
```

**Epic Issue 範本欄位：**
- 功能名稱
- 背景說明（為什麼需要這個功能）
- 驗收條件（格式：Given... / When... / Then...，至少一條）
- 優先順序（P0 緊急 / P1 本 Sprint / P2 下個 Sprint）
- 預計完成日期

---

## 二、系統分析（SA）

```
1. SA 在 Local Pull A-Branch
2. SA 新增以下文件至 issue#{N}/ 資料夾：
   ├─ 商業邏輯說明（Use Case、流程圖、Class Diagram、ER 示意）
   └─ SD-WBS.md（列出 SD 需完成的工作項目）
3. SA Push A-Branch（commitlint 格式驗證）
4. SA 開 Pull Request
   └─ 填寫 PR template（見 PR 規範）
5. PM 指派審查人員 1 人
6. 審查人員審查文件
7. Merge

Merge 後自動觸發：
   ├─ 在 P1-design 建立 D-Branch
   ├─ 在 P1-design 開立 SD Issue（關聯 Epic + SA Issue）
   ├─ 將 SD-WBS.md 的工作項目清單自動複製至 SD Issue body 的「設計範圍」欄位
   ├─ 在 SD Issue 留言通知 SD：「SA 分析完成，請開始系統設計」
   └─ 更新 Epic Issue：填入 SD Issue 編號
```

**審查優先順序：PM > SA > Self**

---

## 三、系統設計（SD）

**SD 收到通知後，若發現 SA 文件描述不清楚或有疑問：**
- SD 直接在 SD Issue 留言，@SA 說明問題點
- SA 須在 2 個工作天內回覆（補充說明或修正文件）
- 若問題需修改已 merge 的 SA 文件，SA 開新 Issue 處理，不重開原 Issue

**若 SD 發現需求有根本性問題（非描述不清，而是需求本身有誤）：**
- SD 在 SD Issue 留言說明問題，加上 `needs-sa-review` 標籤
- 同時在 Epic Issue 留言通知 PM
- PM 決定處理方式：由 SA 補開 Issue 修正分析，或 PM 直接調整需求
- 在問題解決前，SD Issue 加上 `blocked` 標籤，SD 不繼續推進

```
1. SD 在 Local Pull D-Branch
2. SD 修改 Prototype/ 及 Spec/ 下的相關文件
3. SD 在 TestPlan/issue#{N}.md 撰寫測試案例
   （修改項目由系統自動填入，SD 只需填測試案例）
4. SD Push D-Branch（commitlint 格式驗證）
5. SD 開 Pull Request
   └─ 填寫 PR template（見 PR 規範）
6. SD 指派審查人員 1 人
7. 審查人員審查文件
8. Merge

Merge 後自動觸發：
   ├─ 自動比對 diff，將修改項目寫入 TestPlan/issue#{N}.md
   ├─ 在 P1-code 建立 C-Branch
   ├─ 在 P1-code 開立 PG Issue（關聯 Epic + SA + SD Issue，附異動 Spec 清單）
   ├─ 在 PG Issue 留言通知 PG：「SD 設計完成，以下文件已異動，請參考」
   └─ 更新 Epic Issue：填入 PG Issue 編號
```

**審查優先順序：SA > PM > Self**

---

### 活文件衝突處理（多個 D-Branch 同時修改同一 Spec/Prototype）

當同一時期有多個 SD Issue 並行，各自的 D-Branch 可能修改相同的活文件（例如 `Spec/03UserAPI.md`）。Merge 時若發生衝突：

1. **先 merge 的 D-Branch 無需處理**（正常 merge）
2. **後 merge 的 D-Branch 負責解衝突**：
   - 在 merge 前先 rebase（或 merge main），手動解決衝突
   - 解衝突後在 PR 留言說明衝突位置與解決方式，供審查人員確認
3. **預防原則**：SD 開始設計前，先查看 GitHub Projects 有無其他進行中的 SD Issue 修改相同文件；若有，在各自的 SD Issue 留言協調修改範圍，避免重疊

---

### 系統設計拆分（SD 發現工作量過大）

**拆分判斷原則（符合任一條件即應拆分）：**
- SD-WBS.md 工作項目超過 **8 項**
- 工作項目涉及 **3 個以上不同模組**（不同 Spec 文件）
- 預估設計工時超過 **3 個工作天**
- 部分工作項目存在相依關係，可分批完成（如先做 Schema，再做 API）

```
SD 評估後決定拆分：
1. SD 手動在 P1-design 開立新 SD Issue
   標題格式：[{Epic編號}{字母}] {功能說明}
   例：[1b] 請假申請 - API + 畫面設計
   Body：
     - 父 Epic：P1-project #1
     - 原始 SD Issue：P1-design #5
     - 本拆分標記：[1b]

2. 原始 SD Issue #5 繼續處理較小的部分（如 Schema 變更）
3. 系統自動在 Epic Issue 留言通知 PM：「SD 已拆分 Issue，新增 SD Issue #{N}，請確認工時/資源分配」
4. PM assign 新 SD Issue 給對應成員

拆分後的結構：
   Epic #1
   └── SA Issue #4
       ├── SD Issue #5（[1a] Schema 變更）
       │   └── PG Issue #7（SD #5 merge 後自動建立）
       └── SD Issue #6（[1b] API + 畫面設計）
           └── PG Issue #8（SD #6 merge 後自動建立）

PG Issue #7 與 #8 可平行開發。
```

---

## 四、系統開發（PG／AI）

```
1. PG／AI 在 Local Pull C-Branch
   （PG Issue body 已有 SD 異動 Spec 清單與完整關聯鏈）
2. PG／AI 沿關聯鏈讀取：
   ├─ SA 商業邏輯文件（為什麼這樣設計）
   ├─ SD TestPlan 異動清單（這次改了哪些規格）
   └─ 最新 VersionDiff（現有程式碼的狀態）
3. 依據 Spec/Prototype 修改前後端程式碼
4. 依據 TestPlan 撰寫或修改 pytest 測試程式碼
   規則：testpy 測試項目數 >= TestPlan 測試案例數
         每個 test function 需標注對應的 TestPlan ID
5. 確認本地測試通過：
   ├─ 前端靜態測試：ESLint、Prettier（存檔時自動執行）
   ├─ 後端靜態測試：Ruff（存檔時自動執行）
   └─ 後端動態測試：Pytest（git commit 時自動執行）
6. PG Push C-Branch
   └─ 觸發 CI：GitHub Actions 執行自動化測試
7. 若 CI 通過，PG 開 Pull Request
   ├─ 填寫 PR template（見 PR 規範）
   └─ 觸發自動部署測試環境
8. SD 指派審查人員 2 人（一人負責 Code Review，一人負責功能驗證）
9. 審查人員在測試環境確認：
   ├─ Code Review
   ├─ 操作功能驗證
   └─ 美術排版及文字確認
10. 審查人員在 PR 留言記錄測試步驟
11. Merge

Merge 後自動觸發：
   ├─ 自動產生 VersionDiff/issue#{N}_{作者}_{日期}.md
   └─ 若 Epic 下所有 PG Issue 均已 merge，在 Epic Issue 留言通知 PM：「所有 PG Issue 已完成，請驗收後關閉 Epic」

PM 收到通知後：
   ├─ 確認測試環境符合驗收條件（對照 Epic 中的 Given/When/Then）
   └─ 驗收通過則手動關閉 Epic；若有問題則開立新 Issue 描述缺陷
```

**審查優先順序：SD > SA > PM > Self**

---

## 五、PM 介入與中斷機制

流程設計為線性推進，但 PM 在任何階段均可介入：

**介入方式：**
- **退回**：PM 在進行中的 PR 留言要求修改，PR 不得 merge；審查人員重新 assign 給負責人修改後重新開 PR
- **中斷 Epic**：PM 在 Epic Issue 加上 `blocked` 標籤，並留言說明原因；下游不得繼續推進直到 `blocked` 移除
- **緊急更正**：若 SA 分析方向有誤，PM 直接在 SA Issue 留言，SA 需回覆確認後重新產出文件

**PM 可見度：**
- 所有 Epic 及關聯 Issue 在 GitHub Projects 看板可見
- 系統在以下時機自動通知 PM（Epic Issue 留言）：
  - SA PR 已開啟，等待 PM 指派審查人
  - SD 拆分 Issue，需確認工時/資源
  - 所有 PG Issue 完成，待 PM 驗收

---

## 六、GitHub Actions 自動化說明

### P-workflow（P1-project）

| 觸發條件 | 動作 |
|---------|------|
| Epic Issue opened | 在 P1-analysis 建立 SA Issue + A-Branch，自動 assign |

### A-workflow（P1-analysis）

| 觸發條件 | 動作 |
|---------|------|
| A-Branch PR opened | 在 Epic Issue 留言通知 PM：「SA PR 已開啟，請指派審查人員」 |
| A-Branch merge to main | 在 P1-design 建立 SD Issue + D-Branch，將 SD-WBS.md 工作項目複製至 SD Issue「設計範圍」，通知 SD，更新 Epic |

### D-workflow（P1-design）

| 觸發條件 | 動作 |
|---------|------|
| D-Branch merge to main | 比對 diff 寫入 TestPlan 修改項目 |
| D-Branch merge to main | 在 P1-code 建立 PG Issue + C-Branch，附異動清單，通知 PG，更新 Epic |

### C-workflow（P1-code）

| 觸發條件 | 動作 |
|---------|------|
| Push to C-Branch | 執行 CI：pytest + ESLint + Ruff |
| PR opened | 自動部署測試環境 |
| C-Branch merge to main | 自動產生 VersionDiff 文件，若 Epic 所有 PG Issue 完成則通知 PM 驗收（Epic 由 PM 手動關閉） |

---

## 七、PR 規範

### P1-analysis PR template

```markdown
## 分析完整度確認
- [ ] 商業邏輯說明（Use Case / 流程圖）已完成
- [ ] SD WBS 已列出所有下游工作項目

## 變更原因
<!-- 為什麼需要這個功能？背景是什麼？ -->

## 對 SD 的影響
<!-- SD 開始設計前需要特別注意什麼？ -->

## 關聯項目
- Epic：P1-project #
- SA Issue：#
```

### P1-design PR template

```markdown
## 設計完整度確認
- [ ] Prototype 已更新
- [ ] Spec 文件已更新
- [ ] TestPlan 測試案例已填寫（每個 API 至少正常案例 + 錯誤案例，每個畫面至少一個主流程案例）

## 設計決策說明
<!-- 有哪些設計選擇？為什麼這樣決定？ -->

## 對 PG 的影響
<!-- PG 實作時需要特別注意什麼？ -->

## 關聯項目
- Epic：P1-project #
- SA Issue：P1-analysis #
- SD Issue：#
```

### P1-code PR template

```markdown
## 測試通過確認
- [ ] 本地 Pytest 通過
- [ ] CI 自動化測試通過
- [ ] testpy 覆蓋所有 TestPlan 測試案例

## 實作說明
<!-- 有沒有偏離 Spec 的地方？原因是什麼？ -->

## 關聯項目
- Epic：P1-project #
- SA Issue：P1-analysis #
- SD Issue：P1-design #
- PG Issue：#
```

---

## 八、測試分層定義

| 類型 | 說明 | 工具 | 執行時機 |
|------|------|------|---------|
| 靜態測試（前端） | 程式碼風格與型別檢查 | ESLint、Prettier | 存檔時 |
| 靜態測試（後端） | 程式碼風格檢查 | Ruff | 存檔時 |
| 單元測試 | 測試單一函式邏輯，mock 所有外部依賴 | Pytest | git commit 時 |
| 整合測試 | 測試 API + DB + Schema 完整流程 | Pytest | git commit 時 + CI |
| E2E 測試 | 模擬真實使用者從前端到後端的完整操作 | Playwright | MVP 後補充 |

**testpy 撰寫規則：**
```python
# 每個 test function 需標注對應的 TestPlan ID
def test_create_leave_request(client, db_session, auth_headers):
    """對應 TestPlan issue#5 T1"""
    response = client.post("/api/v1/leaves", json={...}, headers=auth_headers)
    assert response.status_code == 201
    leave = db_session.get(Leave, response.json()["id"])
    assert leave is not None
```
