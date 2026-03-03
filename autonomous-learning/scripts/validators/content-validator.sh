#!/bin/bash

# 内容质量校验器
# 检查学习内容的质量，避免垃圾信息污染技能库

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
DATA_DIR="$SKILL_DIR/data"

echo "   🔍 内容质量校验..."

# 质量阈值
MIN_CONTENT_LENGTH=500
MIN_KEYWORDS=3
MAX_SPAM_SCORE=2

# 垃圾关键词列表（用于过滤）
SPAM_KEYWORDS=(
  "赚钱"
  "兼职"
  "刷单"
  "赌博"
  "色情"
  "诈骗"
  "中奖"
  "免费领取"
  "点击查看"
  "限时优惠"
)

# 高质量关键词
QUALITY_KEYWORDS=(
  "文档"
  "教程"
  "官方"
  "最佳实践"
  "开源"
  "GitHub"
  "技术"
  "编程"
  "代码"
  "API"
  "文档"
  "指南"
)

validate_content() {
  local content_file="$1"
  local content_type="$2"
  
  if [ ! -f "$content_file" ]; then
    echo "      ❌ 文件不存在: $content_file"
    return 1
  fi
  
  local score=0
  local warnings=()
  
  echo "      📄 检查: $(basename "$content_file")"
  
  # 1. 检查内容长度
  local content_length=$(wc -c < "$content_file" 2>/dev/null || echo 0)
  if [ "$content_length" -lt "$MIN_CONTENT_LENGTH" ]; then
    warnings+=("内容过短: ${content_length} 字符 (最小: $MIN_CONTENT_LENGTH)")
    score=$((score + 1))
  else
    echo "      ✅ 内容长度: ${content_length} 字符"
  fi
  
  # 2. 检查垃圾关键词
  local spam_count=0
  for keyword in "${SPAM_KEYWORDS[@]}"; do
    if grep -q -i "$keyword" "$content_file" 2>/dev/null; then
      spam_count=$((spam_count + 1))
      warnings+=("检测到垃圾关键词: $keyword")
    fi
  done
  
  if [ "$spam_count" -gt 0 ]; then
    score=$((score + spam_count))
  fi
  
  # 3. 检查高质量关键词
  local quality_count=0
  for keyword in "${QUALITY_KEYWORDS[@]}"; do
    if grep -q -i "$keyword" "$content_file" 2>/dev/null; then
      quality_count=$((quality_count + 1))
    fi
  done
  
  if [ "$quality_count" -ge "$MIN_KEYWORDS" ]; then
    echo "      ✅ 高质量关键词: ${quality_count} 个"
  else
    warnings+=("高质量关键词较少: ${quality_count} 个 (期望: $MIN_KEYWORDS)")
    score=$((score + 1))
  fi
  
  # 4. 检查代码块（技术内容应该有代码示例）
  if [ "$content_type" = "tech" ]; then
    local code_blocks=$(grep -c '```' "$content_file" 2>/dev/null || echo 0)
    if [ "$code_blocks" -ge 2 ]; then
      echo "      ✅ 代码块: ${code_blocks} 个"
    else
      warnings+=("代码示例较少")
    fi
  fi
  
  # 5. 输出结果
  echo ""
  if [ ${#warnings[@]} -gt 0 ]; then
    echo "      ⚠️ 警告:"
    for warning in "${warnings[@]}"; do
      echo "         - $warning"
    done
  fi
  
  if [ "$score" -le "$MAX_SPAM_SCORE" ]; then
    echo "      ✅ 内容通过校验 (分数: $score/$MAX_SPAM_SCORE)"
    return 0
  else
    echo "      ❌ 内容未通过校验 (分数: $score/$MAX_SPAM_SCORE)"
    return 1
  fi
}

validate_website() {
  local url="$1"
  
  echo "      🌐 检查网站: $url"
  
  # 黑名单域名
  local blacklist_domains=(
    "spam.com"
    "scam.com"
    "fake.com"
    "clickbait.com"
  )
  
  # 白名单域名（高质量）
  local whitelist_domains=(
    "github.com"
    "gitlab.com"
    "developer.mozilla.org"
    "docs.github.com"
    "rust-lang.org"
    "python.org"
    "react.dev"
    "tailwindcss.com"
    "webassembly.org"
  )
  
  # 检查是否在白名单
  for domain in "${whitelist_domains[@]}"; do
    if [[ "$url" == *"$domain"* ]]; then
      echo "      ✅ 白名单网站: $domain"
      return 0
    fi
  done
  
  # 检查是否在黑名单
  for domain in "${blacklist_domains[@]}"; do
    if [[ "$url" == *"$domain"* ]]; then
      echo "      ❌ 黑名单网站: $domain"
      return 1
    fi
  done
  
  echo "      ⚠️ 未知网站，需要人工审核"
  return 2
}

# 如果直接运行此脚本，提供测试功能
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  echo "🧐 内容质量校验器"
  echo "=================="
  echo ""
  
  if [ $# -eq 0 ]; then
    echo "使用方法:"
    echo "  $0 <content-file> [content-type]"
    echo ""
    echo "示例:"
    echo "  $0 knowledge.md tech"
    exit 1
  fi
  
  validate_content "$1" "${2:-general}"
fi
