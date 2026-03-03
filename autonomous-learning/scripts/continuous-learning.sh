#!/bin/bash

# OpenClaw 持续学习系统 (进度条优化版)
# 支持时间控制、重复检测、目标管理、时间填充策略、实时进度条

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

# 扩展的技术主题库
TECH_TOPICS=(
  # 系统编程
  "Rust 异步编程"
  "WebAssembly 系统编程"
  "Linux 内核原理"
  "eBPF 可观测性"
  "Go 并发编程"
  
  # 容器与编排
  "Kubernetes 操作"
  "Docker 安全最佳实践"
  "Kubernetes 网络原理"
  "容器运行时对比"
  
  # 前端技术
  "React Server Components"
  "TypeScript 5.0 新特性"
  "Vue 3 Composition API"
  "Tailwind CSS v4 深度解析"
  "前端性能优化"
  "Web 动画原理"
  "PWA 渐进式应用"
  "GraphQL 最佳实践"
  
  # 后端与微服务
  "gRPC 微服务架构"
  "REST API 设计模式"
  "Node.js 性能调优"
  "Python 异步编程"
  "消息队列设计"
  
  # 数据库
  "PostgreSQL 性能优化"
  "Redis 集群原理"
  "MongoDB 设计模式"
  "数据库索引优化"
  "分布式事务"
  
  # DevOps
  "Terraform 基础设施即代码"
  "Prometheus 监控系统"
  "Grafana 可视化"
  "CI/CD 最佳实践"
  "Git 高级技巧"
  "Jenkins Pipeline"
  "GitHub Actions 深度"
  
  # 安全
  "Web 安全 OWASP Top 10"
  "容器安全"
  "零信任架构"
  "加密算法原理"
  
  # 网络
  "Nginx 配置深度"
  "HTTP/3 协议"
  "CDN 原理"
  "网络负载均衡"
  
  # 云原生
  "Serverless 架构"
  "Service Mesh 原理"
  "云原生设计模式"
  
  # AI/ML
  "LLM 应用开发"
  "Prompt Engineering"
  "AI Agent 设计"
  "向量数据库"
  
  # 其他
  "系统设计面试"
  "算法与数据结构"
  "设计模式"
  "代码重构技巧"
  "技术写作"
  "开源项目维护"
)

