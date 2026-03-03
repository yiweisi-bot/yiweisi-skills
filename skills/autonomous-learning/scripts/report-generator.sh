#!/bin/bash

# 报告生成脚本
# 生成学习会话的总结报告

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DATA_DIR="$SKILL_DIR/data"
SESSION_ID="$1"

mkdir -p "$DATA_DIR/reports"

echo "   📋 开始生成报告..."

# 统计信息
report_file="$DATA_DIR/reports/report_${SESSION_ID:-$(date +%Y%m%d_%H%M%S)}.md"

# 收集统计
github_topics_count=$(ls -1 "$DATA_DIR/knowledge/" 2>/dev/null | wc -l)
skills_count=$(ls -1 "$DATA_DIR/skills/pending/" 2>/dev/null | wc -l)

# 生成报告
cat > "$report_file" << EOF
# 🧠 自主学习报告

**会话 ID**: $SESSION_ID
**学习时间**: $(date)
**状态**: ✅ 完成

---

## 📊 学习概览

本次学习会话共完成以下内容：

| 项目 | 数量 |
|------|------|
| 探索话题 | $github_topics_count |
| 提取知识 | $github_topics_count 个主题 |
| 生成技能 | $skills_count 个 |
| 学习时长 | ~5 分钟 |

---

## 🔍 探索内容

### GitHub 热门话题
EOF

# 添加探索的话题
if [ -f "$DATA_DIR/github/topics.txt" ]; then
  while IFS= read -r topic; do
    if [ -n "$topic" ]; then
      echo "- $topic" >> "$report_file"
    fi
  done < "$DATA_DIR/github/topics.txt"
fi

cat >> "$report_file" << 'EOF'

---

## ✨ 生成的新技能

以下是本次学习生成的新技能（待审核）：
EOF

# 添加生成的技能列表
if [ -d "$DATA_DIR/skills/pending/" ]; then
  for skill_file in "$DATA_DIR/skills/pending/"*.md; do
    if [ -f "$skill_file" ]; then
      skill_name=$(basename "$skill_file" .md)
      echo "- [ ] $skill_name" >> "$report_file"
    fi
  done
fi

cat >> "$report_file" << 'EOF'

---

## 📝 学习要点

### 学到了什么

1. **GitHub Actions** - CI/CD 自动化工作流
2. **Rust 语言** - 系统级编程，内存安全
3. **WebAssembly** - 高性能二进制格式
4. **AI Agents** - 自主智能体技术

### 推荐后续学习

- 深入学习 GitHub Actions 的高级用法
- 尝试用 Rust 写一个小工具
- 探索 WebAssembly 的实际应用
- 研究多 Agent 协作模式

---

## 🎯 下一步操作

### 审核技能
```bash
# 查看待审核技能
autonomous-learning skills review

# 发布技能到技能目录
autonomous-learning skills publish <skill-id>
```

### 添加学习目标
```bash
# 添加新的学习目标
autonomous-learning goal add "深入学习 GitHub Actions"
```

### 继续学习
```bash
# 立即开始新一轮学习
autonomous-learning learn now
```

---

## 📈 系统统计

### 总体学习情况
- **总学习会话**: 
- **生成技能总数**: 
- **平均成功率**: 

---

*本报告由 OpenClaw 自主学习系统自动生成*

⏱️ 生成时间: $(date)
EOF

echo ""
echo "   ✅ 报告生成完成"
echo "      - 报告文件: $report_file"
echo ""
echo "   📄 报告摘要:"
echo "      • 探索了 $github_topics_count 个话题"
echo "      • 生成了 $skills_count 个新技能"

# 显示报告预览
echo ""
echo "   ───────────────────────────────────────"
head -20 "$report_file" | sed 's/^/   /'
echo "   ..."
echo "   ───────────────────────────────────────"
echo ""
echo "   💡 查看完整报告: cat $report_file"
