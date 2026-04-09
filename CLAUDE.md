# CLAUDE.md

> **維護說明：** 本文件的正式來源是 `MPinfo-Co/P1-project` 根目錄的 `CLAUDE.md`。
> 各開發者應將此內容複製到自己的 Claude Code 工作目錄（即 P1 專案的本機根目錄）。
> **任何內容有更動，請同步更新 P1-project 與本機兩處。**
> P1-analysis、P1-design、P1-code 不再各自維護 CLAUDE.md。

## 專案簡介

MP-BOX 是一套面向企業用戶的 AI 應用平台，協助企業解決各類作業難題。
核心功能包含：資安日誌解讀與風險處置、專家知識管理、企業技能管理（如 ERP 操作自動化）、
以及企業營運狀況解讀（財務、營運、工作執行）。

## 專案架構

P1 由四個 Repo 組成，對應四個開發階段：

| Repo | 層級 | 負責角色 |
|------|------|---------|
| **P1-project** | 產品管理（Epic、規範文件） | PM |
| **P1-analysis** | 需求分析（業務邏輯、Use Case、SD-WBS） | SA |
| **P1-design** | 系統設計（Prototype、API Spec、Schema、TestPlan） | SD |
| **P1-code** | 系統開發（React/JavaScript + Python/FastAPI） | PG／AI |

## 目錄結構

### P1-project（產品管理）
```
P1-project/
├── README.md                     # 專案總導覽與文件索引
├── CLAUDE.md                     # AI agent 工作指引（本文件，四 Repo 共用）
└── docs/
    ├── repo-design.md            # Repo 結構與格式規範
    ├── AI-review-prompt.md       # AI 文件審查任務 Prompt
    ├── AI-review-gap-prompt.md   # AI 缺口與孤立文件掃描 Prompt
    ├── AI-review-doclist.md      # AI 文件審查範圍清單
    └── workflow/
        ├── guide.md              # 設計理念與整體流程
        ├── quick-start.md        # 各角色操作指南
        └── spec/                 # 各 workflow 技術規格
```

### P1-analysis（需求分析）
```
P1-analysis/
├── issue-{N}/
│   ├── business-logic.md         # 商業邏輯說明
│   └── SD-WBS.md                 # 工作分解結構
└── references/                   # 全域參考文件（架構圖、命名規則等）
```

### P1-design（系統設計）
```
P1-design/
├── Spec/                         # API 規格
├── TestPlan/
│   ├── issue-{N}.md              # 完整測試計畫
│   └── issue-{N}-diff.md         # 本次 delta
├── schema/                       # DB Schema
└── Prototype/                    # UI Prototype（HTML）
```

### P1-code（系統開發）
```
P1-code/
├── backend/
│   ├── app/
│   │   ├── api/                  # API 路由
│   │   ├── core/                 # 設定、依賴、安全
│   │   ├── db/                   # DB Session
│   │   ├── models/               # SQLAlchemy Models
│   │   ├── schemas/              # Pydantic Schemas
│   │   ├── services/             # 業務邏輯層
│   │   └── tasks/                # 背景任務
│   ├── tests/                    # 後端單元測試（CI 執行範圍）
│   └── alembic/                  # Migration
├── frontend/src/                 # 前端主目錄（JavaScript）
│   ├── components/               # 共用元件
│   └── pages/                    # 頁面（依功能分資料夾）
└── VersionDiff/                  # 版本異動紀錄
```

## 開發流程

Epic（P1-project）→ SA Issue（P1-analysis）→ SD Issue（P1-design）→ PG Issue（P1-code）
每個階段由上游 merge 後 GitHub Actions 自動建立下游 Issue 與 Branch。

## AI 實作指引（各階段通用）

Issue body 已包含該階段所需的核心 context；「關聯項目」提供所有上游文件的直接連結。

### SA 階段

收到 SA Issue 後，在 `issue-{N}/` 填寫兩份文件：

1. 從「關聯項目」開啟 business-logic.md（第一個 section 已有 Epic 問題描述）
2. 填寫 business-logic.md（Use Case、流程圖、Class Diagram、ER 示意）
3. 填寫 SD-WBS.md（Schema / API / 畫面 工作項目）

**SD-WBS.md 格式要求：**

```markdown
# SD WBS：{功能名稱}

## 工作項目
| # | 類型 | 說明 |
|---|------|------|
| 1 | Schema | 說明 |
| 2 | API | 說明 |
| 3 | 畫面 | 說明 |

## 備註
<!-- 特殊限制、相依關係、需 SD 決策的設計點 -->
```

類型限定：`Schema`、`API`、`畫面`、`其他`

### SD 階段

收到 SD Issue 後，依「設計範圍」（自動從 SD-WBS.md 複製）完成：

