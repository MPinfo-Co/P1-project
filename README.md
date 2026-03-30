# P1-project — 產品管理（PM）

P1 產品的 Epic 管理中心與開發規範文件庫。

## 在四 Repo 流程中的角色

```
P1-project（PM）  ← 你在這裡
    └─ epic label 觸發 P-workflow
        └─ P1-analysis（SA）→ P1-design（SD）→ P1-code（PG／AI）
```

## 目錄結構

```
P1-project/
├── PRD.md                        # 產品需求文件
├── AI-CONTEXT.md                 # AI 協作背景說明
└── docs/
    └── github-workflow/
        ├── overview.md           # 四 Repo 架構與設計理念
        ├── workflow.md           # 完整工作流程（各角色詳細步驟）
        ├── repo-design.md        # 各 Repo 結構與 Issue 欄位規範
        └── quick-start.md       # 新成員第一天操作指南
```

## PM 工作起點

1. Issues → New Issue → 選 **Epic** template，填寫功能說明與驗收條件
2. 送出後系統自動在 P1-analysis 建立 SA Issue、A-Branch 與 Draft PR
3. 在 Epic Issue 追蹤各階段進度（系統自動回填 SA / SD / PG Issue 連結）
4. 所有 PG Issue merge 後，PM 驗收並手動關閉 Epic

## 開發規範文件

| 文件 | 適合誰看 |
|------|---------|
| [quick-start.md](docs/github-workflow/quick-start.md) | 新成員，第一天操作指南 |
| [overview.md](docs/github-workflow/overview.md) | 所有人，整體設計理念 |
| [workflow.md](docs/github-workflow/workflow.md) | 各角色詳細步驟與例外處理 |
| [repo-design.md](docs/github-workflow/repo-design.md) | Repo 結構、Issue 欄位、Branch 規範 |
