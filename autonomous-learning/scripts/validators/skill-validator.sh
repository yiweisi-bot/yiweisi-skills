#!/bin/bash

# 技能质量校验器
# 检查生成的技能的质量，避免垃圾技能污染技能库

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
DATA_DIR="$SKILL_DIR/data"

echo "   🛡️ 技能质量校验..."

# 技能质量标准
MIN_SKILL_LENGTH=800
MIN_SECTIONS=3
MIN_CODE_BLOCKS=1

# 必需的技能部分
REQUIRED_SECTIONS=(
  "name:"
  "description:"
  "read_when:"
  "---"
  "# "
  "##"
)

# 低质量标志（拒绝生成）
LOW_QUALITY_FLAGS=(
  "占位符"
  "TODO"
  "待补充"
  "示例内容"
  "测试技能"
  "垃圾"
  "无用"
)

validate_skill() {
  local skill_file="$1"
  local skill_name="$2"
  
  if [ ! -f "$skill_file" ]; then
    echo "      ❌ 文件不存在: $skill_file"
    return 1
  fi
  
  local score=0
  local warnings=()
  local passed=true
  
  echo "      📋 检查技能: $skill_name"
  echo "         文件: $(basename "$skill_file")"
  
  # 1. 检查文件大小
  local file_size=$(wc -c < "$skill_file" 2>/dev/null || echo 0)
  if [ "$file_size" -lt "$MIN_SKILL_LENGTH" ]; then
    warnings+=("文件过小: ${file_size} 字节 (最小: $MIN_SKILL_LENGTH)")
    score=$((score + 2))
    passed=false
  else
    echo "         ✅ 文件大小: ${file_size} 字节"
  fi
  
  # 2. 检查必需的部分
  local missing_sections=()
  for section in "${REQUIRED_SECTIONS[@]}"; do
    if ! grep -q "$section" "$skill_file" 2>/dev/null; then
      missing_sections+=("$section")
    fi
  done
  
  if [ ${#missing_sections[@]} -gt 0 ]; then
    warnings+=("缺少必需部分: ${missing_sections[*]}")
    score=$((score + ${#missing_sections[@]}))
    passed=false
  else
    echo "         ✅ 结构完整"
  fi
  
  # 3. 检查章节数量
  local sections=$(grep -c "^## " "$skill_file" 2>/dev/null || echo 0)
  if [ "$sections" -lt "$MIN_SECTIONS" ]; then
    warnings+=("章节过少: $sections (最小: $MIN_SECTIONS)")
    score=$((score + 1))
  else
    echo "         ✅ 章节数: $sections"
  fi
  
  # 4. 检查代码块
  local code_blocks_raw=$(grep -c '```' "$skill_file" 2>/dev/null)
  local code_blocks=${code_blocks_raw:-0}
  # 清理，只保留数字
  code_blocks=$(echo "$code_blocks" | tr -dc '0-9')
  [ -z "$code_blocks" ] && code_blocks=0
  
  if [ "$code_blocks" -lt "$MIN_CODE_BLOCKS" ]; then
    warnings+=("代码块过少: $code_blocks (最小: $MIN_CODE_BLOCKS)")
    score=$((score + 1))
  else
    echo "         ✅ 代码块: $code_blocks"
  fi
  
  # 5. 检查低质量标志
  local low_quality=false
  for flag in "${LOW_QUALITY_FLAGS[@]}"; do
    if grep -q -i "$flag" "$skill_file" 2>/dev/null; then
      warnings+=("检测到低质量标志: $flag")
      low_quality=true
      score=$((score + 5))
      passed=false
    fi
  done
  
  # 6. 检查是否为自动生成的标记
  if grep -q "本技能由自主学习系统自动生成" "$skill_file" 2>/dev/null; then
    echo "         ✅ 来源标记正确"
  fi
  
  # 7. 输出结果
  echo ""
  if [ ${#warnings[@]} -gt 0 ]; then
    echo "         ⚠️ 警告:"
    for warning in "${warnings[@]}"; do
      echo "            - $warning"
    done
  fi
  
  echo ""
  if [ "$passed" = true ] && [ "$score" -le 3 ]; then
    echo "         ✅ 技能通过质量校验 (分数: $score)"
    
    # 创建质量通过标记
    touch "$skill_file.quality_passed"
    return 0
  elif [ "$score" -le 5 ]; then
    echo "         ⚠️ 技能基本通过，但有警告 (分数: $score)"
    echo "         💡 建议人工审核"
    
    # 创建待审核标记
    touch "$skill_file.needs_review"
    return 2
  else
    echo "         ❌ 技能未通过质量校验 (分数: $score)"
    echo "         🗑️ 建议丢弃此技能"
    
    # 移动到低质量目录
    mkdir -p "$DATA_DIR/skills/low_quality/"
    mv "$skill_file" "$DATA_DIR/skills/low_quality/" 2>/dev/null
    return 1
  fi
}

validate_all_pending_skills() {
  local pending_dir="$DATA_DIR/skills/pending/"
  
  if [ ! -d "$pending_dir" ]; then
    echo "      ⚠️ 没有待审核的技能"
    return
  fi
  
  echo "      📂 检查目录: $pending_dir"
  echo ""
  
  local passed=0
  local needs_review=0
  local failed=0
  
  for skill_file in "$pending_dir"*.md; do
    if [ -f "$skill_file" ]; then
      local skill_name=$(basename "$skill_file" .md)
      
      if validate_skill "$skill_file" "$skill_name"; then
        passed=$((passed + 1))
      elif [ $? -eq 2 ]; then
        needs_review=$((needs_review + 1))
      else
        failed=$((failed + 1))
      fi
      
      echo ""
      echo "         ─────────────────────────"
      echo ""
    fi
  done
  
  echo "      📊 校验总结:"
  echo "         ✅ 通过: $passed"
  echo "         ⚠️ 待审核: $needs_review"
  echo "         ❌ 失败: $failed"
}

# 如果直接运行此脚本
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  echo "🛡️ 技能质量校验器"
  echo "===================="
  echo ""
  
  if [ $# -eq 0 ]; then
    echo "使用方法:"
    echo "  $0 <skill-file>          # 校验单个技能"
    echo "  $0 --all                 # 校验所有待审核技能"
    echo ""
    echo "示例:"
    echo "  $0 my-skill.md"
    echo "  $0 --all"
    exit 1
  fi
  
  if [ "$1" = "--all" ]; then
    validate_all_pending_skills
  else
    validate_skill "$1" "$(basename "$1" .md)"
  fi
fi
