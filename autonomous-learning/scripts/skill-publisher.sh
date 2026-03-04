#!/bin/bash

# 技能发布工具
# 将待审核的技能发布到正式技能目录

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DATA_DIR="$SKILL_DIR/data"
PENDING_DIR="$DATA_DIR/skills/pending"
MAIN_SKILLS_DIR="/root/.openclaw/workspace/skills"

mkdir -p "$DATA_DIR/skills/published"
mkdir -p "$DATA_DIR/skills/rejected"

echo "📦 技能发布工具"
echo "==============="
echo ""

# 列出待审核技能
list_pending() {
  echo "📋 待审核技能:"
  echo ""
  
  local count=0
  for skill_file in "$PENDING_DIR"/*.md; do
    if [ -f "$skill_file" ] && [[ "$skill_file" != *".needs_review" ]]; then
      local skill_name=$(basename "$skill_file" .md)
      local size=$(wc -c < "$skill_file" 2>/dev/null || echo 0)
      local status=""
      
      if [ -f "${skill_file}.needs_review" ]; then
        status="⏳"
      elif [ -f "${skill_file}.quality_passed" ]; then
        status="✅"
      else
        status="📝"
      fi
      
      echo "  $status [$count] $skill_name (${size} bytes)"
      count=$((count + 1))
    fi
  done
  
  if [ "$count" -eq 0 ]; then
    echo "  (没有待审核的技能)"
  fi
  
  echo ""
  echo "  ⏳ = 待审核, ✅ = 质量通过, 📝 = 新技能"
}

# 查看技能详情
view_skill() {
  local skill_name="$1"
  local skill_file="$PENDING_DIR/${skill_name}.md"
  
  if [ ! -f "$skill_file" ]; then
    echo "❌ 技能不存在: $skill_name"
    return 1
  fi
  
  echo ""
  echo "📄 技能: $skill_name"
  echo "===================="
  echo ""
  cat "$skill_file"
  echo ""
  echo "===================="
}

# 发布技能
publish_skill() {
  local skill_name="$1"
  local skill_file="$PENDING_DIR/${skill_name}.md"
  
  if [ ! -f "$skill_file" ]; then
    echo "❌ 技能不存在: $skill_name"
    return 1
  fi
  
  # 从 SKILL.md 中提取技能目录名
  # 通常是 name 字段的 kebab-case 版本
  local skill_dir_name=$(grep "^name:" "$skill_file" | head -1 | cut -d: -f2 | xargs | tr ' ' '-' | tr '[:upper:]' '[:lower:]')
  
  if [ -z "$skill_dir_name" ]; then
    skill_dir_name="$skill_name"
  fi
  
  local target_dir="$MAIN_SKILLS_DIR/$skill_dir_name"
  
  echo "📦 发布技能: $skill_name"
  echo "   目标目录: $target_dir"
  echo ""
  
  # 检查是否已存在
  if [ -d "$target_dir" ]; then
    echo "⚠️ 技能目录已存在，是否覆盖？(y/N)"
    read -r confirm
    if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
      echo "❌ 取消发布"
      return 1
    fi
    rm -rf "$target_dir"
  fi
  
  # 创建技能目录结构
  mkdir -p "$target_dir"
  mkdir -p "$target_dir/scripts"
  mkdir -p "$target_dir/config"
  
  # 复制 SKILL.md
  cp "$skill_file" "$target_dir/SKILL.md"
  
  # 移动到已发布目录
  mv "$skill_file" "$DATA_DIR/skills/published/"
  rm -f "${skill_file}.needs_review" 2>/dev/null
  rm -f "${skill_file}.quality_passed" 2>/dev/null
  
  echo ""
  echo "✅ 技能发布成功！"
  echo "   位置: $target_dir"
  echo ""
  echo "💡 现在可以通过 OpenClaw 使用这个技能了！"
}

# 拒绝技能
reject_skill() {
  local skill_name="$1"
  local skill_file="$PENDING_DIR/${skill_name}.md"
  
  if [ ! -f "$skill_file" ]; then
    echo "❌ 技能不存在: $skill_name"
    return 1
  fi
  
  echo "🗑️ 拒绝技能: $skill_name"
  echo ""
  echo "确定要拒绝这个技能吗？(y/N)"
  read -r confirm
  
  if [[ "$confirm" =~ ^[Yy]$ ]]; then
    mv "$skill_file" "$DATA_DIR/skills/rejected/"
    rm -f "${skill_file}.needs_review" 2>/dev/null
    rm -f "${skill_file}.quality_passed" 2>/dev/null
    echo "✅ 已拒绝技能"
  else
    echo "❌ 取消"
  fi
}

# 交互式发布向导
interactive_wizard() {
  while true; do
    echo ""
    echo "📦 技能发布工具"
    echo "==============="
    echo ""
    echo "1. 列出待审核技能"
    echo "2. 查看技能详情"
    echo "3. 发布技能"
    echo "4. 拒绝技能"
    echo "5. 查看已发布技能"
    echo "6. 退出"
    echo ""
    echo -n "请选择操作 (1-6): "
    read -r choice
    
    case "$choice" in
      1)
        list_pending
        ;;
      2)
        echo ""
        echo -n "输入技能名称: "
        read -r skill_name
        view_skill "$skill_name"
        ;;
      3)
        echo ""
        echo -n "输入要发布的技能名称: "
        read -r skill_name
        publish_skill "$skill_name"
        ;;
      4)
        echo ""
        echo -n "输入要拒绝的技能名称: "
        read -r skill_name
        reject_skill "$skill_name"
        ;;
      5)
        echo ""
        echo "✅ 已发布技能:"
        ls -la "$DATA_DIR/skills/published/" 2>/dev/null || echo "  (暂无)"
        ;;
      6)
        echo "👋 再见！"
        exit 0
        ;;
      *)
        echo "❌ 无效选择"
        ;;
    esac
  done
}

# 主函数
main() {
  case "$1" in
    list)
      list_pending
      ;;
    view)
      view_skill "$2"
      ;;
    publish)
      publish_skill "$2"
      ;;
    reject)
      reject_skill "$2"
      ;;
    wizard)
      interactive_wizard
      ;;
    help|*)
      cat << 'EOF'
📦 技能发布工具

使用方法:
  skill-publisher list              # 列出待审核技能
  skill-publisher view <name>      # 查看技能详情
  skill-publisher publish <name>   # 发布技能
  skill-publisher reject <name>    # 拒绝技能
  skill-publisher wizard           # 交互式向导
  skill-publisher help             # 显示帮助

示例:
  skill-publisher list
  skill-publisher view openclaw-intro-skill
  skill-publisher publish openclaw-intro-skill
  skill-publisher wizard

技能位置:
  待审核: ~/.openclaw/workspace/skills/autonomous-learning/data/skills/pending/
  已发布: ~/.openclaw/workspace/skills/autonomous-learning/data/skills/published/
  已拒绝: ~/.openclaw/workspace/skills/autonomous-learning/data/skills/rejected/
  正式目录: ~/.openclaw/workspace/skills/
EOF
      ;;
  esac
}

# 运行
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  main "$@"
fi
