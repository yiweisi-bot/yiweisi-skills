#!/bin/bash

# OpenClaw 专题学习脚本
# 专注于学习 OpenClaw 官方文档、教程和使用实例

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DATA_DIR="$SKILL_DIR/data"
SESSION_ID="$1"

mkdir -p "$DATA_DIR/openclaw"

echo "   🚀 开始 OpenClaw 专题学习..."
echo ""

# OpenClaw 官方资源
OPENCLAW_RESOURCES=(
  "OpenClaw 官方文档|https://docs.openclaw.ai"
  "OpenClaw GitHub|https://github.com/openclaw/openclaw"
  "OpenClaw Discord|https://discord.com/invite/clawd"
  "ClawHub 技能市场|https://clawhub.com"
)

# OpenClaw 核心概念
OPENCLAW_CONCEPTS=(
  "OpenClaw 架构和工作原理"
  "Skills 技能系统"
  "Agents 多Agent协作"
  "Memory 记忆系统"
  "Tools 工具调用"
  "Heartbeat 心跳机制"
  "Configuration 配置管理"
)

# OpenClaw 本地资源探索
explore_local_openclaw() {
  echo "   📂 探索本地 OpenClaw 资源..."
  
  # 1. 检查 OpenClaw 安装
  echo "      🔍 检查 OpenClaw 安装..."
  if command -v openclaw &>/dev/null; then
    local version=$(openclaw --version 2>/dev/null || echo "unknown")
    echo "         ✅ OpenClaw 已安装: $version"
  fi
  
  # 2. 探索本地技能目录
  echo ""
  echo "      📚 探索本地技能目录..."
  local skills_dir="/root/.openclaw/workspace/skills"
  if [ -d "$skills_dir" ]; then
    local skill_count=$(ls -1 "$skills_dir" 2>/dev/null | wc -l)
    echo "         ✅ 发现 $skill_count 个本地技能"
    
    # 列出技能
    echo ""
    echo "         📋 本地技能列表:"
    for skill in "$skills_dir"/*; do
      if [ -d "$skill" ] && [ -f "$skill/SKILL.md" ]; then
        local skill_name=$(basename "$skill")
        echo "            • $skill_name"
      fi
    done
  fi
  
  # 3. 检查 OpenClaw 配置
  echo ""
  echo "      ⚙️ 检查 OpenClaw 配置..."
  local config_dir="/root/.openclaw"
  if [ -d "$config_dir" ]; then
    echo "         ✅ 配置目录存在"
    if [ -f "$config_dir/config.yaml" ]; then
      echo "         ✅ 配置文件存在"
    fi
  fi
}

# 创建 OpenClaw 知识摘要
create_openclaw_knowledge() {
  local knowledge_file="$DATA_DIR/openclaw/knowledge_${SESSION_ID:-latest}.md"
  
  cat > "$knowledge_file" << 'EOF'
# OpenClaw 学习知识摘要

## OpenClaw 简介

OpenClaw 是一个开源的 AI Agent 框架，让你可以构建具有记忆、技能和工具使用能力的 AI 助手。

### 核心特性
- 🧠 **记忆系统** - 长期和短期记忆
- 🛠️ **技能系统** - 可扩展的技能库
- 🤝 **多Agent协作** - 多个Agent协同工作
- 🔧 **工具集成** - 灵活的工具调用框架
- 💓 **心跳机制** - 主动任务调度

---

## 核心概念

### 1. Skills 技能系统
技能是 OpenClaw 的核心扩展机制。每个技能包含：
- `SKILL.md` - 技能定义和文档
- 脚本和工具 - 实现技能功能
- 配置文件 - 技能配置

**技能位置**: `~/.openclaw/workspace/skills/`

### 2. Memory 记忆系统
- `MEMORY.md` - 长期记忆
- `memory/YYYY-MM-DD.md` - 每日记忆
- 记忆搜索和检索

### 3. Agents 多Agent系统
- 主Agent和子Agent
- 角色定义和任务分配
- Agent间通信和协作

### 4. Heartbeat 心跳机制
- 定期检查和任务触发
- 空闲时间利用
- 主动通知和提醒

---

## 快速开始

### 安装 OpenClaw
```bash
# 使用 npm 安装
npm install -g openclaw

# 验证安装
openclaw --version
```

### 基本使用
```bash
# 查看状态
openclaw status

# 启动会话
openclaw start

# 列出技能
openclaw skills list
```

---

## 技能开发

### 技能结构
```
your-skill/
├── SKILL.md          # 技能定义（必需）
├── scripts/          # 脚本文件
├── config/           # 配置文件
└── assets/           # 资源文件
```

### SKILL.md 格式
```markdown
---
name: 技能名称
description: 技能描述
read_when:
  - 何时使用此技能
metadata: {"emoji":"🚀"}
allowed-tools: [允许的工具]
---

# 技能文档内容...
```

---

## 官方资源

- 📖 [官方文档](https://docs.openclaw.ai)
- 🐙 [GitHub 仓库](https://github.com/openclaw/openclaw)
- 💬 [Discord 社区](https://discord.com/invite/clawd)
- 🏪 [ClawHub 技能市场](https://clawhub.com)

---

## 学习路径

### 初学者
1. 阅读官方文档
2. 探索现有技能
3. 运行基本命令
4. 理解核心概念

### 进阶用户
1. 开发自定义技能
2. 配置多Agent系统
3. 集成外部工具
4. 部署生产环境

---

*本摘要由自主学习系统自动生成*
EOF

  echo "      ✅ OpenClaw 知识摘要已创建"
  echo "      📄 文件: $knowledge_file"
}

# 生成 OpenClaw 学习技能
generate_openclaw_skill() {
  local skill_file="$DATA_DIR/skills/pending/openclaw-intro-skill.md"
  
  cat > "$skill_file" << 'EOF'
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
EOF

  echo "      ✅ OpenClaw 入门技能已生成"
}

# 主流程
explore_local_openclaw
echo ""
create_openclaw_knowledge
echo ""
generate_openclaw_skill

echo ""
echo "   ✅ OpenClaw 专题学习完成"
