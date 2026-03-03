#!/bin/bash

# OpenClaw 自主学习系统 - 主入口脚本
# 版本: 1.0.0

# 获取脚本真实路径
SOURCE=${BASH_SOURCE[0]}
while [ -h "$SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
  DIR=$(cd -P "$(dirname "$SOURCE" )" && pwd)
  SOURCE=$(readlink "$SOURCE")
  # if $SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file was located
  [[ $SOURCE != /* ]] && SOURCE=$DIR/$SOURCE
done
DIR=$(cd -P "$(dirname "$SOURCE" )" && pwd)

SKILL_DIR="$(cd "$DIR/.." && pwd)"
SCRIPTS_DIR="$SKILL_DIR/scripts"
VALIDATOR_DIR="$SKILL_DIR/scripts/validators"
CONFIG_DIR="$SKILL_DIR/config"
DATA_DIR="$SKILL_DIR/data"

# 创建必要的目录
mkdir -p "$CONFIG_DIR" "$DATA_DIR" "$DATA_DIR/skills" "$DATA_DIR/history"

# 加载配置文件
load_config() {
  local config_file="$CONFIG_DIR/config.json"
  if [ ! -f "$config_file" ]; then
    cat > "$config_file" << 'EOF'
{
  "idleThreshold": {
    "cpu": 50,
    "memory": 80,
    "inactiveMinutes": 10
  },
  "learningWindows": [
    "02:00-05:00",
    "13:00-14:00"
  ],
  "maxSessionDuration": 60,
  "cooldownMinutes": 30,
  "autoStart": true,
  "requireApproval": true
}
EOF
  fi
}

# 初始化学习目标文件
init_goals() {
  local goals_file="$DATA_DIR/goals.json"
  if [ ! -f "$goals_file" ]; then
    echo '{"goals": []}' > "$goals_file"
  fi
}

# 显示帮助
show_help() {
  cat << 'EOF'
🧠 OpenClaw 自主学习系统

使用方法:
  autonomous-learning [command] [options]

命令:
  help              显示帮助信息
  status            查看学习系统状态
  learn now         立即开始学习（手动触发）
  learn github      只学习 GitHub 内容
  learn web         只学习互联网内容
  learn topic <t>   学习指定主题
  config show       显示当前配置
  config set <k> <v> 设置配置项
  goal add <goal>   添加学习目标
  goal list         列出学习目标
  goal remove <id>  移除学习目标
  history show      显示学习历史
  history skills    显示生成的技能
  skills list       列出自动生成的技能
  skills review     审核待确认的技能

配置项:
  cpu      - CPU 使用率阈值（%）
  memory   - 内存使用率阈值（%）
  idle     - 空闲等待时间（分钟）
  duration - 单次学习时长（分钟）

示例:
  autonomous-learning learn now
  autonomous-learning config set memory 85
  autonomous-learning goal add "学习 Rust"
EOF
}

# 显示状态
show_status() {
  echo "🧠 自主学习系统状态"
  echo "========================"
  echo ""
  
  # 系统资源
  local cpu_usage=$(top -bn1 | grep "Cpu(s)" | sed "s/.*, *\([0-9.]*\)%* id.*/\1/" | awk '{print 100 - $1}')
  local mem_usage=$(free | grep Mem | awk '{print $3/$2 * 100.0}')
  
  echo "📊 当前资源使用:"
  echo "   CPU: ${cpu_usage}%"
  echo "   内存: ${mem_usage}%"
  echo ""
  
  # 配置信息
  echo "⚙️ 当前配置:"
  local config_file="$CONFIG_DIR/config.json"
  if [ -f "$config_file" ]; then
    local cpu_thresh=$(grep -o '"cpu": *[0-9]*' "$config_file" | cut -d: -f2)
    local mem_thresh=$(grep -o '"memory": *[0-9]*' "$config_file" | cut -d: -f2)
    echo "   CPU 阈值: ${cpu_thresh}%"
    echo "   内存阈值: ${mem_thresh}%"
  fi
  echo ""
  
  # 学习目标
  echo "🎯 学习目标:"
  local goals_file="$DATA_DIR/goals.json"
  if [ -f "$goals_file" ]; then
    local goal_count=$(grep -o '"text"' "$goals_file" | wc -l)
    echo "   待完成目标: ${goal_count} 个"
  fi
  echo ""
  
  # 学习历史
  echo "📚 学习历史:"
  local history_count=$(ls -1 "$DATA_DIR/history/" 2>/dev/null | wc -l)
  local skills_count=$(ls -1 "$DATA_DIR/skills/" 2>/dev/null | wc -l)
  echo "   学习会话: ${history_count} 次"
  echo "   生成技能: ${skills_count} 个"
  echo ""
  
  echo "========================"
  echo "运行 'autonomous-learning help' 查看所有命令"
}

# 立即学习
learn_now() {
  echo "🧠 开始自主学习..."
  echo "========================"
  echo ""
  
  # 创建学习会话记录
  local session_id=$(date +%Y%m%d_%H%M%S)
  local session_file="$DATA_DIR/history/session_${session_id}.json"
  
  cat > "$session_file" << EOF
{
  "id": "$session_id",
  "startTime": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "status": "running",
  "topics": [],
  "skills": []
}
EOF
  
  # 第一步：探索 GitHub
  echo "📡 步骤 1/7: 探索 GitHub..."
  explorer_script="$SCRIPTS_DIR/github-explorer.sh"
  if [ -f "$explorer_script" ]; then
    bash "$explorer_script" "$session_id"
  else
    echo "   ⚠️ GitHub 探索脚本未找到: $explorer_script"
  fi
  echo ""
  
  # 第二步：OpenClaw 专题学习 ⭐ 新增
  echo "🐾 步骤 2/7: OpenClaw 专题学习..."
  openclaw_script="$SCRIPTS_DIR/openclaw-learning.sh"
  if [ -f "$openclaw_script" ]; then
    bash "$openclaw_script" "$session_id"
  else
    echo "   ⚠️ OpenClaw 学习脚本未找到"
  fi
  echo ""
  
  # 第三步：探索网络资源
  echo "🌐 步骤 3/7: 探索网络资源..."
  web_explorer_script="$SCRIPTS_DIR/web-explorer.sh"
  if [ -f "$web_explorer_script" ]; then
    bash "$web_explorer_script" "$session_id"
  else
    echo "   ⚠️ 网络探索脚本未找到"
  fi
  echo ""
  
  # 第四步：知识提取
  echo "🔍 步骤 4/7: 提取知识..."
  extractor_script="$SCRIPTS_DIR/knowledge-extractor.sh"
  if [ -f "$extractor_script" ]; then
    bash "$extractor_script" "$session_id"
  else
    echo "   ⚠️ 知识提取脚本未找到"
  fi
  echo ""
  
  # 第五步：生成技能
  echo "🛠️ 步骤 5/7: 生成技能..."
  generator_script="$SCRIPTS_DIR/skill-generator.sh"
  if [ -f "$generator_script" ]; then
    bash "$generator_script" "$session_id"
  else
    echo "   ⚠️ 技能生成脚本未找到"
  fi
  echo ""
  
  # 第六步：技能质量校验 ⭐ 新增
  echo "🛡️ 步骤 6/7: 技能质量校验..."
  skill_validator="$VALIDATOR_DIR/skill-validator.sh"
  if [ -f "$skill_validator" ]; then
    chmod +x "$skill_validator" 2>/dev/null
    bash "$skill_validator" --all
  else
    echo "   ⚠️ 技能校验器未找到"
  fi
  echo ""
  
  # 第七步：总结报告
  echo "📋 步骤 7/7: 生成报告..."
  report_script="$SCRIPTS_DIR/report-generator.sh"
  if [ -f "$report_script" ]; then
    bash "$report_script" "$session_id"
  else
    echo "   ⚠️ 报告生成脚本未找到"
  fi
  echo ""
  
  # 更新会话状态
  if [ -f "$session_file" ]; then
    sed -i 's/"status": "running"/"status": "completed"/' "$session_file"
    echo "  \"endTime\": \"$(date -u +"%Y-%m-%dT%H:%M:%SZ")\"," >> "$session_file.tmp"
    sed -i '/^}/d' "$session_file"
    cat "$session_file" "$session_file.tmp" > "$session_file.new"
    echo "}" >> "$session_file.new"
    mv "$session_file.new" "$session_file"
    rm -f "$session_file.tmp"
  fi
  
  echo "========================"
  echo "✅ 学习会话完成！"
  echo ""
  echo "📊 快速总结:"
  echo "   会话 ID: $session_id"
  echo "   查看详情: autonomous-learning history show"
}

# 配置管理
config_show() {
  local config_file="$CONFIG_DIR/config.json"
  if [ -f "$config_file" ]; then
    echo "⚙️ 当前配置:"
    echo ""
    python3 -m json.tool "$config_file" 2>/dev/null || cat "$config_file"
  else
    echo "❌ 配置文件未找到"
  fi
}

config_set() {
  local key="$1"
  local value="$2"
  local config_file="$CONFIG_DIR/config.json"
  
  case "$key" in
    cpu)
      sed -i "s/\"cpu\": *[0-9]*/\"cpu\": $value/" "$config_file"
      echo "✅ CPU 阈值设置为: ${value}%"
      ;;
    memory)
      sed -i "s/\"memory\": *[0-9]*/\"memory\": $value/" "$config_file"
      echo "✅ 内存阈值设置为: ${value}%"
      ;;
    idle)
      sed -i "s/\"inactiveMinutes\": *[0-9]*/\"inactiveMinutes\": $value/" "$config_file"
      echo "✅ 空闲等待时间设置为: ${value} 分钟"
      ;;
    duration)
      sed -i "s/\"maxSessionDuration\": *[0-9]*/\"maxSessionDuration\": $value/" "$config_file"
      echo "✅ 单次学习时长设置为: ${value} 分钟"
      ;;
    *)
      echo "❌ 未知配置项: $key"
      echo "可用配置项: cpu, memory, idle, duration"
      ;;
  esac
}

