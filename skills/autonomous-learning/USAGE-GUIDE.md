# 自主学习系统 - 完整使用指南

## 🎯 系统概述

这是一个完全自动化的自主学习系统，当 OpenClaw 加载此技能时，会自动：

1. ✅ 检查 Learner Agent 是否存在
2. ✅ 如果不存在，自动创建 Learner Agent
3. ✅ 更新 OpenClaw 配置文件
4. ✅ 创建必要的工作空间和目录
5. ✅ 所有过程无需用户干预

---

## 🚀 快速开始

### 方式1：直接使用（推荐）

```
你: 开始学习 TypeScript 基础类型
我: 好的！启动 LearnerBot 学习...
    ✅ LearnerBot 已启动
    ✅ 正在使用 agent-browser 搜索
    ✅ 正在生成技能
    ✅ 学习完成！技能已生成
```

### 方式2：使用 @ 提及

```
你: @learner 学习 React Hooks
LearnerBot: 好的！开始学习 React Hooks...
```

---

## 📋 学习主题示例

### 前端技术
- TypeScript 基础类型
- React Hooks
- Vue 3 Composition API
- Next.js 路由
- Tailwind CSS

### 后端技术
- Python 装饰器
- Node.js Stream
- GraphQL 查询
- Redis 缓存
- Docker 容器

### 开发工具
- Git 分支策略
- VSCode 快捷键
- Webpack 配置
- ESLint 规则

---

## ⚙️ 自动设置机制

### 当 OpenClaw 加载技能时

```python
# hooks/setup.py 会自动执行

1. 检查 ~/.openclaw/openclaw.json 中是否有 learner agent
2. 如果没有：
   - 备份原配置文件
   - 添加 learner agent 配置
   - 更新 main agent 的 allowAgents
   - 保存配置
3. 创建工作空间目录：
   - ~/.openclaw/learner-workspace/
   - ~/.openclaw/learner-workspace/skills/
   - ~/.openclaw/learner-workspace/memory/
4. 完成！
```

### 配置文件示例

```json
{
  "id": "learner",
  "workspace": "/root/.openclaw/learner-workspace",
  "model": {
    "primary": "doubao/ark-code-latest",
    "fallbacks": ["zhipu/glm-5", "deepseek/deepseek-chat"]
  },
  "identity": {
    "name": "LearnerBot",
    "theme": "自主学习专家",
    "emoji": "📚"
  }
}
```

---

## 🔄 工作流程

```
用户说: "开始学习 TypeScript"
    ↓
乙维斯（主 Agent）接收请求
    ↓
使用 sessions_spawn 工具调用 learner agent
    ↓
LearnerBot（子 Agent）开始工作
    ↓
使用 agent-browser 搜索 TypeScript 相关信息
    ↓
生成完整的 SKILL.md 格式技能
    ↓
执行三层质量验证（规则→AI→人工）
    ↓
返回 JSON 格式结果给乙维斯
    ↓
乙维斯展示结果给用户
```

---

## 📁 生成的技能位置

所有生成的技能都会保存在：
```
~/.openclaw/learner-workspace/skills/
```

每个技能都是一个独立的 `.md` 文件，包含：
- 使用场景
- 快速开始
- 核心概念
- 实用示例
- 最佳实践
- 常见问题

---

## 🎨 学习深度选择

### intro（入门级）
- **时间**: 10分钟
- **Token**: 2000
- **适合**: 快速了解某个概念

```
你: 快速学习 GraphQL
```

### systematic（系统级）- 默认
- **时间**: 30分钟
- **Token**: 5000
- **适合**: 系统学习某个技术

```
你: 学习 TypeScript 基础类型
```

### master（精通级）
- **时间**: 60分钟
- **Token**: 10000
- **适合**: 深入掌握某个领域

```
你: 深入学习 React 架构
```

---

## 🔧 高级配置

### 自定义 Learner Agent 模型

编辑 `~/.openclaw/openclaw.json`：

```json
{
  "id": "learner",
  "model": {
    "primary": "zhipu/glm-5",  // 更改主模型
    "fallbacks": ["deepseek/deepseek-chat"]
  }
}
```

### 自定义工作空间

```json
{
  "id": "learner",
  "workspace": "/custom/path/learner-workspace"
}
```

---

## ❓ 常见问题

### Q1: 如何确认 Learner Agent 已创建？

```bash
openclaw agents list
```

应该看到：
- main (乙维斯)
- dev (DevBot)
- learner (LearnerBot) ✅

### Q2: 如果自动设置失败怎么办？

手动执行安装脚本：
```bash
cd ~/.openclaw/workspace/skills/autonomous-learning
bash install.sh
openclaw gateway restart
```

### Q3: 如何查看生成的技能？

```bash
ls ~/.openclaw/learner-workspace/skills/
cat ~/.openclaw/learner-workspace/skills/技能名称.md
```

### Q4: 可以删除生成的技能吗？

可以！直接删除文件即可：
```bash
rm ~/.openclaw/learner-workspace/skills/技能名称.md
```

### Q5: 如何重置 Learner Agent？

1. 编辑 `~/.openclaw/openclaw.json`
2. 删除 learner agent 配置
3. 重启 OpenClaw
4. 重新加载技能（会自动创建）

---

## 🛠️ 故障排除

### 问题1: Learner Agent 没有出现在 agents list

**解决方案**:
```bash
# 检查配置
grep -A 10 '"id": "learner"' ~/.openclaw/openclaw.json

# 如果不存在，手动执行设置
cd ~/.openclaw/workspace/skills/autonomous-learning
python3 hooks/setup.py

# 重启 OpenClaw
openclaw gateway restart
```

### 问题2: 学习任务超时

**解决方案**:
- 检查网络连接
- 简化学习主题
- 检查 agent-browser 是否安装：`which agent-browser`

### 问题3: 生成的技能质量不高

**解决方案**:
- 提供更具体的学习主题
- 使用更高级的学习深度（systematic 或 master）
- 让 LearnerBot 重新学习

---

## 📊 性能优化

### Token 优化
- 使用合适的学习深度
- 避免过于宽泛的主题
- 定期清理不需要的技能

### 速度优化
- 使用快速学习模式（intro）
- 选择网络良好的时段
- 确保系统资源充足

---

## 🎯 最佳实践

1. **明确学习主题** - 越具体越好
2. **选择合适的深度** - 根据需求选择
3. **查看生成的技能** - 学习完成后查看文档
4. **提供反馈** - 质量不满意可以让 LearnerBot 重新学习
5. **定期整理** - 删除不需要的技能文件

---

## 📚 相关文档

- `SKILL.md` - 技能主文档
- `README.md` - 系统架构说明
- `hooks/setup.py` - 自动设置脚本
- `skill.json` - 技能配置文件

---

## 🔄 更新日志

### v3.0.0 (2026-03-04)
- ✅ 实现完全自动化的安装机制
- ✅ 使用 Learner Agent（不是 dev agent）
- ✅ 添加 hooks/setup.py 自动设置脚本
- ✅ 创建 skill.json 配置文件
- ✅ 完善文档和使用指南

### v2.0.0 (2026-03-04)
- ✅ 实现真实的子 Agent 调用
- ✅ 集成 Google 搜索 + LLM 提取
- ✅ 生产环境可用

### v1.0.0 (2026-03-04)
- ✅ 基础架构设计
- ✅ 核心功能实现

---

**🎉 享受自动化学习！让 OpenClaw 为你自动学习新知识！**
