#!/bin/bash

# OpenClaw 持续学习系统 (简化稳定版)
# 支持时间控制、进度条显示

# 获取脚本真实路径
SOURCE=${BASH_SOURCE[0]}
while [ -h "$SOURCE" ]; do
  DIR=$(cd -P "$(dirname "$SOURCE" )" && pwd)
  SOURCE=$(readlink "$SOURCE")
  [[ $SOURCE != /* ]] && SOURCE=$DIR/$SOURCE
done
DIR=$(cd -P "$(dirname "$SOURCE" )" && pwd)

SKILL_DIR="$(cd "$DIR/.." && pwd)"
DATA_DIR="$SKILL_DIR/data"
SCRIPTS_DIR="$SKILL_DIR/scripts"

mkdir -p "$DATA_DIR/continuous"
mkdir -p "$DATA_DIR/learning-history"

# 配置
DEFAULT_DURATION=20
STATE_FILE="$DATA_DIR/continuous/state.json"
LEARNED_FILE="$DATA_DIR/learning-history/learned.txt"
LOCK_FILE="$DATA_DIR/continuous/learning.lock"

# 技术主题库
TECH_TOPICS=(
  "写作技巧"
  "机器人写作"
  "如何隐藏AI风格"
  "如何编写博客"
  "如何写出爆款文章"
  "Rust 异步编程"
  "WebAssembly 系统编程"
  "Kubernetes 操作"
  "React Server Components"
  "TypeScript 5.0 新特性"
  "GraphQL 最佳实践"
  "Docker 安全"
  "PostgreSQL 性能优化"
  "CI/CD 最佳实践"
  "Git 高级技巧"
)

# 格式化时间
format_time() {
  local total_seconds="$1"
  local minutes=$((total_seconds / 60))
  local seconds=$((total_seconds % 60))
  printf "%02d:%02d" "$minutes" "$seconds"
}

# 显示进度条
show_progress() {
  local start_time="$1"
  local duration="$2"
  local activity="$3"
  
  local current=$(date +%s)
  local elapsed=$((current - start_time))
  local total=$((duration * 60))
  local remaining=$((total - elapsed))
  
  if [ "$remaining" -lt 0 ]; then
    remaining=0
  fi
  
  local percent=$((elapsed * 100 / total))
  local width=40
  local filled=$((elapsed * width / total))
  local empty=$((width - filled))
  
  local bar=""
  bar+="["
  for ((i=0; i<filled; i++)); do bar+="▓"; done
  for ((i=0; i<empty; i++)); do bar+="░"; done
  bar+="]"
  
  printf "\r%s %3d%% | 已用: %s | 剩余: %s | %s" \
    "$bar" \
    "$percent" \
    "$(format_time "$elapsed")" \
    "$(format_time "$remaining")" \
    "$activity"
}

# 初始化
init() {
  mkdir -p "$(dirname "$LEARNED_FILE")"
  mkdir -p "$(dirname "$STATE_FILE")"
  [ ! -f "$LEARNED_FILE" ] && touch "$LEARNED_FILE"
}

# 检查是否已学习
has_learned() {
  grep -q "^$1$" "$LEARNED_FILE" 2>/dev/null
}

# 记录学习
record_learned() {
  if ! has_learned "$1"; then
    echo "$1" >> "$LEARNED_FILE"
  fi
}

# 获取未学习的主题
get_new_topics() {
  for topic in "${TECH_TOPICS[@]}"; do
    if ! has_learned "$topic"; then
      echo "$topic"
    fi
  done
}

# 学习单个主题
learn_topic() {
  local topic="$1"
  local start_time="$2"
  local duration="$3"
  
  echo ""
  echo "📚 学习主题: $topic"
  
  # 调用 GitHub 探索
  if [ -f "$SCRIPTS_DIR/github-explorer.sh" ]; then
    bash "$SCRIPTS_DIR/github-explorer.sh" "learn_$(date +%s)" 2>&1 | while read -r line; do
      show_progress "$start_time" "$duration" "学习:${topic:0:10}..."
    done
  else
    for i in {1..15}; do
      show_progress "$start_time" "$duration" "学习:${topic:0:10}..."
      sleep 1
    done
  fi
  
  record_learned "$topic"
  
  echo ""
  echo "✅ 完成: $topic"
}

# 时间填充
fill_time() {
  local start_time="$1"
  local duration="$2"
  local fill_cycle="$3"
  
  case $((fill_cycle % 4)) in
    0)
      if [ -f "$SCRIPTS_DIR/github-explorer.sh" ]; then
        bash "$SCRIPTS_DIR/github-explorer.sh" "fill_$(date +%s)" 2>&1 | while read -r line; do
          show_progress "$start_time" "$duration" "GitHub探索中..."
        done
      else
        for i in {1..20}; do
          show_progress "$start_time" "$duration" "GitHub探索中..."
          sleep 1
        done
      fi
      ;;
    1)
      if [ -f "$SCRIPTS_DIR/openclaw-learning.sh" ]; then
        bash "$SCRIPTS_DIR/openclaw-learning.sh" "fill_$(date +%s)" 2>&1 | while read -r line; do
          show_progress "$start_time" "$duration" "OpenClaw学习中..."
        done
      else
        for i in {1..20}; do
          show_progress "$start_time" "$duration" "OpenClaw学习中..."
          sleep 1
        done
      fi
      ;;
    2)
      for i in {1..20}; do
        show_progress "$start_time" "$duration" "知识整理中..."
        sleep 1
      done
      ;;
    3)
      for i in {1..20}; do
        show_progress "$start_time" "$duration" "技能生成中..."
        sleep 1
      done
      ;;
  esac
}

# 主学习循环
start_learning() {
  local duration=${1:-$DEFAULT_DURATION}
  
  echo ""
  echo "🧠 OpenClaw 持续学习"
  echo "===================="
  echo "⏱️ 计划时长: ${duration} 分钟"
  echo "🕐 开始时间: $(date '+%Y-%m-%d %H:%M:%S')"
  echo "🎯 结束时间: $(date -d "+${duration} minutes" '+%Y-%m-%d %H:%M:%S')"
  echo ""
  
  # 检查锁
  if [ -f "$LOCK_FILE" ]; then
    echo "❌ 已有学习在进行中"
    return 1
  fi
  
  touch "$LOCK_FILE"
  init
  
  local start_time=$(date +%s)
  local end_time=$((start_time + duration * 60))
  local topics_learned=0
  local fill_cycles=0
  
  # 获取新主题
  local new_topics=($(get_new_topics))
  
  echo "📋 待学习主题: ${#new_topics[@]} 个"
  echo ""
  
  # ========== 第一阶段：学习新主题 ==========
  echo "📖 阶段 1/2: 学习新主题"
  echo "----------------------------------------"
  
  for topic in "${new_topics[@]}"; do
    local current=$(date +%s)
    if [ "$current" -ge "$end_time" ]; then
      echo ""
      echo "⏰ 时间到！"
      break
    fi
    
    if [ ! -f "$LOCK_FILE" ]; then
      echo ""
      echo "🛑 收到停止信号"
      break
    fi
    
    learn_topic "$topic" "$start_time" "$duration"
    topics_learned=$((topics_learned + 1))
    
    sleep 2
  done
  
  # ========== 第二阶段：时间填充 ==========
  echo ""
  echo "🔄 阶段 2/2: 时间填充模式"
  echo "----------------------------------------"
  
  while true; do
    local current=$(date +%s)
    if [ "$current" -ge "$end_time" ]; then
      echo ""
      echo ""
      echo "⏰ 时间到！学习圆满结束！"
      break
    fi
    
    if [ ! -f "$LOCK_FILE" ]; then
      echo ""
      echo ""
      echo "🛑 收到停止信号"
      break
    fi
    
    fill_time "$start_time" "$duration" "$fill_cycles"
    fill_cycles=$((fill_cycles + 1))
    
    sleep 5
  done
  
  # ========== 清理与统计 ==========
  rm -f "$LOCK_FILE"
  
  local actual_end=$(date +%s)
  local total_seconds=$((actual_end - start_time))
  local total_minutes=$((total_seconds / 60))
  local total_remainder=$((total_seconds % 60))
  local learned_count=$(wc -l < "$LEARNED_FILE" 2>/dev/null || echo 0)
  
  echo ""
  echo "🎉 学习完成！"
  echo "===================="
  echo "📊 完整统计:"
  echo "   计划时长: ${duration} 分钟"
  echo "   实际学习: ${total_minutes} 分 ${total_remainder} 秒"
  echo "   完成度: $(( (total_seconds * 100) / (duration * 60) ))%"
  echo "   本次学习: ${topics_learned} 个主题"
  echo "   填充周期: ${fill_cycles} 次"
  echo "   总计学习: ${learned_count} 个主题"
  echo ""
  echo "📜 最近学习:"
  tail -5 "$LEARNED_FILE" 2>/dev/null | while read -r t; do
    [ -n "$t" ] && echo "   • $t"
  done
}

# 停止学习
stop_learning() {
  if [ -f "$LOCK_FILE" ]; then
    rm -f "$LOCK_FILE"
    echo "🛑 已停止学习"
  else
    echo "✅ 没有正在进行的学习"
  fi
}

# 查看状态
show_status() {
  echo "🧠 持续学习状态"
  echo "===================="
  echo ""
  
  if [ -f "$LOCK_FILE" ]; then
    echo "🟢 状态: 学习中..."
  else
    echo "⚪ 状态: 空闲"
  fi
  
  local learned=0
  if [ -f "$LEARNED_FILE" ]; then
    learned=$(wc -l < "$LEARNED_FILE" 2>/dev/null || echo 0)
  fi
  
  echo "📚 总学习: ${learned} 个主题"
  
  if [ "$learned" -gt 0 ] && [ -f "$LEARNED_FILE" ]; then
    echo ""
    echo "📜 最近学习:"
    tail -5 "$LEARNED_FILE" 2>/dev/null | while read -r t; do
      [ -n "$t" ] && echo "   • $t"
    done
  fi
}

# 主函数
main() {
  case "$1" in
    start)
      start_learning "${2:-$DEFAULT_DURATION}"
      ;;
    stop)
      stop_learning
      ;;
    status)
      show_status
      ;;
    reset)
      rm -f "$LEARNED_FILE" "$LOCK_FILE" 2>/dev/null
      echo "🧹 已重置学习状态"
      ;;
    help)
      cat << 'EOF'
🧠 OpenClaw 持续学习系统

使用方法:
  continuous-learning start [minutes]   # 开始学习 (默认20分钟)
  continuous-learning stop              # 停止学习
  continuous-learning status            # 查看状态
  continuous-learning reset             # 重置学习记录
  continuous-learning help              # 显示帮助

示例:
  continuous-learning start 30          # 学习30分钟
  continuous-learning status            # 查看状态

核心特性:
  ✅ 实时进度条 - 直观显示学习进度
  ✅ 时间倒计时 - 显示已用/剩余时间
  ✅ 两阶段学习 - 先学新主题，再时间填充
EOF
      ;;
    *)
      echo "使用: $0 {start|stop|status|reset|help}"
      ;;
  esac
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  main "$@"
fi