# 目标管理
goal_add() {
  local goal_text="$*"
  local goals_file="$DATA_DIR/goals.json"
  
  # 简单的 JSON 操作（使用 Python 更可靠）
  if command -v python3 &>/dev/null; then
    python3 << PYTHON
import json
import sys
from datetime import datetime

goals_file = "$DATA_DIR/goals.json"
goal_text = """$goal_text"""

try:
    with open(goals_file, 'r') as f:
        data = json.load(f)
except:
    data = {"goals": []}

new_goal = {
    "id": len(data["goals"]) + 1,
    "text": goal_text,
    "priority": "medium",
    "createdAt": datetime.utcnow().isoformat() + "Z",
    "completed": False
}

data["goals"].append(new_goal)

with open(goals_file, 'w') as f:
    json.dump(data, f, indent=2)

print(f"✅ 学习目标已添加: {goal_text}")
PYTHON
  else
    # 简单的后备方案
    echo "⚠️ Python 不可用，使用简单模式"
    echo "{\"text\": \"$goal_text\", \"time\": \"$(date)\"}" >> "$DATA_DIR/goals.simple.txt"
    echo "✅ 学习目标已添加"
  fi
}

goal_list() {
  local goals_file="$DATA_DIR/goals.json"
  
  if command -v python3 &>/dev/null && [ -f "$goals_file" ]; then
    python3 << PYTHON
import json

goals_file = "$DATA_DIR/goals.json"

try:
    with open(goals_file, 'r') as f:
        data = json.load(f)
    
    print("🎯 学习目标列表")
    print("=" * 40)
    
    if not data["goals"]:
        print("暂无学习目标")
    else:
        for goal in data["goals"]:
            status = "✅" if goal.get("completed", False) else "⬜"
            priority = goal.get("priority", "medium")
            print(f"{status} [{goal['id']}] {goal['text']}")
            print(f"   优先级: {priority}")
            print()
except Exception as e:
    print(f"读取目标失败: {e}")
PYTHON
  else
    echo "📋 学习目标:"
    if [ -f "$DATA_DIR/goals.simple.txt" ]; then
      cat "$DATA_DIR/goals.simple.txt"
    else
      echo "暂无学习目标"
    fi
  fi
}

