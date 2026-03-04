# 自主学习技能 - 快速开始指南

## 📋 安装步骤

### 1. 运行安装脚本
```bash
cd ~/.openclaw/workspace/skills/autonomous-learning
bash install.sh
```

### 2. 重启 OpenClaw
```bash
openclaw gateway restart
```

### 3. 验证安装
```bash
openclaw agents list
```

应该看到三个 agent：
- main (乙维斯)
- dev (DevBot)
- learner (LearnerBot) ✅

---

## 🚀 使用方法

### 方式1: 直接对话（推荐）
```
你: 开始学习 TypeScript 基础类型
乙维斯: 好的！启动 LearnerBot 学习...
        ✅ LearnerBot 已启动
        ✅ 正在使用 agent-browser 搜索
        ✅ 正在生成技能
        ✅ 学习完成！技能已生成
```

### 方式2: 使用命令
```
你: @learner 学习 React Hooks
LearnerBot: 好的！开始学习 React Hooks...
```

---

## 📚 学习主题示例

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

## ⚙️ 配置说明

### Learner Agent 配置
- **模型**: doubao/ark-code-latest（可配置）
- **工作空间**: ~/.openclaw/learner-workspace
- **功能**: agent-browser、技能生成、质量验证

### 自定义配置
编辑 `~/.openclaw/openclaw.json`：
```json
{
  "id": "learner",
  "model": {
    "primary": "doubao/ark-code-latest",
    "fallbacks": ["zhipu/glm-5", "deepseek/deepseek-chat"]
  }
}
```

---

## 🎯 工作流程

```
用户 → 乙维斯 → LearnerBot → 学习任务
                      ↓
                  agent-browser 搜索
                      ↓
                  技能生成
                      ↓
                  质量验证
                      ↓
                  返回结果 → 乙维斯 → 用户
```

---

## ❓ 常见问题

### Q1: 为什么需要重启 OpenClaw？
A: 因为添加了新的 agent 配置，需要重启才能生效。

### Q2: LearnerBot 和 DevBot 有什么区别？
A: 
- LearnerBot: 专门用于自主学习，生成技能
- DevBot: 专门用于开发任务，编写代码

### Q3: 生成的技能在哪里？
A: `~/.openclaw/learner-workspace/skills/`

### Q4: 可以自定义学习深度吗？
A: 可以！说"深入学习 [主题]"或"快速学习 [主题]"

---

## 🔧 故障排除

### 问题1: LearnerBot 没有出现在 agents list
**解决方案**: 
```bash
# 检查配置
grep -A 10 '"id": "learner"' ~/.openclaw/openclaw.json

# 重启 OpenClaw
openclaw gateway restart
```

### 问题2: agent-browser 找不到
**解决方案**:
```bash
npm install -g agent-browser
```

### 问题3: 学习任务超时
**解决方案**: 
- 检查网络连接
- 简化学习主题
- 增加超时时间（修改配置）

---

## 📞 获取帮助

- 查看 SKILL.md 了解详细功能
- 查看 README.md 了解系统架构
- 查看 memory/2026-03-04.md 了解开发历史

---

**🎉 享受自主学习！**
