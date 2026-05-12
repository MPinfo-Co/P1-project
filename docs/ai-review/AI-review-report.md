# AI 文件審查報告

## 2026-05-12 18:04 (v43)

#### doclist 完整性缺口
- 無（所有 14 份文件均存在）

#### P1-project（審查 13 份文件，4 份有問題）

**README.md**：
- **[待處理]** 「重要文件索引」表格缺少 spec-guide.md，其餘非 AI-review 的 doclist 文件均已列出，應補上。（優化，續自 v40）

**setup.md**：
- **[待處理]** 第 139 行「每次 push 到 `pg-*` branch 或開 PR 時，CI 自動執行」，但 `wf_pg_ci.yml` 觸發條件僅有 `push` 到 `pg-*` branch，無 `pull_request` 觸發，「或開 PR 時」應刪除。（事實差異，續自 v39）

**techStack.md**：
- **[待處理]** 「排程與非同步任務」section 列 Celery + Celery Beat，但 requirements.txt 無 celery 套件，後端實際使用 APScheduler（`APScheduler==3.11.2`），應將 Celery / Celery Beat 改為 APScheduler。（事實差異）
- **[待處理]** 「資料庫 & 基礎設施」section 列 Redis（Celery Broker），但 requirements.txt 無 redis 套件且後端程式碼未使用 Redis，應移除或改列為「規劃中」。（事實差異）

**CLAUDE.md**：
- **[待處理]** Repo 總覽表格 P1-design 職責欄寫「SA 分析 + SD 設計（含 sdPrototype）」，但 repo-design.md 同一表格為「SA 分析 + SD 設計（含 sdPrototype / sdSpec）」，且 `P1-design/SD/sdSpec/` 確實存在，應補上「/ sdSpec」。（事實差異，續自 v39）
- **[待處理]** 「工作所需檔案路徑」表格列 `schema.md` → `P1-design/SD/schema.md`，但該路徑不存在，實際檔案為 `P1-design/SD/model.md`（repo-design.md 目錄樹亦記為 `model.md`）。SD 流程、PG 流程中所有 `schema.md` 引用均應改為 `model.md`。（事實差異）

#### P1-design（審查 1 份文件，1 份有問題）

**functionList.md**：
- **[待處理]** fn_navbar 功能名稱為「頂端導覽列」，但功能說明寫「左側功能導覽列」，兩者指稱不同 UI 區域（頂端 ≠ 左側），描述矛盾。（優化，續自 v39）

### 摘要
> 本次審查 14 份文件，發現 5 份有問題。

（v42 的 4 項問題均維持；新增 2 項：techStack.md 排程工具與 Redis 聲明與實際不符、CLAUDE.md schema.md 路徑已改為 model.md。）

### 未發現問題的文件
> 以下 9 份文件未發現問題：repo-design.md、workflow_guide.md、issue-body-spec.md、auto-file-format.md、spec-guide.md、coding-rule-backend.md、coding-rule-frontend.md、AI-review-prompt.md、AI-review-doclist.md。

---

## 2026-05-10 18:08 (v42)

#### doclist 完整性缺口
- 無（所有 14 份文件均存在）

#### P1-project（審查 13 份文件，3 份有問題）

**README.md**：
- **[待處理]** 「重要文件索引」表格缺少 spec-guide.md，其餘非 AI-review 的 doclist 文件均已列出，應補上。（優化，續自 v40）

**setup.md**：
- **[待處理]** 第 139 行「每次 push 到 `pg-*` branch 或開 PR 時，CI 自動執行」，但 `wf_pg_ci.yml` 觸發條件僅有 `push` 到 `pg-*` branch，無 `pull_request` 觸發，「或開 PR 時」應刪除。（事實差異，續自 v39）

**CLAUDE.md**：
- **[待處理]** Repo 總覽表格 P1-design 職責欄寫「SA 分析 + SD 設計（含 sdPrototype）」，但 repo-design.md 同一表格為「SA 分析 + SD 設計（含 sdPrototype / sdSpec）」，且 `P1-design/SD/sdSpec/` 確實存在，應補上「/ sdSpec」。（事實差異，續自 v39）

#### P1-design（審查 1 份文件，1 份有問題）

**functionList.md**：
- **[待處理]** fn_navbar 功能名稱為「頂端導覽列」，但功能說明寫「左側功能導覽列」，兩者指稱不同 UI 區域（頂端 ≠ 左側），描述矛盾。（優化，續自 v39）

### 摘要
> 本次審查 14 份文件，發現 4 份有問題。

（v41 的 4 項問題均維持：README.md 重要文件索引缺少 spec-guide.md、setup.md CI 觸發條件、CLAUDE.md P1-design 職責描述缺少 sdSpec、functionList.md fn_navbar 名稱與說明矛盾。無新增問題。）

### 未發現問題的文件
> 以下 10 份文件未發現問題：repo-design.md、workflow_guide.md、techStack.md、issue-body-spec.md、auto-file-format.md、spec-guide.md、coding-rule-backend.md、coding-rule-frontend.md、AI-review-prompt.md、AI-review-doclist.md。

---

## 2026-05-09 18:10 (v41)

#### doclist 完整性缺口
- 無（所有 14 份文件均存在）

#### P1-project（審查 13 份文件，3 份有問題）

**README.md**：
- **[待處理]** 「重要文件索引」表格缺少 spec-guide.md，其餘非 AI-review 的 doclist 文件均已列出，應補上。（優化，續自 v40）

**setup.md**：
- **[待處理]** 第 139 行「每次 push 到 `pg-*` branch 或開 PR 時，CI 自動執行」，但 `wf_pg_ci.yml` 觸發條件僅有 `push` 到 `pg-*` branch，無 `pull_request` 觸發，「或開 PR 時」應刪除。（事實差異，續自 v39）

**CLAUDE.md**：
- **[待處理]** Repo 總覽表格 P1-design 職責欄寫「SA 分析 + SD 設計（含 sdPrototype）」，但 repo-design.md 同一表格為「SA 分析 + SD 設計（含 sdPrototype / sdSpec）」，且 `P1-design/SD/sdSpec/` 確實存在，應補上「/ sdSpec」。（事實差異，續自 v39）
- v40 指出 SD 流程類型限定「Schema」應為「Model」，本版確認第 77 行已修正為 `Model`，與 auto-file-format.md 及 coding-rule-backend.md 一致，已解決。

#### P1-design（審查 1 份文件，1 份有問題）

**functionList.md**：
- **[待處理]** fn_navbar 功能名稱為「頂端導覽列」，但功能說明寫「左側功能導覽列」，兩者指稱不同 UI 區域（頂端 ≠ 左側），描述矛盾。（優化，續自 v39）

### 摘要
> 本次審查 14 份文件，發現 4 份有問題。

（v40 的 5 項問題中，CLAUDE.md TDD 類型限定 Schema→Model 已解決；其餘 4 項維持：README.md 重要文件索引缺少 spec-guide.md、setup.md CI 觸發條件、CLAUDE.md P1-design 職責描述缺少 sdSpec、functionList.md fn_navbar 名稱與說明矛盾。）

### 未發現問題的文件
> 以下 10 份文件未發現問題：repo-design.md、workflow_guide.md、techStack.md、issue-body-spec.md、auto-file-format.md、spec-guide.md、coding-rule-backend.md、coding-rule-frontend.md、AI-review-prompt.md、AI-review-doclist.md。
