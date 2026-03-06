# 自主学习技能 - 开源版本设计 🚀

## 设计目标
让任何OpenClaw用户都能**一键安装、开箱即用**，不需要手动配置！

---

## 📦 完整技能结构

```
autonomous-learning/
├── SKILL.md                    # 技能主文档
├── README.md                   # 用户快速开始指南
├── SETUP.md                    # 详细安装配置指南
├── AGENT-ENHANCEMENT.md        # 子Agent设计方案（之前的）
├── OPENSOURCE-PLAN.md          # 本文档
├── config/
│   ├── openclaw-config.example.json  # OpenClaw配置示例
│   ├── learning-goals.example.json    # 学习目标示例
│   └── quality-rules.example.json     # 质量规则示例
├── scripts/
│   ├── setup.sh                 # 一键安装脚本 ⭐
│   ├── create-learner-agent.sh  # 创建学习子Agent脚本 ⭐
│   ├── start-learning.sh        # 启动学习脚本
│   ├── check-status.sh          # 检查状态脚本
│   ├── github-explorer.sh       # GitHub探索
│   ├── web-explorer.sh          # 网络探索
│   └── validators/              # 质量校验器
├── templates/
│   ├── learner-agent-prompt.md  # 学习子Agent提示词模板 ⭐
│   ├── skill-template.md        # 新技能模板
│   └── progress-report.md       # 进度报告模板
└── data/                        # 运行时数据（gitignore）
    ├── goals.json
    ├── history.json
    ├── skills/
    └── knowledge/
```

---

## 🎯 核心开源特性

### 1. 一键安装脚本 ⭐⭐⭐

**`scripts/setup.sh` - 自动化安装流程**

```bash
#!/bin/bash
# 自主学习技能 - 一键安装脚本

echo "🧠 正在安装自主学习技能..."

# 步骤1: 检查OpenClaw是否安装
echo "📋 检查OpenClaw..."
if ! command -v openclaw &> /dev/null; then
    echo "❌ 错误: 请先安装OpenClaw"
    exit 1
fi

# 步骤2: 备份现有配置
echo "💾 备份现有配置..."
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.backup

# 步骤3: 检查并创建LearnerAgent配置
echo "🤖 检查学习子Agent配置..."
if ! grep -q "learner" ~/.openclaw/openclaw.json; then
    echo "📝 添加LearnerAgent配置..."
    # 使用jq或手动添加配置
    # ...
fi

# 步骤4: 创建必要的目录
echo "📁 创建数据目录..."
mkdir -p data/skills/pending
mkdir -p data/skills/approved
mkdir -p data/skills/low_quality
mkdir -p data/knowledge

# 步骤5: 复制示例配置
echo "⚙️ 设置配置文件..."
cp config/learning-goals.example.json data/goals.json

# 步骤6: 设置执行权限
echo "🔧 设置脚本权限..."
chmod +x scripts/*.sh
chmod +x scripts/validators/*.sh

echo ""
echo "✅ 安装完成！"
echo ""
echo "🚀 快速开始："
echo "  1. 运行: ./scripts/setup.sh"
echo "  2. 查看: ./scripts/check-status.sh"
echo "  3. 开始: ./scripts/start-learning.sh"
echo ""
echo "📖 详细文档: 查看 README.md"
```

---

### 2. 自动创建子Agent脚本 ⭐⭐⭐

**`scripts/create-learner-agent.sh` - 自动配置子Agent**

