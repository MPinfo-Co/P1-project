# 開發工作流程

## 流程總覽

| 階段 | 負責人 | Repo | 觸發條件 | 產出 |
|------|--------|------|---------|------|
| 工作分派 | PM | P1-analysis | PM 手動開立 Issue | A-Branch 建立 |
| 系統分析 | SA | P1-analysis | A-Branch 建立後 | 商業邏輯文件、SD WBS |
| 系統設計 | SD | P1-design | SA merge 後自動觸發 | Spec、Prototype、TestPlan |
| 系統開發 | PG | P1-code | SD merge 後自動觸發 | 程式碼、測試、VersionDiff |

**關鍵原則：下游分支在上游 merge 後才建立，確保 PG 永遠依據最新規格開發。**

---

## 一、工作分派（PM）

```
PM 在 P1-analysis 使用 Issue 範本開立 Issue
    └─ 觸發 A-workflow
        ├─ 自動建立 A-Branch（issue-{N}-{slug}）
        └─ 自動 assign SA
PM 手動 assign Issue 給 SA
```

**若需要拆分 Issue：**
```
SA 在 P1-analysis 手動開立子 Issue
    └─ 觸發相同 A-workflow 流程
PM 手動 assign 新 Issue
```

**Issue 範本欄位（P1-analysis）：**
- 功能名稱
- 背景說明（為什麼需要這個功能）
- 驗收條件

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
   ├─ 在 P1-design 開立 Sub Issue（關聯 SA Issue）
   └─ 在 Sub Issue 留言通知 SD：「SA 分析完成，請開始系統設計」
```

**審查優先順序：PM > SA > Self**

---

## 三、系統設計（SD）

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
   ├─ 在 P1-code 開立 Sub Issue（關聯 SD Issue）
   └─ 在 Sub Issue 留言通知 PG：
      「SD 設計完成，以下文件已異動，請參考」
      附上異動的 Spec/Prototype 清單
```

**審查優先順序：SA > PM > Self**

---

## 四、系統開發（PG）

```
1. PG 在 Local Pull C-Branch
   （C-Repo Issue 已有 SD 異動清單，直接對照開發）
2. PG 依據異動的 Spec/Prototype 修改前後端程式碼
3. PG 依據 TestPlan 撰寫或修改 pytest 測試程式碼
   規則：testpy 測試項目數 >= TestPlan 測試案例數
         每個 test function 需標注對應的 TestPlan ID
4. PG 確認本地測試通過：
   ├─ 前端靜態測試：ESLint、Prettier（存檔時自動執行）
   ├─ 後端靜態測試：Ruff（存檔時自動執行）
   └─ 後端動態測試：Pytest（git commit 時自動執行）
5. PG Push C-Branch
   └─ 觸發 CI：GitHub Actions 執行自動化測試
6. 若 CI 通過，PG 開 Pull Request
   └─ 填寫 PR template（見 PR 規範）
   └─ 觸發自動部署測試環境
7. SD 指派審查人員 2 人
8. 審查人員在測試環境確認：
   ├─ Code Review
   ├─ 操作功能驗證
   └─ 美術排版及文字確認
9. 審查人員在 PR 留言記錄測試步驟
10. Merge

Merge 後自動觸發：
   └─ 自動產生 VersionDiff/issue#{N}_{作者}_{日期}.md
```

**審查優先順序：SD > SA > PM > Self**

---

## 五、GitHub Actions 自動化說明

### A-workflow（P1-analysis）

| 觸發條件 | 動作 |
|---------|------|
| Issue opened | 建立 `issue-{N}-{slug}` A-Branch |
| A-Branch merge to main | 在 P1-design 建立 D-Branch + 開立 Sub Issue + 留言通知 SD |

### D-workflow（P1-design）

| 觸發條件 | 動作 |
|---------|------|
| D-Branch merge to main | 比對 diff 寫入 TestPlan 修改項目 |
| D-Branch merge to main | 在 P1-code 建立 C-Branch + 開立 Sub Issue + 留言通知 PG（附異動清單） |

### C-workflow（P1-code）

| 觸發條件 | 動作 |
|---------|------|
| Push to C-Branch | 執行 CI：pytest + ESLint + Ruff |
| PR opened | 自動部署測試環境 |
| C-Branch merge to main | 自動產生 VersionDiff 文件 |

---

## 六、PR 規範

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
- SA Issue：#
```

### P1-design PR template

```markdown
## 設計完整度確認
- [ ] Prototype 已更新
- [ ] Spec 文件已更新
- [ ] TestPlan 測試案例已填寫

## 設計決策說明
<!-- 有哪些設計選擇？為什麼這樣決定？ -->

## 對 PG 的影響
<!-- PG 實作時需要特別注意什麼？ -->

## 關聯項目
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
- SA Issue：P1-analysis #
- SD Issue：P1-design #
- PG Issue：#
```

---

## 七、測試分層定義

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
    """對應 TestPlan issue#4 T1"""
    response = client.post("/api/v1/leaves", json={...}, headers=auth_headers)
    assert response.status_code == 201
    leave = db_session.get(Leave, response.json()["id"])
    assert leave is not None
```
