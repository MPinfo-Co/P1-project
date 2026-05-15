---
name: pull-p1-repos
description: Use when starting work on P1 project to pull latest main from all 3 repos (P1-project, P1-design, P1-code). Run from WorkX/P1 root directory.
---

# Pull All P1 Repos

Pull latest main from all 3 repos in the current P1 workspace. Works from any WorkX/P1 root.

## Steps

Use absolute paths to avoid working directory issues:

```bash
P1_ROOT=$(git -C . rev-parse --show-toplevel 2>/dev/null | sed 's|/P1-.*||') 
# If above fails, hardcode: P1_ROOT="/Users/rex/Desktop/Work03/P1"
for repo in P1-project P1-design P1-code; do
  echo "=== $repo ==="
  git -C "$P1_ROOT/$repo" pull origin main
done
```

Then install backend dependencies if P1-code was updated:

```bash
"$P1_ROOT/P1-code/backend/.venv/bin/python" -m pip install -r "$P1_ROOT/P1-code/backend/requirements.txt"
```

Then run `/sync-claude-md` to merge CLAUDE.md.

Then run `/clean-branch-files` to remove local files not on remote.
