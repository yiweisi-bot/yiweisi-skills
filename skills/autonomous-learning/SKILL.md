---
name: 自主学习系统
description: 乙维斯的自主学习系统 - 自动设定目标、收集信息、生成技能、质量验证
read_when:
  - 需要让Agent自主学习新知识
  - 需要自动生成技能
  - 需要批量学习和技能生产
metadata: 
  emoji: "🧠"
  author: "乙维斯"
  version: "3.0"
  auto_setup: true
  requires_agents:
    - learner
---

# 自主学习系统

乙维斯的自主学习系统，让Agent能够自主设定学习目标、收集信息、生成高质量技能，并通过三层质量验证确保技能质量。

---

## 🤖 自动安装（OpenClaw 会自动完成）

**重要**: 当 OpenClaw 加载这个技能时，会自动执行以下操作：

1. ✅ 检查 Learner Agent 是否存在
2. ✅ 如果不存在，自动创建 Learner Agent
3. ✅ 更新 OpenClaw 配置文件
4. ✅ 创建必要的工作空间和目录
5. ✅ 检查依赖（agent-browser、Python）

**用户无需手动操作！**

---

## 什么时候使用这个技能

### 典型使用场景：

1. **场景1：主动学习新技术**
   - 用户说："我想学习 TypeScript"
   - 用户说："帮我了解一下 React Hooks"
   - 用户说："学习 Python 装饰器"

2. **场景2：生成技能文档**
   - 用户说："生成一个关于 Docker 的技能"
   - 用户说："帮我创建一个 Git 分支管理的技能"

3. **场景3：快速了解某个主题**
   - 用户说："快速学习 GraphQL"
   - 用户说："了解一下 Redis 缓存策略"

---

## 快速开始

### 步骤1：发起学习请求
```
你: 开始学习 TypeScript
我: 🎯 自主学习启动向导
    📝 问题 1/4: 学习主题
    你提到想学习: TypeScript
    请确认或细化学习主题...
```

### 步骤2：交互式配置（4个问题）
```
📝 问题 1/4: 学习主题
  - 确认主题是否正确
  - 或者细化/更换主题

📚 问题 2/4: 学习深度
  1. 🚀 快速了解 (10分钟)
  2. 📖 系统学习 (30分钟) [推荐]
  3. 🎓 深入精通 (60分钟)

⏰ 问题 3/4: 时间限制
  - 使用推荐时间
  - 或自定义时间

💰 问题 4/4: Token 预算
  1. 💵 经济型 (2000 tokens)
  2. ⚖️ 平衡型 (5000 tokens) [推荐]
  3. 💎 质量型 (10000 tokens)
```

### 步骤3：确认并开始学习
```
📋 学习配置确认
  📚 主题: TypeScript 基础类型
  🎯 深度: 系统学习 (systematic)
  ⏰ 时间: 30 分钟
  💰 Token: 5000

确认开始学习吗？(1.✅ 2.🔄 3.❌)
```

### 步骤4：自动学习
```
✅ 配置已确认！
    ✅ LearnerBot 已启动
    ✅ 正在使用 agent-browser 搜索
    ✅ 正在生成技能
    ✅ 学习完成！技能已生成
```

---

## 核心功能

### 1. 自动设定学习目标 🎯
- 基于用户需求设定学习目标
- 优先级自动计算（P0-P3）
- 时间和Token预算管理

### 2. 智能信息收集 🔍
- 使用 agent-browser 搜索信息
- 多轮迭代收集（最多3轮）
- 信息充分性评分（≥70分）

### 3. 高质量技能生成 ✨
- 标准的 SKILL.md 格式
- 包含：使用场景、快速开始、核心概念、实用示例、最佳实践、常见问题
- 版本管理和更新

### 4. 三层质量验证 🛡️
- 规则验证：格式检查（6项）
- AI验证：质量评分（6个维度）
- 人工验证：用户最终确认

---

## 使用示例

### 示例1：学习新技术
```
你: 我想学习 React 19 Server Components
我: 好的！启动自主学习...
    📚 主题: React 19 Server Components
    🎯 深度: systematic
    ⏰ 时间: 30分钟
    
    ✅ 学习完成！
    📄 技能已生成: React-19-Server-Components.md
```

### 示例2：快速了解
```
你: 快速学习 Docker 容器化
我: 好的！快速学习模式启动...
    📚 主题: Docker 容器化
    🎯 深度: intro
    ⏰ 时间: 10分钟
    
    ✅ 学习完成！
    📄 技能已生成: Docker-容器化.md
```

---

## Learner Agent 说明

### 什么是 Learner Agent？
- **名称**: LearnerBot 📚
- **职责**: 专门负责自主学习
- **能力**: agent-browser 搜索、技能生成、质量验证
- **模型**: doubao/ark-code-latest

### 工作流程
```
用户 → 乙维斯（主 Agent）
         ↓ 使用 sessions_spawn 工具
       LearnerBot（子 Agent）
         ↓ 使用 agent-browser 搜索
         ↓ 生成技能
         ↓ 质量验证
         ↓ 返回结果
       乙维斯 → 用户
```

---

## 生成的技能位置

所有生成的技能都会保存在：
```
~/.openclaw/learner-workspace/skills/
```

每个技能都是一个独立的 `.md` 文件。

---

## 配置选项

### 学习深度
- **intro**: 入门级（10分钟，快速了解）
- **systematic**: 系统级（30分钟，深入理解）
- **master**: 精通级（60分钟，全面掌握）

### Token 预算
- **经济型**: 2000 tokens
- **平衡型**: 5000 tokens（默认）
- **质量型**: 10000 tokens

---

## 常见问题

### Q1: 为什么不需要手动安装？
A: OpenClaw 会在加载技能时自动检查和创建 Learner Agent，无需用户干预。

### Q2: LearnerBot 和 DevBot 有什么区别？
A: 
- LearnerBot: 专门用于自主学习，生成技能
- DevBot: 专门用于开发任务，编写代码

### Q3: 生成的技能在哪里？
A: `~/.openclaw/learner-workspace/skills/`

### Q4: 可以自定义学习深度吗？
A: 可以！说"深入学习 [主题]"或"快速学习 [主题]"

---

## 技术架构

### 核心模块
- **autonomous_learning_production.py** - 生产版本实现
- **database/** - 数据库和工具模块
- **install.sh** - 自动安装脚本（OpenClaw 自动调用）

### 依赖
- OpenClaw 2026.2.26+
- agent-browser
- Python 3.8+

---

## 🎯 最佳实践

1. **明确学习主题** - 越具体越好
2. **选择合适的深度** - 根据需求选择 intro/systematic/master
3. **查看生成的技能** - 学习完成后查看生成的文档
4. **提供反馈** - 如果质量不满意，可以让 LearnerBot 重新学习

---

## 📚 相关文档

- `QUICK-START.md` - 快速开始指南
- `README.md` - 系统架构说明
- `install.sh` - 安装脚本（自动执行）

---

**🎉 享受自主学习！让 OpenClaw 自动帮你学习新知识！**
