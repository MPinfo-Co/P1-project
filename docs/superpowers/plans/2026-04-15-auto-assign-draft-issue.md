# Auto-Assign Draft Issue Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在 MPinfo-Co 組織下，任何人建立 Draft Issue 沒有填 assignee 時，自動指派給建立者本人。

**Architecture:** 在新建的 `MPinfo-Co/.github` repo 放一個 org-level workflow，監聽 `projects_v2_item.created` 事件。偵測到 DraftIssue 且 assignees 為空時，用 GraphQL 把 sender 設為 assignee。

**Tech Stack:** GitHub Actions, GitHub App (tibdex/github-app-token@v2), actions/github-script@v7, GitHub GraphQL API v4

---

## 前置確認

**已知：**
- `APP_ID` 和 `APP_PRIVATE_KEY` 存在於 P1-project secrets（需手動同步到 .github repo）
- `MPinfo-Co/.github` 目前不存在

**需人工確認：**
- GitHub App 是否有 `Projects: Read & Write` 權限（見 Task 1）

---

### Task 1：確認 GitHub App 的 Projects 權限

**目標：** 確保 App 有操作 Projects v2 draft issue 的權限

- [ ] **Step 1：開啟 GitHub App 設定頁**

前往：`https://github.com/organizations/MPinfo-Co/settings/apps`  
找到目前使用的 App，點擊 **Edit**

- [ ] **Step 2：確認 Permissions**

在 **Repository permissions** 或 **Organization permissions** 區段，確認：
- `Projects` → `Read and write`

若沒有，將其設定為 `Read and write`，按 **Save changes**

- [ ] **Step 3：接受權限更新請求**

GitHub 會發送 email 通知 org owner 需要審核新增的權限，前往：  
`https://github.com/organizations/MPinfo-Co/settings/installations`  
找到該 App，點擊 **Review request** 並 **Accept**

---

### Task 2：建立 MPinfo-Co/.github repo

**Files:**
- Create: `MPinfo-Co/.github`（GitHub repo，非本機檔案）

- [ ] **Step 1：建立 repo**

```bash
gh repo create MPinfo-Co/.github --public --description "MPinfo-Co org-level GitHub configurations"
```

預期輸出：
```
✓ Created repository MPinfo-Co/.github on GitHub
```

- [ ] **Step 2：確認建立成功**

```bash
gh repo view MPinfo-Co/.github --json name,visibility
```

預期輸出：
```json
{"name":".github","visibility":"PUBLIC"}
```

---

### Task 3：在 .github repo 設定 Secrets

**目標：** 將 APP_ID 和 APP_PRIVATE_KEY 同步到新 repo

- [ ] **Step 1：取得現有 APP_ID 的值**

前往 GitHub：`https://github.com/organizations/MPinfo-Co/settings/apps`  
開啟目前使用的 App，複製 **App ID**（數字）

- [ ] **Step 2：設定 APP_ID secret**

```bash
gh secret set APP_ID --repo MPinfo-Co/.github
```

提示輸入時，貼上 App ID 數字值

- [ ] **Step 3：取得 APP_PRIVATE_KEY**

在同一個 App 設定頁，下載 private key（`.pem` 檔），或從現有 repo 複製使用中的值。

- [ ] **Step 4：設定 APP_PRIVATE_KEY secret**

```bash
gh secret set APP_PRIVATE_KEY --repo MPinfo-Co/.github < path/to/private-key.pem
```

- [ ] **Step 5：確認兩個 secrets 都存在**

```bash
gh secret list --repo MPinfo-Co/.github
```

預期輸出：
```
APP_ID           Updated ...
APP_PRIVATE_KEY  Updated ...
```

---

### Task 4：建立 Workflow 檔案

**Files:**
- Create: `.github/workflows/auto-assign-draft-issue.yml`（在 MPinfo-Co/.github repo 中）

- [ ] **Step 1：clone .github repo**

```bash
gh repo clone MPinfo-Co/.github /tmp/mpinfo-github
cd /tmp/mpinfo-github
mkdir -p .github/workflows
```

- [ ] **Step 2：建立 workflow 檔案**

建立 `/tmp/mpinfo-github/.github/workflows/auto-assign-draft-issue.yml`，內容如下：

```yaml
name: Auto-assign Draft Issue to Creator

on:
  projects_v2_item:
    types: [created]

permissions:
  contents: read

jobs:
  auto-assign:
    if: github.event.projects_v2_item.content_type == 'DraftIssue'
    runs-on: ubuntu-latest

    steps:
      - name: Create GitHub App token
        id: app-token
        uses: tibdex/github-app-token@v2
        with:
          app_id: ${{ secrets.APP_ID }}
          private_key: ${{ secrets.APP_PRIVATE_KEY }}

      - name: Assign creator to draft issue
        uses: actions/github-script@v7
        with:
          github-token: ${{ steps.app-token.outputs.token }}
          script: |
            const draftIssueId = context.payload.projects_v2_item.content_node_id;
            const senderNodeId = context.payload.sender.node_id;

            // 查詢目前的 assignees
            const queryResult = await github.graphql(`
              query($id: ID!) {
                node(id: $id) {
                  ... on ProjectV2DraftIssue {
                    assignees(first: 5) {
                      nodes { id login }
                    }
                  }
                }
              }
            `, { id: draftIssueId });

            const assignees = queryResult.node?.assignees?.nodes ?? [];

            if (assignees.length > 0) {
              console.log(`已有 assignee（${assignees.map(a => a.login).join(', ')}），跳過`);
              return;
            }

            // 指派給建立者
            await github.graphql(`
              mutation($draftIssueId: ID!, $assigneeIds: [ID!]!) {
                updateProjectV2DraftIssue(input: {
                  draftIssueId: $draftIssueId
                  assigneeIds: $assigneeIds
                }) {
                  draftIssue {
                    assignees(first: 5) {
                      nodes { login }
                    }
                  }
                }
              }
            `, {
              draftIssueId,
              assigneeIds: [senderNodeId],
            });

            console.log(`✅ Draft Issue 已指派給 ${context.payload.sender.login}`);
```

- [ ] **Step 3：commit 並 push**

```bash
cd /tmp/mpinfo-github
git add .github/workflows/auto-assign-draft-issue.yml
git commit -m "feat: auto-assign draft issue to creator"
git push origin main
```

預期輸出：
```
[main ...] feat: auto-assign draft issue to creator
...
To https://github.com/MPinfo-Co/.github.git
   ... main -> main
```

---

### Task 5：冒煙測試

**目標：** 確認 workflow 實際運作

- [ ] **Step 1：前往任一 GitHub Project**

開啟 MPinfo-Co 下的任何 GitHub Project（如 P1 board）

- [ ] **Step 2：建立 Draft Issue，不填 assignee**

點擊 **Add item** → 輸入標題 → 按 Enter  
**不要**填寫 assignee 欄位

- [ ] **Step 3：確認 Workflow 觸發**

前往：`https://github.com/MPinfo-Co/.github/actions`  
確認 **Auto-assign Draft Issue to Creator** workflow 有執行記錄，狀態為 ✅

- [ ] **Step 4：確認 assignee 已填入**

回到 GitHub Project，確認剛建立的 Draft Issue 的 Assignee 欄位已自動填入你的帳號

- [ ] **Step 5：測試有 assignee 的情況（確認不會覆蓋）**

再建立一個 Draft Issue，手動填入其他人為 assignee，確認 workflow 執行後 assignee **沒有**被改成建立者

---

## 清理

測試完成後，刪除測試用的 Draft Issue：在 Project 中選取並刪除即可。
