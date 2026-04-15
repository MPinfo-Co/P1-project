# 設計文件：Draft Issue 建立者自動指派

**日期：** 2026-04-15  
**狀態：** 待實作

---

## 需求

在 MPinfo-Co GitHub 組織下，當任何人建立 Draft Issue（不填 assignee）時，自動將該 Draft Issue 指派給建立者本人。

**範圍限制：**
- 僅針對 `DraftIssue` 類型（排除 real issue 及 PR）
- 僅在**建立時**觸發（不補填已存在的空 assignee）
- 僅在 assignees 為空時才指派（已有指派者不覆蓋）

---

## 架構

### 新增 Repo

建立 `MPinfo-Co/.github`（GitHub 組織特殊用途 repo），用於存放 org-level workflow。

### 檔案結構

```
MPinfo-Co/.github/
└── workflows/
    └── auto-assign-draft-issue.yml
```

### 觸發事件

```yaml
on:
  projects_v2_item:
    types: [created]
```

`projects_v2_item.created` 為 org-level 事件，覆蓋 MPinfo-Co 下所有 GitHub Projects。

---

## 執行流程

```
Draft Issue 建立（无 assignee）
  └─ projects_v2_item.created 觸發
      └─ 取得 GitHub App token
          └─ GraphQL：查詢 draft issue 的 assignees
              └─ assignees 為空？
                  ├─ 否 → 跳過
                  └─ 是 → GraphQL updateProjectV2DraftIssue
                              assigneeIds = [sender.node_id]
```

---

## 技術細節

### 權限

使用現有 GitHub App（`APP_ID` + `APP_PRIVATE_KEY`），需確認 App 具備：
- `projects: write`（操作 Projects v2 必要權限）

### Secrets 設定

在 `MPinfo-Co/.github` repo 的 Settings > Secrets 加入：
- `APP_ID`
- `APP_PRIVATE_KEY`

（與其他 repo 相同的值，需手動同步）

### GraphQL Mutation

```graphql
mutation($draftIssueId: ID!, $assigneeIds: [ID!]!) {
  updateProjectV2DraftIssue(input: {
    draftIssueId: $draftIssueId,
    assigneeIds: $assigneeIds
  }) {
    draftIssue {
      assignees(first: 5) {
        nodes { login }
      }
    }
  }
}
```

`draftIssueId` 來自 `event.projects_v2_item.content_node_id`  
`assigneeIds` 來自 `event.sender.node_id`

---

## 風險與對策

| 風險 | 說明 | 對策 |
|------|------|------|
| App 缺少 projects 權限 | 現有 App 只授權 issues/contents/pull-requests | 建立前確認 App scopes，必要時新增 |
| Secrets 未同步 | `.github` repo 不繼承其他 repo 的 secrets | 建立後手動在新 repo 設定 secrets |

---

## 不在範圍內

- 已存在但無 assignee 的 draft issue（不回填）
- Real issue 的自動指派（另有 GitHub 設定可處理）
- 多人指派邏輯