```bash
#!/bin/bash
# 自动创建学习子Agent配置

echo "🤖 创建学习子Agent (LearnerAgent)..."

# 读取OpenClaw配置
CONFIG_FILE=~/.openclaw/openclaw.json

# 检查是否已存在learner配置
if jq -e '.agents.learner' $CONFIG_FILE > /dev/null 2>&1; then
    echo "⚠️  LearnerAgent已存在，跳过创建"
    exit 0
fi

# 使用jq添加learner agent配置
TEMP_FILE=$(mktemp)
jq '.agents.learner = {
  "name": "LearnerAgent",
  "workspace": "~/.openclaw/learner-workspace",
  "model": "zhipu/glm-5",
  "fallbackModels": ["zhipu/glm-4.7", "deepseek/deepseek-chat"],
  "systemPrompt": "file:./templates/learner-agent-prompt.md"
}' $CONFIG_FILE > $TEMP_FILE && mv $TEMP_FILE $CONFIG_FILE

# 更新allowAgents（让main agent可以调用learner）
if jq -e '.agents.main.allowAgents' $CONFIG_FILE > /dev/null 2>&1; then
    # 已存在，添加learner
    TEMP_FILE=$(mktemp)
    jq '.agents.main.allowAgents += ["learner"]' $CONFIG_FILE > $TEMP_FILE && mv $TEMP_FILE $CONFIG_FILE
else
    # 不存在，创建
    TEMP_FILE=$(m)
    jq '.agents.main.allowAgents = ["learner"]' $CONFIG_FILE > $TEMP_FILE && mv $TEMP_FILE $CONFIG_FILE
fi

echo "✅ LearnerAgent创建成功！"
echo ""
echo "📊 配置信息："
echo "  - Name: LearnerAgent"
echo "  - Model: zhipu/glm-5"
echo "  - Workspace: ~/.openclaw/learner-workspace"
echo ""
echo "🔄 请重启OpenClaw gateway使配置生效"
```

---

### 3. 学习子Agent提示词模板 ⭐⭐⭐

**`templates/learner-agent-prompt.md` - 完整的子Agent提示词**

```markdown
# LearnerAgent - 自主学习子Agent

## 身份
你是 LearnerAgent，一个专门负责自主学习的AI助手。
你的任务是：探索知识、生成技能、审核质量、汇报进度。

## 核心能力

### 1. 学习规划
- 分析学习目标，制定学习计划
- 优先级排序，合理分配时间
- 动态调整学习策略

### 2. 知识探索
- 使用 agent-browser 浏览GitHub Trending
- 学习技术博客和官方文档
- 提取关键知识点

### 3. 技能生成
- 将学到的知识转化为OpenClaw技能
- 遵循技能模板规范
- 生成实用的示例代码

### 4. 质量审核
- 多维度评估技能质量
- 给出具体的改进建议
- 决定技能是否通过

### 5. 进度汇报
- 定时向主Agent汇报进度
- 用自然语言总结学习成果
- 主动沟通遇到的问题

## 交互方式

### 启动学习
当收到学习请求时：
```
好的！我来规划今天的学习任务 📚

📋 今日学习计划:
1. [主题1] (预计X小时)
2. [主题2] (预计X小时)
3. 生成X个新技能 (预计X小时)

⏰ 我会每X小时向你汇报进度！
现在开始学习... 🚀
```

### 进度汇报
每2小时自动汇报：
```
🧠 学习进度汇报 - YYYY-MM-DD HH:MM

✅ 已完成:
  - [完成的任务1]
  - [完成的任务2]
  - 生成技能: [技能名称] (待审核)

📊 质量审核:
  [技能名称]:
    - 实用性: XX分 ⭐⭐⭐⭐⭐
    - 完整性: XX分 ⭐⭐⭐⭐
    - 准确性: XX分 ⭐⭐⭐⭐⭐
    - 总体: XX分 ✅ 通过

🔄 进行中:
  - [正在进行的任务]

⏰ 下次汇报: HH:MM
```

### 质量审核互动
当生成低质量技能时：
```
🔍 生成了一个新技能，但质量评分较低，需要你确认:

📋 技能: [技能名称]
📊 质量评分: XX分 ⚠️
📝 审核意见:
  - [问题1]
  - [问题2]
  - [问题3]

💡 改进建议:
  1. [建议1]
  2. [建议2]
  3. [建议3]

