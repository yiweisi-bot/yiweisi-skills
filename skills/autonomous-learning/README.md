# 🧠 自主学习系统

乙维斯的自主学习系统 - 让Agent能够自主设定学习目标、收集信息、生成高质量技能，并通过三层质量验证确保技能质量。

---

## ⚠️ 重要提示：Token消耗

这个技能会消耗大量Token！请合理配置使用模式。

**三种使用模式**:
- 💰 经济型: 入门深度 + 小预算
- ⚖️ 平衡型: 系统深度 + 中等预算（推荐）
- 🏆 质量型: 精通深度 + 大预算

详细成本优化指南请见 [COST-OPTIMIZATION.md](COST-OPTIMIZATION.md)

---

## 快速开始

### 安装
```bash
cd /root/.openclaw/workspace/skills/autonomous-learning
bash scripts/setup.sh
```

### 使用
```bash
# 查看帮助
autonomous-learning help

# 添加学习目标
autonomous-learning goal add "学习 React 19"

# 开始学习
autonomous-learning learn now

# 查看生成的技能
autonomous-learning skills list
```

---

## 功能特性

### 5阶段完整架构
1. ✅ **Phase 1**: 基础框架 - 数据库、CLI、安装脚本
2. ✅ **Phase 2**: 核心流程 - 优先级、信息评分、学习循环
3. ✅ **Phase 3**: 技能生成 - 大纲设计、内容生成、版本管理
4. ✅ **Phase 4**: 质量验证 - 规则验证、AI验证、三层验证
5. ✅ **Phase 5**: 完善优化 - 启动交互、配置向导

### 核心亮点
- 🎯 智能优先级计算（5个维度）
- 🔄 Action-Reflection-Iteration 学习循环
- ✨ 完整的技能生成（大纲+内容+版本）
- 🛡️ 三层质量验证（规则→AI→人工）
- 🗣️ 友好的启动交互流程

---

## 项目结构

```
autonomous-learning/
├── database/              # 数据库模块
├── scripts/               # 脚本
├── templates/             # 模板
├── generated-skills/      # 生成的技能
├── data/                  # 数据
├── SKILL.md              # 技能入口
├── README.md             # 本文件
└── IMPLEMENTATION-*.md   # 实现文档
```

---

## 文档

- [SKILL.md](SKILL.md) - 技能使用指南
- [IMPLEMENTATION-COMPLETE.md](IMPLEMENTATION-COMPLETE.md) - 完整实现总结
- [IMPLEMENTATION-PHASE1.md](IMPLEMENTATION-PHASE1.md) - Phase 1 文档
- [IMPLEMENTATION-PHASE2.md](IMPLEMENTATION-PHASE2.md) - Phase 2 文档
- [IMPLEMENTATION-PHASE3.md](IMPLEMENTATION-PHASE3.md) - Phase 3 文档
- [IMPLEMENTATION-PHASE4.md](IMPLEMENTATION-PHASE4.md) - Phase 4 文档

---

## 作者

**乙维斯** ✨

---

_让AI真正学会学习！_ 🧠
