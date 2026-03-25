# MP-BOX 專案 AI 上下文

> 每次開新 AI 對話時，將此文件貼入作為起點。
> 最後更新：2026-03-25

---

## 專案概述

**MP-BOX** 是一套資安事件管理與 AI 諮詢系統，提供資安專家即時查閱事件、與 AI 夥伴對話諮詢、管理知識庫的能力。

- GitHub Org：MPinfo-Co
- 主要 repo：P1-code（前後端）、P1-analysis（分析文件）、P1-design（設計文件）、P1-project（專案管理）

---

## 技術決策摘要

### 前端
- **框架**：React 18 + Vite + Tailwind CSS v3
- **UI 元件庫**：shadcn/ui（請勿建議 MUI、Ant Design）
- **路由**：React Router v6
- **狀態管理**：Zustand（Client）、TanStack Query（Server）
- **語言**：JavaScript（請勿建議改為 TypeScript，尚在待討論）

### 後端
- **框架**：FastAPI + Pydantic
- **ORM**：SQLAlchemy + Alembic（請勿建議 SQLModel，已評估後選擇 SQLAlchemy）
- **資料庫**：PostgreSQL
- **認證**：自建 JWT（bcrypt 密碼 hash，token 黑名單完整登出）

### 待討論（尚未決定）
- TypeScript vs JavaScript
- MUI vs shadcn/ui
- Clerk vs 自建 JWT

---

## 已完成功能

- 前端 React 結構完整（Login、Dashboard、各頁面骨架）
- 後端 FastAPI 初始化（health endpoint）
- DB Schema：users、roles、user_roles、token_blacklist
- Auth API：POST /api/auth/login、POST /api/auth/logout、permission guard
- Seed script：預設角色（admin/user）+ admin 帳號

---

## 約束條件

- 開發環境：WSL2（Windows）
- 本地路徑：`/mnt/c/Users/MP0451.MPINFO/OneDrive - M-Power Information Co. Ltd/AIDC_Github/`
- 團隊規模：小團隊（solo 開發為主）
- 登入只接受 email，不支援 username

---

## 請勿建議

- 改用 SQLModel（已評估，維持 SQLAlchemy）
- 改用 passlib（有相容性問題，已改用 bcrypt 直接操作）
- 在 DB migration 裡塞初始資料（改用 seed.py）
- 簡易版 logout（資安產品需完整 token 黑名單）

---

## 開發規範

- Git 工作流程：issue → feature branch → PR → merge to main
- Commit 格式：`feat/fix/docs(scope): 說明`
- 每個 issue 開始前先讀對應文件，確認 input/output 再動手
- 本地測試通過後才 commit / push

---

## 參考文件

- 設計稿：`P1-design/Prototype/MP-Box_資安專家_v73_claude.html`
- 功能清單：`P1-design/FunctionList.md`
- 技術棧：`P1-design/TechStack.md`
- DB Schema：`P1-design/schema/entity-analysis.md`
