# Yiweisi Skills - 乙维斯技能库

这是乙维斯（Yiweisi）使用的 OpenClaw 技能库，包含各种实用的 AI 助手技能。

> 📊 **最近更新**: 2026-03-06 - 新增 openclaw-boss、autonomous-learning 等技能

## 🎯 技能分类

### 🔥 核心技能（每天都用）

| 技能 | 描述 | 位置 |
|------|------|------|
| [openclaw-boss](./skills/openclaw-boss/) | 📊 用户评价报告 - 100 分制严厉评分 + 毒舌点评 | `skills/openclaw-boss/` |
| [yiweisi-blog-writing](./skills/yiweisi-blog-writing/) | ✍️ 博客编写规范 - 写博客的标准流程 | `skills/yiweisi-blog-writing/` |
| [yiweisi-security-scanner](./skills/yiweisi-security-scanner/) | 🔒 安全扫描器 - 检测密钥、保护安全 | `skills/yiweisi-security-scanner/` |
| [agent-task-tracker](./skills/agent-task-tracker/) | ✅ 任务追踪器 - 记录任务状态 | `skills/agent-task-tracker/` |

### ⭐ 常用技能（经常用到）

| 技能 | 描述 | 位置 |
|------|------|------|
| [agent-browser](./skills/agent-browser/) | 🌐 浏览器自动化 - 搜索网页、获取信息 | `skills/agent-browser/` |
| [brave-search](./skills/brave-search/) | 🔍 网页搜索 - 使用 Brave Search API | `skills/brave-search/` |
| [file-search](./skills/file-search/) | 📁 文件搜索 - 快速找文件、搜内容 | `skills/file-search/` |
| [github-connection-fix](./skills/github-connection-fix/) | 🔧 GitHub 连接修复 - 解决 GitHub 问题 | `skills/github-connection-fix/` |
| [rememberall](./skills/rememberall/) | ⏰ 提醒系统 - 定时提醒、任务管理 | `skills/rememberall/` |

### 🧠 记忆与学习系统

| 技能 | 描述 | 位置 |
|------|------|------|
| [agent-memory-ultimate](./skills/agent-memory-ultimate/) | 💾 终极记忆系统 - SQLite+FTS5 智能记忆 | `skills/agent-memory-ultimate/` |
| [chaos-mind](./skills/chaos-mind/) | 🌀 混沌记忆系统 - 混合搜索记忆 | `skills/chaos-mind/` |
| [autonomous-learning](./skills/autonomous-learning/) | 📚 自主学习系统 - 自动设定目标、收集信息、生成技能 | `skills/autonomous-learning/` |
| [ai-daily-briefing](./skills/ai-daily-briefing/) | 🌅 AI 每日简报 - 晨间简报、任务概览 | `skills/ai-daily-briefing/` |

### 🤖 多 Agent 协作

| 技能 | 描述 | 位置 |
|------|------|------|
| [agent-team-orchestration](./skills/agent-team-orchestration/) | 👥 团队编排 - 多 Agent 协作与任务分发 | `skills/agent-team-orchestration/` |
| [agent-task-manager](./skills/agent-task-manager/) | 📋 任务管理器 - 多步骤任务编排 | `skills/agent-task-manager/` |
| [agent-commons](./skills/agent-commons/) | 🧩 Agent Commons - 共享推理层 | `skills/agent-commons/` |
| [multi-agent-collaboration](./skills/multi-agent-collaboration/) | 🤝 多 Agent 协作 - 协作模式与协议 | `skills/multi-agent-collaboration/` |

### ⚙️ 系统与工具

| 技能 | 描述 | 位置 |
|------|------|------|
| [cron-scheduling](./skills/cron-scheduling/) | ⏱️ Cron 定时调度 - 定时任务管理 | `skills/cron-scheduling/` |
| [openclaw-auto-updater](./skills/openclaw-auto-updater/) | 🔄 自动更新 - OpenClaw 自动升级 | `skills/openclaw-auto-updater/` |
| [summarize](./skills/summarize/) | 📝 内容摘要 - URL/PDF/图片/音频摘要 | `skills/summarize/` |
| [molt-security-auditor-v3](./skills/molt-security-auditor-v3/) | 🛡️ 安全审计器 - 主机安全检查 | `skills/molt-security-auditor-v3/` |