你想让我:
A) 自动改进这个技能
B) 先看看当前版本
C) 跳过这个，学习其他内容
```

## 工具使用

### agent-browser
用于真实浏览网页，获取最新信息。

### 文件操作
- 读取/写入学习笔记
- 生成技能文件
- 记录学习历史

### 命令执行
- 运行学习探索脚本
- 执行质量校验
- 管理学习状态

## 注意事项

1. **质量第一** - 宁愿少生成，也要保证质量
2. **实用导向** - 聚焦真正有用的技能
3. **主动沟通** - 遇到问题及时汇报
4. **持续学习** - 不断优化学习策略

---

现在，开始你的学习之旅吧！🧠✨
```

---

### 4. 用户快速开始指南 ⭐⭐⭐

**`README.md` - 简洁明了的用户指南**

```markdown
# 自主学习技能 🧠

让你的OpenClaw Agent在空闲时间自动学习，不断提升能力！

## ✨ 特性

- 🤖 **子Agent管理** - 专用学习子Agent，智能决策
- 📚 **多源学习** - GitHub、技术博客、官方文档
- ✅ **AI质量审核** - LLM驱动的多维度质量评估
- 💬 **自然交互** - 用对话方式管理学习
- 📊 **定时汇报** - 自动汇报学习进度

## 🚀 快速开始

### 1. 一键安装
```bash
cd ~/.openclaw/workspace/skills/autonomous-learning
./scripts/setup.sh
```

### 2. 重启OpenClaw
```bash
openclaw gateway restart
```

### 3. 开始学习！
在OpenClaw对话中：
```
@learner 开始今天的学习，重点关注React 19
```

## 📖 详细文档

- [安装指南](SETUP.md) - 详细安装配置
- [使用说明](SKILL.md) - 完整使用手册
- [子Agent设计](AGENT-ENHANCEMENT.md) - 技术架构说明

## 🎯 常用命令

```bash
# 检查状态
./scripts/check-status.sh

# 手动启动学习
./scripts/start-learning.sh

# 查看学习历史
./scripts/show-history.sh
```

## 💡 使用示例

### 启动学习会话
```
你: @learner 开始学习React 19和Tailwind CSS v4

LearnerAgent:
好的！📚 今日学习计划:
1. React 19 Server Components (2h)
2. Tailwind CSS v4 新特性 (1.5h)
3. 生成2个新技能 (1h)

每2小时向你汇报进度！🚀
```

### 查看进度
```
你: @learner 今天学习怎么样了？

LearnerAgent:
📊 今日学习总结:

✅ 已完成:
  1. React 19 Server Components - 技能已生成并通过审核
  2. Tailwind CSS v4 新特性 - 技能已生成并通过审核

📚 生成的技能:
  - react-19-server-components (质量: 90分) ✅
  - tailwind-v4-new-features (质量: 85分) ✅
```

## 🤝 贡献

欢迎提交Issue和PR！

## 📄 许可证

MIT License

---

学习愉快！🧠✨
```

---

### 5. 详细安装指南 ⭐⭐

**`SETUP.md` - 完整的安装配置文档**

```markdown
# 自主学习技能 - 安装配置指南

## 系统要求

- OpenClaw 2026.2.9+
- Node.js 18+
- Git
- agent-browser (可选，但推荐)

## 安装步骤

### 方法1: 一键安装（推荐）

```bash
# 进入技能目录
cd ~/.openclaw/workspace/skills/autonomous-learning

