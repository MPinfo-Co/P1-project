# Stale Issue & Branch 自動清理 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在 P1-project 建立集中式 stale-cleanup workflow，每週自動標記並關閉三個 repo 中 30 天沒活動的 issue，同時修正 P1-code c-workflow 的 branch pattern bug。

**Architecture:** 兩個 repo 各修改一個 workflow 檔案。P1-project 新增 `stale-cleanup.yml`（含 mark-stale 和 close-stale 兩個 job）；P1-code 修改 `c-workflow.yml`，將三處 `issue-*` pattern 統一改為 `pg-*`。兩者都透過 GitHub App token 操作跨 repo 的 issues 和 branches。

**Tech Stack:** GitHub Actions, actions/github-script@v7, tibdex/github-app-token@v2

---

## 檔案清單

| 操作 | 檔案 |
|------|------|
| Create | `P1-project/.github/workflows/stale-cleanup.yml` |
| Modify | `P1-code/.github/workflows/c-workflow.yml`（5 處 pattern 修正）|

---

## Task 1：修正 P1-code c-workflow.yml 的 branch pattern bug

**Files:**
- Modify: `P1-code/.github/workflows/c-workflow.yml`

c-workflow.yml 有 5 處使用舊的 `issue-*` pattern，但 P1-code 的 branch 實際格式為 `pg-{N}-{slug}`，需全部更新。

- [ ] **Step 1：更新 push trigger**

將 `c-workflow.yml` 第 7 行：
```yaml
      - 'issue-*'
```
改為：
```yaml
      - 'pg-*'
```

- [ ] **Step 2：更新 notify-test-env job 的 if 條件**

將第 79 行：
```yaml
    if: startsWith(github.event.pull_request.head.ref, 'issue-')
```
改為：
```yaml
    if: startsWith(github.event.pull_request.head.ref, 'pg-')
```

- [ ] **Step 3：更新 notify-test-env job 的 script 內 regex**

將第 95 行：
```javascript
            const match = branch.match(/^issue-(\d+)/);
```
改為：
```javascript
            const match = branch.match(/^pg-(\d+)/);
```

- [ ] **Step 4：更新 close-issues job 的 if 條件**

將第 121-123 行：
```yaml
    if: >
      github.event.pull_request.merged == true &&
      startsWith(github.event.pull_request.head.ref, 'issue-')
```
改為：
```yaml
    if: >
      github.event.pull_request.merged == true &&
      startsWith(github.event.pull_request.head.ref, 'pg-')
```

- [ ] **Step 5：更新 close-issues job 的 script 內 regex**

將第 139-140 行：
```javascript
            const match = branchName.match(/^issue-(\d+)-/);
            const issueNum = match ? match[1] : branchName.replace(/^issue-/, '').split('-')[0];
```
改為：
```javascript
            const match = branchName.match(/^pg-(\d+)-/);
            const issueNum = match ? match[1] : branchName.replace(/^pg-/, '').split('-')[0];
```

- [ ] **Step 6：驗證 YAML 語法**

```bash
python3 -c "import yaml; yaml.safe_load(open('/mnt/c/dev/AIDC_Github/P1-code/.github/workflows/c-workflow.yml')); print('YAML OK')"
```
Expected output: `YAML OK`

- [ ] **Step 7：Commit**

```bash
git -C /mnt/c/dev/AIDC_Github/P1-code add .github/workflows/c-workflow.yml
git -C /mnt/c/dev/AIDC_Github/P1-code commit -m "fix(c-workflow): 修正 branch pattern 從 issue-* 改為 pg-*"
```

---

## Task 2：建立 stale-cleanup.yml（mark-stale job）

**Files:**
- Create: `P1-project/.github/workflows/stale-cleanup.yml`

- [ ] **Step 1：建立檔案，寫入 workflow 基本結構與 mark-stale job**

建立 `P1-project/.github/workflows/stale-cleanup.yml`，內容如下：

```yaml
name: Stale Cleanup

on:
  schedule:
    - cron: '0 2 * * 1'
  workflow_dispatch:

permissions:
  issues: write
  contents: write

jobs:
  mark-stale:
    name: Mark Stale Issues
    runs-on: ubuntu-latest

    steps:
      - name: Create GitHub App token
        id: app-token
        uses: tibdex/github-app-token@v2
        with:
          app_id: ${{ secrets.APP_ID }}
          private_key: ${{ secrets.APP_PRIVATE_KEY }}

      - name: Mark stale issues across repos
        uses: actions/github-script@v7
        with:
          github-token: ${{ steps.app-token.outputs.token }}
          script: |
            const org = 'MPinfo-Co';
            const repos = ['P1-analysis', 'P1-design', 'P1-code'];
            const STALE_DAYS = 30;
            const now = new Date();

            for (const repo of repos) {
              const marked = [];

              const issues = await github.paginate(github.rest.issues.listForRepo, {
                owner: org,
                repo,
                state: 'open',
                per_page: 100,
              });

              for (const issue of issues) {
                if (issue.pull_request) continue;

                const labels = issue.labels.map(l => l.name);
                if (labels.includes('stale') || labels.includes('no-stale')) continue;

                const daysSince = (now - new Date(issue.updated_at)) / (1000 * 60 * 60 * 24);
                if (daysSince <= STALE_DAYS) continue;

                await github.rest.issues.addLabels({
                  owner: org,
                  repo,
                  issue_number: issue.number,
                  labels: ['stale'],
                });

                await github.rest.issues.createComment({
                  owner: org,
                  repo,
                  issue_number: issue.number,
                  body: '此 Issue 已超過 30 天沒有活動，將在 7 天後自動關閉。如仍在進行中，請留言或移除 stale label。',
                });

                marked.push(`#${issue.number}`);
              }

              console.log(`[${repo}] marked stale: ${marked.length > 0 ? marked.join(', ') : 'none'}`);
            }
