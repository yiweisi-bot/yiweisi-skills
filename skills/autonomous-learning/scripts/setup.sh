#!/bin/bash
# ============================================
# 自主学习系统 - 一键安装脚本
# ============================================

set -e

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                    🧠 自主学习系统安装                           ║"
echo "║              OpenClaw Agent Autonomous Learning               ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

echo -e "${BLUE}📂 技能目录: $SKILL_DIR${NC}"

# 创建必要的目录
echo -e "${YELLOW}📁 创建目录结构...${NC}"
mkdir -p "$SKILL_DIR/data"
mkdir -p "$SKILL_DIR/data/backups"
mkdir -p "$SKILL_DIR/templates"
mkdir -p "$SKILL_DIR/database"

echo -e "${GREEN}✅ 目录创建完成${NC}"

# 初始化数据库
echo -e "${YELLOW}💾 初始化数据库...${NC}"
cd "$SKILL_DIR"
python3 -c "
from database.db import get_db
db = get_db()
print('数据库初始化成功:', db.db_path)
"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ 数据库初始化成功${NC}"
else
    echo -e "${RED}❌ 数据库初始化失败${NC}"
    exit 1
fi

# 设置执行权限
echo -e "${YELLOW}🔧 设置执行权限...${NC}"
chmod +x "$SKILL_DIR/scripts/autonomous-learning.py"
chmod +x "$SKILL_DIR/database/db.py"

echo -e "${GREEN}✅ 权限设置完成${NC}"

# 创建符号链接（如果还没有）
echo -e "${YELLOW}🔗 创建命令链接...${NC}"
if [ ! -f "/usr/local/bin/autonomous-learning" ]; then
    ln -sf "$SKILL_DIR/scripts/autonomous-learning.py" /usr/local/bin/autonomous-learning
    echo -e "${GREEN}✅ 命令链接创建成功${NC}"
else
    echo -e "${YELLOW}⚠️  命令链接已存在${NC}"
fi

# 显示安装完成信息
echo -e ""
echo -e "${GREEN}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║                    ✅ 安装完成！                                ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════════════════════════╝${NC}"
echo -e ""
echo -e "${BLUE}📋 快速开始:${NC}"
echo -e "  ${GREEN}autonomous-learning help${NC}          - 查看帮助"
echo -e "  ${GREEN}autonomous-learning status${NC}        - 查看状态"
echo -e "  ${GREEN}autonomous-learning learn now${NC}      - 立即学习"
echo -e "  ${GREEN}autonomous-learning goal add${NC}       - 添加学习目标"
echo -e ""
echo -e "${BLUE}📂 项目结构:${NC}"
echo -e "  技能目录: $SKILL_DIR"
echo -e "  数据库: $SKILL_DIR/data/learning.db"
echo -e ""
echo -e "${YELLOW}💡 提示:${NC}"
echo -e "  当前为 Phase 1 基础框架版本"
echo -e "  完整学习流程即将推出..."
echo -e ""
