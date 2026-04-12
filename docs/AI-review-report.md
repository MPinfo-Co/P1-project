# AI 文件審查報告

## 2026-04-12 13:51 (v13)

> **背景脈絡（重要）**：今日（2026-04-12）P1-code 有新 commit 合入（issue-102），TypeScript 工具鏈已全面就緒：`package.json` 新增 `typescript ^6.0.2`、`tsconfig.json` 存在、`eslint.config.js` 已涵蓋 `**/*.{js,jsx,ts,tsx}`、lint-staged 亦涵蓋 `.ts/.tsx`、`axios ^1.15.0` 也已加入。`frontend/src/` 仍為 0 個 `.tsx`、22 個 `.jsx`（工具鏈已備妥，源碼尚未轉換）。v12 的工具鏈差異（#2、#6）與架構表一致性問題（#1）已全部解決；TechStack.md Tailwind/TanStack 亦已移除（#8）。本輪新增兩項差異：repo-design.md（今日更新後）仍寫 "React + JavaScript"；d-workflow.md 與 CLAUDE.md 對測試報告目錄命名不一致（`PG測試報告` vs `TestReport`）。

### 建議修改清單

| # | 來源 | 修改類型 | 風險 | 修改標的 | 位置 | 建議修改內容 |
|---|------|---------|------|---------|------|------------|
| 1 | v13 | 事實差異 | 中 | [P1-project/docs/repo-design.md](https://github.com/MPinfo-Co/P1-project/blob/main/docs/repo-design.md) | P1-code 目錄結構 | `frontend/  ← React + JavaScript` 改為 `frontend/  ← React + TypeScript（遷移中，src/ 仍為 .jsx）`。今日 git pull 更新後此行仍說 JavaScript，與 CLAUDE.md（`React/TypeScript + Python/FastAPI 實作`）及 README.md（`React/TypeScript`）不一致。另：同文件 VersionDiff 範例已使用 `.tsx`，形成內部不一致 |
| 2 | v13 | 事實差異 | 中 | [P1-project/docs/workflow/spec/d-workflow.md](https://github.com/MPinfo-Co/P1-project/blob/main/docs/workflow/spec/d-workflow.md) | Step 1 #8 | "Scaffold `PG測試報告/issue-{N}.md`" 與 `P1-project/CLAUDE.md` PG 指引表格中 `` `TestReport` `` 命名不一致。P1-code 目前兩目錄並存：`TestReport/`（issue-38/40/45）與 `PG測試報告/`（issue-90）。新 PG 依 CLAUDE.md 指引會找不到 d-workflow 實際 scaffold 的目錄。建議統一命名後同步 d-workflow.md 與 CLAUDE.md |
| 3 | v12 | 事實差異 | 中 | [P1-project/CLAUDE.md](https://github.com/MPinfo-Co/P1-project/blob/main/CLAUDE.md) | 技術棧「樣式」與「State」行 | `Tailwind CSS v3 + MUI`（`樣式`行）應改為 `MUI`；`TanStack Query（Server）`（`State`行）應移除。`frontend/package.json` 無 `tailwindcss`／`@tanstack/react-query` 相依，`src/index.css` 無 `@tailwind` 指令。Axios 已解決（現已在 package.json），本項僅剩 Tailwind 與 TanStack |
| 4 | v12 | 優化 | 低 | [P1-project/CLAUDE.md](https://github.com/MPinfo-Co/P1-project/blob/main/CLAUDE.md) | Commit 格式章節 | `` `{type}({scope}): 說明` `` 與 `docs/workflow/quick-start.md`（速查區塊及 L86）及 `P1-code/SETUP.md`（L49）的 `` `{type}: 工作說明` `` 不一致。`commitlint.config.js` `scope-empty: [0]` 兩者技術上均合法，需人類成員確立權威後同步三處 |
| 5 | v12 | 事實差異 | 中 | [P1-project/docs/AI-review-doclist.md](https://github.com/MPinfo-Co/P1-project/blob/main/docs/AI-review-doclist.md) | L24、L26、L30 | 列出 `P1-analysis/CLAUDE.md`、`P1-design/CLAUDE.md`、`P1-code/CLAUDE.md`，三份檔案已不存在（已集中於 P1-project/CLAUDE.md）。建議刪除三行，或改為單一備註 |
| 6 | v12 | 事實差異 | 低 | [P1-design/TechStack.md](https://github.com/MPinfo-Co/P1-design/blob/main/TechStack.md) | 程式語言章節（L5） | `**JavaScript**（前端語言，目前使用 `.jsx`；TypeScript 遷移規劃中）` — 工具鏈現已就緒（`typescript ^6.0.2`、`tsconfig.json`、eslint/.ts.tsx、lint-staged/.ts.tsx），「規劃中」已不準確。建議改為「TypeScript（遷移中；src/ 目前仍使用 `.jsx`，逐步轉換）」，與 CLAUDE.md 及 README.md 一致 |

### 摘要
> 本次審查 20 份文件（doclist 列 23 份，3 份子 Repo CLAUDE.md 因集中化已刪除），發現 5 份有問題，共 6 項建議修改（本輪新增 2 項；v12 共 8 項的處理結果：5 項已解決〔#1 CLAUDE.md 架構表一致、#2 TypeScript 工具鏈補齊、#3 Axios 加入 package.json、#6 SETUP.md/.ts.tsx 一致、#8 TechStack.md Tailwind/TanStack 已移除且 Axios 已加入〕；3 項未解決續列為 v13 #3/#4/#5；#7 更新語境後列為 v13 #6）。

### 未發現問題的文件
> 以下 15 份文件未發現問題：P1-project/README.md、guide.md、quick-start.md、project-board-guide.md、p-workflow.md、a-workflow.md、c-workflow.md、chore-workflow.md、AI-review-prompt.md、AI-review-gap-prompt.md、P1-analysis/README.md、P1-design/README.md、FunctionList.md、P1-code/README.md、P1-code/SETUP.md。

### Doclist 完整性提醒
- **本輪最重要**：`AI-review-doclist.md` L24、L26、L30 列出的三份子 Repo CLAUDE.md 已不存在（詳見 #5，應優先處理）
- `P1-code/SYSTEM.md` — 存在且為系統架構權威文件，建議納入審查清單（延續 v7-v12 提醒）
- `P1-code/frontend-mui/` — 今日掃描發現此目錄存在但未見於任何文件說明，建議確認是否需補充文件或納入 doclist

---

## 2026-04-09 18:36 (v12)

> **背景脈絡（重要）**：今日（2026-04-09）多個 commit 顯示人類成員正在確立「前端 TypeScript 遷移」方向：commit `1a109ea`（CLAUDE.md L130 技術棧 JavaScript→TypeScript）、`2eae5ea`（repo-design.md VersionDiff 範例 .jsx→.tsx）、`8dd7a25`（README.md L22 React/JavaScript→React/TypeScript）。但 `P1-code/frontend/src/` 目前 0 個 `.tsx`、29 個 `.jsx`，工具鏈（ESLint `files: ['**/*.{js,jsx}']`、lint-staged `*.{js,jsx}`）亦未同步。本輪多項建議源於「已宣告 TS 方向但實作與其他文件未跟上」的過渡狀態，修改選項多為「補齊工具鏈 vs 回退文件」二擇一。

### 建議修改清單

| # | 來源 | 修改類型 | 風險 | 修改標的 | 位置 | 建議修改內容 |
|---|------|---------|------|---------|------|------------|
| 1 | v12 | 事實差異 | 中 | [P1-project/CLAUDE.md](https://github.com/MPinfo-Co/P1-project/blob/main/CLAUDE.md) | 專案架構表 L22 | `P1-code` 列「React/JavaScript + Python/FastAPI 實作」與 README.md L22（今日 commit `8dd7a25` 已改為 `React/TypeScript`）及 CLAUDE.md 自身 L130 技術棧章節「TypeScript，舊 .jsx 漸進遷移」**內部不一致**。commit `8dd7a25` 只更新 README.md 未同步 CLAUDE.md。建議 L22 改為 `React/TypeScript + Python/FastAPI 實作` 以與 README.md／L130 一致（或三處統一為 `React/JS-TS 遷移中`）|
| 2 | v12 | 事實差異 | 中 | [P1-project/CLAUDE.md](https://github.com/MPinfo-Co/P1-project/blob/main/CLAUDE.md) | PG 指引 L110、技術棧 L130 | L130「前端 \| React 19 + Vite + React Router v7（TypeScript，舊 .jsx 漸進遷移）」與 L110「前端新檔案一律使用 `.tsx`」宣告 TS 遷移，但工具鏈未同步：`frontend/src/` 0 個 `.tsx`／29 個 `.jsx`；`eslint.config.js` 僅 `files: ['**/*.{js,jsx}']`；`package.json` lint-staged 僅涵蓋 `*.{js,jsx}`。若依此聲明建立 `.tsx` 檔將無 lint/format 把關。建議二擇一—(a) 補齊 ESLint/lint-staged/CI 對 `.tsx` 支援、刪除 `jsconfig.json`（目前與 `tsconfig.json` 並存）；(b) 回退 L110、L130 至「JavaScript（.jsx），TypeScript 遷移規劃中」與 TechStack.md L5 一致 |
| 3 | v12 | 事實差異 | 中 | [P1-project/CLAUDE.md](https://github.com/MPinfo-Co/P1-project/blob/main/CLAUDE.md) | 技術棧 L131-133 | 移除未實際使用的 `Tailwind CSS v3`、`TanStack Query（Server）`、`Axios`。`frontend/package.json` 無 `tailwindcss`／`@tanstack/react-query`／`axios` 相依；`frontend/src/index.css` 無 `@tailwind` 指令；`tailwind.config.js` 為孤立設定檔。實際為 `MUI + Emotion`，目前無 HTTP client 套件（尚未導入）。與 #6 TechStack.md 同步修正 |
| 4 | v12 | 優化 | 低 | [P1-project/CLAUDE.md](https://github.com/MPinfo-Co/P1-project/blob/main/CLAUDE.md) | Commit 格式 L117 | `` `{type}({scope}): 說明` `` 與 `P1-code/SETUP.md` L49／`quick-start.md` L197、L211、L86 的 `` `{type}: 工作說明` `` 不一致。commit `f578183`（2026-04-08）曾將 CLAUDE.md 改為無 scope，但今日 rewrite commit `57aa3c2` 復原為有 scope。`frontend/commitlint.config.js` 設定 `'scope-empty': [0]`（兩種格式技術上都合法），需人類成員確立權威後同步 CLAUDE.md L117、SETUP.md L49、quick-start.md 三處（L86 目前為無 scope，若改回有 scope 需一併更新） |
| 5 | v12 | 事實差異 | 中 | [P1-project/docs/AI-review-doclist.md](https://github.com/MPinfo-Co/P1-project/blob/main/docs/AI-review-doclist.md) | L24、L26、L30 | 列出 `P1-analysis/CLAUDE.md`、`P1-design/CLAUDE.md`、`P1-code/CLAUDE.md`，但三份檔案已於 commit `f620722 chore: remove CLAUDE.md (centralized in P1-project)` 移除，本輪掃描確認不存在。建議三行刪除，或整併為單一備註：「CLAUDE.md 已集中於 `P1-project/CLAUDE.md`，子 Repo 不再維護」 |
| 6 | v12 | 事實差異 | 低 | [P1-code/SETUP.md](https://github.com/MPinfo-Co/P1-code/blob/main/SETUP.md) | L44 | `對暫存的 `.js/.jsx/.ts/.tsx` 檔執行 ESLint + Prettier` 與 `frontend/package.json` lint-staged 實際 glob `*.{js,jsx}` 不符，`eslint.config.js` 也僅 lint `.{js,jsx}`。與 #2 (a) 方案搭配則反向補齊 lint-staged／ESLint 設定；採 (b) 方案則將 L44 改為 `對暫存的 `.js/.jsx` 檔執行 ESLint + Prettier` |
| 7 | v12 | 優化 | 低 | [P1-code/README.md](https://github.com/MPinfo-Co/P1-code/blob/main/README.md) | L5 | `React 19 + TypeScript + FastAPI 前後端程式碼庫` 與 `P1-design/TechStack.md` L5「JavaScript（目前使用 `.jsx`；TypeScript 遷移規劃中）」措辭不一致。README.md 以肯定式聲明 TypeScript 但隻字未提遷移狀態，首次閱讀的 PG 會誤以為已完成遷移。建議改為與 TechStack.md L5 同樣的「遷移規劃中」措辭，維持兩份權威文件描述一致 |
| 8 | v10 | 事實差異 | 中 | [P1-design/TechStack.md](https://github.com/MPinfo-Co/P1-design/blob/main/TechStack.md) | 前端章節 L11、L14、L15 | 同 #3：移除未實際使用的 `Tailwind CSS v3`、`TanStack Query`、`Axios`（`package.json` 無對應相依；`src/` 無引用；`index.css` 無 `@tailwind`；實際為 `MUI + Emotion`）。`frontend/tailwind.config.js` 為孤立設定檔，建議一併評估刪除。注意：v10 #1 TechStack.md L5 TypeScript→JavaScript 已於 v11 後解決 |

### 摘要
> 本次審查 20 份文件（doclist 列 23 份，3 份子 Repo CLAUDE.md 因集中化已刪除，詳見 #5），發現 5 份有問題，共 8 項建議修改（本輪新增 7 項；v11 10 項處理結果：6 項已解決〔#1-#3 子 Repo CLAUDE.md 因集中化刪除、#4 chore-workflow.md 角色措辭、#5 TechStack.md L5 改 JavaScript、#8 quick-start.md L86 SA 卡關格式〕，1 項未解決續列為本輪 #8〔#6 TechStack.md L11/14/15〕，3 項被人類成員反轉方向而自動消解〔#7 P1-code/README Tailwind → 整檔簡化；#9 README L22、#10 quick-start L165 — 後兩者今日由 commit `8dd7a25` 與歷次 commit 明確改為 TypeScript 方向，原「改為 JavaScript」建議撤除〕）。本輪核心問題：人類成員正在推動 TypeScript 遷移但只改了部分文件，產生「CLAUDE.md 與 README.md／TechStack.md 內部不一致」與「宣告 TS 但工具鏈仍是 JS」兩類事實差異，需決定是「補齊工具鏈」還是「讓文件誠實反映『遷移規劃中』狀態」。

### 未發現問題的文件
> 以下 15 份文件未發現問題：P1-project/README.md、docs/workflow/guide.md、project-board-guide.md、repo-design.md、p-workflow.md、a-workflow.md、d-workflow.md、c-workflow.md、chore-workflow.md、docs/workflow/quick-start.md、AI-review-prompt.md、AI-review-gap-prompt.md、P1-analysis/README.md、P1-design/README.md、FunctionList.md。

### Doclist 完整性提醒
- **本輪最重要**：`AI-review-doclist.md` L24、L26、L30 列出的三份子 Repo CLAUDE.md 已不存在（詳見修改 #5，應優先處理）
- `P1-code/SYSTEM.md` — 存在且為系統架構權威文件，建議納入審查清單（延續 v7-v11 提醒）
- `P1-code/frontend/README.md` 與 `P1-code/backend/README.md` — 雖不再被簡化後的 P1-code/README.md 明示引用，但檔案仍存在且有實質內容，建議評估是否納入（延續 v10-v11 提醒）

---

## 2026-04-09 00:41 (v11)

### 建議修改清單

| # | 來源 | 修改類型 | 風險 | 修改標的 | 位置 | 建議修改內容 |
|---|------|---------|------|---------|------|------------|
| 1 | v11 | 優化 | 低 | [P1-analysis/CLAUDE.md](https://github.com/MPinfo-Co/P1-analysis/blob/main/CLAUDE.md) | Commit 格式章節 | `` `{type}({scope}): 說明` `` 改為 `` `{type}: 工作說明` ``，範例由 `docs(issue-4): 完成請假申請 SA 分析` 改為 `docs: 完成請假申請 SA 分析`。P1-project 已於 commit `f578183` 將 CLAUDE.md／quick-start.md 統一為無 scope，以對齊 P1-code/SETUP.md；三個子 Repo 的 CLAUDE.md 需同步，避免再次產生新的不一致 |
| 2 | v11 | 優化 | 低 | [P1-design/CLAUDE.md](https://github.com/MPinfo-Co/P1-design/blob/main/CLAUDE.md) | Commit 格式章節 | 同 #1：`` `{type}({scope}): 說明` `` 改為 `` `{type}: 工作說明` ``，範例由 `feat(spec): 新增 POST /api/users API 規格` 改為 `feat: 新增 POST /api/users API 規格` |
| 3 | v11 | 優化 | 低 | [P1-code/CLAUDE.md](https://github.com/MPinfo-Co/P1-code/blob/main/CLAUDE.md) | 本地 Hook 章節（L32） | 同 #1：`Commit message 格式：` `` `{type}({scope}): 說明` `` 改為 `` `{type}: 工作說明` ``。此為 P1-code 內部 CLAUDE 與 SETUP.md L49 直接衝突，修正優先度較高 |
| 4 | v11 | 優化 | 低 | [P1-project/docs/workflow/spec/chore-workflow.md](https://github.com/MPinfo-Co/P1-project/blob/main/docs/workflow/spec/chore-workflow.md) | 用途章節（L6） | `讓 PG 可直接 checkout 開始作業` 改為 `讓對應角色（SA／SD／PG）可直接 checkout 開始作業`。chore-workflow 實際部署於 P1-analysis／P1-design／P1-code 三個 Repo（L9 自己亦清楚列出 a-/d-/c- 三版），「讓 PG」的措辭與範圍不符 |
| 5 | v10 | 事實差異 | 中 | [P1-design/TechStack.md](https://github.com/MPinfo-Co/P1-design/blob/main/TechStack.md) | 程式語言章節（L5） | `**TypeScript**（前端語言，React 生態主流）` 改為 `**JavaScript**（前端語言）`。`P1-code/frontend/package.json` 無 typescript 相依、無 tsconfig.json（僅 jsconfig.json）、`frontend/src/` 完全為 `.js/.jsx`。TechStack.md 是技術棧權威文件，錯誤會誤導 SD／PG |
| 6 | v10 | 事實差異 | 中 | [P1-design/TechStack.md](https://github.com/MPinfo-Co/P1-design/blob/main/TechStack.md) | 前端章節（L11、L14、L15） | 移除未實際使用的條目：`Tailwind CSS v3`、`TanStack Query`、`Axios`。`P1-code/frontend/package.json` 無對應依賴、`frontend/src/` 無任何引用；實際 CSS/UI 為 `MUI + Emotion`，無 HTTP client 套件（可能尚未導入）。`frontend/tailwind.config.js` 為孤立設定檔，建議一併評估刪除 |
| 7 | v10 | 事實差異 | 低 | [P1-code/README.md](https://github.com/MPinfo-Co/P1-code/blob/main/README.md) | 目錄結構 frontend 行（L20） | `React 19 + Vite + JavaScript + Tailwind CSS` 改為 `React 19 + Vite + JavaScript + MUI`（與 #6 同步，實際使用 MUI + Emotion，非 Tailwind）|
| 8 | v10 | 優化 | 低 | [P1-project/docs/workflow/quick-start.md](https://github.com/MPinfo-Co/P1-project/blob/main/docs/workflow/quick-start.md) | SA 常見卡關章節（L86） | L86 稱「最常見的是忘記小括號 scope，或說明用中文但格式符號不對。正確格式：`feat(leaves): 說明`」仍要求 scope，但同檔案 L197／L211 已於 commit `f578183` 改為無 scope 格式 `{type}: 工作說明`。建議 L86 改為「commitlint 格式錯誤：最常見是 `type:` 後缺少空格，或 type 不在允許清單。正確格式：`feat: 說明`」，與速查區塊一致 |
| 9 | v2 | 事實差異 | 低 | [P1-project/README.md](https://github.com/MPinfo-Co/P1-project/blob/main/README.md) | 四個 Repo 表格 P1-code 列（L22） | `React/TypeScript` 改為 `React/JavaScript`（package.json 僅含 `.js/.jsx`，無 TypeScript 相依） |
| 10 | v2 | 事實差異 | 低 | [P1-project/docs/workflow/quick-start.md](https://github.com/MPinfo-Co/P1-project/blob/main/docs/workflow/quick-start.md) | PG 第 5 步「撰寫程式碼與測試」（L165） | `前端 React/TypeScript `.tsx`` 改為 `前端 React/JavaScript `.jsx`` |

### 摘要
> 本次審查 23 份文件，發現 8 份有問題，共 10 項建議修改（本輪新增 4 項；v10 共 7 項中解決 0 項、超越 1 項〔#7 SETUP.md scope 格式—專案已於 commit `f578183` 反轉方向統一為無 scope，SETUP.md 自動成為基準，原建議撤除〕，6 項持續未解決）。

### 未發現問題的文件
> 以下 15 份文件未發現問題：P1-project/CLAUDE.md、guide.md、project-board-guide.md、repo-design.md、p-workflow.md、a-workflow.md、d-workflow.md、c-workflow.md、AI-review-prompt.md、AI-review-gap-prompt.md、AI-review-doclist.md、P1-analysis/README.md、P1-design/README.md、FunctionList.md、P1-code/SETUP.md。

### Doclist 完整性提醒
- `P1-code/SYSTEM.md` — 存在且 P1-code/CLAUDE.md L11 明確導引至此（完整系統架構、資料流、SSB 整合、事件合併機制），建議納入審查清單（延續 v7/v8/v9/v10 提醒）
- `P1-code/frontend/README.md` 與 `P1-code/backend/README.md` — 被 P1-code/README.md L28 明確引用為「詳細說明」入口，但未納入審查清單，建議評估是否納入（延續 v10 提醒）
