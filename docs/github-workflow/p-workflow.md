# p-workflow

## 用途
Epic Issue 加上 `epic` label 時，自動在 P1-analysis 建立 SA Issue、A-Branch 與 Draft PR。

## 觸發條件
- Repo：P1-project
- 事件：`issues: labeled`
- Label：`epic`

## 執行步驟
1. 在 P1-analysis 建立 SA Issue（標題加 `[SA]` 前綴）
2. 將 SA Issue 掛為 Epic 的 sub-issue
3. 取得 P1-analysis main SHA，建立 A-Branch（`issue-{N}-{slug}`）
4. Scaffold `issue-{N}/business-logic.md` 與 `issue-{N}/SD-WBS.md`
5. 建立 SA Draft PR
6. 回填 SA Issue body（加入分支連結、Draft PR 連結）
7. 更新 Epic Issue body（加入「關聯 Issue」區塊）
8. 在 Epic Issue 留言通知

## 輸入
| 來源 | 欄位 |
|------|------|
| Epic Issue | `title`（去除 `[PM]` 前綴後用作 slug） |
| Epic Issue | `number`（用作關聯項目） |

## 輸出
| 產出 | 位置 |
|------|------|
| SA Issue | P1-analysis |
| A-Branch | P1-analysis（`issue-{N}-{slug}`） |
| `issue-{N}/business-logic.md` | P1-analysis A-Branch |
| `issue-{N}/SD-WBS.md` | P1-analysis A-Branch |
| SA Draft PR | P1-analysis |
