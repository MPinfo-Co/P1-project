# P1 開發流程快速上手

> [← 回到總導覽](../../README.md)

> 本文件是新成員的「第一天操作指南」。完整規範請閱讀 [guide.md](guide.md)；Repo 結構與格式規範請閱讀 [repo-design.md](../repo-design.md)。

---

## 我的角色是什麼？

| 我是 | 我在哪個 Repo 工作 | 我的工作起點 |
|------|-----------------|------------|
| PM | P1-project | 開立 Epic Issue |
| SA | P1-analysis | 收到 SA Issue 通知 |
| SD | P1-design | 收到 SD Issue 通知 |
| PG | P1-code | 收到 PG Issue 通知 |

---

## PM：今天要開一個新功能

**1. 開立 Epic Issue**
- 前往 P1-project → Issues → New Issue → 選擇 **Epic** template
- 填寫必填欄位：功能說明、驗收條件
- 送出後，`epic` label 自動套用，P-workflow 自動在 P1-analysis 建立 SA Issue 並建立 A-branch，關聯 Issue 區塊由系統自動回填，**不需手動建立 SA Issue**

**2. 指派 SA**
- 收到 SA PR 開啟通知時，指派審查人員（PM 自己或有經驗的 SA）

**3. 追蹤進度**
- 開啟 GitHub Projects 看板 → **Epic 全覽** view，確認各 Epic 狀態
- 有 `blocked` 標籤的 Issue 需優先處理

**⚠️ 常見卡關：** Epic 開立後若 15 分鐘內未在 P1-analysis 看到 SA Issue，代表 P-workflow 失敗。參考 workflow.md 第六節「P-workflow 應急方案」手動建立。

## PM：今天有行政事務要記錄

**1. 開立 Chore Issue**
- 前往 P1-project → Issues → New Issue → 選擇 **Chore（PM 行政事務）** template
- 選擇類型（學習 / 文件 / 環境維護 / 其他），填寫說明與完成條件
- 送出後手動追蹤，**不會觸發任何自動化流程**

**2. 完成後**
- 手動關閉 Issue

---

## SA：今天收到一個 SA Issue

**1. 確認任務**
- 開啟收到的 SA Issue，閱讀「功能說明」與「關聯 Epic」
- 到 P1-project 對應的 Epic Issue 看「驗收條件」，理解商業目標

**2. Pull 分支，開始撰寫**
```bash
git fetch origin
git checkout -b issue-{N}-{slug} origin/issue-{N}-{slug}
# 若本地已有該分支：git checkout issue-{N}-{slug}
```
- 在 `issue-{N}/` 資料夾建立兩份文件：
  - `business-logic.md`（Use Case、流程圖、ER 示意等，格式自由）
  - `SD-WBS.md`（SD 需要做什麼的工作清單，**必須用表格格式 + 類型標記**）

**3. Commit 與 Push**
```bash
git add .
git commit -m "docs(issue-{N}): 完成請假申請 SA 分析"
# ↑ 格式必須是 type(scope): 說明（P1-code 有 commitlint 自動強制，其他 Repo 靠自覺）
git push origin issue-{N}-{slug}
```

**4. 確認 Draft PR（系統自動開立）**
- 系統在 A-Branch 建立後自動開立 Draft PR，PR body 已預填 Epic 編號、SA Issue 編號與 `Closes #N`
- SA 只需 push commits；完成後把 Draft 轉成 **Ready for Review**，在 PR 留言 @PM 請求審查

**5. Merge 後**
- 手動在 P1-analysis 的 `README.md` 新增一行 Issue 索引
  ```markdown
  | #4 | 請假申請 | 請假、leave | P1-project #1 | 2026-03-01 |
  ```
- SA Issue 自動關閉；系統自動在 P1-design 建立 SD Issue + D-Branch，SA 工作完成

**⚠️ 常見卡關：**
- commitlint 格式錯誤：最常見的是忘記小括號 scope，或說明用中文但格式符號不對。正確格式：`feat(leaves): 說明`
- SD-WBS.md 格式不合：確保有 `| # | 類型 | 說明 |` 表頭，類型限定 `Schema`、`API`、`畫面`、`其他`

---

## SD：今天收到一個 SD Issue

**1. 確認任務**
- 開啟收到的 SD Issue，查看「設計範圍」（自動從 SD-WBS.md 複製過來的工作項目）
- 如有疑問，直接在 SD Issue 留言 @SA

**2. 確認有無衝突**
- 查看 P1-design 的 open Issues，確認有無其他 SD Issue 在修改相同的 Spec 文件或 Schema.md
- 若有，先在雙方 Issue 留言協調修改範圍

**3. Pull 分支，開始設計**
```bash
git fetch origin
git checkout -b issue-{N}-{slug} origin/issue-{N}-{slug}
# 若本地已有該分支：git checkout issue-{N}-{slug}
```
- 修改 `Prototype/` 下的 HTML 原型（活文件，直接改最新版）
- 修改 `Spec/` 下的 API/畫面規格文件（活文件，直接改最新版）
- 若有 Schema 異動，修改 `Schema.md`

**4. 撰寫 TestPlan**
- 建立 `TestPlan/issue-{N}.md`（系統會自動填入修改的檔案清單，你只需填測試案例）
- 最低要求：每個 API 至少一個成功案例（2xx）+ 一個失敗案例（4xx/5xx）；每個畫面至少一個主流程案例
- 測試案例數量不得少於 SD-WBS.md 工作項目數（硬性要求，審查時會驗收）

