# a-workflow

> [← 回到總導覽](../../../README.md)

## 用途
P1-analysis 的 `issue-*` branch PR merge 到 main 時，自動在 P1-design 建立 SD Issue、D-Branch 與 Draft PR。

## 觸發條件
- Repo：P1-analysis
- 事件：`pull_request: closed`（merged == true）
- Branch 條件：head.ref 以 `issue-` 開頭

## 執行步驟
1. 從 branch 名稱取出 SA Issue 編號
2. 讀取 SA Issue body，取得 Epic 編號
3. 從 Epic Issue 取乾淨標題（去除 `[PM]` 前綴）
4. 讀取 `issue-{N}/SD-WBS.md` 內容（merge 後已在 main）
5. 在 P1-design 建立 SD Issue（標題加 `[SD]` 前綴，含 WBS 內容）
6. 將 SD Issue 掛為 Epic 的 sub-issue
7. 建立 D-Branch（`issue-{N}-{slug}`）
8. Scaffold `TDD/issue-{N}.md`
9. 建立 SD Draft PR
10. 回填 SD Issue body（分支連結、Draft PR 連結）
11. 更新 Epic Issue body（填入 SD Issue 連結）
12. 回填 SA Issue body（填入 SD Issue 連結）
13. 在 SA Issue 與 Epic Issue 留言通知
14. 關閉 SA Issue

## 輸入
| 來源 | 欄位 |
|------|------|
| PR head.ref | SA Issue 編號（`issue-{N}-*`） |
| SA Issue body | Epic 編號 |
| Epic Issue | title（用作 SD Issue 標題與 slug） |
| `issue-{N}/SD-WBS.md` | WBS 工作項目清單 |

## 輸出
| 產出 | 位置 |
|------|------|
| SD Issue | P1-design |
| D-Branch | P1-design（`issue-{N}-{slug}`） |
| `TDD/issue-{N}.md` | P1-design D-Branch |
| SD Draft PR | P1-design |
