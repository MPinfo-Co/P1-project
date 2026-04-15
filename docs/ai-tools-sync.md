# AI 工具同步說明

P1 專案的 AI 審查工具（skill + agents）統一由 P1-project repo 維護，  
團隊成員透過同步流程取得工具，不需手動設定。

---

## 工具清單

| 類型 | 名稱 | 用途 |
|------|------|------|
| Skill | `ai-work-review` | 自動判斷 SA/SD/PG 情境，dispatch 對應 reviewer |
| Agent | `sa-reviewer` | 審查 SA 產出的 business-logic.md |
| Agent | `sd-reviewer` | 審查 SD 產出的 TDD |
| Agent | `pg-reviewer` | 審查 PG 產出的 TestReport 與 pytest |

工具存放於 repo 的 `.claude/` 目錄：

```
P1-project/
└── .claude/
    ├── skills/
    │   └── ai-work-review/
    │       └── SKILL.md
    └── agents/
        ├── sa-reviewer.md
        ├── sd-reviewer.md
        └── pg-reviewer.md
```

---

## 初次設定（新成員）

clone P1-project 後，將 `.claude/` 目錄複製到本機 P1 工作目錄根層：

```bash
cp -r P1-project/.claude/ /你的本機路徑/P1/.claude/
```

完成後即可在 P1 工作目錄中使用 `/ai-work-review` 指令。

---

## 同步流程

### 本機 → Repo（發布更新）

在本機修改工具後，同步到 repo 讓全員取得：

```
將本機 P1 工作目錄的 Claude skill 與 agents 同步到 P1-project repo。

來源路徑：{本機}/P1/.claude/
目標路徑：{本機}/P1/P1-project/.claude/

需同步的檔案：
- skills/ai-work-review/SKILL.md
- agents/sa-reviewer.md
- agents/sd-reviewer.md
- agents/pg-reviewer.md

執行步驟：
1. 若目標 .claude/ 目錄不存在，建立對應子目錄結構
2. 將來源四個檔案複製覆蓋到目標對應位置
3. 在 P1-project 執行 git add/commit/push，commit message：
   chore: sync ai-work-review skill and reviewer agents from local .claude
```

### Repo → 本機（拉取最新版）

repo 有更新時，拉回本機套用：

```
將 P1-project repo 的 Claude skill 與 agents 同步回本機 P1 工作目錄。

來源路徑：{本機}/P1/P1-project/.claude/
目標路徑：{本機}/P1/.claude/

需同步的檔案：
- skills/ai-work-review/SKILL.md
- agents/sa-reviewer.md
- agents/sd-reviewer.md
- agents/pg-reviewer.md

執行步驟：
1. 先在 P1-project 執行 git pull 確保來源是最新版本
2. 將來源四個檔案複製覆蓋到 {本機}/P1/.claude/ 對應位置
3. 不需 commit（目標是本機 .claude 目錄，不在 git 管理範圍）
```

---

## 使用方式

同步完成後，在 Claude Code 中輸入：

```
/ai-work-review
```

工具會自動偵測當前 branch 或檔案，判斷是 SA / SD / PG 階段，  
並 dispatch 對應的 reviewer agent 進行審查。
