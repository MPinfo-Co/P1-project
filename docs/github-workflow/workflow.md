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

> **規模化補充：** 當同時有多個 SA Issue 進行中時，PM 可預先授權指定 SA 成員擔任常設審查人（不需每次通知 PM 指派），以避免 PM 成為審查瓶頸。授權方式：PM 在 P1-project 以 Issue 或 Discussion 記錄授權清單，例如「SA Issue 審查：優先由 SA-A 擔任，PM 退為備援」。

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
3. **預防原則**：SD 開始設計前，先查看 P1-design 的 open Issues 清單，確認有無其他進行中的 SD Issue 修改相同文件；若有，在各自的 SD Issue 留言協調修改範圍，避免重疊

### Schema.md 衝突處理（特殊規則）

`Schema.md` 是整個系統的資料庫全覽，結構牽一髮動全身，衝突風險高於一般 Spec 文件。

**預防原則（開始設計前）：**
- SD 開始 Schema 變更前，在自己的 SD Issue 留言標記「Schema.md 異動」，列出預計新增／修改的 Table 名稱
- 若同期有其他 SD Issue 也標記了 Schema.md 異動，雙方 SD 需先留言協調（確認 Table 範圍不重疊，或約定修改順序）
- 若異動範圍有重疊（例如兩個 Issue 都要修改 User Table），需在 SD Issue 留言確認最終欄位清單，統一由一方處理

**解衝突規則（Merge 時）：**
- 後 merge 的 D-Branch 在 PR 留言說明：衝突的 Table 名稱、衝突原因、解決方式（保留哪些欄位、刪除哪些）
- Schema 衝突解決後，審查人員需確認最終 Schema 與對應 Spec 文件的 API / 畫面描述一致（無孤立欄位、無缺失欄位）

> Schema.md 異動影響範圍廣，建議多個 Epic 同時進行時，由 PM 在 Sprint 規劃階段確認各 Epic 的 Schema 影響範圍，提前識別衝突點。

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

### AI 自主實作資訊讀取指引

AI 接到 PG Issue 後，依下表逐項取得所需資訊：

| 需求 | 來源 | 路徑 |
|------|------|------|
| 要做什麼（設計範圍） | PG Issue body「實作範圍」欄位 | 系統自動填入 SD 異動 Spec 清單 |
| 怎麼做（API 規格） | P1-design Spec/ 活文件（當前最新狀態） | `P1-design/Spec/{異動文件}` |
| 怎麼做（畫面規格） | P1-design Prototype/ 活文件（當前最新狀態） | `P1-design/Prototype/{異動文件}` |
| 本次改了什麼（delta） | SD TestPlan diff | `P1-design/TestPlan/issue#{SD#}_diff.md` |
| 為什麼（商業邏輯背景） | SA 商業邏輯說明文件 | `P1-analysis/issue#{SA#}/商業邏輯說明.md` |
| 現有程式碼狀態 | VersionDiff（最近一筆） | `P1-code/VersionDiff/`（依日期取最新）|
| 測試標準 | SD TestPlan 測試案例 | `P1-design/TestPlan/issue#{SD#}.md` |

> **注意：Spec/ 是活文件，永遠反映最新狀態。** AI 應讀 Spec/ 的完整文件，而非只看 diff，以掌握現有程式碼應對應的完整規格。

> **第一個 Issue 無 VersionDiff 的情況：** 若 `P1-code/VersionDiff/` 尚無任何檔案，代表這是初始實作，AI 應直接依據 Spec/ 全量實作，無需參考歷史 diff。

```
1. PG／AI 取得 C-Branch（AI 透過 GitHub API 讀取；人類 PG 在 Local Pull）
   （PG Issue body 已有 SD 異動 Spec 清單與完整關聯鏈）
2. PG／AI 依上表讀取所有必要資訊
3. 依據 Spec/Prototype（活文件當前狀態）修改前後端程式碼
4. 依據 TestPlan 撰寫或修改 pytest 測試程式碼
   規則：testpy 測試項目數 >= TestPlan 測試案例數
         每個 test function 需標注對應的 TestPlan ID
5. Push C-Branch
   └─ 觸發 CI：GitHub Actions 執行自動化測試（pytest + ESLint + Ruff）
   【人類 PG】在 push 前可於本地執行靜態測試（ESLint、Ruff）與動態測試（pytest）
   【AI PG】無本地執行環境，push 後等待 CI 結果；若 CI 失敗則修正後重新 push
6. 若 CI 通過，開 Pull Request
   ├─ 填寫 PR template（見 PR 規範）
   └─ 觸發自動部署測試環境
7. SD 指派審查人員 2 人（一人負責 Code Review，一人負責功能驗證）
8. 審查人員在測試環境確認：
   ├─ Code Review
   ├─ 操作功能驗證
   └─ 美術排版及文字確認
9. 審查人員在 PR 留言記錄測試步驟
10. Merge

Merge 後自動觸發：
   ├─ 自動產生 VersionDiff/issue#{N}_{作者}_{日期}.md
   └─ 若 Epic 下所有 PG Issue 均已 merge，在 Epic Issue 留言通知 PM：「所有 PG Issue 已完成，請驗收後關閉 Epic」

PM 收到通知後：
   ├─ 確認測試環境符合驗收條件（對照 Epic 中的 Given/When/Then）
   └─ 驗收通過則手動關閉 Epic；若有問題則開立新 Issue 描述缺陷
```

