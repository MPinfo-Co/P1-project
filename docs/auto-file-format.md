# 自動產生 md 文件格式規範

> [← 回到 workflow_guide.md](workflow_guide.md)

各階段由 GitHub Actions workflow 自動建立的 md 文件，格式如下。

---

## business-logic.md

由 [p-workflow.yml](https://github.com/MPinfo-Co/P1-project/blob/main/.github/workflows/p-workflow.yml) 產生，SA 人工填寫。

```markdown
# 業務邏輯分析：{功能標題}

## 需求說明
（PM 填寫的原始需求描述，不修改）

## 畫面/操作邏輯示意（選填）
（需求涉及使用者操作流程時填入；描述版面配置、操作步驟與互動行為）
```

---

## TDD/issue-{N}.md

由 [a-workflow.yml](https://github.com/MPinfo-Co/P1-analysis/blob/main/.github/workflows/a-workflow.yml) 產生，SD 人工填寫。

```markdown
# TDD：[SD] {功能標題}

## 工作項目
| # | 類型 | 工作內容 | 參照規格 |
|---|------|--------|--------|
| 1 | API  | 建立 fn_xxx_add_api | [Spec/fn_xxx/Api/fn_xxx_add_api.md](../Spec/fn_xxx/Api/fn_xxx_add_api.md) |
| 2 | 畫面 | 建立 fn_xxx_01_list | [Spec/fn_xxx/fn_xxx_01_list.md](../Spec/fn_xxx/fn_xxx_01_list.md) |
| 3 | Test | 建立 _fn_xxx_test_api.md | [Spec/fn_xxx/Api/_fn_xxx_test_api.md](../Spec/fn_xxx/Api/_fn_xxx_test_api.md) |
```

> 類型限定：`Schema`、`API`、`畫面`、`Test`、`其他`

---

## TestReport/issue-{N}.md

由 [d-workflow.yml](https://github.com/MPinfo-Co/P1-design/blob/main/.github/workflows/d-workflow.yml) 產生，PG 人工填寫。

```markdown
# TestReport：[SD] {功能標題}

## 工作項目
| # | 類型 | 說明 | PG執行註記 |
|---|------|------|---|
| 1 | API  | POST /api/leaves（建立請假申請） |  |
| 2 | 畫面 | 請假申請表單 |  |

## 測試案例
| ID | 類型 | 前置條件 | 操作 | 預期結果 | PG執行註記 |
|----|------|---------|------|---------|---|
| T1 | 整合 | 登入 Tenant A | POST /api/leaves | 201，回傳 leave_id |  |
| T2 | 整合 | 未登入 | POST /api/leaves | 401 Unauthorized |  |
| T3 | 畫面 | 登入狀態 | 填寫表單，結束日早於開始日 | 顯示日期錯誤提示，禁止送出 |  |
```

> PG執行註記：工作項目填「已執行」或簡短註記；測試案例填「通過」、「失敗」或簡短註記。

---

## Spec/{fn_xxx}/Api/_{fn_xxx}_test_api.md

由 SD 人工建立與維護，活文件。

```markdown
# {功能} API 測試規格

> 活文件：每次 SD 有 API 異動時同步更新，ID 累積不重置。

| ID | 說明 | 前置條件 | 操作 | 預期結果 |
|----|------|----------|------|----------|
| T1 | 新增成功 | 已登入且具權限 | POST /api/xxx，傳入有效資料 | 201 新增成功 |
| T2 | 新增失敗（重複） | 已登入且具權限，資料已存在 | POST /api/xxx，傳入重複資料 | 400 {錯誤訊息} |
```

---

## SpecDiff/issue-{N}.md

由 [d-workflow.yml](https://github.com/MPinfo-Co/P1-design/blob/main/.github/workflows/d-workflow.yml) 產生，勿手動編輯。

```markdown
# SpecDiff：Issue #N 標題

## 修改項目及內容
- **Spec/02HomeAPI.md**（added，+20 -0）
  {diff 內容}
- **Prototype/03B.html**（modified，+5 -2）
  {diff 內容}

## 關聯項目
- Epic：MPinfo-Co/P1-project#1
- SA Issue：MPinfo-Co/P1-analysis#4
- SD Issue：P1-design #5
- 上一個 commit：{前一個 commit hash}
- 本次 commit：{本次 commit hash}
```
