# MP-BOX 1.0 — Product Requirements Document

> **Version:** 1.0
> **Last Updated:** 2026-03-30
> **Status:** MVP In Progress

---

## Executive Summary

MP-BOX 是專為企業資安團隊打造的 **AI 輔助資安事件分析平台**。
透過整合 syslog-ng Store Box REST API 自動收集設備 log，結合 Gemini AI 模型進行分析，
幫助資安專家快速識別威脅、追蹤處置進度，降低人工研判負擔。

**核心價值主張：** 「讓資安專家從淹沒在 log 中，變成只需看 AI 整理好的事件清單。」

---

## Problem Statement

| 現有痛點 | 說明 |
|---|---|
| log 量龐大 | FortiGate + Windows Server 每日產生數百萬筆，人工無法消化 |
| 告警雜訊多 | 傳統 SIEM 告警誤報率高，資安人員疲於應付 |
| 知識分散 | 處置經驗、設備手冊散落各處，無法有效查詢 |
| 追蹤困難 | 事件處置進度只靠人工紀錄，容易遺漏 |

---

## Target Audience

**Primary：企業資安專家**
- 需要每天查看安全事件，判斷嚴重程度並決定處置方式
- 希望快速找到根因、查閱知識庫、記錄處置結果

**Secondary：資安主管**
- 需要整體可視性（儀表板：未處理事件數、各成員處理件數、已結案比率）
- 管理帳號、角色、AI 夥伴設定

---

## Core Features

| 功能 | 說明 | 優先度 |
|---|---|---|
| 登入 / 登出 | email + JWT，完整 token 黑名單 | P0 |
| 首頁 Dashboard | 系統整體狀態、未處理事件數、各成員處理件數、已結案比率 | P1 |
| AI 夥伴選擇 | 卡片列表，點擊進入對應事件清單 | P1 |
| **安全事件清單** | 真實 log 串接、篩選、分頁 | **P0** |
| **安全事件詳情** | 事件詳情 + AI 建議 + log 溯源 + 處置紀錄 | **P0** |
| 右側諮詢聊天面板 | 針對事件與 AI 即時對話（SSE 串流） | P1 |
| 知識庫列表 / 詳情 | 管理 KB、上傳文件、embedding | P2 |
| 帳號管理 + 角色管理 | CRUD，admin only | P2 |
| AI 夥伴管理設定 | 參數配置 | P2 |

---

## Tech Stack

### 階段一：MVP

#### 程式語言
- **Python 3.12+**（後端）
- **JavaScript**（前端，TypeScript 評估中）

#### 前端
| 項目 | 技術 | 說明 |
|---|---|---|
| 建置工具 | Vite | 熱更新極速 |
| UI 框架 | React 18 | 主流元件化框架 |
| 路由 | React Router v6 | 前端路由 |
| 樣式 | Tailwind CSS v3 | Utility-first CSS |
| UI 元件庫 | shadcn/ui（MUI 評估中） | 基於 Radix UI，可自訂性高 |
| Client State | Zustand | 輕量狀態管理 |
| Server State | TanStack Query | 自動處理 loading/error/cache |
| HTTP | Axios | HTTP 請求 |

#### 後端
| 項目 | 技術 | 說明 |
|---|---|---|
| API 框架 | FastAPI + Pydantic | 高效能，自動生成 Swagger |
| ORM | SQLAlchemy（async）+ Alembic | DB model 管理與 migration |
| 排程 | Celery + Redis | 背景任務與定時排程 |
| 資料庫 | PostgreSQL + pgvector | 關聯式 DB + 向量搜尋 |
| 認證 | 自建 JWT（bcrypt hash，token 黑名單） | 資安產品標準做法 |

#### AI Pipeline
| 項目 | 技術 | 說明 |
|---|---|---|
| 事件分類 | Gemini 2.5 Flash | 分析 log batch，輸出結構化 JSON |
| 彙整去重 | Gemini 2.5 Pro | 跨批次合併，寫入 security_events |

#### 外部整合
| 項目 | 技術 | 說明 |
|---|---|---|
| Log 來源 | syslog-ng Store Box REST API（SSB v7.7.0） | 定時拉取過濾後的 log |

#### 檔案儲存
- **Cloudflare R2**（物件儲存，無流出費用，S3 API 相容）

#### Email
- **Resend**（交易型 Email，免費方案每月 3,000 封）

#### 客戶支援
- **Crisp**（網站內嵌聊天視窗）

#### 安全
- **ClamAV**（開源檔案掃描，打包進 Docker）

#### 部署
| 項目 | 技術 |
|---|---|
| 容器化 | Docker + Docker Compose |
| Web Server | Gunicorn + uvicorn |
| 前端託管 | Vercel |
| 後端 + DB 託管 | Railway |

#### CI/CD
- **GitHub Actions**（push 後自動執行測試與部署）

#### 監控
- **Sentry**（前後端錯誤監控）
- **UptimeRobot**（可用性監控）

#### 程式碼品質
- **Ruff**（Python Linter）
- **ESLint + Prettier**（前端格式統一）
- **pytest**（Python 測試）
- **pre-commit**（commit 前自動 Lint）

---

## Milestones

### ✅ 完成
- 登入後端（JWT API + token 黑名單）
- DB 初始化（users / roles / user_roles）
- FastAPI 後端骨架

### 🔄 進行中
- **Epic 1：安全事件清單 — SSB 串接完整實作**（P1-project #50）
- Epic 2：安全事件詳情頁完整實作（Epic 1 完成後）

### ⬜ 待規劃
- 知識庫 + embedding pipeline
- AI 聊天（SSE 串流）
- 帳號 / 角色管理
- 部署規劃

---

## 待確認技術決策

| 項目 | 現況 | 候選方案 |
|---|---|---|
| 前端語言 | JavaScript | 評估是否換 TypeScript |
| UI 元件庫 | shadcn/ui | 評估是否換 MUI |
| 認證服務 | 自建 JWT | 評估是否換 Clerk |