**審查優先順序：SD > SA > PM > Self**

---

### PG 發現 TestPlan 問題的處理路徑

PG／AI 在實作過程中若發現 TestPlan 有下列問題：
- 測試案例描述模糊，無法對應程式行為
- 缺少關鍵邊界條件（如空值、上限值、權限異常）
- 測試案例與 Spec 描述矛盾

**處理方式：**
1. 在 PG Issue 留言，描述問題點（附上 TestPlan ID 與具體疑問），@SD
2. SD 須在 1 個工作天內回覆（補充說明或修正 TestPlan）
3. 若需修正 TestPlan，SD 開立新 Branch 更新 `TestPlan/issue#{N}.md` 並 merge，不重開 SD Issue
4. PG 確認 TestPlan 更新後繼續實作

> 在等待 SD 回覆期間，PG 可先實作確定部分，待 TestPlan 釐清後補齊對應測試。

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
| D-Branch merge to main | 比對 diff 寫入 TestPlan 修改項目，並產生 `TestPlan/issue#{N}_diff.md` 供 PG 參考 |
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
- [ ] TestPlan 測試案例已填寫（每個 API 至少正常案例（2xx）+ 錯誤案例（4xx/5xx），每個畫面至少一個主流程案例）

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
- [ ] CI 自動化測試通過（必填）
- [ ] 本地 Pytest 通過（人類 PG 填寫；AI PG 無本地環境，此項留空）
- [ ] testpy 覆蓋所有 TestPlan 測試案例

## 實作說明
<!-- 1. 有沒有偏離 Spec 的地方？原因是什麼？（主動偏離需說明） -->
<!-- 2. 實作過程中是否發現 Spec 本身有誤或描述不清？若有，請說明發現的問題及本次如何處理，並在 SD Issue 留言通知 SD 修正 Spec -->

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

---

## 九、例外處理

### 9.1 Hotfix（線上緊急 bug）

Hotfix 需要跳過 SA/SD 直接修程式碼，不走正常的 Epic 流程。

**觸發條件：** 線上環境出現影響用戶使用的緊急 bug，無法等待下個 Sprint 修復。

**處理流程：**

```
1. PM 在 P1-project 開立 Hotfix Issue（標題加上 [HOTFIX] 前綴，優先順序標 P0）
2. PG 直接從 P1-code main branch 開立 hotfix-{N}-{slug} 分支
3. PG 修復 bug 並 push，CI 自動執行
4. CI 通過後開 PR，指定 PM 或 SA 至少 1 人審查（不需 SD 審查）
5. 審查通過後 merge
6. Merge 後 24 小時內，PG 需在 Hotfix Issue 留言補充說明：
   - 根本原因（Root Cause）
   - 修改了哪些程式碼
   - 是否需要後續修正 SA/SD 文件（若有，開立對應 Issue 處理）
```

> Hotfix 是緊急例外，不產生完整的 SA/SD 文件，但事後補充 Root Cause 說明是必要的，以便後續維護。

---

### 9.2 需求變更（SA 已 merge，SD 進行中）

第五節「PM 介入與中斷機制」涵蓋退回與中斷 Epic，但未說明「SA 已 merge 後需求改變」的完整處置。

**處理流程：**

```
1. PM 在 Epic Issue 加上 `blocked` 標籤，留言說明需求變更的內容與範圍
2. SD 收到通知後，在進行中的 SD Issue 加上 `blocked` 標籤，暫停設計，不 push 也不開 PR
3. PM 評估變更範圍：
   ├─ 小幅調整（僅補充說明）：PM 直接在 SA Issue 留言，SA 開新 Issue 補充分析文件
   └─ 大幅變更（需求根本改變）：PM 關閉現有 SD Issue，重走 SA 流程（開新 Epic 或新 SA Issue）
4. SA 補充/修正文件並 merge 後，PM 移除 Epic Issue 的 `blocked` 標籤
5. PM 移除 Epic Issue 的 `blocked` 標籤後，SD 須在 1 個工作天內回報進度評估，保留可用部分後繼續設計
```