```

- [ ] **Step 2：驗證 YAML 語法**

```bash
python3 -c "import yaml; yaml.safe_load(open('/mnt/c/dev/AIDC_Github/P1-project/.github/workflows/stale-cleanup.yml')); print('YAML OK')"
```
Expected output: `YAML OK`

- [ ] **Step 3：Commit**

```bash
git -C /mnt/c/dev/AIDC_Github/P1-project add .github/workflows/stale-cleanup.yml
git -C /mnt/c/dev/AIDC_Github/P1-project commit -m "feat(stale-cleanup): 新增 mark-stale job"
```

---

## Task 3：加入 close-stale job

**Files:**
- Modify: `P1-project/.github/workflows/stale-cleanup.yml`

- [ ] **Step 1：在 mark-stale job 後面加入 close-stale job**

在 `stale-cleanup.yml` 末尾（`mark-stale` job 結束後）附加：

```yaml
  close-stale:
    name: Close Stale Issues
    runs-on: ubuntu-latest
    needs: mark-stale

    steps:
      - name: Create GitHub App token
        id: app-token
        uses: tibdex/github-app-token@v2
        with:
          app_id: ${{ secrets.APP_ID }}
          private_key: ${{ secrets.APP_PRIVATE_KEY }}

      - name: Close stale issues and delete branches
        uses: actions/github-script@v7
        with:
          github-token: ${{ steps.app-token.outputs.token }}
          script: |
            const org = 'MPinfo-Co';
            const repos = ['P1-analysis', 'P1-design', 'P1-code'];
            const WARN_DAYS = 7;
            const now = new Date();

            for (const repo of repos) {
              const closed = [];

              const issues = await github.paginate(github.rest.issues.listForRepo, {
                owner: org,
                repo,
                state: 'open',
                labels: 'stale',
                per_page: 100,
              });

              for (const issue of issues) {
                if (issue.pull_request) continue;

                const events = await github.paginate(github.rest.issues.listEvents, {
                  owner: org,
                  repo,
                  issue_number: issue.number,
                  per_page: 100,
                });

                const staleLabelEvent = events
                  .filter(e => e.event === 'labeled' && e.label?.name === 'stale')
                  .sort((a, b) => new Date(b.created_at) - new Date(a.created_at))[0];

                if (!staleLabelEvent) continue;

                const daysSinceLabel = (now - new Date(staleLabelEvent.created_at)) / (1000 * 60 * 60 * 24);
                if (daysSinceLabel <= WARN_DAYS) continue;

                // 從 issue body 抓 branch 名稱
                const branchMatch = (issue.body || '').match(/分支：\[([^\]]+)\]/);
                const branchName = branchMatch ? branchMatch[1] : null;

                await github.rest.issues.update({
                  owner: org,
                  repo,
                  issue_number: issue.number,
                  state: 'closed',
                  state_reason: 'not_planned',
                });

                let branchStatus = '（無 branch 資訊）';
                if (branchName) {
                  try {
                    await github.rest.git.deleteRef({
                      owner: org,
                      repo,
                      ref: `heads/${branchName}`,
                    });
                    branchStatus = `branch ${branchName} deleted`;
                  } catch (e) {
                    branchStatus = `branch ${branchName} not found`;
                  }
                }

                closed.push(`#${issue.number} (${branchStatus})`);
              }

              console.log(`[${repo}] closed: ${closed.length > 0 ? closed.join(', ') : 'none'}`);
            }
```

- [ ] **Step 2：驗證 YAML 語法**

```bash
python3 -c "import yaml; yaml.safe_load(open('/mnt/c/dev/AIDC_Github/P1-project/.github/workflows/stale-cleanup.yml')); print('YAML OK')"
```
Expected output: `YAML OK`

- [ ] **Step 3：Commit**

```bash
git -C /mnt/c/dev/AIDC_Github/P1-project add .github/workflows/stale-cleanup.yml
git -C /mnt/c/dev/AIDC_Github/P1-project commit -m "feat(stale-cleanup): 加入 close-stale job"
```

---

## Task 4：手動建立 Labels（GitHub Web UI）

**這是手動步驟，不需要寫 code。**

依序在三個 repo 的 Labels 頁面各建立以下兩個 label：

**P1-analysis / P1-design / P1-code → Issues → Labels → New label**

| Label | 顏色 | 說明 |
|-------|------|------|
| `stale` | `#808080`（灰） | 停滯超過 30 天，待關閉 |
| `no-stale` | `#2da44e`（綠） | 永久豁免，不自動關閉 |

- [ ] **Step 1：在 P1-analysis 建立 `stale` 和 `no-stale` label**
- [ ] **Step 2：在 P1-design 建立 `stale` 和 `no-stale` label**
- [ ] **Step 3：在 P1-code 建立 `stale` 和 `no-stale` label**

---

## Task 5：Push 並觸發測試

- [ ] **Step 1：push P1-code 的修改**

```bash
git -C /mnt/c/dev/AIDC_Github/P1-code push
```

- [ ] **Step 2：push P1-project 的修改**

```bash
git -C /mnt/c/dev/AIDC_Github/P1-project push
```

- [ ] **Step 3：手動觸發 stale-cleanup workflow 測試**

前往 GitHub → P1-project → Actions → Stale Cleanup → Run workflow

確認：
- workflow 成功執行
- log 中看到 `[P1-analysis] marked stale: ...` 等輸出
- 無 API 錯誤（token 權限、label 不存在等）
