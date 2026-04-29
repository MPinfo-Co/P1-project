# AI 文件審查報告

## 2026-04-29 18:14 (v31)

#### doclist 完整性缺口
- 無（所有 14 份文件均存在）

#### P1-project（審查 12 份文件，7 份有問題）

**README.md**：
- **[待處理]** 重要文件索引中 SETUP.md（第 19 行）連結指向 `P1-code/SETUP.md`（GitHub 絕對 URL），但該檔案不存在。開發環境準備指引實際位於 `P1-project/docs/setup.md`，應更正 Repo 與路徑。（事實差異）

**issue-body-spec.md**：
- **[待處理]** SA / SD / PG Issue body 分別標示由 `p-workflow.yml`、`a-workflow.yml`、`d-workflow.yml` 產生，但這三個 workflow 檔案已不存在（已改名）。實際檔案為 `wf_epic_to_sa.yml`（P1-project）、`wf_sa_to_sd.yml`（P1-design）、`wf_sd_to_pg.yml`（P1-design）。檔案名稱與 GitHub 連結皆須更新。（事實差異，續自 v30）

**repo-design.md**：
- **[待處理]** P1-project 目錄結構樹狀圖未列出 `coding-rule-backend.md`、`coding-rule-frontend.md`、`setup.md`。這三份檔案已存在且被 README.md 索引或審查清單收錄，應補入樹狀圖。（事實差異，續自 v30 擴充）

**spec-guide.md**：
- **[待處理]** 目錄結構樹狀圖使用 `{fn_功能}/` 作為目錄佔位符，暗示所有功能目錄帶有 `fn_` 前綴，但命名規則表已正確記載為 `{功能編號}`（範例含 `fn_user/` 和 `auth/`）。樹狀圖應改為 `{功能編號}/` 以與下方命名規則表一致。（事實差異，續自 v30）

**setup.md**：
- **[待處理]** 第 139 行「每次 push 到 `issue-*` branch 或開 PR 時，CI 自動執行」，但 `wf_pg_ci.yml` 實際觸發條件為 push 到 `pg-*` branch，應更正分支 pattern。（事實差異）

**AI-review-doclist.md**：
- **[待處理]** `setup.md` 連結使用同 Repo（P1-project）的 GitHub 絕對 URL `https://github.com/MPinfo-Co/P1-project/blob/main/docs/setup.md`，同表其他 P1-project 文件均使用本機相對路徑，應改為 `../setup.md` 以維持一致性。（優化建議）

**coding-rule-frontend.md**：
- **[待處理]** 「二、架構規則」章節序號不連續且順序錯誤：2-1 → 2-2 → 2-3 → 2-5 → 2-6 → 2-4。Section 2-4「Token 取得方式」排在 2-6 之後，應重新編號或調整順序。（優化）

#### P1-design（審查 2 份文件，1 份有問題）

**functionList.md**：
- **[待處理]** 功能清單中功能編號 `auth` 與 Spec 實際目錄名稱 `Spec/fn_auth/` 不一致（目錄內檔案亦使用 `fn_auth` 前綴，如 `fn_auth_00_overview.md`）。文件規定「目錄名稱 = 功能編號」，兩者應統一。（事實差異，續自 v30）

### 摘要
> 本次審查 14 份文件，發現 8 份有問題。

（v30 的 9 項問題中 4 項已解決：CLAUDE.md Repo 數量已改為「三個」與表格一致、auto-file-format.md workflow 名稱已更新為正確檔名、AI-review-doclist.md 所列 coding-rule-backend.md 已建立、techStack.md React Query 已安裝於 package.json。README.md 原 coding-rule-backend.md 連結問題亦隨檔案建立而解決。本次新增 3 項：README.md SETUP.md 連結指向不存在的 P1-code 路徑、setup.md CI 分支 pattern 錯誤、coding-rule-frontend.md 章節序號不連續。AI-review-doclist.md 新增 1 項同 Repo 絕對 URL 優化建議。repo-design.md 問題擴充為 3 份缺失檔案。）

### 未發現問題的文件
> 以下 6 份文件未發現問題：CLAUDE.md、workflow_guide.md、auto-file-format.md、techStack.md、AI-review-prompt.md、coding-rule-backend.md。

---

## 2026-04-26 18:07 (v30)

#### doclist 完整性缺口
- `P1-project/docs/coding-rule-backend.md`：列於審查清單但檔案不存在，本次略過

#### P1-project（審查 10 份文件，7 份有問題）

**README.md**：
- **[待處理]** 重要文件索引連結 `docs/coding-rule-backend.md`（第 22 行）指向不存在的檔案，連結無法導航。（事實差異）

**CLAUDE.md**：
- **[待處理]** 開頭敘述「專案由四個 Repo 組成」，但下方 Repo 總覽表格僅列 3 個 Repo（P1-project、P1-design、P1-code），未包含 P1-analysis。數量與表格不符，應補入 P1-analysis 或修正數量描述。（事實差異，續自 v29）

**issue-body-spec.md**：
- **[待處理]** SA / SD / PG Issue body 分別標示由 `p-workflow.yml`、`a-workflow.yml`、`d-workflow.yml` 產生，但這三個 workflow 檔案已不存在（已改名）。實際檔案為 `wf_epic_to_sa.yml`（P1-project）、`wf_sa_to_sd.yml`（P1-design）、`wf_sd_to_pg.yml`（P1-design）。檔案名稱與 GitHub 連結皆須更新。（事實差異，續自 v29）

**auto-file-format.md**：
- **[待處理]** 與 issue-body-spec.md 同一問題：`sa-{N}-logic.md`、`sd-{N}-TDD.md`、`TestReport/issue-{N}.md`、`sd-{N}-Diff.md` 各節標示的產生來源 workflow 均引用已不存在的舊檔名（`p-workflow.yml`、`a-workflow.yml`、`d-workflow.yml`），應更新為實際 workflow 檔案名稱。（事實差異，續自 v29）

