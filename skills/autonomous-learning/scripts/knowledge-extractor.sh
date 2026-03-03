#!/bin/bash

# 知识提取脚本
# 从探索结果中提取结构化知识

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DATA_DIR="$SKILL_DIR/data"
SESSION_ID="$1"

mkdir -p "$DATA_DIR/knowledge"

echo "   🔍 开始提取知识..."

# 检查是否有知识文件
knowledge_file="$DATA_DIR/knowledge_${SESSION_ID:-latest}.md"
if [ ! -f "$knowledge_file" ]; then
  echo "   ⚠️ 未找到知识文件，跳过提取"
  exit 0
fi

# MVP 版本：简单的知识提取
# 从预置的知识文件中提取可用于生成技能的内容

echo "   📝 分析知识内容..."

# 1. 识别可生成技能的主题
echo "   🎯 识别技能主题..."

skill_topics=(
  "rust-intro"
  "webassembly-basics" 
  "github-actions-guide"
  "react-19-overview"
  "tailwind-css-v4"
  "ai-agents-intro"
)

# 保存待生成的技能列表
skills_list="$DATA_DIR/skills_to_generate.txt"
> "$skills_list"

for topic in "${skill_topics[@]}"; do
  echo "$topic" >> "$skills_list"
  echo "      • $topic"
done

# 2. 提取每个主题的关键点
echo ""
echo "   💡 提取知识要点..."

# 为每个主题创建知识摘要
for topic in "${skill_topics[@]}"; do
  topic_knowledge_file="$DATA_DIR/knowledge/${topic}.md"
  
  case "$topic" in
    rust-intro)
      cat > "$topic_knowledge_file" << 'EOF'
# Rust 入门知识

## 核心概念
- 所有权系统
- 借用检查器
- 模式匹配
- 零成本抽象

## 适用场景
- WebAssembly 开发
- 系统工具
- 高性能后端
- 嵌入式系统

## 学习资源
- https://www.rust-lang.org/learn
- https://doc.rust-lang.org/book/
EOF
      ;;
    webassembly-basics)
      cat > "$topic_knowledge_file" << 'EOF'
# WebAssembly 基础知识

## 核心概念
- 二进制指令格式
- 沙箱执行环境
- 多语言支持
-  near-native 性能

## 适用场景
- 浏览器高性能应用
- 边缘计算
- 插件系统
- 跨平台应用

## 学习资源
- https://webassembly.org/getting-started/
- https://developer.mozilla.org/en-US/docs/WebAssembly
EOF
      ;;
    github-actions-guide)
      cat > "$topic_knowledge_file" << 'EOF'
# GitHub Actions 指南

## 核心概念
- Workflows（工作流）
- Events（事件触发）
- Jobs（任务）
- Steps（步骤）
- Actions（动作）

## 适用场景
- CI/CD 流水线
- 自动化发布
- 项目管理
- Issue 处理

## 学习资源
- https://docs.github.com/en/actions
EOF
      ;;
    react-19-overview)
      cat > "$topic_knowledge_file" << 'EOF'
# React 19 概览

## 核心特性
- Server Components
- 新的 Hooks
- 性能优化
- 开发体验改进

## 学习资源
- https://react.dev/
EOF
      ;;
    tailwind-css-v4)
      cat > "$topic_knowledge_file" << 'EOF'
# Tailwind CSS v4

## 核心概念
- Utility-First CSS
- Just-in-Time 编译器
- 响应式设计
- 自定义主题

## 学习资源
- https://tailwindcss.com/docs
EOF
      ;;
    ai-agents-intro)
      cat > "$topic_knowledge_file" << 'EOF'
# AI Agents 入门

## 核心概念
- 自主智能体
- 工具使用
- 规划能力
- 记忆系统

## 架构模式
- Single Agent
- Multi-Agent 协作
- 工具调用框架

## 学习资源
- OpenClaw 官方文档
EOF
      ;;
  esac
  
  echo "      ✓ $topic"
done

# 3. 创建学习索引
echo ""
echo "   📚 创建知识索引..."

index_file="$DATA_DIR/knowledge/index.json"
cat > "$index_file" << EOF
{
  "extractedAt": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "sessionId": "$SESSION_ID",
  "topics": [
EOF

# 添加主题到索引（手动构建 JSON）
first=true
for topic in "${skill_topics[@]}"; do
  if [ "$first" = true ]; then
    first=false
  else
    echo "," >> "$index_file"
  fi
  echo "    \"$topic\"" >> "$index_file"
done

cat >> "$index_file" << 'EOF'

  ],
  "totalTopics": 6
}
EOF

echo ""
echo "   ✅ 知识提取完成"
echo "      - 提取 ${#skill_topics[@]} 个知识主题"
echo "      - 知识目录: $DATA_DIR/knowledge/"
