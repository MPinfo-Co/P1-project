---
name: clean-branch-files
description: Use after pulling a branch to remove local files that don't exist on remote. Cleans untracked files while preserving .venv, node_modules, and .env files.
---

# Clean Branch Files

pull 分支後，清除 remote 沒有的本地檔案。

## Steps

### 1. Dry-run

```bash
git clean -fdn -e .venv -e node_modules -e .env
```

### 2. 分類報告

將 dry-run 結果依下列分類整理後呈現給使用者：

| 分類 | 判斷條件 |
|------|---------|
| macOS 系統檔 | `.DS_Store`、`__MACOSX/` |
| 重複檔案 | 檔名含空格加數字，如 `* 2.py`、`* 2` |
| 其他 untracked 檔 | 不符合以上條件 |

格式範例：
```
【macOS 系統檔】1 個（無風險）
  - .DS_Store

【重複檔案】28 個（無風險）
  - app/api/notice 2.py
  - ...

【其他 untracked 檔】0 個（低風險：可能含自行新增的設定或草稿，請確認）
```

若清單為空則結束，不需確認。

### 3. 確認後執行

使用者確認後才執行：

```bash
git clean -fd -e .venv -e node_modules -e .env
```
