# chore-workflow（a- / d- / c-）

> [← 回到總導覽](../../../README.md)

## 用途
Issue 加上 `chore` label 時，自動建立對應的 chore branch，讓對應角色（SA／SD／PG）可直接 checkout 開始作業。

## 觸發條件
- Repo：P1-analysis（a-chore-workflow.yml）、P1-design（d-chore-workflow.yml）、P1-code（c-chore-workflow.yml）
- 事件：`issues: labeled`
- Label：`chore`

## 執行步驟
1. 從 Issue 標題產生 slug（去除 `[Chore]` 前綴、轉小寫、特殊字元轉 `-`）
2. 建立 branch（`chore-{N}-{slug}`）
3. 在 Issue 留言通知分支名稱與操作說明

## 輸入
| 來源 | 欄位 |
|------|------|
| Issue | `number`（用作 branch 編號） |
| Issue | `title`（用作 slug） |

## 輸出
| 產出 | 位置 |
|------|------|
| chore branch（`chore-{N}-{slug}`） | 同 Repo |
| Issue 留言 | 同 Issue |

## 注意
三個 Repo 的 chore-workflow 邏輯完全相同，只有檔名不同（`a-`/`d-`/`c-` 前綴）。