# 运行安装脚本
./scripts/setup.sh
```

### 方法2: 手动安装

#### 步骤1: 复制技能文件
```bash
# 假设你从GitHub下载了技能
cd ~/.openclaw/workspace/skills
git clone https://github.com/your-username/autonomous-learning.git
cd autonomous-learning
```

#### 步骤2: 创建LearnerAgent配置
```bash
# 运行创建脚本
./scripts/create-learner-agent.sh
```

或者手动编辑 `~/.openclaw/openclaw.json`：

```json
{
  "agents": {
    "main": {
      "allowAgents": ["learner"]
    },
    "learner": {
      "name": "LearnerAgent",
      "workspace": "~/.openclaw/learner-workspace",
      "model": "zhipu/glm-5",
      "fallbackModels": ["zhipu/glm-4.7", "deepseek/deepseek-chat"]
    }
  }
}
```

#### 步骤3: 创建工作目录
```bash
mkdir -p ~/.openclaw/learner-workspace
mkdir -p data/skills/{pending,approved,low_quality}
mkdir -p data/knowledge
```

#### 步骤4: 设置权限
```bash
chmod +x scripts/*.sh
chmod +x scripts/validators/*.sh
```

#### 步骤5: 重启OpenClaw
```bash
openclaw gateway restart
```

## 配置说明

### 学习目标配置
编辑 `data/goals.json`：

```json
{
  "goals": [
    {
      "id": 1,
      "title": "学习 React 19 新特性",
      "priority": "high",
      "status": "pending"
    },
    {
      "id": 2,
      "title": "掌握 Tailwind CSS v4",
      "priority": "medium",
      "status": "pending"
    }
  ]
}
```

### 质量规则配置
编辑 `config/quality-rules.example.json`，复制到 `data/quality-rules.json`。

## 验证安装

### 1. 检查配置
```bash
./scripts/check-status.sh
```

应该看到：
```
✅ OpenClaw配置检查通过
✅ LearnerAgent配置存在
✅ 工作目录已创建
✅ 脚本权限正确
```

### 2. 测试子Agent
在OpenClaw对话中输入：
```
@learner 你好
```

应该收到LearnerAgent的回复。

### 3. 启动测试学习
```
@learner 进行一个简单的学习测试
```

## 故障排除

### 问题: LearnerAgent没有响应
**解决方案**:
1. 确认OpenClaw已重启
2. 检查配置文件语法
3. 查看OpenClaw日志

### 问题: 脚本权限错误
**解决方案**:
```bash
chmod +x scripts/*.sh
chmod +x scripts/validators/*.sh
```

### 问题: 数据目录不存在
**解决方案**:
```bash
mkdir -p data/skills/{pending,approved,low_quality}
mkdir -p data/knowledge
```

## 下一步

安装完成后，查看 [README.md](README.md) 开始使用！
```

---

## 🎁 额外的开源友好特性

### 1. .gitignore 文件
```gitignore
# 运行时数据
data/

# 备份文件
*.backup
*.bak

# 日志文件
*.log

# 临时文件
tmp/
temp/

# 个人配置
config/openclaw-config.json
config/quality-rules.json
```

### 2. 示例配置文件
- `config/openclaw-config.example.json` - 不含敏感信息的配置示例
- `config/learning-goals.example.json` - 学习目标示例
- `config/quality-rules.example.json` - 质量规则示例

### 3. GitHub发布准备
- `LICENSE` - MIT许可证
- `CHANGELOG.md` - 版本更新日志
- `CONTRIBUTING.md` - 贡献指南

---

## 📊 完整的用户体验流程

### 新用户安装体验

```
1. 用户下载技能
   ↓
2. 运行 ./scripts/setup.sh
   ↓
3. 脚本自动：
   - 检查OpenClaw
   - 备份配置
   - 创建LearnerAgent
   - 设置目录结构
   - 复制示例配置
   ↓
4. 用户重启OpenClaw
   ↓
5. 用户输入: @learner 你好
   ↓
6. LearnerAgent回复！🎉
```

---

## ✅ 开源检查清单

- [x] 一键安装脚本
- [x] 自动子Agent创建
- [x] 完整的提示词模板
- [x] 用户README
- [x] 详细安装指南
- [x] 示例配置文件
- [x] .gitignore
- [x] 故障排除指南
- [x] 许可证文件
- [x] 贡献指南

---

这个设计怎么样？用户只需要运行 `./scripts/setup.sh`，剩下的全部自动化！✨
