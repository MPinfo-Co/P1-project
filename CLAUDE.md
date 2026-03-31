# CLAUDE.md

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
| **P1-code** | 系統開發（React/TypeScript + Python/FastAPI） | PG／AI |

## 目錄結構

### P1-project（產品管理）
```
P1-project/
├── PRD.md                        # 產品需求文件
├── AI-CONTEXT.md                 # AI 背景資訊
└── docs/github-workflow/         # GitHub 工作流程文件
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
│   │   └── schemas/              # Pydantic Schemas
│   └── alembic/                  # Migration
├── frontend/src/             # 前端主目錄
│   ├── components/               # 共用元件
│   └── pages/                    # 頁面（依功能分資料夾）
├── tests/                        # 測試報告
└── VersionDiff/                  # 版本異動紀錄
```

## 開發流程

Epic（P1-project）→ SA Issue（P1-analysis）→ SD Issue（P1-design）→ PG Issue（P1-code）
每個階段由上游 merge 後 GitHub Actions 自動建立下游 Issue 與 Branch。

## AI 實作指引（PG 階段）

收到 PG Issue 後，沿關聯鏈讀取：
1. PG Issue body「實作範圍」（系統自動填入 SD 異動的 Spec 清單）
2. `P1-design/Spec/` — API 與畫面規格
3. `P1-design/TestPlan/issue-{SD#}-diff.md` — 本次 delta
4. `P1-analysis/issue-{SA#}/business-logic.md` — 商業邏輯背景
5. `P1-design/TestPlan/issue-{SD#}.md` — 測試標準（pytest 數量 ≥ TestPlan 案例數）

## Branch 與 Commit 規範

- Branch：`issue-{N}-{slug}`，由 GitHub Actions 自動建立，**不手動建立**
- 跨 Repo 溝通加前綴：`A-issue-N`（analysis）、`D-issue-N`（design）、`C-issue-N`（code）
- Commit：`{type}({scope}): 說明`，由 commitlint 強制執行
  - 常用 type：`feat` / `fix` / `docs` / `refactor` / `test` / `chore`

## 任務規模判斷

任務涉及以下情況時，主動建議使用 Subagent 平行處理：
- 需要跨多個 Repo 操作
- 有多個可獨立進行的步驟（無相依關係）
- 預計需要 5 個以上工具呼叫

## 技術棧（MVP 階段）

| 層級 | 選型 |
|------|------|
| **前端** | React 18 + Vite + React Router v6 |
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

## 語言

所有文件與 Issue template 使用繁體中文（zh-TW）。
