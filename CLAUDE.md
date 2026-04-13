# 專案架構

P1 由四個 Repo 組成，對應四個開發階段：

| Repo            | 職責                                   | 角色 | Merge 方式          |
| --------------- | ------------------------------------ | -- | ----------------- |
| **P1-project**  | Epic、規範文件                            | PM | 直接 push to main   |
| **P1-analysis** | 商業邏輯分析                                | SA | 直接 merge（無需 PR）   |
| **P1-design**   | Prototype、API Spec、Schema、TDD        | SD | PR + SA/PM Review |
| **P1-code**     | React/TypeScript + Python/FastAPI 實作 | PG | PR + SA/PM Review |

> Repo 結構、Issue 格式、命名規則：[repo-design.md](docs/repo-design.md)

---

## GitHub 物件操作原則

Issue 與分支由 GitHub Actions (workflow) 自動建立，**不手動操作**。自動串接流程：

```
開立Epic issue(epic label)
 └─ 自動建立 SA Issue + SA Branch → SA merge → 
     └─ 自動建立 SD Issue + SD Branch → SD merge → 
         └─ 自動建立 PG Issue + PG Branch → PG merge → 關閉資源 
```

> 如需排查 workflow 請參考：[workflow_guide.md](docs/workflow_guide.md)

---

# 處理特定 SA,SD或PG Issue 時

當人類成員指定處理特定 Issue 時，若Issue類型為:SA,SD或PG(在issue 標題中會標示)，開始實作前：

1. 需要的資訊及相關連結都在 Issue body 之中，請以其中的資訊為主，不要發散，遇到問題詢問人類成員
2. 從 issue body 的「分支」欄位取得 branch 名稱，切換到該 branch 並執行 `git pull`。Branch 由 GitHub Actions 自動建立，**不手動建立**。
3. Commit 格式：`{type}(scope?): 說明`，常用 type：`feat` / `fix` / `docs` / `refactor` / `test` / `chore`
4. 所有文件產出使用繁體中文（zh-TW）
5. 依Issue類型(SA,SD或PG)執行下面對應流程：

---

## SA 流程

###  讀取
1. `business-logic.md` 的 `需求說明` — 預設值為 PM 填寫的需求描述

###  產出
1. `business-logic.md` — 需求說明、商業邏輯、資料模型示意、SD 注意事項、畫面示意

---

## SD 流程

###  讀取
1. `business-logic.md` — 商業邏輯背景（由 SA 填寫）
###  產出

1. **TDD（Technical Design Document）**：包含設計說明與測試案例，作為 PG 實作依據，以 Issue 為單位保存。(文件位置：`TDD/issue-{N}.md`) 
	+ 先填寫「本次工作範圍」表格（類型限定：`Schema`、`API`、`畫面`、`其他`）
	+ 測試案例以 T1、T2... 編號
	+ 每個 API：至少 1 個成功案例（2xx）+ 1 個失敗案例（4xx/5xx）
	+ 每個畫面：至少 1 個主要操作流程的正常案例
	+ 測試案例總數 ≥ 工作範圍項目數
	+ 設計決定只寫結論與理由，不寫曾考慮過的替代方案

 

2. 依TDD 「本次工作範圍」內容調整：`Prototype/`、`Spec/`、`schema/`（如有異動）
	+ **活文件原則：** `Spec/`、`Prototype/`、`schema/` 永遠反映最新狀態，直接修改，不保留舊版。
	

---

## PG 流程

###  讀取
1. `business-logic.md` — 商業邏輯背景（由 SA 填寫）
2. `SpecDiff/issue-{N}.md` — 本次 SD 對 Schema / Spec / Prototype 的變更摘要（由 workflow 及 AI 在 SD merge 後自動寫入）
3. `TDD/issue-{N}.md` — 技術設計說明與測試案例（由 SD 填寫）
4. [TechStack.md](https://github.com/MPinfo-Co/P1-design/blob/main/TechStack.md) — 確認本次相關技術選型

###  產出
1. 實作 code
2. `TestReport/issue-{N}.md` — 填寫測試結果與備註

**pytest 標準：**
- pytest 數量 ≥ TDD 案例數
- 每個 test function 標注對應 TDD ID：

```python
def test_create_user(client, db_session):
    """對應 TDD T1"""
```

- 前端新檔案一律使用 `.tsx`（舊 `.jsx` 漸進式遷移，不強制）

---

> **維護說明：** 正式來源為 `MPinfo-Co/P1-project` 根目錄的 `CLAUDE.md`。
> 各開發者將此內容複製到本機 P1 工作目錄。內容有更動時，兩處同步更新。
> P1-analysis、P1-design、P1-code 不再各自維護 CLAUDE.md。
