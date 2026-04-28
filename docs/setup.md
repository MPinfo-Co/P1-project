# 開發環境準備指引

## 前置需求

| 工具 | 最低版本 | 驗證指令 |
|------|---------|---------|
| Python | 3.12+ | `python --version` |
| Node.js | 20+ | `node --version` |
| Git | 任意 | `git --version` |
| Claude Code | 任意 | `claude --version` |

---

## 1. 建立 P1 根目錄

```bash
mkdir P1
cd P1
```

Clone 三個 repo：

```bash
git clone https://github.com/MPinfo-Co/P1-project.git
git clone https://github.com/MPinfo-Co/P1-design.git
git clone https://github.com/MPinfo-Co/P1-code.git
```

完成後結構如下：

```
P1/
├── .claude/
│   └── skills/
├── P1-project/
├── P1-design/
└── P1-code/
```

---

## 2. 同步 Skills

Skills 的正式來源為 `P1-project/.claude/skills/`，需手動複製到 P1 根目錄供 Claude Code 使用。

**首次設定：**

```bash
mkdir -p .claude/skills
cp -r P1-project/.claude/skills/. .claude/skills/
```

**後續更新（P1-project 有新版時）：**

```bash
git -C P1-project pull
cp -r P1-project/.claude/skills/. .claude/skills/
```

---

## 3. Python 環境設定

```bash
cd P1-code/backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd ../..
```

---

## 4. 安裝 pre-commit（CLI 工具，需手動一次）

```bash
pip install pre-commit
```

> **不需要執行 `pre-commit install`**。
> Python hook 已整合進 husky，由 husky 的 `pre-commit` hook 統一呼叫。
> 只需確保 `pre-commit` 指令在 PATH 中可用即可。

---

## 5. 前端環境設定（hook 自動啟用）

```bash
cd P1-code/frontend
npm install
```

`npm install` 會透過 `prepare` script 自動設定 husky，啟用以下本地 hook：
- **pre-commit**：對暫存的 `.js/.jsx/.ts/.tsx` 檔執行 ESLint + Prettier，`.css/.json` 執行 Prettier
- **commit-msg**：commitlint 驗證 commit message 格式

---

## 6. Commit Message 格式

範例格式：`{type}(scope?): 工作說明`

| Type | 使用時機 |
|------|---------|
| `feat` | 新功能 |
| `fix` | 修復 bug |
| `docs` | 文件變更 |
| `refactor` | 重構 |
| `test` | 測試相關 |
| `chore` | 設定、建置相關 |

---

## 7. 推薦 IDE 插件（VS Code）

| 插件 | 用途 |
|------|------|
| ESLint（dbaeumer.vscode-eslint） | 即時顯示 JS/JSX 錯誤 |
| Prettier（esbenp.prettier-vscode） | 儲存時自動格式化 |
| Ruff（charliermarsh.ruff） | 即時顯示 Python lint/format 錯誤 |

VS Code 建議設定（`.vscode/settings.json`）：
```json
{
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "[python]": {
    "editor.defaultFormatter": "charliermarsh.ruff"
  }
}
```

---

## 8. 驗證環境

### 驗證 Python hook
```bash
echo "x=1" >> P1-code/backend/app/main.py
git -C P1-code add backend/app/main.py
git -C P1-code commit -m "chore: test"
# 會被擋，顯示錯誤後自動修改，重新 commit
```

### 驗證前端 hook
```bash
git -C P1-code commit --allow-empty -m "bad message"
# 預期：commit 被擋，顯示 type may not be empty

git -C P1-code commit --allow-empty -m "chore: 測試"
# 預期：通過
git -C P1-code reset HEAD~1
```

---

## 9. CI 檢查項目

每次 push 到 `issue-*` branch 或開 PR 時，CI 自動執行：

| 檢查 | 工具 |
|------|------|
| Python lint | ruff check |
| Python 格式 | ruff format --check |
| Python 測試（含 coverage） | pytest |
| 前端 lint | ESLint |
| 前端格式 | Prettier |

---

## 10. Skills 使用

從 `P1/` 根目錄啟動 Claude Code，skills 會自動載入。

### `/pg-orchestrator`

執行 PG issue 實作。自動偵測 TDD 範圍，依需要派遣 backend / frontend agent。

```
/pg-orchestrator 66
```

```
/pg-orchestrator 66 pg/issue-66-backend pg/issue-66-frontend
```

> 參數：issue 編號（必填）、backend branch（選填）、frontend branch（選填）

### `/ai-docs-review`

審查 P1 三個 Repo 的文件狀況，依 `docs/ai-review/AI-review-prompt.md` 的 Phase 1–4 順序執行，輸出結構化建議報告。

```
/ai-docs-review
```
