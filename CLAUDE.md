# 專案Repo 設計

專案由三個 Repo 組成，對應三個開發階段

| Repo            | 職責                                   | 角色 | Merge 方式          |
| --------------- | ------------------------------------ | -- | ----------------- |
| **P1-project**  | Epic、規範文件                            | PM | 直接 push to main   |
| **P1-design**   | SA 分析 + SD 設計（含 Prototype）           | SA / SD | PR + Review |
| **P1-code**     | React/TypeScript + Python/FastAPI 實作 | PG | PR + SA/PM Review |

> 「Repo 結構細節」，請參考：[repo-design.md](docs/repo-design.md)
> 「workflow細節」或「串接流程」，請參考：[workflow_guide.md](docs/workflow_guide.md)
> 「Issue body內文」，請參考：[issue-body-spec.md](docs/issue-body-spec.md)
> 「自動產生檔案的內文格式」，請參考：[auto-file-format.md](docs/auto-file-format.md)

---
# 專案限制

- Branch 由 GitHub Actions 自動建立，**不手動建立**。
- 所有文件產出使用繁體中文（zh-TW）
- Commit 格式：`{type}(scope?): 說明`，常用 type：`feat` / `fix` / `docs` / `refactor` / `test` / `chore`

---
# 處理特定 SA,SD或PG Issue 時

當人類成員指定處理特定 Issue 時，若Issue類型為:SA,SD或PG(在issue 標題中會標示)，開始實作前：

1. 需要的資訊及相關連結都在 Issue body 之中，請以其中的資訊為主，不要發散，遇到問題詢問人類成員
2. 從 issue body 的「分支」欄位取得 branch 名稱，切換到該 branch 並執行 `git pull`。
3. 依Issue類型(SA,SD或PG)執行下面對應流程：

---

## SA 流程

###  讀取
1. `SA/sa-{N}-logic.md` 的 `需求說明` — 預設值為 PM 填寫的需求描述

###  產出
1. `SA/sa-{N}-logic.md` — 需求說明、商業邏輯、資料模型示意、SD 注意事項、畫面示意

---

## SD 流程

###  讀取
1. `SA/sa-{N}-logic.md` — 商業邏輯背景（由 SA 填寫）
2. `docs/spec-guide.md`（P1-project）— Spec 目錄結構、命名規則、各檔案格式與撰寫規範
3. 依 `SA/sa-{N}-logic.md` 指出的範圍，按需讀取對應的現有 `Spec/`、`schema/`、`Prototype/` 檔案（修改前先讀，非全讀）
4. 若本次涉及修改既有 API 行為，按需讀取對應的 `Spec/{fn_xxx}/Api/_{fn_xxx}_test_api.md`

###  產出

1. **TDD（Technical Design Document）**：工作項目清單，作為 PG 實作依據，以 Issue 為單位保存。(文件位置：`SD/sd-{N}-TDD.md`)
	+ 填寫「工作項目」表格，欄位：`| # | 類型 | 工作內容 | 參照規格 |`（類型限定：`Schema`、`API`、`畫面`、`Test`、`其他`）
	+ 工作內容格式：建立 `{對象}` / 調整 `{對象}：{異動內容}` / 刪除 `{對象}`
	+ 設計決定只寫結論與理由，不寫曾考慮過的替代方案

2. 依 TDD「工作項目」內容調整：`Prototype/`、`Spec/`、`schema/`（如有異動）
	+ **活文件原則：** `Spec/`、`Prototype/`、`schema/` 永遠反映最新狀態，直接修改，不保留舊版。

3. 有 API 新增或修改時，同步更新對應的 `Spec/{fn_xxx}/Api/_{fn_xxx}_test_api.md`（活文件）
	+ 新增 API → 新增測試案例，ID 接續上一筆
	+ 修改 API 行為 → 更新對應測試案例
	+ 刪除 API → 移除對應測試案例，ID 不補號
	+ 若修改影響其他功能的 API（如跨功能改了權限機制），一併更新那些功能的 `_test_api.md`
	

---

## PG 流程

###  讀取
1. `SA/sa-{N}-logic.md` — 商業邏輯背景（由 SA 填寫）
2. `SD/sd-{N}-Diff.md` — 本次 SD 對 Schema / Spec / Prototype 的變更摘要（由 workflow 及 AI 在 SD merge 後自動寫入）
3. `SD/sd-{N}-TDD.md` — 工作項目清單（由 SD 填寫）
4. 依 TDD 工作項目，按需讀取對應的 `Spec/`、`schema/` 檔案及 `Spec/{fn_xxx}/Api/_{fn_xxx}_test_api.md`（非全讀）
5. [techStack.md](https://github.com/MPinfo-Co/P1-project/blob/main/docs/techStack.md) — 確認本次相關技術選型

###  產出
1. 實作 code
2. `TestReport/issue-{N}.md` — 填寫測試結果與備註

**pytest 標準：**
- pytest 數量 ≥ `_test_api.md` 測試案例數
- 每個 test function 標注對應 TestSpec ID：

```python
def test_create_user(client, db_session):
    """對應 T3"""
```

- 前端新檔案一律使用 `.tsx`（舊 `.jsx` 漸進式遷移，不強制）

---

> **維護說明：** 正式來源為 `MPinfo-Co/P1-project` 根目錄的 `CLAUDE.md`。
> 各開發者將此內容複製到本機 P1 工作目錄。內容有更動時，兩處同步更新。
> P1-design、P1-code 不再各自維護 CLAUDE.md。