# ⭐ 主题扩展库（当主主题库学完时使用）
EXTENDED_TOPICS=(
  # 更深入的系统编程
  "Rust 内存安全原理"
  "WebAssembly 内存模型"
  "Linux 进程调度"
  "eBPF 程序开发"
  "Go 垃圾回收原理"
  
  # 更深入的容器技术
  "Kubernetes 控制器开发"
  "Docker 镜像优化"
  "Kubernetes 安全策略"
  "容器网络 CNI 插件"
  
  # 更深入的前端
  "React 并发特性"
  "TypeScript 类型体操"
  "Vue 3 响应式原理"
  "CSS Houdini 魔法"
  "前端编译原理"
  "WebGL 图形编程"
  "WebRTC 实时通信"
  
  # 更深入的后端
  "gRPC 流式编程"
  "GraphQL 解析器优化"
  "Node.js 内存泄漏调试"
  "Python 元编程"
  "分布式一致性算法"
  
  # 更深入的数据库
  "PostgreSQL 查询优化器"
  "Redis 持久化机制"
  "MongoDB 聚合管道"
  "NewSQL 数据库对比"
  "图数据库原理"
  
  # 更深入的DevOps
  "Terraform 模块开发"
  "Prometheus 自定义指标"
  "Grafana 插件开发"
  "Kubernetes Operators"
  "混沌工程实践"
  
  # 更深入的安全
  "Web 渗透测试"
  "容器逃逸技术"
  "零信任网络实现"
  "同态加密原理"
  "量子密码学"
  
  # 更深入的网络
  "eBPF 网络编程"
  "QUIC 协议深度"
  "CDN 架构设计"
  "SDN 软件定义网络"
  
  # 更深入的云原生
  "Serverless 冷启动优化"
  "Istio 流量管理"
  "Knative 服务编排"
  "云原生可观测性"
  
  # 更深入的AI/ML
  "LLM 微调技术"
  "RAG 系统设计"
  "AI Agent 框架开发"
  "向量数据库索引"
  "机器学习工程化"
  
  # 更多主题
  "区块链原理"
  "Web3 开发"
  "元宇宙技术"
  "边缘计算"
  "物联网协议"
  "5G 网络架构"
  "自动驾驶技术"
  "机器人操作系统"
  "3D 图形编程"
  "游戏引擎开发"
  "编译器原理"
  "操作系统开发"
  "数据库引擎开发"
  "编程语言设计"
  "形式化验证"
  "可信计算"
  "隐私计算"
  "联邦学习"
  "强化学习"
  "深度学习优化"
  "计算机视觉"
  "自然语言处理"
  "语音识别技术"
  "推荐系统"
  "搜索算法优化"
  "大数据处理"
  "流式计算"
  "批处理框架"
  "消息队列深度"
  "缓存架构设计"
  "负载均衡算法"
  "分布式事务深度"
  "一致性哈希"
  "CAP 理论实践"
  "微服务设计模式"
  "领域驱动设计"
  "事件驱动架构"
  "CQRS 模式"
  "事件溯源"
  "API 网关"
  "服务网格深度"
  "无服务器架构"
  "函数即服务"
  "后端即服务"
  "低代码平台"
  "无代码开发"
  "AI 辅助编程"
  "代码生成技术"
  "自动化测试"
  "持续部署"
  "GitOps 实践"
  "DevSecOps"
  "Site Reliability Engineering"
  "性能工程"
  "容量规划"
  "故障注入"
  "混沌工程"
  "灾难恢复"
  "多区域部署"
  "混合云架构"
  "多云策略"
  "云成本优化"
  "FinOps 实践"
  "绿色计算"
  "可持续技术"
  "技术伦理"
  "AI 安全"
  "数据隐私"
  "GDPR 合规"
  "网络安全法规"
  "技术标准"
  "开源协议"
  "软件许可"
  "技术创业"
  "产品管理"
  "项目管理"
  "敏捷开发"
  "Scrum 实践"
  "Kanban 方法"
  "极限编程"
  "结对编程"
  "代码审查"
  "技术债务"
  "重构模式"
  "遗留系统改造"
  "现代化迁移"
  "云原生迁移"
  "单体拆分"
  "服务化改造"
  "数据迁移"
  "系统迁移"
  "零停机部署"
  "蓝绿部署"
  "金丝雀发布"
  "A/B 测试"
  "特性开关"
  "灰度发布"
  "用户实验"
  "数据驱动决策"
  "产品分析"
  "用户行为分析"
  "增长黑客"
  "产品市场匹配"
  "商业模式"
  "技术商业化"
  "开发者生态"
  "API 经济"
  "平台战略"
  "生态系统"
  "技术领导力"
  "团队管理"
  "技术沟通"
  "技术写作"
  "技术演讲"
  "技术培训"
  "技术导师"
  "职业发展"
  "技术规划"
  "技术战略"
  "技术愿景"
  "技术创新"
  "研发管理"
  "技术风险"
  "技术债管理"
  "技术治理"
  "技术审计"
  "技术评估"
  "技术选型"
  "架构评审"
  "代码质量"
  "工程效能"
  "研发效率"
  "工程师文化"
  "技术团队文化"
  "远程团队管理"
  "分布式团队"
  "全球化团队"
  "跨文化协作"
  "技术协作"
  "开源协作"
  "社区建设"
  "开发者关系"
  "技术传播"
  "技术营销"
  "技术品牌"
  "技术影响力"
  "个人品牌"
  "技术社交"
  "技术网络"
  "技术合作"
  "技术投资"
  "技术并购"
  "技术创业"
  "技术孵化器"
  "技术加速器"
  "技术风投"
  "技术天使投资"
  "技术众筹"
  "技术社区"
  "技术 meetup"
  "技术会议"
  "技术展览"
  "技术沙龙"
  "技术工作坊"
  "技术训练营"
  "技术学院"
  "技术大学"
  "技术教育"
  "终身学习"
  "技术学习路径"
  "技能树"
  "能力模型"
  "胜任力模型"
  "技术认证"
  "技术证书"
  "技术职称"
  "技术职级"
  "技术晋升"
  "技术薪酬"
  "技术期权"
  "技术股权"
  "技术分红"
  "技术奖金"
  "技术福利"
  "技术工作环境"
  "技术工作生活平衡"
  "技术心理健康"
  "技术职业倦怠"
  "技术职业转型"
  "技术退休"
  "技术传承"
  "技术遗产"
  "技术历史"
  "技术发展史"
  "技术哲学"
  "技术思想"
  "技术方法论"
  "技术范式"
  "技术革命"
  "技术创新"
  "技术变革"
  "技术未来"
  "技术趋势"
  "技术预测"
  "技术预见"
  "技术展望"
  "技术愿景"
  "技术使命"
  "技术价值"
  "技术伦理"
  "技术道德"
  "技术责任"
  "技术治理"
  "技术监管"
  "技术政策"
  "技术法律"
  "技术法规"
  "技术标准"
  "技术规范"
  "技术指南"
  "技术最佳实践"
  "技术原则"
  "技术模式"
  "技术模式语言"
  "技术框架"
  "技术库"
  "技术工具"
  "技术平台"
  "技术生态"
  "技术系统"
  "技术架构"
  "技术设计"
  "技术实现"
  "技术测试"
  "技术部署"
  "技术运维"
  "技术监控"
  "技术告警"
  "技术故障"
  "技术恢复"
  "技术优化"
  "技术改进"
  "技术迭代"
  "技术演进"
  "技术升级"
  "技术迁移"
  "技术淘汰"
  "技术更新"
  "技术维护"
  "技术支持"
  "技术服务"
  "技术咨询"
  "技术顾问"
  "技术专家"
  "技术大师"
  "技术权威"
  "技术泰斗"
  "技术宗师"
  "技术先驱"
  "技术先锋"
  "技术创新者"
  "技术发明家"
  "技术发现者"
  "技术研究者"
  "技术科学家"
  "技术工程师"
  "技术开发者"
  "技术程序员"
  "技术架构师"
  "技术设计师"
  "技术测试员"
  "技术运维师"
  "技术产品经理"
  "技术项目经理"
  "技术经理"
  "技术总监"
  "技术VP"
  "技术CTO"
  "技术CEO"
  "技术创始人"
  "技术联合创始人"
  "技术投资人"
  "技术分析师"
  "技术评论家"
  "技术记者"
  "技术作家"
  "技术博主"
  "技术网红"
  "技术KOL"
  "技术意见领袖"
  "技术布道师"
  "技术传教士"
  "技术大使"
  "技术代表"
  "技术发言人"
  "技术公关"
  "技术市场"
  "技术销售"
  "技术客服"
  "技术支持"
  "技术培训师"
  "技术讲师"
  "技术教练"
  "技术导师"
  "技术师傅"
  "技术学徒"
  "技术实习生"
  "技术新人"
  "技术菜鸟"
  "技术老鸟"
  "技术大牛"
  "技术大神"
  "技术大佬"
  "技术巨擘"
  "技术巨头"
  "技术霸主"
  "技术王者"
  "技术皇帝"
  "技术神"
  "技术上帝"
  "技术造物主"
)

