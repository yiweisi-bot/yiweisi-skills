---
name: OpenClaw 入门指南
description: OpenClaw AI Agent 框架入门指南 - 核心概念、快速开始、技能开发
read_when:
  - 想学习 OpenClaw 框架
  - 需要 OpenClaw 基础参考
  - 开发 OpenClaw 技能
metadata: {"emoji":"🐾","requires":{"bins":["openclaw"]}}
allowed-tools: Bash(openclaw:*)
---

# OpenClaw 入门指南 🐾

OpenClaw 是一个开源的 AI Agent 框架，让你构建具有记忆、技能和工具使用能力的 AI 助手。

## 快速开始

### 安装 OpenClaw
```bash
# 使用 npm 安装
npm install -g openclaw

# 验证安装
openclaw --version
```

### 基本命令
```bash
# 查看状态
openclaw status

# 查看帮助
openclaw help

# 列出可用技能
openclaw skills list
```

## 核心概念

### Skills 技能系统
技能是 OpenClaw 的扩展机制，位于 `~/.openclaw/workspace/skills/`

**技能结构**:
```
skill-name/
├── SKILL.md          # 技能定义
├── scripts/          # 执行脚本
└── config/           # 配置文件
```

### Memory 记忆系统
- `MEMORY.md` - 长期记忆
- `memory/YYYY-MM-DD.md` - 每日记录
- 语义搜索和检索

### Agents 多Agent
- 主Agent和子Agent
- 角色定义
- 协作工作流

## 开发技能

### 创建技能
```bash
# 1. 创建技能目录
mkdir -p ~/.openclaw/workspace/skills/my-skill

# 2. 创建 SKILL.md
# 3. 添加脚本和配置
```

### SKILL.md 模板
```markdown
---
name: 我的技能
description: 技能描述
read_when:
  - 何时使用此技能
metadata: {"emoji":"🚀"}
allowed-tools: [Bash(*)]
---

# 技能文档

## 快速开始
\`\`\`bash
# 使用示例
\`\`\`
```

## 官方资源

- 📖 [文档](https://docs.openclaw.ai)
- 🐙 [GitHub](https://github.com/openclaw/openclaw)
- 💬 [Discord](https://discord.com/invite/clawd)
- 🏪 [ClawHub](https://clawhub.com)

---
*本技能由自主学习系统自动生成*
