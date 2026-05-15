---
name: sync-claude-md
description: Use when syncing CLAUDE.md from P1-project (canonical source) to the local P1 workspace root. P1-project is always authoritative — workspace copy is overwritten.
---

# Sync CLAUDE.md

P1-project → workspace（單向覆蓋）

## Steps

```bash
P1_ROOT=$(pwd | sed 's|/P1-[^/]*.*||')
cp "$P1_ROOT/P1-project/CLAUDE.md" "$P1_ROOT/CLAUDE.md"
diff "$P1_ROOT/P1-project/CLAUDE.md" "$P1_ROOT/CLAUDE.md" && echo "identical"
```
