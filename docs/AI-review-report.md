# AI 文件審查報告

## 2026-04-08 15:11 (v10)

### 建議修改清單

| # | 來源 | 修改類型 | 風險 | 修改標的 | 位置 | 建議修改內容 |
|---|------|---------|------|---------|------|------------|
| 1 | v10 | 事實差異 | 中 | [P1-design/TechStack.md](https://github.com/MPinfo-Co/P1-design/blob/main/TechStack.md) | 程式語言章節（L5） | `**TypeScript**（前端語言，React 生態主流）` 改為 `**JavaScript**（前端語言）`。package.json 無 typescript 相依、無 tsconfig.json（僅 jsconfig.json）、`frontend/src/` 完全為 `.js/.jsx`。TechStack.md 是技術棧權威文件，錯誤會誤導 SD／PG |
| 2 | v10 | 事實差異 | 中 | [P1-design/TechStack.md](https://github.com/MPinfo-Co/P1-design/blob/main/TechStack.md) | 前端章節（L11、L14、L15） | 移除未實際使用的條目：`Tailwind CSS v3`、`TanStack Query`、`Axios`。package.json 無對應依賴、`frontend/src/` 無任何引用；實際 CSS/UI 為 `MUI + Emotion`，無 HTTP client 套件（可能尚未導入）|
| 3 | v10 | 事實差異 | 低 | [P1-code/README.md](https://github.com/MPinfo-Co/P1-code/blob/main/README.md) | 目錄結構 frontend 行（L20） | `React 19 + Vite + JavaScript + Tailwind CSS` 改為 `React 19 + Vite + JavaScript + MUI`（與 #2 同步，實際使用 MUI + Emotion，非 Tailwind）|
| 4 | v10 | 優化 | 低 | [P1-project/docs/workflow/quick-start.md](https://github.com/MPinfo-Co/P1-project/blob/main/docs/workflow/quick-start.md) | 同檔內不一致：Commit 格式速查區塊（L194-214）vs SA 常見卡關（L86）| L86 稱「正確格式：`feat(leaves): 說明`」含 scope，但 L197 與 L211 的格式速查寫 `{type}: 工作說明` 無 scope，且範例亦無 scope。建議速查與範例統一為 `{type}({scope}): 說明`，與 L86 以及 P1-code/CLAUDE.md、P1-analysis/CLAUDE.md、P1-design/CLAUDE.md 一致 |
| 5 | v2 | 事實差異 | 低 | [P1-project/README.md](https://github.com/MPinfo-Co/P1-project/blob/main/README.md) | 四個 Repo 表格 P1-code 列（L22） | `React/TypeScript` 改為 `React/JavaScript`（package.json 僅含 `.js/.jsx`，無 TypeScript 相依） |
| 6 | v2 | 事實差異 | 低 | [P1-project/docs/workflow/quick-start.md](https://github.com/MPinfo-Co/P1-project/blob/main/docs/workflow/quick-start.md) | PG 第 5 步「撰寫程式碼與測試」（L165） | `前端 React/TypeScript `.tsx`` 改為 `前端 React/JavaScript `.jsx`` |
| 7 | v7 | 優化 | 低 | [P1-code/SETUP.md](https://github.com/MPinfo-Co/P1-code/blob/main/SETUP.md) | 第 5 節「範例格式」（L49）與範例（L51-54） | `` `{type}: 工作說明` `` 改為 `` `{type}({scope}): 說明` ``，範例同步加上 scope，與 P1-code/CLAUDE.md、P1-analysis/CLAUDE.md、P1-design/CLAUDE.md 一致 |

### 摘要
> 本次審查 23 份文件，發現 5 份有問題，共 7 項建議修改（本輪新增 4 項；v9 共 5 項中解決 2 項〔repo-design.md 補 CLAUDE.md、repo-design.md frontend 標註 React+JavaScript〕，3 項持續未解決）。

### 未發現問題的文件
> 以下 18 份文件未發現問題：P1-project/CLAUDE.md、repo-design.md、guide.md、quick-start.md 之外的 workflow 文件（p-workflow.md、a-workflow.md、d-workflow.md、c-workflow.md、chore-workflow.md、project-board-guide.md）、AI-review-prompt.md、AI-review-gap-prompt.md、AI-review-doclist.md、P1-analysis/README.md、P1-analysis/CLAUDE.md、P1-design/README.md、P1-design/CLAUDE.md、FunctionList.md、P1-code/CLAUDE.md。

### Doclist 完整性提醒
- `P1-code/SYSTEM.md` — 存在且 P1-code/CLAUDE.md 明確導引至此（完整系統架構、資料流、SSB 整合、事件合併機制），建議納入審查清單（延續 v7/v8/v9 提醒）
- `P1-code/frontend/README.md` 與 `P1-code/backend/README.md` — 被 P1-code/README.md L28 明確引用為「詳細說明」入口，但未納入審查清單，建議評估是否納入

---

## 2026-04-08（v9）

### 建議修改清單

| # | 來源 | 修改類型 | 風險 | 修改標的 | 位置 | 建議修改內容 |
|---|------|---------|------|---------|------|------------|
| 1 | v8 | 事實差異 | 低 | [P1-project/docs/repo-design.md](https://github.com/MPinfo-Co/P1-project/blob/main/docs/repo-design.md) | P1-project 目錄樹（約 L20-33） | 在 `README.md` 下方補上 `CLAUDE.md` 一行（此樹目前未列出實際存在的 CLAUDE.md；v8 #4 同時提出的 PRD.md 經核對並不存在，該部分應從建議中移除） |
| 2 | v2 | 事實差異 | 低 | [P1-project/README.md](https://github.com/MPinfo-Co/P1-project/blob/main/README.md) | 四個 Repo 表格 P1-code 列（L22） | `React/TypeScript` 改為 `React/JavaScript`（package.json 僅含 `.js/.jsx`，無 TypeScript 相依） |
| 3 | v2 | 事實差異 | 低 | [P1-project/docs/workflow/quick-start.md](https://github.com/MPinfo-Co/P1-project/blob/main/docs/workflow/quick-start.md) | PG 第 5 步「撰寫程式碼與測試」（L165） | `前端 React/TypeScript `.tsx`` 改為 `前端 React/JavaScript `.jsx`` |
| 4 | v2 | 事實差異 | 低 | [P1-project/docs/repo-design.md](https://github.com/MPinfo-Co/P1-project/blob/main/docs/repo-design.md) | P1-code 目錄樹 frontend/ 標註（L227） | `← React + TypeScript` 改為 `← React + JavaScript` |
| 5 | v7 | 事實差異 | 低 | [P1-code/SETUP.md](https://github.com/MPinfo-Co/P1-code/blob/main/SETUP.md) | 第 5 節「範例格式」行（L49） | `` `{type}: 工作說明` `` 改為 `` `{type}({scope}): 說明` ``，範例同步加上 scope（與 P1-project/CLAUDE.md、quick-start.md 一致） |

### 摘要
> 本次審查 23 份文件，發現 4 份有問題，共 5 項建議修改（本輪新增 0 項；v8 共 12 項中解決 7 項，5 項持續未解決）。

### 未發現問題的文件
> P1-project/CLAUDE.md、guide.md、project-board-guide.md、p-workflow.md、a-workflow.md、d-workflow.md、c-workflow.md、chore-workflow.md、AI-review-prompt.md、AI-review-gap-prompt.md、AI-review-doclist.md、P1-analysis/README.md、P1-analysis/CLAUDE.md、P1-design/README.md、P1-design/CLAUDE.md、TechStack.md、FunctionList.md、P1-code/README.md、P1-code/CLAUDE.md（共 19 份）

### Doclist 完整性提醒
- `P1-code/SYSTEM.md` — 實際存在且 P1-code/CLAUDE.md 明確導引至此（完整系統架構、資料流、SSB 整合），建議納入審查清單（延續 v7/v8 提醒）
- v8 曾提醒 `PRD.md`，本輪經檔案系統比對確認 P1-project 根目錄並無此檔案，該提醒應撤除

---

## 2026-04-08（v8）

### 建議修改清單

| # | 來源 | 修改類型 | 風險 | 修改標的 | 位置 | 建議修改內容 |
|---|------|---------|------|---------|------|------------|
| 1 | v8 | 事實差異 | 低 | [P1-project/CLAUDE.md](https://github.com/MPinfo-Co/P1-project/blob/main/CLAUDE.md) | P1-project 目錄樹 | 移除 `AI-CONTEXT.md` 一行（檔案不存在） |
| 2 | v8 | 事實差異 | 低 | [P1-project/CLAUDE.md](https://github.com/MPinfo-Co/P1-project/blob/main/CLAUDE.md) | P1-code 目錄樹 | 移除根目錄 `tests/` 一行（目錄不存在） |
| 3 | v8 | 事實差異 | 中 | [P1-project/docs/repo-design.md](https://github.com/MPinfo-Co/P1-project/blob/main/docs/repo-design.md) | P1-analysis 目錄樹 | 補上 `references/` 目錄（存在且含 10+ 重要參考文件） |
| 4 | v8 | 事實差異 | 低 | [P1-project/docs/repo-design.md](https://github.com/MPinfo-Co/P1-project/blob/main/docs/repo-design.md) | P1-project 目錄樹 | 補上 `CLAUDE.md` 與 `PRD.md` |
| 5 | v8 | 事實差異 | 低 | [P1-project/docs/repo-design.md](https://github.com/MPinfo-Co/P1-project/blob/main/docs/repo-design.md) | P1-code 目錄樹 | 移除根目錄 `tests/` 與 `docs/` 兩行（均不存在） |
| 6 | v8 | 事實差異 | 低 | [P1-project/docs/repo-design.md](https://github.com/MPinfo-Co/P1-project/blob/main/docs/repo-design.md) | VersionDiff 格式範例 | `LeavePage.tsx` 改為 `LeavePage.jsx` |
| 7 | v8 | 事實差異 | 低 | [P1-project/docs/workflow/spec/c-workflow.md](https://github.com/MPinfo-Co/P1-project/blob/main/docs/workflow/spec/c-workflow.md) | backend-ci 說明 | 移除「根目錄 `tests/` 整合測試不在 CI 執行範圍」（目錄已不存在） |
| 8 | v7 | 事實差異 | 低 | [P1-analysis/README.md](https://github.com/MPinfo-Co/P1-analysis/blob/main/README.md) | 流程圖第 4 行 | `（PG／AI` 補上閉括號 → `（PG／AI）` |
| 9 | v7 | 優化 | 低 | [P1-code/SETUP.md](https://github.com/MPinfo-Co/P1-code/blob/main/SETUP.md) | 第 5 節「範例格式」行 | `` `{type}: 工作說明` `` 改為 `` `{type}({scope}): 說明` `` |
| 10 | v2 | 事實差異 | 低 | [P1-project/README.md](https://github.com/MPinfo-Co/P1-project/blob/main/README.md) | 四個 Repo 表格 P1-code 列 | `React/TypeScript` 改為 `React/JavaScript` |
| 11 | v2 | 事實差異 | 低 | [P1-project/docs/workflow/quick-start.md](https://github.com/MPinfo-Co/P1-project/blob/main/docs/workflow/quick-start.md) | PG 第 5 步「撰寫程式碼與測試」 | `React/TypeScript .tsx` 改為 `React/JavaScript .jsx` |
| 12 | v2 | 事實差異 | 低 | [P1-project/docs/repo-design.md](https://github.com/MPinfo-Co/P1-project/blob/main/docs/repo-design.md) | P1-code 目錄樹 `frontend/` 標註 | `React + TypeScript` 改為 `React + JavaScript` |

### 摘要
> 本次審查 23 份文件，發現 6 份有問題，共 12 項建議修改（新增 7 項，舊有 5 項持續未解決）。

### 未發現問題的文件
> guide.md、project-board-guide.md、p-workflow.md、a-workflow.md、d-workflow.md、chore-workflow.md、AI-review-prompt.md、AI-review-gap-prompt.md、AI-review-doclist.md、P1-analysis/CLAUDE.md、P1-design/README.md、P1-design/CLAUDE.md、TechStack.md、FunctionList.md、P1-code/README.md、P1-code/CLAUDE.md

### Doclist 完整性提醒
- `P1-code/SYSTEM.md` — CLAUDE.md 明確引用，建議納入審查清單（延續 v7 提醒）
- `AI-CONTEXT.md`、`PRD.md` — 已確認 AI-CONTEXT.md 不存在，PRD.md 存在但未納入