goal_remove() {
  local goal_id="$1"
  echo "⚠️ 目标删除功能需要 Python，手动编辑 $DATA_DIR/goals.json"
}

# 历史记录
history_show() {
  echo "📚 学习历史"
  echo "============"
  echo ""
  
  local history_dir="$DATA_DIR/history"
  if [ ! -d "$history_dir" ] || [ -z "$(ls -A "$history_dir" 2>/dev/null)" ]; then
    echo "暂无学习记录"
    echo ""
    echo "提示: 运行 'autonomous-learning learn now' 开始第一次学习"
    return
  fi
  
  local session_count=$(ls -1 "$history_dir/" | wc -l)
  echo "总学习会话: ${session_count} 次"
  echo ""
  
  # 显示最近 5 次会话
  echo "最近会话:"
  for session_file in "$history_dir"/session_*.json; do
    if [ -f "$session_file" ]; then
      local filename=$(basename "$session_file")
      local session_id=$(echo "$filename" | sed 's/session_//' | sed 's/.json//')
      echo "  • $session_id"
    fi
  done | tail -5
  
  echo ""
  echo "提示: 运行 'autonomous-learning history skills' 查看生成的技能"
}

history_skills() {
  echo "✨ 生成的技能"
  echo "============"
  echo ""
  
  local skills_dir="$DATA_DIR/skills"
  if [ ! -d "$skills_dir" ] || [ -z "$(ls -A "$skills_dir" 2>/dev/null)" ]; then
    echo "暂无生成的技能"
    return
  fi
  
  local skills_count=$(ls -1 "$skills_dir/" 2>/dev/null | wc -l)
  echo "总技能数: ${skills_count} 个"
  echo ""
  
  for skill_file in "$skills_dir"/*.md; do
    if [ -f "$skill_file" ]; then
      local skill_name=$(basename "$skill_file" .md)
      echo "  • $skill_name"
    fi
  done
}

# 技能管理
skills_list() {
  history_skills
}

skills_review() {
  echo "🔍 技能审核"
  echo "==========="
  echo ""
  echo "⚠️ 审核功能开发中..."
  echo ""
  echo "技能目录: $DATA_DIR/skills/"
  ls -la "$DATA_DIR/skills/" 2>/dev/null || echo "暂无技能"
}

# 主函数
main() {
  load_config
  init_goals
  
  case "$1" in
    help)
      show_help
      ;;
    status)
      show_status
      ;;
    learn)
      case "$2" in
        now)
          learn_now
          ;;
        github)
          echo "📡 GitHub 学习模式"
          learn_now  # 暂时复用，后续可拆分
          ;;
        web)
          echo "🌐 网络学习模式"
          learn_now  # 暂时复用，后续可拆分
          ;;
        topic)
          echo "📚 主题学习: $3"
          learn_now  # 暂时复用，后续可拆分
          ;;
        *)
          echo "❌ 未知学习命令: $2"
          echo "使用方法: autonomous-learning learn [now|github|web|topic <topic>]"
          ;;
      esac
      ;;
    config)
      case "$2" in
        show)
          config_show
          ;;
        set)
          config_set "$3" "$4"
          ;;
        *)
          echo "❌ 未知配置命令: $2"
          echo "使用方法: autonomous-learning config [show|set <key> <value>]"
          ;;
      esac
      ;;
    goal)
      case "$2" in
        add)
          shift 2
          goal_add "$@"
          ;;
        list)
          goal_list
          ;;
        remove)
          goal_remove "$3"
          ;;
        *)
          echo "❌ 未知目标命令: $2"
          echo "使用方法: autonomous-learning goal [add|list|remove <id>]"
          ;;
      esac
      ;;
    history)
      case "$2" in
        show)
          history_show
          ;;
        skills)
          history_skills
          ;;
        *)
          history_show
          ;;
      esac
      ;;
    skills)
      case "$2" in
        list)
          skills_list
          ;;
        review)
          skills_review
          ;;
        *)
          skills_list
          ;;
      esac
      ;;
    *)
      if [ -z "$1" ]; then
        show_status
      else
        echo "❌ 未知命令: $1"
        echo ""
        show_help
      fi
      ;;
  esac
}

# 运行主函数
main "$@"