**repo-design.md**：
- **[待處理]** P1-project 目錄結構樹狀圖未列出 `coding-rule-frontend.md`。該檔案已存在且被 README.md 索引與審查清單收錄，應補入樹狀圖。（事實差異）

**spec-guide.md**：
- **[待處理]** 目錄結構樹狀圖使用 `{fn_功能}/` 作為目錄佔位符，暗示所有功能目錄帶有 `fn_` 前綴，但命名規則表已正確記載為 `{功能編號}`（範例含 `fn_user/` 和 `auth/`）。樹狀圖應改為 `{功能編號}/` 以與下方命名規則表一致。（事實差異，續自 v29）

**AI-review-doclist.md**：
- **[待處理]** 清單列出 `docs/coding-rule-backend.md` 但該檔案不存在，應建立檔案或從清單移除。（事實差異）

#### P1-design（審查 2 份文件，2 份有問題）

**techStack.md**：
- **[待處理]** 前端技術棧列出 React Query 為 Server State 管理工具，但 `P1-code/frontend/package.json` 的 dependencies 中未包含 `@tanstack/react-query`。應安裝該套件或在文件中標註為「規劃中」。（事實差異）

**functionList.md**：
- **[待處理]** 功能清單中功能編號 `auth` 與 Spec 實際目錄名稱 `Spec/fn_auth/` 不一致（目錄內檔案亦使用 `fn_auth` 前綴，如 `fn_auth_00_overview.md`）。文件規定「目錄名稱 = 功能編號」，兩者應統一。（事實差異，續自 v29）

#### P1-code（審查 1 份文件，0 份有問題）

### 摘要
> 本次審查 13 份文件，發現 9 份有問題。

（v29 的 6 項問題中 1 項已解決：AI-review-doclist.md spec-guide.md 連結已更新為正確的本機相對路徑。其餘 5 項延續。本次新增 4 項：README.md 連結指向不存在的 coding-rule-backend.md、repo-design.md 樹狀圖缺少 coding-rule-frontend.md、AI-review-doclist.md 列出不存在的 coding-rule-backend.md、techStack.md React Query 未安裝。）

### 未發現問題的文件
> 以下 4 份文件未發現問題：workflow_guide.md、AI-review-prompt.md、coding-rule-frontend.md、SETUP.md。

---

## 2026-04-25 18:16 (v29)

#### P1-project（審查 8 份文件，4 份有問題）

**CLAUDE.md**：
- **[待處理]** 開頭敘述「專案由四個 Repo 組成」，但下方 Repo 總覽表格僅列 3 個 Repo（P1-project、P1-design、P1-code），未包含 P1-analysis。數量與表格不符，應補入 P1-analysis 或修正數量描述。（事實差異）

**issue-body-spec.md**：
- **[待處理]** SA / SD / PG Issue body 分別標示由 `p-workflow.yml`、`a-workflow.yml`、`d-workflow.yml` 產生，但這三個 workflow 檔案已不存在（已改名）。實際檔案為 `wf_epic_to_sa.yml`（P1-project）、`wf_sa_to_sd.yml`（P1-design）、`wf_sd_to_pg.yml`（P1-design）。檔案名稱與 GitHub 連結皆須更新。（事實差異）

**auto-file-format.md**：
- **[待處理]** 與 issue-body-spec.md 同一問題：`sa-{N}-logic.md`、`sd-{N}-TDD.md`、`TestReport/issue-{N}.md`、`sd-{N}-Diff.md` 各節標示的產生來源 workflow 均引用已不存在的舊檔名（`p-workflow.yml`、`a-workflow.yml`、`d-workflow.yml`），應更新為實際 workflow 檔案名稱。（事實差異）

**AI-review-doclist.md**：
- **[待處理]** `spec-guide.md` 的連結使用本機相對路徑 `(../../../P1-design/spec-guide.md)`，而同表其他跨 Repo 文件（techStack.md、functionList.md、SETUP.md）均使用 GitHub 絕對 URL。此相對路徑在 GitHub 頁面無法正確導航，應改為 `https://github.com/MPinfo-Co/P1-design/blob/main/spec-guide.md` 以維持一致性。（優化建議，續自 v28）

#### P1-design（審查 3 份文件，2 份有問題）

**spec-guide.md**：
- **[待處理]** 目錄結構樹狀圖使用 `{fn_功能}/` 作為目錄佔位符，暗示所有功能目錄帶有 `fn_` 前綴，但命名規則表已正確記載為 `{功能編號}`（範例含 `fn_user/` 和 `auth/`）。樹狀圖應改為 `{功能編號}/` 以與下方命名規則表一致。（事實差異，續自 v28）

**functionList.md**：
- **[待處理]** 功能清單中功能編號 `auth` 與 Spec 實際目錄名稱 `Spec/fn_auth/` 不一致（目錄內檔案亦使用 `fn_auth` 前綴，如 `fn_auth_00_overview.md`）。文件規定「目錄名稱 = 功能編號」，兩者應統一。（事實差異，續自 v28）

#### P1-code（審查 1 份文件，0 份有問題）

### 摘要
> 本次審查 12 份文件，發現 6 份有問題。

（v28 的 3 項問題均未解決，續列於本次報告。本次新增 3 項事實差異：CLAUDE.md Repo 數量與表格不符、issue-body-spec.md 及 auto-file-format.md workflow 檔案名稱過時。）

### 未發現問題的文件
> 以下 6 份文件未發現問題：README.md、workflow_guide.md、repo-design.md、techStack.md、SETUP.md、AI-review-prompt.md。