> 關鍵原則：SD Issue 的 `blocked` 標籤由 SD 加、由 PM 確認需求穩定後指示 SD 移除。

---

### 9.3 CI 持續失敗

第四節提到「若 CI 失敗則修正後重新 push」，但未定義重試上限與升級機制。

**處理規則：**

| 狀態 | 行動 |
|------|------|
| CI 失敗第 1～2 次 | PG 自行診斷修正，重新 push |
| CI 失敗第 3 次 | PG 在 PG Issue 留言說明失敗原因與已嘗試的修正方式，@SD 確認是否 Spec 問題，@PM 告知進度 |
| CI 失敗超過 3 個工作天仍未解決 | PM 介入，決定是否調整需求、請 SA/SD 協助、或暫時標記 `blocked` |

> CI 失敗的根本原因通常是：測試案例與實作不符（TestPlan 問題）、環境設定問題、或 Spec 描述有誤。第 3 次失敗時應優先確認根本原因而非繼續盲目重試。

---

### 9.4 審查人員不可用

**備案原則：** 任何 PR 指定審查人員後，若 1 個工作天內無回應，按以下優先順序尋找備援：

| 階段 | 主要審查順序 | 備援順序 |
|------|------------|---------|
| SA PR | PM > SA > Self | SA 備援 → PM 代審 |
| SD PR | SA > PM > Self | PM 代審 |
| PG PR | SD > SA > PM > Self | SA 代審 → PM 代審 |

**操作步驟：**

```
1. PR 開立後 1 個工作天內無審查回應
2. PR 開立者在 PR 留言 @備援審查人，說明原指定審查人不可用
3. 備援審查人接手審查
4. 若所有可用人員均無法在 2 個工作天內審查，PM 決定是否暫時標記 PR 為 `on-hold`

> **關於「Self」審查**：主要審查順序中「Self」為最後手段，僅在所有其他審查人均不可用時由 PM 授權使用。
```

---

### 9.5 錯誤的 merge（半成品 merge 進 main）

**誰有權限執行回滾：** 只有 PM 可以授權執行回滾操作；PG 執行，SA/SD 確認影響範圍。

**處理流程：**

```
1. 發現錯誤 merge 後，立即在該 PR 留言標記問題，@PM 說明情況
2. PM 確認影響範圍（是否已觸發下游自動化、是否影響線上環境）
3. PM 授權後，PG 執行 Revert：
   git revert -m 1 <merge-commit-hash>
   （使用 revert 而非 reset，保留歷史記錄）
4. PG 將 revert commit push 並開 PR，由 PM 審查後 merge
5. 若自動化已觸發並建立了下游 Issue/Branch，PM 手動關閉這些 Issue 並刪除對應 Branch
6. 在原 Issue 留言記錄：發生原因、影響範圍、回滾操作時間
```

> 禁止使用 `git reset --hard` 直接修改 main 的歷史，必須使用 `git revert` 以保留完整記錄。

---

### 9.6 跨 Issue 相依（PG Issue A 依賴 PG Issue B）

SD 拆分章節說明拆分後「可平行開發」，但未處理有相依關係的情境。

**相依關係的識別與宣告：**

SD 在建立 PG Issue 時，若發現兩個 Issue 存在相依關係，需在 Issue body 明確標註：

```
## 相依關係
- 本 Issue 依賴：P1-code #{N}（原因：需要 #{N} 的 Schema 變更先 merge）
- 預計可開始實作時間：#{N} merge 後
```

**處理流程：**

```
前置 Issue（被依賴的 Issue B）：
1. 正常開發，完成後 merge

後置 Issue（依賴 Issue A）：
1. 在 PG Issue A 加上 `blocked` 標籤，等待 Issue B merge
2. Issue B merge 後，PG 確認相依已滿足，在 PG Issue A 留言通知 PM，由 PM 確認後移除 `blocked` 標籤
3. PG 在開始 Issue A 前先 pull 最新 main，確保 C-Branch 包含 Issue B 的變更
4. 若 C-Branch 建立時間早於 Issue B 的 merge，需先 rebase C-Branch：
   git rebase main
   解決衝突後繼續開發
```

> 若相依關係在 SD 階段未被識別、到 PG 階段才發現，PG 在 PG Issue 留言說明相依關係，@SD 確認後由 SD 補標相依資訊，流程同上。
