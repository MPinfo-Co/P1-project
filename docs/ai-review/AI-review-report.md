# AI 文件審查報告

## 2026-04-23 18:15 (v27)

#### P1-project（審查 9 份文件，2 份有問題）

**repo-design.md**：
- **[待處理]** P1-design 目錄結構樹狀圖未列出 `spec-guide.md`。該檔案位於 P1-design 根目錄，是 Spec 撰寫規範的重要文件，應補入樹狀圖。（事實差異）

**AI-review-doclist.md**：
- **[待處理]** `spec-guide.md` 的連結使用本機相對路徑 `(../../../P1-design/spec-guide.md)`，而同表其他跨 Repo 文件（techStack.md、functionList.md、SETUP.md）均使用 GitHub 絕對 URL。此相對路徑在 GitHub 頁面無法正確導航，應改為 `https://github.com/MPinfo-Co/P1-design/blob/main/spec-guide.md` 以維持一致性。（優化建議）

#### P1-design（審查 3 份文件，1 份有問題）

**spec-guide.md**：
- **[待處理]** 目錄結構樹狀圖使用 `{fn_功能}/` 作為目錄佔位符，暗示所有功能目錄帶有 `fn_` 前綴，但命名規則表已正確記載為 `{功能編號}`（範例含 `fn_user/` 和 `auth/`）。樹狀圖應改為 `{功能編號}/` 以與下方命名規則表一致。（事實差異，續自 v26——命名規則表已修正，僅剩樹狀圖未同步更新）

#### P1-code（審查 1 份文件，0 份有問題）

### 摘要
> 本次審查 13 份文件，發現 3 份有問題。

（v26 的 2 項問題已解決：project-board-guide.md WIP 數字已統一為 2 個；FunctionList.md「km」對應目錄已從 `Spec/kb/` 修正為 `Spec/km/`。）

### 未發現問題的文件
> 以下 10 份文件未發現問題：README.md、CLAUDE.md、workflow_guide.md、issue-body-spec.md、auto-file-format.md、project-board-guide.md、techStack.md、FunctionList.md、SETUP.md、AI-review-prompt.md。

---

## 2026-04-22 18:04 (v26)

#### P1-project（審查 9 份文件，1 份有問題）

**project-board-guide.md**：
- **[待處理]** Status 表格記載 In progress「上限 2 個」，但 WIP 原則記載「同時 In progress 不超過 3 個，控制在2個之內」，同一文件內上限數字不一致（2 vs 3），應統一。（事實差異，續自 v25）

#### P1-design（審查 3 份文件，2 份有問題）

**spec-guide.md**：
- **[待處理]** 命名規則表的功能目錄規則寫 `fn_{功能}`（範例 `fn_user/`），但實際 Spec 目錄中 `auth/`、`expert/`、`home/`、`kb/`、`partner/`、`framework/` 均無 `fn_` 前綴，且 FunctionList.md 規定「目錄名稱 = 功能編號」。命名規則表應改為 `{功能編號}` 以符合實際慣例。（事實差異）

**FunctionList.md**：
- **[待處理]** 功能清單的功能欄位「km」與 Spec 實際目錄名稱 `Spec/kb/` 不一致。文件規定「目錄名稱 = 功能編號」，兩者應統一。（事實差異，續自 v25）

#### P1-code（審查 1 份文件，0 份有問題）

### 摘要
> 本次審查 13 份文件，發現 3 份有問題。

### 未發現問題的文件
> 以下 10 份文件未發現問題：README.md、CLAUDE.md、workflow_guide.md、issue-body-spec.md、auto-file-format.md、repo-design.md、TechStack.md、SETUP.md、AI-review-prompt.md、AI-review-doclist.md。

---

## 2026-04-21 18:07 (v25)

#### P1-project（審查 9 份文件，1 份有問題）

**project-board-guide.md**：
- **[待處理]** Status 表格記載 In progress「上限 2 個」，但 WIP 原則記載「同時 In progress 不超過 3 個，控制在2個之內」，同一文件內上限數字不一致（2 vs 3），應統一。（事實差異，續自 v24）

#### P1-design（審查 2 份文件，1 份有問題）

**FunctionList.md**：
- **[待處理]** 功能清單的功能欄位「km」與 Spec 實際目錄名稱 `Spec/kb/` 不一致。文件規定「目錄名稱 = 功能編號」，兩者應統一。（事實差異，續自 v24）

#### P1-code（審查 1 份文件，0 份有問題）

### 摘要
> 本次審查 12 份文件，發現 2 份有問題。

### 未發現問題的文件
> 以下 10 份文件未發現問題：README.md、CLAUDE.md、workflow_guide.md、issue-body-spec.md、auto-file-format.md、repo-design.md、TechStack.md、SETUP.md、AI-review-prompt.md、AI-review-doclist.md。

（補充：v24 列出的 FunctionList.md「user」對應目錄 `Spec/f_user/` 問題為誤判——功能編號為 `fn_user`，對應目錄 `Spec/fn_user/` 一致，僅 `km`/`kb` 差異仍存在。）
