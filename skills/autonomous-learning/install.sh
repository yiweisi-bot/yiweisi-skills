#!/bin/bash
# 自主学习技能 - 安装脚本
# 检查并创建 Learner Agent

set -e

echo "=================================================="
echo "🧠 自主学习技能 - 安装向导"
echo "=================================================="
echo ""

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 检查 OpenClaw 是否安装
echo "📋 步骤 1/4: 检查 OpenClaw 环境..."
if ! command -v openclaw &> /dev/null; then
    echo -e "${RED}❌ OpenClaw 未安装${NC}"
    echo "请先安装 OpenClaw: npm install -g openclaw"
    exit 1
fi
echo -e "${GREEN}✅ OpenClaw 已安装${NC}"
echo ""

# 检查是否有 learner agent
echo "📋 步骤 2/4: 检查 Learner Agent..."
OPENCLAW_CONFIG="$HOME/.openclaw/openclaw.json"

if [ ! -f "$OPENCLAW_CONFIG" ]; then
    echo -e "${RED}❌ OpenClaw 配置文件不存在${NC}"
    exit 1
fi

# 检查配置中是否已有 learner agent
LEARNER_IN_CONFIG=$(grep -c '"id": "learner"' "$OPENCLAW_CONFIG" || true)

if [ "$LEARNER_IN_CONFIG" -gt 0 ]; then
    echo -e "${GREEN}✅ Learner Agent 已存在于配置中${NC}"
else
    echo -e "${YELLOW}⚠️  Learner Agent 不存在，正在创建...${NC}"
    
    # 备份原配置文件
    cp "$OPENCLAW_CONFIG" "$OPENCLAW_CONFIG.backup.$(date +%Y%m%d_%H%M%S)"
    
    # 使用 Python 来更新 JSON 配置
    python3 << 'PYTHON_SCRIPT'
import json
import sys

config_file = "/root/.openclaw/openclaw.json"

try:
    with open(config_file, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    # 添加 learner agent 到 agents.list
    learner_agent = {
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
        },
        "groupChat": {
            "mentionPatterns": ["@learner", "@学习", "@learn"]
        }
    }
    
    # 检查是否已存在
    exists = False
    for agent in config['agents']['list']:
        if agent['id'] == 'learner':
            exists = True
            break
    
    if not exists:
        config['agents']['list'].append(learner_agent)
        print("✅ Learner Agent 已添加到配置")
    
    # 更新 main agent 的 allowAgents
    for agent in config['agents']['list']:
        if agent['id'] == 'main':
            if 'subagents' not in agent:
                agent['subagents'] = {}
            if 'allowAgents' not in agent['subagents']:
                agent['subagents']['allowAgents'] = []
            
            # 添加 learner 到 allowAgents（如果不存在）
            if 'learner' not in agent['subagents']['allowAgents']:
                agent['subagents']['allowAgents'].append('learner')
                print("✅ Learner Agent 已添加到 main agent 的 allowAgents")
    
    # 保存配置
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print("✅ OpenClaw 配置已更新")
    
except Exception as e:
    print(f"❌ 更新配置失败: {e}")
    sys.exit(1)
PYTHON_SCRIPT

    echo -e "${GREEN}✅ Learner Agent 配置完成${NC}"
fi

echo ""

# 创建 Learner Agent 工作空间
echo "📋 步骤 3/4: 创建 Learner Agent 工作空间..."
LEARNER_WORKSPACE="$HOME/.openclaw/learner-workspace"

if [ ! -d "$LEARNER_WORKSPACE" ]; then
    mkdir -p "$LEARNER_WORKSPACE"
    mkdir -p "$LEARNER_WORKSPACE/skills"
    mkdir -p "$LEARNER_WORKSPACE/memory"
    
    # 创建 AGENTS.md
    cat > "$LEARNER_WORKSPACE/AGENTS.md" << 'EOF'
# AGENTS.md - LearnerBot Workspace

这是 LearnerBot 的工作空间。

## 工作流程

1. 接收学习任务
2. 使用 agent-browser 搜索信息
3. 生成技能内容
4. 执行质量验证
5. 返回结果

## 输出目录

- `skills/` - 生成的技能
- `memory/` - 学习记忆
EOF
    
    echo -e "${GREEN}✅ 工作空间已创建${NC}"
else
    echo -e "${GREEN}✅ 工作空间已存在${NC}"
fi

echo ""

# 检查技能依赖
echo "📋 步骤 4/4: 检查技能依赖..."

# 检查 agent-browser
if command -v agent-browser &> /dev/null; then
    echo -e "${GREEN}✅ agent-browser 已安装${NC}"
else
    echo -e "${YELLOW}⚠️  agent-browser 未安装${NC}"
    echo "   建议安装: npm install -g agent-browser"
fi

# 检查 Python
if command -v python3 &> /dev/null; then
    echo -e "${GREEN}✅ Python3 已安装${NC}"
else
    echo -e "${RED}❌ Python3 未安装${NC}"
    exit 1
fi

echo ""
echo "=================================================="
echo -e "${GREEN}✅ 自主学习技能安装完成！${NC}"
echo "=================================================="
echo ""
echo "⚠️  重要：需要重启 OpenClaw 使配置生效"
echo ""
echo "   重启命令:"
echo "   openclaw gateway restart"
echo ""
echo "📝 使用方法:"
echo "   1. 对乙维斯说: '开始学习 [主题]'"
echo "   2. 乙维斯会调用 LearnerBot 进行学习"
echo "   3. LearnerBot 会返回学习结果"
echo ""
echo "🎯 示例:"
echo "   - '开始学习 TypeScript 基础类型'"
echo "   - '学习 React Hooks'"
echo "   - '学习 Python 装饰器'"
echo ""
echo "📚 生成的技能会保存在:"
echo "   ~/.openclaw/learner-workspace/skills/"
echo ""
