# GitHub Projects 看板使用指南

> [← 回到總導覽](../README.md)


## MP-BOX專案看板 [MP-BOX Project Board](https://github.com/orgs/MPinfo-Co/projects/4)

---

![[Pasted image 20260414153338.png]]

## Views(頁籤) 說明

| View(頁籤名稱)   | 使用者 | 用途                           |
| ------------ | --- | ---------------------------- |
| 工作管理(PM)     | PM  | 無篩選全覽，分派週期給所有工作              |
| 近期工作(PM)     | PM  | 調整項目欄位內容                     |
| 專案週報(PM)     | PM  | 向上報告                         |
| 工作管理(Member) | 全員  | 查詢管理自己的工作（預設 `assignee:@me`） |
| 工作規劃(Member) | 全員  | 填入個人實際 Start / Target date   |


---

## 看板欄位說明

| 欄位                      | 用途                                           |
| ----------------------- | -------------------------------------------- |
| **Status**              | 工作階段 idea → Next → Todo → In progress → Done |
| **Scope**               | 分類標記（MP-Box / 資安專家 / Learn / Other）          |
| **週期**                  | 所屬工作週（5 天一個週期，PM 分配）                         |
| **Start / Target date** | 工作者填入實際開始與完成日                                |
| **Estimate**            | 預估工時（單位：天，導入中）                               |
| **References**          | Learn 項目的學習筆記連結（純網址或 `[標題](網址)`）             |
| **Parent issue**        | 上層 Epic                                      |
| **Sub-issues progress** | 子 issue 完成比例（自動計算）                           |

## Status 狀態說明

| 狀態           | 說明                        |
| ------------ | ------------------------- |
| idea         | 剛進來的想法，未評估                |
| Next         | 評估可行，下版本候補                |
| Todo         | 本版本（本季）確認要做               |
| In progress  | 進行中（上限 2 個）               |
| Done         | 完成                        |

> 一季一個版本（Q1/Q2/Q3/Q4）， todo項目 即為當季(新版本)工作

---



## 工作步驟

1. 在**工作管理(Member)頁籤** 中，整理自己的工作
2. 選擇欲執行的 Todo 項目，將對應工作 Status 切換為 **「In progress」** 
3. Pull 對應的分支到Local環境，開始作業
4. 作業完成後，將 Draft PR 改為 **「Ready for review」** 
5. 等待Approve
6. Merge
7. 在**工作規劃(Member)頁籤** 中，透過**點擊**填入實際完成時間 Start / Target date 

> WIP 原則：**同時 In progress 不超過 3 個，控制在2個之內**。
> **自動化串接流程**與各**角色職責**詳見 [workflow_guide.md](workflow_guide.md)。

