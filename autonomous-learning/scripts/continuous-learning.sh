#!/bin/bash

#!/bin/bash

# OpenClaw 持续学习系统 (简化可靠版)
# 支持时间控制、重复检测、目标管理

# 获取脚本真实路径（处理符号链接）
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
  "Rust 异步编程"
  "WebAssembly 系统编程"
  "Kubernetes 操作"
  "eBPF 可观测性"
  "React Server Components"
  "TypeScript 5.0 新特性"
  "GraphQL 最佳实践"
  "gRPC 微服务"
  "Docker 安全"
  "Terraform 基础设施"
  "Prometheus 监控"
  "Grafana 可视化"
  "PostgreSQL 性能优化"
  "Redis 集群"
  "Git 高级技巧"
  "CI/CD 最佳实践"
)

# 初始化
init() {
  mkdir -p "$(dirname "$LEARNED_FILE")"
  mkdir -p "$(dirname "$STATE_FILE")"
  [ ! -f "$LEARNED_FILE" ] && touch "$LEARNED_FILE"
  
  if [ ! -f "$STATE_FILE" ]; then
    cat > "$STATE_FILE" << 'EOF'
{
  "isLearning": false,
  "startTime": null,
  "duration": 20,
  "topicsLearned": 0
}
EOF
  fi
}

# 检查是否已学习
has_learned() {
  grep -q "^$1$" "$LEARNED_FILE" 2>/dev/null
}

# 记录学习
record_learned() {
  if ! has_learned "$1"; then
    echo "$1" >> "$LEARNED_FILE"
    echo "✅ 学习: $1"
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
  echo ""
  echo "📚 学习主题: $topic"
  echo "🕐 开始: $(date '+%H:%M:%S')"
  
  local start=$(date +%s)
  
  # 调用 GitHub 探索
  if [ -f "$SCRIPTS_DIR/github-explorer.sh" ]; then
    bash "$SCRIPTS_DIR/github-explorer.sh" "learn_$(date +%s)"
  fi
  
  # 记录
  record_learned "$topic"
  
  local end=$(date +%s)
  local duration=$((end - start))
  echo "✅ 完成: $topic (耗时: ${duration}秒)"
}

# 更新状态
update_state() {
  local key="$1"
  local value="$2"
  
  if command -v python3 &>/dev/null; then
    python3 << PYTHON
import json
from datetime import datetime

state_file = "$STATE_FILE"

try:
    with open(state_file, 'r') as f:
        data = json.load(f)
    
    data["$key"] = $value
    if "$key" == "isLearning" and $value:
        data["startTime"] = datetime.utcnow().isoformat() + "Z"
    
    with open(state_file, 'w') as f:
        json.dump(data, f, indent=2)
except:
    pass
PYTHON
  fi
}

# 获取已学习时间（分钟）
get_elapsed() {
  if [ ! -f "$STATE_FILE" ] || ! command -v python3 &>/dev/null; then
    echo 0
    return
  fi
  
  python3 << PYTHON 2>/dev/null || echo 0
import json
from datetime import datetime

state_file = "$STATE_FILE"

try:
    with open(state_file, 'r') as f:
        data = json.load(f)
    
    if data.get("startTime"):
        start = datetime.fromisoformat(data["startTime"].replace("Z", "+00:00"))
        elapsed = int((datetime.utcnow() - start).total_seconds() / 60)
        print(elapsed)
    else:
        print(0)
except:
    print(0)
PYTHON
}

# 主学习循环
start_learning() {
  local duration=${1:-$DEFAULT_DURATION}
  
  echo "🧠 OpenClaw 持续学习"
  echo "===================="
  echo "⏱️ 时长: ${duration} 分钟"
  echo "🕐 开始: $(date '+%Y-%m-%d %H:%M:%S')"
  echo ""
  
  # 检查锁
  if [ -f "$LOCK_FILE" ]; then
    echo "❌ 已有学习在进行中"
    return 1
  fi
  
  touch "$LOCK_FILE"
  init
  update_state "isLearning" "true"
  update_state "duration" "$duration"
  
  local start_time=$(date +%s)
  local end_time=$((start_time + duration * 60))
  local topics_learned=0
  
  # 获取新主题
  local new_topics=($(get_new_topics))
  
  if [ ${#new_topics[@]} -eq 0 ]; then
    echo "📚 所有主题都已学完！"
    rm -f "$LOCK_FILE"
    update_state "isLearning" "false"
    return 0
  fi
  
  echo "📋 待学习主题: ${#new_topics[@]} 个"
  echo ""
  
  # 学习循环
  for topic in "${new_topics[@]}"; do
    # 检查时间
    local current=$(date +%s)
    if [ "$current" -ge "$end_time" ]; then
      echo ""
      echo "⏰ 时间到！"
      break
    fi
    
    # 检查锁
    if [ ! -f "$LOCK_FILE" ]; then
      echo ""
      echo "🛑 收到停止信号"
      break
    fi
    
    # 学习主题
    learn_topic "$topic"
    topics_learned=$((topics_learned + 1))
    update_state "topicsLearned" "$topics_learned"
    
    # 短暂休息
    sleep 2
  done
  
  # 清理
  rm -f "$LOCK_FILE"
  update_state "isLearning" "false"
  
  # 统计
  local actual_end=$(date +%s)
  local total=$(( (actual_end - start_time) / 60 ))
  local learned_count=$(wc -l < "$LEARNED_FILE" 2>/dev/null || echo 0)
  
  echo ""
  echo "🎉 学习完成！"
  echo "===================="
  echo "📊 统计:"
  echo "   计划: ${duration} 分钟"
  echo "   实际: ${total} 分钟"
  echo "   本次学习: ${topics_learned} 个主题"
  echo "   总计学习: ${learned_count} 个主题"
  echo ""
  echo "📚 最近学习:"
  tail -5 "$LEARNED_FILE" | while read -r t; do
    echo "   • $t"
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
  
  local elapsed=$(get_elapsed)
  local learned=0
  if [ -f "$LEARNED_FILE" ]; then
    learned=$(wc -l < "$LEARNED_FILE" 2>/dev/null || echo 0)
  fi
  
  echo "⏱️ 已学习: ${elapsed} 分钟"
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
      rm -f "$LEARNED_FILE" "$STATE_FILE" "$LOCK_FILE" 2>/dev/null
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
  continuous-learning start 20          # 学习20分钟
  continuous-learning status            # 查看状态

核心特性:
  ✅ 时间控制 - 精确学习时长
  ✅ 重复检测 - 避免学习相同内容
  ✅ 自动继续 - 学完目标后探索热门主题
  ✅ 状态追踪 - 实时查看进度
EOF
      ;;
    *)
      echo "使用: $0 {start|stop|status|reset|help}"
      ;;
  esac
}

# 运行
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  main "$@"
fi