1. Issue body「功能說明」已包含 business-logic.md 完整內容
2. 修改 **Prototype/**（活文件，直接改最新版）
3. 修改 **Spec/**（活文件，直接改最新版）
4. 若有 Schema 異動，修改 **schema/**
5. 填寫 **TestPlan/issue-{N}.md**（系統自動建立框架）

**TestPlan 最低要求：**
- 每個 API：至少一個成功案例（2xx）+ 一個失敗案例（4xx/5xx）
- 每個畫面：至少一個主要操作流程的正常案例
- 測試案例總數 ≥ SD-WBS.md 工作項目數

```markdown
| ID | 類型 | 前置條件 | 操作 | 預期結果 |
|----|------|---------|------|---------|
| T1 | 整合 | 已登入 | POST /api/xxx | 201，回傳 id |
| T2 | 整合 | 已登入 | POST /api/xxx（缺少必填欄位）| 422 |
```

**活文件原則：** `Spec/`、`Prototype/`、`schema/` 永遠反映最新狀態，直接修改，不保留舊版。
`TestPlan/issue-{N}.md` 是 delta record，以 Issue 為單位保存。

### PG 階段

收到 PG Issue 後，沿關聯鏈讀取：

| 需要什麼 | 去哪裡找 |
|----------|---------|
| 實作範圍 | PG Issue body「實作範圍」欄位 |
| API 規格 | `P1-design/Spec/` |
| 畫面規格 | `P1-design/Prototype/` |
| 本次異動 delta | 從「關聯檔案」開啟 SpecDiff |
| 商業邏輯背景 | `P1-analysis/issue-{SA#}/business-logic.md` |
| 測試標準 | 從「關聯檔案」開啟 TestPlan |
| 填寫結果 | 從「關聯檔案」開啟 TestReport — 填寫「結果」「備註」兩欄 |

**前端新檔案一律使用 `.tsx`**，舊 `.jsx` 不需強制遷移（漸進式）。

**pytest 數量 ≥ TestPlan 案例數**，每個 test function 標注對應的 TestPlan ID：

```python
def test_create_leave_request(client, db_session, auth_headers):
    """對應 TestPlan issue-5 T1"""
    ...
```

## Branch 與 Commit 規範

- Branch：`issue-{N}-{slug}`，由 GitHub Actions 自動建立，**不手動建立**
- 跨 Repo 溝通加前綴：`A-issue-N`（analysis）、`D-issue-N`（design）、`C-issue-N`（code）
- Commit：`{type}({scope}): 說明`，由 commitlint 強制執行
  - 常用 type：`feat` / `fix` / `docs` / `refactor` / `test` / `chore`

每次 commit 自動執行本地 Hook：
- **Python**：`ruff check`（lint）+ `ruff format`（格式化）
- **前端**：`ESLint` + `Prettier`（僅對暫存檔案）
- **Commit message**：commitlint 驗證格式

## 任務規模判斷

任務涉及以下情況時，主動建議使用 Subagent 平行處理：
- 需要跨多個 Repo 操作
- 有多個可獨立進行的步驟（無相依關係）
- 預計需要 5 個以上工具呼叫

## AI 工作方法

**實作、修改、建立類請求**的預設流程：

1. **Brainstorm**（如適用）：需求模糊、涉及架構決策、或有多種合理路徑時，
   先列出方案與 tradeoff，請用戶確認方向

2. **待辦清單**：列出已優化的執行計劃，每項包含：
   - 做什麼 / 怎麼做 / 如何驗證
   - 單項預計超過 3 個工具呼叫則拆小

3. **詢問執行**：呈現清單後問「是否執行？」，
   用戶明確說「執行」或「開始」前不進行任何實際變更

4. **用戶修改計劃後**：重新整合最終版本，再確認一次才執行

純問答、解釋、討論不適用此流程。

## 技術棧（MVP 階段）

| 層級 | 選型 |
|------|------|
| **前端** | React 19 + Vite + React Router v7（JavaScript）|
| **樣式** | Tailwind CSS v3 + MUI |
| **State** | Zustand（Client）+ TanStack Query（Server）|
| **HTTP** | Axios |
| **後端** | Python 3.12 + FastAPI + Pydantic |
| **ORM** | SQLAlchemy + Alembic（Migration）|
| **資料庫** | PostgreSQL |
| **認證** | 自建 JWT（bcrypt 密碼 hash）|
| **檔案儲存** | Cloudflare R2（S3 相容 API）|
| **Email** | Resend |
| **測試** | pytest |
| **Linter** | Ruff（Python）/ ESLint + Prettier（前端）|
| **部署** | Docker + Railway（後端）+ Vercel（前端）|

完整技術選型說明見 [P1-design/TechStack.md](https://github.com/MPinfo-Co/P1-design/blob/main/TechStack.md)。

## 語言

所有文件與 Issue template 使用繁體中文（zh-TW）。
