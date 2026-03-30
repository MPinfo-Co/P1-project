# c-workflow

## 用途
P1-code 的 CI 流程：push 時執行靜態檢查與測試；PR 開啟時通知測試環境設定；PR merge 時產生 VersionDiff 並關閉 PG Issue。

## 觸發條件
| 事件 | 觸發 Job |
|------|---------|
| push 到 `issue-*` branch | backend-ci、frontend-ci |
| PR opened to main（issue-* branch） | notify-test-env |
| PR merged to main（issue-* branch） | generate-version-diff |

## Jobs

### backend-ci
- `ruff check .`（Lint）
- `pytest tests/ -v`

### frontend-ci
- `npm run lint`（ESLint）

### notify-test-env
PR 開啟時，在 PR 留言測試環境 checklist：
- 啟動後端（uvicorn）
- 啟動前端（npm run dev）
- 確認資料庫連線
- 依 TestPlan 執行測試，填寫測試報告

### generate-version-diff
PR merge 後：
1. 取得 PR 異動的所有檔案（最多 300 筆）
2. 產生 `VersionDiff/issue-{N}_{author}_{date}.md`
3. 關閉對應的 PG Issue

## 輸出
| 產出 | 位置 |
|------|------|
| `VersionDiff/issue-{N}_{author}_{date}.md` | P1-code main |
| PG Issue 狀態 | 自動關閉 |
