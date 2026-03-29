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

## 按角色快速跳轉

| 我是 | 我需要看哪一節 |
|------|-------------|
| PM | [第一節：工作分派](#一工作分派pm)、[第五節：PM 介入機制](#五pm-介入與中斷機制) |
| SA | [第二節：系統分析](#二系統分析sa) |
| SD | [第三節：系統設計](#三系統設計sd)（含活文件衝突、Schema 衝突、拆分） |
| PG／AI | [第四節：系統開發](#四系統開發pgai)（含 AI 資訊讀取指引） |
| 所有人 | [第七節：PR 規範](#七pr-規範)、[第九節：例外處理](#九例外處理)（Hotfix、需求變更、CI 失敗…） |

> **新成員**：建議先讀 [quick-start.md](quick-start.md) 按步驟操作，遇到細節再回來查對應章節。

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
   ├─ 自動比對 diff，產生 TestPlan/issue#{N}_diff.md（修改項目 + 關聯項目）
   ├─ 在 P1-code 建立 C-Branch
   ├─ 在 P1-code 開立 PG Issue（關聯 Epic + SA + SD Issue，附異動 Spec 清單）
   ├─ 在 PG Issue 留言通知 PG：「SD 設計完成，以下文件已異動，請參考」
   └─ 更新 Epic Issue：填入 PG Issue 編號
```

**審查優先順序：SA > PM > Self**

> **規模化補充：** 多個 SD Issue 並行時，SA 可預先指定備援 SD 審查人，避免 SA 成為單點瓶頸（與第二節 PM 授權機制相同）。

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
   規則：pytest 測試項目數 >= TestPlan 測試案例數
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

### Token 權限說明

本流程跨越四個 Repo，大量自動化操作需要存取非當前 Repo 的資源（如在 P1-analysis 的 workflow 建立 P1-design 的 Issue）。以下說明兩種可行方案及其限制：

| 方案 | 說明 | 限制 |
|------|------|------|
| **PAT（Personal Access Token）** | 由特定成員產生，授予跨 Repo 的 `repo` 權限，以 GitHub Secret 儲存於各 Repo | 與個人帳號綁定，人員異動時需更換；若帳號被停用 token 立即失效 |
| **GitHub App Token** | 建立專屬 GitHub App，授予組織層級特定權限，workflow 中用 `actions/create-github-app-token` 取得短效 token | 需要建立與維護 GitHub App；設定較複雜，但權限範圍更精確，適合長期維護 |

**建議：** MVP 階段使用 **PAT**（快速可用）；人員穩定後遷移至 **GitHub App Token**（安全性更高）。無論使用哪種方案，token 均以 **Org-level Secret** 集中管理，各 Repo workflow 直接引用，避免重複設定。

> 跨 Repo 操作（P-workflow、A-workflow、D-workflow 的 Issue/Branch 建立）均屬「中等難度」，需在環境設定 token 後才能運作。CI 測試（C-workflow Push）屬「簡單」，使用預設的 `GITHUB_TOKEN` 即可。

---

### 自動化項目總覽（難度 × 優先級）

| Workflow | 觸發條件 | 動作 | 難度 | 優先級 |
|----------|---------|------|------|--------|
| P-workflow | Epic Issue opened | 在 P1-analysis 建立 SA Issue + A-Branch，自動 assign | 中等（跨 Repo） | P0 關鍵路徑 |
| A-workflow | A-Branch PR opened | 在 Epic Issue 留言通知 PM：「SA PR 已開啟，請指派審查人員」 | 中等（跨 Repo） | P2 錦上添花 |
| A-workflow | A-Branch merge to main | 在 P1-design 建立 SD Issue + D-Branch，通知 SD，更新 Epic | 中等（跨 Repo） | P0 關鍵路徑 |
| A-workflow | A-Branch merge to main | 解析 SD-WBS.md，將工作項目複製至 SD Issue「設計範圍」欄位 | 複雜（需解析文件內容） | P1 重要 |
| D-workflow | D-Branch merge to main | 比對 diff，自動寫入 TestPlan 修改項目，產生 `_diff.md` | 複雜（需解析 diff + 文件內容） | P1 重要 |
| D-workflow | D-Branch merge to main | 在 P1-code 建立 PG Issue + C-Branch，附異動清單，通知 PG，更新 Epic | 中等（跨 Repo） | P0 關鍵路徑 |
| D-workflow（SD 拆分時） | SD 手動開立新 SD Issue | 在 Epic Issue 留言通知 PM | 中等（跨 Repo） | P2 錦上添花 |
| C-workflow | Push to C-Branch | 執行 CI：pytest + ESLint + Ruff | 簡單（單一 Repo） | P0 關鍵路徑 |
| C-workflow | PR opened | 自動部署測試環境 | 複雜（需部署基礎設施） | P1 重要 |
| C-workflow | C-Branch merge to main | 自動產生 VersionDiff 文件 | 簡單（單一 Repo） | P1 重要 |
| C-workflow | C-Branch merge to main | 檢查 Epic 下所有 PG Issue 是否均已 merge，若是則通知 PM | 中等（跨 Repo + 狀態查詢） | P1 重要 |

---

### P0 關鍵路徑說明

以下自動化若未實作，**下游流程將無法啟動，人工替代成本極高**：

1. **P-workflow：Epic → SA Issue + A-Branch 建立**
   - 若未自動化：PM 需手動到 P1-analysis 建立 Issue 並建立 Branch，流程起點即為手動，容易遺漏且格式不一致。
   - 應急方案（見下節）。

2. **A-workflow：A-Branch merge → SD Issue + D-Branch 建立**
   - 若未自動化：SA merge 後無任何通知，SD 不知道何時可以開始，C-Branch 也無從建立。
   - 應急方案（見下節）。

3. **D-workflow：D-Branch merge → PG Issue + C-Branch 建立**
   - 若未自動化：SD merge 後 PG 無法取得任何任務，整個開發流程中斷。
   - 應急方案（見下節）。

4. **C-workflow：Push to C-Branch → CI 執行**
   - 若未自動化：程式碼品質無法自動驗證，需完全依賴人工 Code Review，合併風險大幅提高。
   - 應急方案（見下節）。

---

### P1 重要項目說明

以下自動化**省時省力，但人工替代成本可接受**。建議在 P0 關鍵路徑完成後實作：

- A-workflow：WBS 複製至 SD Issue body（複雜，文件解析）
- D-workflow：比對 diff 寫入 TestPlan + 產生 _diff.md（複雜，git diff 解析）
- D-workflow：附異動 Spec 清單至 PG Issue（中等，跨 Repo）
- C-workflow：自動產生 VersionDiff 文件（中等，解析 git log）
- C-workflow：PR opened → 自動部署測試環境（複雜，需雲端整合）

---

### P2 錦上添花說明

以下自動化若未實作，**流程仍可靠人工完成，但較麻煩**：

1. **A-workflow：PR opened → 通知 PM 指派審查人**
   - 未自動化時：SA 手動在 PR 留言 @PM，或 PM 設定 GitHub 通知訂閱 P1-analysis Repo 的 PR 事件。

2. **D-workflow（SD 拆分）：新 SD Issue → 通知 PM**
   - 未自動化時：SD 手動在 Epic Issue 留言通知 PM，成本極低。

---

### P-workflow（P1-project）

| 觸發條件 | 動作 | 難度 | 優先級 |
|---------|------|------|--------|
| Epic Issue opened | 在 P1-analysis 建立 SA Issue + A-Branch，自動 assign | 中等（跨 Repo，需 PAT/App Token） | P0 |

**應急方案（P-workflow 失敗時）：**
1. PM 手動至 P1-analysis 依 Epic Issue 內容開立 SA Issue，標題格式：`[{Epic編號}] {功能名稱}`，body 貼上 Epic 連結
2. PM 手動建立 A-Branch：`issue-{SA#}-{slug}`
3. PM 手動 assign SA
4. PM 在 Epic Issue 留言記錄：「自動化失敗，已手動建立 SA Issue #{N}，A-Branch: issue-{N}-{slug}」

---

### A-workflow（P1-analysis）

| 觸發條件 | 動作 | 難度 | 優先級 |
|---------|------|------|--------|
| A-Branch PR opened | 在 Epic Issue 留言通知 PM：「SA PR 已開啟，請指派審查人員」 | 中等（跨 Repo） | P2 |
| A-Branch merge to main | 在 P1-design 建立 SD Issue + D-Branch，通知 SD，更新 Epic | 中等（跨 Repo） | P0 |
| A-Branch merge to main | 解析 SD-WBS.md，將工作項目複製至 SD Issue「設計範圍」欄位 | 複雜（文件解析） | P1 |

**應急方案（A-workflow 失敗時）：**

*PR 通知失敗（P2，影響低）：*
- SA 手動在 PR 留言 @PM，說明「SA PR 已開啟，請指派審查人員」

*SA merge 後跨 Repo 建立失敗（P0，影響高）：*
1. SA 手動至 P1-design 開立 SD Issue，標題格式：`[SD] {功能名稱}`，body 填入：
   ```
   - 父 Epic：P1-project #{Epic#}
   - SA Issue：P1-analysis #{SA#}
   - 設計範圍：（貼上 SD-WBS.md 的工作項目清單）
   ```
2. SA 手動建立 D-Branch：`issue-{SD#}-{slug}`
3. SA 在 SD Issue 留言：「SA 分析完成，請開始系統設計」，@SD
4. SA 在 Epic Issue 留言更新 SD Issue 編號

*SD-WBS.md 複製失敗（P1，影響中）：*
- SA 手動開啟已建立的 SD Issue，將 SD-WBS.md 的工作項目清單貼入「設計範圍」欄位

---

### D-workflow（P1-design）

| 觸發條件 | 動作 | 難度 | 優先級 |
|---------|------|------|--------|
| D-Branch merge to main | 比對 diff，自動寫入 TestPlan 修改項目，產生 `TestPlan/issue#{N}_diff.md` | 複雜（diff 解析 + 文件寫入） | P1 |
| D-Branch merge to main | 在 P1-code 建立 PG Issue + C-Branch，附異動清單，通知 PG，更新 Epic | 中等（跨 Repo） | P0 |

**應急方案（D-workflow 失敗時）：**

*diff 寫入 TestPlan 失敗（P1，影響中）：*
1. SD 手動執行 `git diff main...{D-Branch}` 取得異動清單
2. SD 手動在 `TestPlan/issue#{N}.md` 補充修改項目欄位
3. SD 手動建立 `TestPlan/issue#{N}_diff.md`，貼入異動清單

*跨 Repo 建立 PG Issue + C-Branch 失敗（P0，影響高）：*
1. SD 手動至 P1-code 開立 PG Issue，標題格式：`[PG] {功能名稱}`，body 填入：
   ```
   - 父 Epic：P1-project #{Epic#}
   - SA Issue：P1-analysis #{SA#}
   - SD Issue：P1-design #{SD#}
   - 實作範圍：（貼上異動 Spec 清單，格式見 AI 自主實作資訊讀取指引）
   ```
2. SD 手動建立 C-Branch：`issue-{PG#}-{slug}`
3. SD 在 PG Issue 留言：「SD 設計完成，以下文件已異動，請參考」，@PG，附異動清單
4. SD 在 Epic Issue 留言更新 PG Issue 編號

---

### C-workflow（P1-code）

| 觸發條件 | 動作 | 難度 | 優先級 |
|---------|------|------|--------|
| Push to C-Branch | 執行 CI：pytest + ESLint + Ruff | 簡單（單一 Repo，用預設 GITHUB_TOKEN） | P0 |
| PR opened | 自動部署測試環境 | 複雜（需部署基礎設施，與雲端環境綁定） | P1 |
| C-Branch merge to main | 自動產生 VersionDiff 文件 | 簡單（單一 Repo） | P1 |
| C-Branch merge to main | 檢查 Epic 下所有 PG Issue 均已 merge，通知 PM | 中等（跨 Repo 狀態查詢） | P1 |

**應急方案（C-workflow 失敗時）：**

*CI 失敗（P0，影響高）：*
- 依 9.3 CI 持續失敗處理規則操作（第 1～2 次自行修正，第 3 次 @SD + @PM）
- CI 若因 workflow 設定錯誤（非程式碼問題）導致無法執行：人類 PG 需在本地執行 `pytest`、`eslint`、`ruff` 並在 PR 留言附上本地測試結果截圖，PM 授權後可人工確認合規

*測試環境部署失敗（P1，影響中）：*
- 審查人員在本地啟動測試環境（`docker compose up` 或對應指令），在本地執行功能驗證
- 審查人員在 PR 留言說明：「自動部署失敗，已於本地環境完成功能驗證」

*VersionDiff 產生失敗（P1，影響中）：*
- PG 手動建立 `VersionDiff/issue#{PG#}_{作者}_{日期}.md`，依 diff 內容填寫異動摘要
- PG 在 PG Issue 留言說明已手動產生 VersionDiff

*Epic 完成通知失敗（P1，影響中）：*
- PG 完成最後一個 PG Issue merge 後，手動至 Epic Issue 留言：「所有 PG Issue 已完成，請 PM 驗收後關閉 Epic」，@PM

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
- [ ] pytest 覆蓋所有 TestPlan 測試案例

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

**pytest 撰寫規則：**
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
