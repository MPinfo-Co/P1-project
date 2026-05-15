# Claude Code Skills 規格

## 存放位置

Skills 正式來源：`P1-project/.claude/skills/`

```
P1-project/
└── .claude/
    └── skills/
        ├── ai-docs-review
        ├── clean-branch-files
        ├── epic-launcher
        ├── pg-orchestrator
        ├── plan-go-check-report
        ├── pull-p1-repos
        └── sync-claude-md
```

---

## 佈署方式

### 工作目錄為 `P1-project/`（直接 clone 使用）

Clone 後即可使用，無需額外設定。

### 工作目錄為上層 workspace（如 `P1/`）

需將 skills 複製到 workspace 根目錄：

```bash
cp -r P1-project/.claude/skills/. .claude/skills/
```

複製後目錄結構：

```
P1/
└── .claude/
    └── skills/
        ├── ai-docs-review
        ├── clean-branch-files
        ├── epic-launcher
        ├── pg-orchestrator
        ├── plan-go-check-report
        ├── pull-p1-repos
        └── sync-claude-md
```

---

## Skills 說明

### `/pg-orchestrator`

執行 PG issue 實作。自動偵測 TDD 範圍，依需要派遣 backend / frontend agent。

**使用方式：**

```
/pg-orchestrator {issue編號}
```

```
/pg-orchestrator {issue編號} {backend-branch} {frontend-branch}
```

| 參數 | 必填 | 說明 |
|------|------|------|
| issue 編號 | 必填 | PG Issue 編號 |
| backend branch | 選填 | 指定 backend 分支名稱 |
| frontend branch | 選填 | 指定 frontend 分支名稱 |

**範例：**

```
/pg-orchestrator 66
/pg-orchestrator 66 pg/issue-66-backend pg/issue-66-frontend
```

---

### `/ai-docs-review`

審查 P1 三個 Repo 的文件狀況，依 `docs/ai-review/AI-review-prompt.md` 的審查指令與清單，逐一分析文件，輸出結構化建議報告。

**使用方式：**

```
/ai-docs-review
```

> 此 skill 亦透過排程自動執行（每天台灣時間凌晨 2:00），詳見 [workflow_guide.md](workflow_guide.md) 第 2.2 節。

---

### `/epic-launcher`

啟動 P1 完整功能開發流程。支援兩種入口：提供既有 Epic Issue 編號（接續執行），或描述新功能需求（建立新 Epic）。可選擇執行停止點（SA / SD / 全程至 PG），各階段停止前執行品質確認。

**使用方式：**

```
/epic-launcher
```

---

### `/plan-go-check-report`

執行涉及多個檔案或 repo 的實作任務。在動手前先確認範圍，執行後驗證結果並輸出報告。適用於 config、workflow、prompt 等異動。

**使用方式：**

```
/plan-go-check-report
```

---

### `/pull-p1-repos`

拉取 P1-project、P1-design、P1-code 三個 repo 的最新 main。在開始任何 P1 工作前執行。

**使用方式：**

```
/pull-p1-repos
```

---

### `/clean-branch-files`

切換至某個 branch 後，移除本地存在但遠端不存在的多餘檔案。保留 `.venv`、`node_modules`、`.env`。

**使用方式：**

```
/clean-branch-files
```

---

### `/sync-claude-md`

將 `P1-project` 根目錄的 `CLAUDE.md`（正式來源）同步覆蓋至本機 P1 工作目錄。P1-project 永遠為權威來源。

**使用方式：**

```
/sync-claude-md
```
