# Stale Issue & Branch 自動清理設計

## 背景

三個開發 repo（P1-analysis、P1-design、P1-code）隨時間累積了停滯的 Issue 和孤立的 Branch，需要定期自動清理。

## 目標

- 自動偵測 30 天沒有活動的 open issue，先警告再關閉
- 關閉 issue 時一併刪除對應的 branch
- 所有清理邏輯集中在 P1-project 統一管理
- 同時修正 P1-code c-workflow 中 branch pattern 的 bug

---

## 架構

### 新增檔案

`P1-project/.github/workflows/stale-cleanup.yml`

### 修改檔案

`P1-code/.github/workflows/c-workflow.yml`（修正 branch pattern bug）

### 手動前置作業

三個 repo 各需建立兩個 label：
- `stale`（灰色）— 標記停滯的 issue
- `no-stale`（綠色）— 永久豁免，不受清理影響

---

## 觸發方式

```yaml
on:
  schedule:
    - cron: '0 2 * * 1'   # 每週一 UTC 02:00
  workflow_dispatch:        # 手動觸發（測試用）
```

---

## Job 設計

### Job 1：mark-stale

**目的：** 找出停滯 issue，加警告標籤

**邏輯：**
1. 對三個 repo 各別執行
2. 撈 `state: open` 的所有 issues
3. 過濾條件（同時滿足）：
   - `updated_at` 距今超過 30 天
   - 沒有 `stale` label
   - 沒有 `no-stale` label
   - `pull_request` 欄位為空（排除 PR）
4. 對每個符合的 issue：
   - 加 `stale` label
   - 留言：「此 Issue 已超過 30 天沒有活動，將在 7 天後自動關閉。如仍在進行中，請留言或移除 stale label。」

---

### Job 2：close-stale

**目的：** 關閉警告超過 7 天仍未回應的 issue，並刪除對應 branch

**依賴：** `needs: mark-stale`（確保同週期內 mark 先執行完）

**邏輯：**
1. 對三個 repo 各別執行
2. 撈有 `stale` label 且 `state: open` 的 issues
3. 用 `issues.listEvents` 找最近一次 `labeled` 為 `stale` 的事件時間
4. 若距今超過 7 天：
   - 關閉 issue（`state_reason: not_planned`）
   - 從 issue body 的「分支」欄位用 regex 抓 branch 名稱
   - 呼叫 `git.deleteRef` 刪除 branch
   - Branch 不存在時靜默略過，不中斷 job

**Branch 名稱解析：**

Issue body 中的分支欄位格式為：
```
分支：[branch-name](https://github.com/...)
```
用 regex `分支：\[([^\]]+)\]` 抓取 branch 名稱。

---

## Bug 修正：P1-code c-workflow

**問題：** `close-issues` job 的觸發條件使用 `issue-*`，但 D-workflow 實際建立的 P1-code branch 格式為 `pg-{N}-{slug}`，導致 PG Issue 和 Epic Issue 在 PR merge 後未被自動關閉。

**修正：** 將 c-workflow.yml 的 close-issues job 判斷條件從：
```
startsWith(github.event.pull_request.head.ref, 'issue-')
```
改為：
```
startsWith(github.event.pull_request.head.ref, 'pg-')
```

---

## 邊界條件

| 情境                              | 處理方式                 |
| ------------------------------- | -------------------- |
| Issue 有 `no-stale` label        | 永遠跳過，不標記、不關閉         |
| Issue 是 PR（`pull_request` 欄位非空） | 跳過                   |
| Issue body 找不到分支資訊              | 跳過刪 branch，只關閉 issue |
| Branch 已不存在                     | 靜默略過，繼續關閉 issue      |
| Branch 刪除 API 失敗                | 記錄 log，不中斷整個 job     |

---

## 執行紀錄

每次 job 結束於 workflow log 印出摘要，格式：

```
[P1-analysis] marked stale: #12, #15
[P1-design]   closed: #8 (branch sd-8-xxx deleted)
[P1-code]     no action
```

---

## 權限

使用現有 GitHub App token（`APP_ID` + `APP_PRIVATE_KEY` secrets），與其他 workflow 一致。所需 API 權限：
- `issues: write`
- `contents: write`（刪除 branch）
- `pull-requests: read`

---

## 實作清單

1. **P1-project** — 新增 `stale-cleanup.yml`
2. **P1-code** — 修改 `c-workflow.yml`（`issue-*` → `pg-*`）
3. **手動** — 三個 repo 各建立 `stale` / `no-stale` label