# ⭐ 动态主题库（用于智能探索）
DYNAMIC_TOPICS=()

# ========== 进度条工具函数 ==========

# 绘制进度条
draw_progress_bar() {
  local current="$1"
  local total="$2"
  local width=${3:-50}
  local label="$4"
  
  local percent=$((current * 100 / total))
  local filled=$((current * width / total))
  local empty=$((width - filled))
  
  # 构建进度条
  local bar=""
  bar+="["
  for ((i=0; i<filled; i++)); do bar+="="; done
  for ((i=0; i<empty; i++)); do bar+=" "; done
  bar+="]"
  
  # 输出（使用 printf 确保对齐）
  if [ -n "$label" ]; then
    printf "\r%s %s %3d%%" "$label" "$bar" "$percent"
  else
    printf "\r%s %3d%%" "$bar" "$percent"
  fi
}

# 格式化时间显示
format_time() {
  local total_seconds="$1"
  local minutes=$((total_seconds / 60))
  local seconds=$((total_seconds % 60))
  printf "%02d:%02d" "$minutes" "$seconds"
}

# 显示详细进度条（带时间信息）
show_detailed_progress() {
  local start_time="$1"
  local duration="$2"
  local phase="$3"
  local activity="$4"
  
  local current=$(date +%s)
  local elapsed=$((current - start_time))
  local total=$((duration * 60))
  local remaining=$((total - elapsed))
  
  # 确保不显示负数
  if [ "$remaining" -lt 0 ]; then
    remaining=0
  fi
  
  # 颜色代码
  local GREEN='\033[0;32m'
  local YELLOW='\033[1;33m'
  local BLUE='\033[0;34m'
  local NC='\033[0m' # No Color
  
  # 选择阶段颜色
  local phase_color=""
  case "$phase" in
    "新主题")
      phase_color="$GREEN"
      ;;
    "时间填充")
      phase_color="$YELLOW"
      ;;
    *)
      phase_color="$BLUE"
      ;;
  esac
  
  # 第一行：进度条 + 百分比
  local percent=$((elapsed * 100 / total))
  local width=40
  local filled=$((elapsed * width / total))
  local empty=$((width - filled))
  
  local bar=""
  bar+="["
  for ((i=0; i<filled; i++)); do bar+="▓"; done
  for ((i=0; i<empty; i++)); do bar+="░"; done
  bar+="]"
  
  # 第二行：时间信息
  printf "\r${phase_color}%s${NC} | 进度: %s %3d%% | 已用: %s | 剩余: %s | 活动: %s" \
    "$phase" \
    "$bar" \
    "$percent" \
    "$(format_time "$elapsed")" \
    "$(format_time "$remaining")" \
    "$activity"
}

