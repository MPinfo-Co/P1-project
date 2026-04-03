# d-workflow

> [← 回到總導覽](../../../README.md)

## 用途
P1-design 的 `issue-*` branch PR merge 到 main 時，自動在 P1-code 建立 PG Issue、C-Branch 與 Draft PR，並產生 TestPlan diff 檔案。

## 觸發條件
- Repo：P1-design
- 事件：`pull_request: closed`（merged == true）
- Branch 條件：head.ref 以 `issue-` 開頭

## Step 1：Create PG Issue
1. 從 branch 名稱取出 SD Issue 編號
2. 讀取 SD Issue body，取得 Epic + SA 編號
3. 從 Epic Issue 取乾淨標題（去除 `[PM]` 前綴）
4. 列出 PR 異動的 `schema/`、`Prototype/`、`Spec/` 檔案（順序：schema → Prototype → Spec）
5. 在 P1-code 建立 PG Issue（含異動檔案清單）
6. 將 PG Issue 掛為 Epic 的 sub-issue
7. 取得 P1-code main SHA，建立 C-Branch（`issue-{N}-{slug}`）
8. Scaffold `PG測試報告/issue-{N}.md`
9. 建立 PG Draft PR
10. 回填 PG Issue body（PG Issue 編號、分支連結、Draft PR 連結）
11. 更新 Epic Issue body（填入 PG Issue 連結）
12. 回填 SD Issue body（填入 PG Issue 連結）
13. 在 SD Issue 與 Epic Issue 留言通知
14. 關閉 SD Issue

## Step 2：Generate TestPlan diff
1. 使用 Step 1 第 4 步已取得的異動檔案清單（順序：schema → Prototype → Spec）
2. 寫入 `TestPlan/issue-{N}-diff.md`

## 輸入
| 來源 | 欄位 |
|------|------|
| PR head.ref | SD Issue 編號（`issue-{N}-*`） |
| SD Issue body | Epic 編號、SA 編號 |
| Epic Issue | title |
| PR files | 異動的 schema/、Prototype/、Spec/ 檔案清單與 patch 內容 |

## 輸出
| 產出 | 位置 |
|------|------|
| PG Issue | P1-code |
| C-Branch | P1-code（`issue-{N}-{slug}`） |
| `PG測試報告/issue-{N}.md` | P1-code C-Branch |
| PG Draft PR | P1-code |
| `TestPlan/issue-{N}-diff.md` | P1-design main |
