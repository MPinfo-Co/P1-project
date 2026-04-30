# Issue Body 格式規範

> [← 回到 workflow_guide.md](workflow_guide.md)

各階段 Issue body 由 GitHub Actions workflow 自動產生，格式如下。

---

## Epic Issue body

由 [epic.yml](https://github.com/MPinfo-Co/P1-project/blob/main/.github/ISSUE_TEMPLATE/epic.yml) 規範（PM 手動填寫）

```Markdown
### 需求說明

（PM 填寫的功能需求描述）
```

---

## SA Issue body

由 [p-workflow.yml](https://github.com/MPinfo-Co/P1-project/blob/main/.github/workflows/p-workflow.yml) 產生

```Markdown
## 關聯項目

### SA 工作文件
- sa-4-logic.md：[SA/saLogic/sa-4-logic.md]

### 關聯 Issue
- Epic：MPinfo-Co/P1-project#1
- SA Issue：#4
- SD Issue：P1-design #（merge 後自動填入）

### 相關連結
- 分支：[sa-4-xxx]
- Draft PR：[#3]
```

---

## SD Issue body

由 [a-workflow.yml](https://github.com/MPinfo-Co/P1-design/blob/main/.github/workflows/a-workflow.yml) 產生

```markdown
## 關聯項目

### SD 工作文件
- sa-4-logic.md：[SA/saLogic/sa-4-logic.md]
- TDD：[SD/TDD/sd-5-TDD.md]

### 關聯 Issue
- Epic：MPinfo-Co/P1-project#1
- SA Issue：MPinfo-Co/P1-design#4
- SD Issue：#5
- PG Issue：P1-code #（merge 後自動填入）

### 相關連結
- 分支：[sd-5-xxx]
- Draft PR：[#6]
```

---

## PG Issue body

由 [d-workflow.yml](https://github.com/MPinfo-Co/P1-design/blob/main/.github/workflows/d-workflow.yml) 產生

```Markdown
## 關聯項目

### PG 工作文件
- sa-4-logic.md：[SA/saLogic/sa-4-logic.md]
- SpecDiff：[SD/sdDiff/sd-5-Diff.md]
- TDD：[SD/TDD/sd-5-TDD.md]
- TestReport：[TestReport/issue-5.md]

### 關聯 Issue
- Epic：MPinfo-Co/P1-project#1
- SA Issue：MPinfo-Co/P1-design#4
- SD Issue：MPinfo-Co/P1-design#5
- PG Issue：#7

### 相關連結
- 分支：[pg-7-xxx]
- Draft PR：[#8]
```