# 清除进度条行
clear_progress_line() {
  echo ""
}

# ========== 主题管理函数 ==========

# 获取可用主题（智能策略）
get_available_topics() {
  local mode="$1"
  
  # 1. 先从主主题库获取未学习的
  local primary_new=()
  for topic in "${TECH_TOPICS[@]}"; do
    if ! has_learned "$topic"; then
      primary_new+=("$topic")
    fi
  done
  
  # 2. 如果主主题库还有未学的，直接返回
  if [ ${#primary_new[@]} -gt 0 ]; then
    echo "${primary_new[@]}"
    return
  fi
  
  echo ""
  return
}

# 获取复习主题（当所有主题都学完时使用）
get_review_topics() {
  local count=${1:-5}
  local learned=()
  while IFS= read -r line; do
    [ -n "$line" ] && learned+=("$line")
  done < "$LEARNED_FILE"
  
  if [ ${#learned[@]} -eq 0 ]; then
    echo ""
    return
  fi
  
  # 随机选择
  local review=()
  for ((i=0; i<count && i<${#learned[@]}; i++)); do
    local idx=$((RANDOM % ${#learned[@]})
    review+=("${learned[$idx]}")
  done
  
  echo "${review[@]}"
}

# 检查是否所有主主题都已学完
all_primary_topics_finished() {
  for topic in "${TECH_TOPICS[@]}"; do
    if ! has_learned "$topic"; then
      return 1
    fi
  done
  return 0
}

# ========== 核心功能函数 ==========

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
  "topicsLearned": 0,
  "fillMode": false
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

# 获取随机已学主题（用于复习模式）
get_random_review_topic() {
  local count=$(wc -l < "$LEARNED_FILE" 2>/dev/null || echo 0)
  if [ "$count" -eq 0 ]; then
    return
  fi
  
  local random_line=$(( (RANDOM % count) + 1 ))
  sed -n "${random_line}p" "$LEARNED_FILE"
}

# 时间填充：探索 GitHub
fill_time_github() {
  local start_time="$1"
  local duration="$2"
  
  if [ -f "$SCRIPTS_DIR/github-explorer.sh" ]; then
    bash "$SCRIPTS_DIR/github-explorer.sh" "fill_$(date +%s)" 2>&1 | while read -r line; do
      show_detailed_progress "$start_time" "$duration" "时间填充" "GitHub探索中..."
    done
  else
    # 模拟进度
    for i in {1..30}; do
      show_detailed_progress "$start_time" "$duration" "时间填充" "GitHub探索中..."
      sleep 1
    done
  fi
}

# 时间填充：OpenClaw 专题学习
fill_time_openclaw() {
  local start_time="$1"
  local duration="$2"
  
  if [ -f "$SCRIPTS_DIR/openclaw-learning.sh" ]; then
    bash "$SCRIPTS_DIR/openclaw-learning.sh" "fill_$(date +%s)" 2>&1 | while read -r line; do
      show_detailed_progress "$start_time" "$duration" "时间填充" "OpenClaw专题中..."
    done
  else
    # 模拟进度
    for i in {1..30}; do
      show_detailed_progress "$start_time" "$duration" "时间填充" "OpenClaw专题中..."
      sleep 1
    done
  fi
}

# 时间填充：复习已学主题
fill_time_review() {
  local start_time="$1"
  local duration="$2"
  local review_topic=$(get_random_review_topic)
  
  if [ -n "$review_topic" ]; then
    if [ -f "$SCRIPTS_DIR/github-explorer.sh" ]; then
      bash "$SCRIPTS_DIR/github-explorer.sh" "review_$(date +%s)" 2>&1 | while read -r line; do
        show_detailed_progress "$start_time" "$duration" "时间填充" "复习:${review_topic:0:10}..."
      done
    else
      for i in {1..30}; do
        show_detailed_progress "$start_time" "$duration" "时间填充" "复习:${review_topic:0:10}..."
        sleep 1
      done
    fi
  else
    for i in {1..30}; do
      show_detailed_progress "$start_time" "$duration" "时间填充" "休息中..."
      sleep 1
    done
  fi
}

# 时间填充：知识整合与技能生成
fill_time_integrate() {
  local start_time="$1"
  local duration="$2"
  
  if [ -f "$SCRIPTS_DIR/knowledge-extractor.sh" ]; then
    bash "$SCRIPTS_DIR/knowledge-extractor.sh" "integrate_$(date +%s)" 2>&1 | while read -r line; do
      show_detailed_progress "$start_time" "$duration" "时间填充" "知识整合中..."
    done
  fi
  
  if [ -f "$SCRIPTS_DIR/skill-generator.sh" ]; then
    bash "$SCRIPTS_DIR/skill-generator.sh" "integrate_$(date +%s)" 2>&1 | while read -r line; do
      show_detailed_progress "$start_time" "$duration" "时间填充" "技能生成中..."
    done
  fi
  
  # 模拟进度
  for i in {1..15}; do
    show_detailed_progress "$start_time" "$duration" "时间填充" "知识整合中..."
    sleep 1
  done
}

# 学习单个主题
learn_topic() {
  local topic="$1"
  local start_time="$2"
  local duration="$3"
  local mode="${4:-新主题}" # "新主题" 或 "复习"
  
  # 显示正在学习的主题
  echo ""
  if [ "$mode" = "复习" ]; then
    echo "📝 复习主题: $topic"
  else
    echo "📚 学习主题: $topic"
  fi
  
  # 调用 GitHub 探索并显示进度
  if [ -f "$SCRIPTS_DIR/github-explorer.sh" ]; then
    bash "$SCRIPTS_DIR/github-explorer.sh" "learn_$(date +%s)" 2>&1 | while read -r line; do
      if [ "$mode" = "复习" ]; then
        show_detailed_progress "$start_time" "$duration" "复习" "复习:${topic:0:12}..."
      else
        show_detailed_progress "$start_time" "$duration" "新主题" "学习:${topic:0:12}..."
      fi
    done
  else
    # 模拟学习进度
    for i in {1..20}; do
      if [ "$mode" = "复习" ]; then
        show_detailed_progress "$start_time" "$duration" "复习" "复习:${topic:0:12}..."
      else
        show_detailed_progress "$start_time" "$duration" "新主题" "学习:${topic:0:12}..."
      fi
      sleep 1
    done
  fi
  
  # 记录（复习模式也记录，标记为已复习）
  if [ "$mode" != "复习" ]; then
    record_learned "$topic"
  fi
  
  echo ""
  if [ "$mode" = "复习" ]; then
    echo "✅ 复习完成: $topic"
  else
    echo "✅ 学习完成: $topic"
  fi
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

# 获取剩余时间（秒）
get_remaining_seconds() {
  local start_time="$1"
  local duration="$2"
  local current=$(date +%s)
  local end_time=$((start_time + duration * 60))
  echo $((end_time - current))
}

# 主学习循环（进度条优化版）
start_learning() {
  local duration=${1:-$DEFAULT_DURATION}
  
  echo ""
  echo "🧠 OpenClaw 持续学习"
  echo "===================="
  echo "⏱️ 计划时长: ${duration} 分钟"
  echo "🕐 开始时间: $(date '+%Y-%m-%d %H:%M:%S')"
  echo "🎯 结束时间: $(date -d "+${duration} minutes" '+%Y-%m-%d %H:%M:%S')"
  echo "📚 主题库: ${#TECH_TOPICS[@]} 个主题"
  echo ""
  echo "📊 进度条将在下面实时显示..."
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
  update_state "fillMode" "false"
  
  local start_time=$(date +%s)
  local end_time=$((start_time + duration * 60))
  local topics_learned=0
  local fill_cycles=0
  
  # 获取新主题
  local new_topics=($(get_new_topics))
  
  echo "📋 待学习新主题: ${#new_topics[@]} 个"
  echo "📚 主主题库: ${#TECH_TOPICS[@]} 个主题"
  echo "📖 扩展主题库: ${#EXTENDED_TOPICS[@]} 个主题"
  
  # 检查是否所有主主题都已学完
  local all_primary_finished=true
  for topic in "${TECH_TOPICS[@]}"; do
    if ! has_learned "$topic"; then
      all_primary_finished=false
      break
    fi
  done
  
  if [ "$all_primary_finished" = true ]; then
    echo ""
    echo "🎉 恭喜！主主题库 50+ 个主题已全部学完！"
    echo ""
    echo "📚 接下来的策略："
    echo "   1️⃣  复习模式 - 复习已学过的主题"
    echo "   2️⃣  扩展模式 - 学习扩展主题库"
    echo "   3️⃣  时间填充 - 持续探索和整合"
    echo ""
    echo "🔄 将进入智能复习+扩展模式"
  elif [ ${#new_topics[@]} -eq 0 ]; then
    echo "ℹ️ 所有主题都已学完，将直接进入时间填充模式"
  fi
  echo ""
  
  # ========== 第一阶段：学习新主题（智能策略） ==========
  echo "📖 阶段 1/2: 学习新主题"
  echo "----------------------------------------"
  
  # 智能主题选择策略
  local learning_topics=()
  
  if [ "$all_primary_finished" = true ]; then
    # 策略1：所有主主题已学完，使用混合策略
    echo "🎯 使用智能混合策略（复习+扩展）"
    
    # 获取复习主题
    local review_topics=($(get_review_topics 3))
    echo "📝 选择 3 个复习主题"
    
    # 从扩展库选择新主题
    local extended_new=()
    for topic in "${EXTENDED_TOPICS[@]}"; do
      if ! has_learned "$topic"; then
        extended_new+=("$topic")
        if [ ${#extended_new[@]} -ge 2 ]; then
          break
        fi
      fi
    done
    echo "📖 选择 ${#extended_new[@]} 个扩展主题"
    
    # 合并
    learning_topics=("${review_topics[@]}" "${extended_new[@]}")
  else
    # 策略2：还有未学的主主题，优先学习主主题
    learning_topics=("${new_topics[@]}")
  fi
  
  echo "📋 本次学习主题: ${#learning_topics[@]} 个"
  echo ""
  
  for topic in "${learning_topics[@]}"; do
    # 检查时间
    local remaining=$(get_remaining_seconds "$start_time" "$duration")
    if [ "$remaining" -le 0 ]; then
      echo ""
      echo "⏰ 时间到！"
      break
    fi
    
    # 如果剩余时间不足（小于3分钟），跳过主题学习，直接进入填充模式
    if [ "$remaining" -lt 180 ]; then
      echo ""
      echo "⏱️ 剩余时间不足，进入时间填充模式"
      break
    fi
    
    # 检查锁
    if [ ! -f "$LOCK_FILE" ]; then
      echo ""
      echo "🛑 收到停止信号"
      break
    fi
    
    # 判断是新学习还是复习
    local phase_label="新主题"
    if has_learned "$topic"; then
      phase_label="复习"
    fi
    
    # 学习主题
    learn_topic "$topic" "$start_time" "$duration" "$phase_label"
    topics_learned=$((topics_learned + 1))
    update_state "topicsLearned" "$topics_learned"
    
    # 短暂休息（除非时间紧张）
    if [ "$remaining" -gt 120 ]; then
      for i in {1..2}; do
        show_detailed_progress "$start_time" "$duration" "$phase_label" "休息中..."
        sleep 1
      done
    fi
  done
  
  # ========== 第二阶段：时间填充 ==========
  echo ""
  echo "🔄 阶段 2/2: 时间填充模式"
  echo "----------------------------------------"
  update_state "fillMode" "true"
  
  # 填充策略循环
  while true; do
    # 检查时间
    local remaining=$(get_remaining_seconds "$start_time" "$duration")
    if [ "$remaining" -le 0 ]; then
      echo ""
      echo ""
      echo "⏰ 时间到！学习圆满结束！"
      break
    fi
    
    # 检查锁
    if [ ! -f "$LOCK_FILE" ]; then
      echo ""
      echo ""
      echo "🛑 收到停止信号"
      break
    fi
    
    # 轮流使用不同的填充策略
    case $((fill_cycles % 4)) in
      0)
        fill_time_github "$start_time" "$duration"
        ;;
      1)
        fill_time_openclaw "$start_time" "$duration"
        ;;
      2)
        fill_time_review "$start_time" "$duration"
        ;;
      3)
        fill_time_integrate "$start_time" "$duration"
        ;;
    esac
    
    fill_cycles=$((fill_cycles + 1))
    
    # 短暂休息（如果还有足够时间）
    if [ "$remaining" -gt 60 ]; then
      for i in {1..10}; do
        show_detailed_progress "$start_time" "$duration" "时间填充" "休息中..."
        sleep 1
      done
    fi
  done
  
  # ========== 清理与统计 ==========
  rm -f "$LOCK_FILE"
  update_state "isLearning" "false"
  
  # 统计
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
  echo "   本次新学: ${topics_learned} 个主题"
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
  
  local elapsed=$(get_elapsed)
  local learned=0
  if [ -f "$LEARNED_FILE" ]; then
    learned=$(wc -l < "$LEARNED_FILE" 2>/dev/null || echo 0)
  fi
  
  echo "⏱️ 已学习: ${elapsed} 分钟"
  echo "📚 总学习: ${learned} 个主题"
  echo "📖 主题库: ${#TECH_TOPICS[@]} 个主题"
  
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
🧠 OpenClaw 持续学习系统（进度条优化版）

使用方法:
  continuous-learning start [minutes]   # 开始学习 (默认20分钟)
  continuous-learning stop              # 停止学习
  continuous-learning status            # 查看状态
  continuous-learning reset             # 重置学习记录
  continuous-learning help              # 显示帮助

示例:
  continuous-learning start 3           # 快速测试3分钟
  continuous-learning start 20          # 学习20分钟
  continuous-learning status            # 查看状态

核心特性:
  ✅ 实时进度条 - 直观显示学习进度
  ✅ 时间倒计时 - 显示已用/剩余时间
  ✅ 两阶段学习 - 先学新主题，再时间填充
  ✅ 活动显示 - 显示当前正在做什么
  ✅ 重复检测 - 避免学习相同内容
  ✅ 智能填充 - 4种填充策略轮流使用

进度条说明:
  [▓▓▓▓▓▓▓▓▓▓░░░░░░░░░░] 45%
   ▓ = 已完成, ░ = 未完成
  
  新主题 | [▓▓▓▓▓▓▓▓▓▓░░░░] 50% | 已用: 10:00 | 剩余: 10:00 | 活动: 学习:React...
   阶段       进度条            时间统计           当前活动
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