**5. 確認 Draft PR（系統自動開立）**
- D-Branch 建立時系統自動開立 Draft PR，body 已預填 Epic、SA Issue、SD Issue 編號與 `Closes #N`
- SD 只需 push commits；完成後把 Draft 轉成 **Ready for Review**（同 SA 流程）

**⚠️ 常見卡關：**
- TestPlan 忘記填：這是審查必查項目，PR checklist 上有，別跳過
- Schema.md 衝突：修改 Schema 前先在 Issue 留言標記「Schema.md 異動：預計異動的 Table」

---

## PG：今天收到一個 PG Issue

**1. 確認任務**
- 開啟 PG Issue，查看「實作範圍」（系統自動填入 SD 異動的 Spec 清單）
- 按照 Issue 中的關聯鏈，逐一讀取必要資訊：

| 我要知道什麼 | 去哪裡找 |
|------------|---------|
| 要做什麼 | PG Issue body「實作範圍」 |
| API 規格 | `P1-design/Spec/{異動文件}` |
| 畫面規格 | `P1-design/Prototype/{異動文件}` |
| 這次改了什麼（delta） | `P1-design/TestPlan/issue-{SD#}-diff.md` |
| 商業邏輯背景 | `P1-analysis/issue-{SA#}/business-logic.md` |
| 測試標準 | `P1-design/TestPlan/issue-{SD#}.md` |

**2. 確認 Draft PR（系統自動開立）**
- C-Branch 建立時系統自動開立 Draft PR，body 已預填完整關聯鏈（Epic→SA→SD→PG）與 `Closes #N`

**3. 環境準備（首次，僅需執行一次）**

詳見 [P1-code/SETUP.md](https://github.com/MPinfo-Co/P1-code/blob/main/SETUP.md)，摘要：
```bash
pip install -r backend/requirements.txt
pip install pre-commit
cd frontend && npm install   # 自動啟用 husky git hooks
```

**4. Pull 分支，開始實作**
```bash
git fetch origin
git checkout -b issue-{N}-{slug} origin/issue-{N}-{slug}
# 若本地已有該分支：git checkout issue-{N}-{slug}
```

**5. 撰寫程式碼與測試**
- 依 Spec 實作（前端 React/TypeScript，後端 Python/FastAPI）
- 依 TestPlan 撰寫 pytest 測試，每個 test function 標注對應的 TestPlan ID：
  ```python
  def test_create_leave_request(client, db_session, auth_headers):
      """對應 TestPlan issue-5 T1"""
      ...
  ```
- pytest test function 數量 ≥ TestPlan 案例數

**6. Push，等待 CI**
```bash
git push origin issue-{N}-{slug}
# CI 自動執行：
# - Python：ruff lint + ruff format check + pytest（含 coverage）
# - 前端：ESLint + Prettier check
```
- CI 通過後把 Draft PR 轉成 **Ready for Review**，指派 2 位審查人
- CI 失敗：修正後重新 push；第 3 次仍失敗則在 Issue 留言 @SD @PM

**7. PR 審查與 Merge**
- Merge 後系統自動產生 VersionDiff 文件，PG Issue 自動關閉

**⚠️ 常見卡關：**
- CI 失敗最常見原因：測試案例 import 錯誤、環境變數未設定、Spec 描述與實作不符
- pytest test function 數量不足：TestPlan 有幾個案例，就要有至少幾個 test function
- Draft PR 未轉 Ready：CI 通過後記得把 Draft 狀態改成 Ready for Review，否則無法 merge

---

## Commit Message 格式速查

```
{type}({scope}): {說明}
```

| Type | 什麼時候用 |
|------|---------|
| `feat` | 新功能 |
| `fix` | 修復 bug |
| `docs` | 只改文件 |
| `refactor` | 重構（沒改功能） |
| `test` | 新增或修改測試 |
| `chore` | 設定、建置相關 |

**範例：**
```
feat(leaves): 新增請假申請 API
docs(issue-4): 完成 SA 分析文件
test(leaves): 新增 POST /api/leaves 整合測試
```

> commitlint 在 P1-code 的每次 commit 時自動驗證格式（其他 Repo 靠自覺遵守）。不符合的 commit 會被擋下，修改 message 後重新 commit 即可（不需強制 push）。

---

## 跨 Repo Issue 編號速查

四個 Repo 各有獨立的 Issue 編號，`issue-4` 在不同 Repo 代表不同 Issue。

**跨 Repo 溝通時，加上前綴：**
- `A-issue-4`：P1-analysis Issue #4（SA）
- `D-issue-5`：P1-design Issue #5（SD）
- `C-issue-7`：P1-code Issue #7（PG）

---

## 第一個 Issue 建議

1. 先確認自己的角色對應的 Repo 有被 assign 存取權限
2. 由有經驗的同角色成員（或 PM）陪同走一遍：pull 分支 → 撰寫文件/程式碼 → commit → push → 開 PR → 審查 → merge
3. 走過一遍後，日後的流程基本相同，只是內容不同

> 若無同角色資深成員可陪同，由 PM 擔任引導人。任何卡關直接在對應 Issue 留言，不要卡超過半天才問。
