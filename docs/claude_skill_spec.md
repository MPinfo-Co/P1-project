# Claude Code Skills 規格

## 存放位置

Skills 正式來源：`P1-project/.claude/skills/`

```
P1-project/
└── .claude/
    └── skills/
        ├── ai-docs-review
        └── pg-orchestrator
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
        └── pg-orchestrator
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
