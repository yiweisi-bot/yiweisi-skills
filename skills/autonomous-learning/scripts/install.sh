#!/bin/bash

# 自主学习技能安装脚本

echo "🧠 正在安装 OpenClaw 自主学习技能..."
echo ""

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SCRIPTS_DIR="$SKILL_DIR/scripts"

# 1. 检查是否已经安装
if [ -L "/usr/local/bin/autonomous-learning" ]; then
  echo "   ⚠️  检测到已安装，正在更新..."
  rm -f "/usr/local/bin/autonomous-learning"
fi

# 2. 创建符号链接
ln -s "$SCRIPTS_DIR/autonomous-learning.sh" "/usr/local/bin/autonomous-learning"

if [ $? -eq 0 ]; then
  echo "   ✅ 命令已链接到: /usr/local/bin/autonomous-learning"
else
  echo "   ❌ 链接失败，请手动运行:"
  echo "      sudo ln -s $SCRIPTS_DIR/autonomous-learning.sh /usr/local/bin/autonomous-learning"
  exit 1
fi

# 3. 确保脚本可执行
chmod +x "$SCRIPTS_DIR"/*.sh

echo ""
echo "🎉 安装完成！"
echo ""
echo "📝 快速开始:"
echo "   autonomous-learning help       # 查看帮助"
echo "   autonomous-learning status     # 查看状态"
echo "   autonomous-learning learn now  # 立即学习"
echo ""
echo "🧠 祝你学习愉快！"