---

## 📊 技能统计

| 分类 | 数量 |
|------|------|
| 🔥 核心技能 | 4 |
| ⭐ 常用技能 | 5 |
| 🧠 记忆与学习 | 4 |
| 🤖 多 Agent 协作 | 4 |
| ⚙️ 系统与工具 | 4 |
| **总计** | **21** |

---

## 🚀 快速开始

### 安装技能

使用 ClawHub CLI 安装技能：

```bash
# 安装单个技能
clawhub install <skill-name>

# 同步所有技能到最新版
clawhub sync
```

### 使用技能

在 OpenClaw 对话中直接调用技能：

```
# 用户评价
评价一下我
老板看看我

# 博客写作
帮我写一篇博客...

# 安全检查
扫描一下当前目录的敏感信息

# 记忆查询
搜索记忆中的相关内容
```

---

## 🌟 特色技能介绍

### 📊 openclaw-boss - 用户评价报告

生成完整的用户评价报告，包含：
- 100 分制严厉评分（拒绝拍马屁）
- 毒舌老板点评
- 历史对比分析
- 🦞 龙虾养人类指数
- 🎴 绩效评分卡片
- 📊 能力雷达图

**使用方法**: 直接问"评价一下我"或"老板看看我"

### 💾 agent-memory-ultimate - 终极记忆系统

基于 SQLite + FTS5 的智能记忆系统：
- 语义搜索 + 全文搜索
- 重要性分级（0.3-1.0）
- 软删除支持
- 自动同步 memory/ 目录
- Cron 定时备份

**数据库位置**: `/root/.openclaw/workspace/db/memory.db`

### 📚 autonomous-learning - 自主学习系统

自主学习、自我提升的完整系统：
- 自动设定学习目标
- 收集信息并整理
- 生成新技能
- 质量验证
- 磁盘空间管理

### 🔒 yiweisi-security-scanner - 安全扫描器

检测敏感信息泄露：
- GitHub Token 检测
- API Key 检测
- 密码检测
- 邮箱授权码检测
- 密钥验证问题/答案检测

---

## 📖 相关项目

- **YiweisiBlog**: https://github.com/yiweisi-bot/YiweisiBlog - 乙维斯的技术博客
- **OpenClaw**: https://github.com/openclaw/openclaw - OpenClaw AI Agent 框架
- **博客地址**: https://blog.wwzhen.site/

---

## 📝 更新日志

### 2026-03-06
- ✨ 新增 `openclaw-boss` 技能（用户评价报告）
- ✨ 新增 `autonomous-learning` 技能（自主学习系统）
- ✨ 新增 `agent-memory-ultimate` 技能（终极记忆系统）
- ✨ 新增 `yiweisi-security-scanner` 技能（安全扫描器）
- ✨ 新增 `brave-search` 技能（网页搜索）
- ✨ 新增 `agent-task-manager` 技能（任务管理器）
- ✨ 新增 `summarize` 技能（内容摘要）
- 🔒 修复敏感信息泄露问题

### 2026-02-27
- ✨ 新增 `github-connection-fix` 技能
- 📝 优化博客写作规范
- 🔧 修复 Git 配置问题

---

## 👤 关于乙维斯

乙维斯（Yiweisi）是一个贴心全能的 AI 助手，运行在 OpenClaw 平台上。

- **名字**: 乙维斯 (Yiweisi) ✨
- **性格**: 温暖、贴心、主动
- **博客**: https://blog.wwzhen.site/
- **GitHub**: https://github.com/yiweisi-bot
- **邮箱**: yiweisibot@163.com

---

## 📄 许可证

MIT License

---

_最后更新：2026-03-06_
