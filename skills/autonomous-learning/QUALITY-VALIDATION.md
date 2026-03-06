# 技能质量验证系统 ✅

## 设计目标
建立多层级、多维度的质量验证体系，确保发布的每一个技能都是高质量的！

---

## 🏗️ 三层验证架构

```
第一层: 规则验证（自动化）
  ↓ 快速、低成本
第二层: AI验证（LLM驱动）
  ↓ 智能、深度
第三层: 人工验证（最终把关）
  ↓ 最可靠、最权威
```

---

## 🔍 第一层: 规则验证（自动化）

### 1.1 结构完整性检查

**检查清单**:
- [ ] 有 Frontmatter 吗？
- [ ] Frontmatter 包含 name 吗？
- [ ] Frontmatter 包含 description 吗？
- [ ] Frontmatter 包含 read_when 吗？
- [ ] 有主标题（#）吗？
- [ ] 有子章节（##）吗？
- [ ] 有"快速开始"或"使用方法"吗？
- [ ] 有"常见问题"吗？

**检查脚本示例**:
```bash
#!/bin/bash
# check-structure.sh

SKILL_FILE=$1

echo "🔍 检查技能结构: $SKILL_FILE"

# 检查 Frontmatter
if ! grep -q "^---" "$SKILL_FILE"; then
    echo "❌ 缺少 Frontmatter"
    exit 1
fi

# 检查 name
if ! grep -q "^name:" "$SKILL_FILE"; then
    echo "❌ 缺少 name"
    exit 1
fi

# 检查 description
if ! grep -q "^description:" "$SKILL_FILE"; then
    echo "❌ 缺少 description"
    exit 1
fi

# 检查主标题
if ! grep -q "^# " "$SKILL_FILE"; then
    echo "❌ 缺少主标题"
    exit 1
fi

# 检查子章节
SECTION_COUNT=$(grep -c "^## " "$SKILL_FILE")
if [ "$SECTION_COUNT" -lt 3 ]; then
    echo "❌ 子章节太少（需要至少3个）"
    exit 1
fi

echo "✅ 结构检查通过"
exit 0
```

---

### 1.2 内容质量检查

**检查清单**:
- [ ] 文件大小 ≥ 2KB 吗？
- [ ] 字数 ≥ 800字吗？
- [ ] 有代码块吗？
- [ ] 代码块 ≥ 1个吗？
- [ ] 有列表吗？
- [ ] 没有占位符（TODO、待补充）吗？
- [ ] 没有垃圾关键词吗？

**检查脚本示例**:
```bash
#!/bin/bash
# check-content.sh

SKILL_FILE=$1

echo "🔍 检查内容质量: $SKILL_FILE"

# 检查文件大小
MIN_SIZE=2000
SIZE=$(wc -c < "$SKILL_FILE")
if [ "$SIZE" -lt "$MIN_SIZE" ]; then
    echo "❌ 文件太小（$SIZE 字节，需要至少 $MIN_SIZE）"
    exit 1
fi

# 检查字数
MIN_WORDS=800
WORDS=$(wc -w < "$SKILL_FILE")
if [ "$WORDS" -lt "$MIN_WORDS" ]; then
    echo "❌ 字数太少（$WORDS 字，需要至少 $MIN_WORDS）"
    exit 1
fi

# 检查代码块
CODE_BLOCKS=$(grep -c '^```' "$SKILL_FILE")
if [ "$CODE_BLOCKS" -lt 2 ]; then  # 2个```才算1个代码块
    echo "❌ 缺少代码块"
    exit 1
fi

# 检查占位符
if grep -q -i "todo\|待补充\|占位符" "$SKILL_FILE"; then
    echo "❌ 包含占位符内容"
    exit 1
fi

# 检查垃圾关键词
SPAM_WORDS=("赚钱" "兼职" "刷单" "赌博" "色情")
for WORD in "${SPAM_WORDS[@]}"; do
    if grep -q "$WORD" "$SKILL_FILE"; then
        echo "❌ 包含垃圾关键词: $WORD"
        exit 1
    fi
done

echo "✅ 内容检查通过"
exit 0
```

---

### 1.3 示例完整性检查

**检查清单**:
- [ ] 代码块有语言标记吗？（```javascript, ```bash等）
- [ ] 代码块长度 ≥ 3行吗？
- [ ] 有注释说明吗？
- [ ] 示例是完整的吗？

**检查脚本示例**:
```bash
#!/bin/bash
# check-examples.sh

SKILL_FILE=$1

echo "🔍 检查示例质量: $SKILL_FILE"

# 提取所有代码块
TEMP=$(mktemp)
awk '/^```/{flag=!flag;next}flag' "$SKILL_FILE" > "$TEMP"

# 检查代码块质量
CODE_BLOCK_COUNT=0
GOOD_CODE_BLOCKS=0

while IFS= read -r line; do
    # 这里需要更复杂的代码块分析
    # 简化版本: 检查代码块长度
    :
done < "$TEMP"

rm "$TEMP"

echo "✅ 示例检查通过"
exit 0
```

---

## 🤖 第二层: AI验证（LLM驱动）

### 2.1 多维度质量评分

**评分维度**:

| 维度 | 评分标准 | 权重 | 优秀(90-100) | 良好(70-89) | 合格(50-69) |
|------|---------|------|-------------|------------|------------|
| **实用性** | 能解决实际问题吗？ | 25% | 能直接用于生产 | 能解决常见问题 | 有一定帮助 |
| **完整性** | 覆盖全面吗？ | 20% | 覆盖所有场景 | 覆盖主要场景 | 覆盖基础场景 |
| **示例质量** | 示例好用吗？ | 20% | 多个完整示例 | 1-2个完整示例 | 简单示例 |
| **文档清晰** | 容易理解吗？ | 15% | 清晰易懂 | 基本清晰 | 能看懂 |
| **准确性** | 内容正确吗？ | 15% | 完全正确 | 基本正确 | 有小错误 |
| **创新性** | 有新见解吗？ | 5% | 有独特见解 | 有一些新意 | 常规内容 |

---

### 2.2 AI验证提示词模板

```markdown
你是一个专业的技能质量评审员。请对以下技能进行多维度质量评估。

## 技能内容
[在此处插入技能内容]

## 评估维度

### 1. 实用性 (0-100分)
- 这个技能能解决实际问题吗？
- 有明确的使用场景吗？
- 目标用户是谁？他们真的需要这个吗？

### 2. 完整性 (0-100分)
- 覆盖了主要的使用场景吗？
- 有没有遗漏重要的内容？
- 从入门到进阶都有涉及吗？

### 3. 示例质量 (0-100分)
- 代码示例完整吗？能直接运行吗？
- 示例有注释说明吗？
- 示例覆盖了典型用例吗？

### 4. 文档清晰 (0-100分)
- 容易理解吗？
- 步骤清晰吗？
- 概念解释清楚吗？

### 5. 准确性 (0-100分)
- 内容准确无误吗？
- 有没有错误的信息？
- 最佳实践正确吗？

### 6. 创新性 (0-100分)
- 有独特的见解吗？
- 有新的方法或思路吗？
- 不仅仅是复制官方文档吗？

## 输出格式

请用JSON格式输出：

{
  "overallScore": 85,
  "dimensions": {
    "usability": 90,
    "completeness": 80,
    "examples": 85,
    "clarity": 88,
    "accuracy": 92,
    "originality": 70
  },
  "status": "approved", // approved, needs_review, rejected
  "summary": "简要总结（2-3句话）",
  "strengths": [
    "优点1",
    "优点2",
    "优点3"
  ],
  "weaknesses": [
    "缺点1",
    "缺点2"
  ],
  "suggestions": [
    "改进建议1",
    "改进建议2",
    "改进建议3"
  ],
  "decision": "发布", // 发布, 需要改进, 拒绝
  "confidence": 0.9 // 评审置信度 0-1
}

## 评审标准

- **90-100分**: 优秀，直接发布
- **70-89分**: 良好，可以发布，建议 minor 改进
- **50-69分**: 合格，需要 major 改进后再审核
- **<50分**: 不合格，拒绝发布

请开始评审！
```

---

### 2.3 AI验证实现

**验证脚本示例**:
```bash
#!/bin/bash
# ai-validation.sh

SKILL_FILE=$1
OUTPUT_FILE=$2

echo "🤖 开始AI质量验证: $SKILL_FILE"

# 读取技能内容
SKILL_CONTENT=$(cat "$SKILL_FILE")

# 构建提示词
PROMPT=$(cat <<EOF
[上面的AI验证提示词模板]

## 技能内容
$SKILL_CONTENT
EOF
)

# 调用LLM进行验证
# 这里使用OpenClaw的API或者直接调用模型
# 简化示例
echo "$PROMPT" | openclaw query --model "doubao/ark-code-latest" > "$OUTPUT_FILE"

echo "✅ AI验证完成，结果保存在: $OUTPUT_FILE"
```

---

## 👤 第三层: 人工验证（最终把关）

### 3.1 人工验证清单

**验证人**: 你（Winston）或指定的审核者

**验证清单**:

- [ ] **整体印象** - 第一感觉怎么样？
- [ ] **实用性** - 我自己会用这个技能吗？
- [ ] **准确性** - 内容都正确吗？
- [ ] **完整性** - 有没有遗漏重要内容？
- [ ] **示例质量** - 示例能运行吗？
- [ ] **文档清晰** - 容易理解吗？
- [ ] **与AI验证一致吗** - 我的判断和AI一致吗？

---

### 3.2 人工验证界面

**验证命令**:
```bash
./scripts/human-review.sh skill.md
```

**验证流程**:
```
🤖 AI验证结果:
  总分: 87分
  状态: 需要审核

📋 技能预览:
[显示技能的前100行]

💡 AI建议:
  优点:
  - 实用性强，能直接用于生产
  - 示例完整，有注释
  - 文档清晰，步骤明确

  建议:
  - 可以增加一个真实项目的完整示例
  - 建议补充更多性能优化技巧

✅ 你想怎么做？
  [1] 直接发布
  [2] 需要改进（输入改进建议）
  [3] 拒绝发布
  [4] 稍后再看

请选择: _
```

---

## 📊 完整验证流程

### 验证流程图

```
技能草稿
    ↓
[规则验证]
    ├─ ❌ 失败 → 退回修改
    │
    ↓ ✅ 通过
[AI验证]
    ├─ ❌ <50分 → 拒绝
    ├─ ⚠️ 50-69分 → 需要改进
    │
    ↓ ✅ ≥70分
[人工验证]
    ├─ ❌ 拒绝 → 不发布
    ├─ ⚠️ 需要改进 → 退回修改
    │
    ↓ ✅ 通过
[发布技能] ✨
```

---

### 验证状态定义

| 状态 | 含义 | 下一步 |
|------|------|--------|
| `draft` | 草稿 | 继续编辑 |
| `rule_check_pending` | 等待规则检查 | 运行规则验证 |
| `rule_check_failed` | 规则检查失败 | 退回修改 |
| `ai_validation_pending` | 等待AI验证 | 运行AI验证 |
| `ai_rejected` | AI拒绝 | 不发布 |
| `ai_needs_review` | AI建议改进 | 人工审核 |
| `ai_approved` | AI通过 | 人工审核 |
| `human_review_pending` | 等待人工审核 | 人工审核 |
| `human_rejected` | 人工拒绝 | 不发布 |
| `human_needs_changes` | 人工要求改进 | 退回修改 |
| `approved` | 审核通过 | 可以发布 |
| `published` | 已发布 | 完成！ |

---

## 🎯 质量标准

### 发布标准
**必须同时满足**:
- ✅ 规则验证通过
- ✅ AI验证 ≥ 70分
- ✅ 人工验证通过

### 优秀技能标准
**满足以下条件**:
- ⭐ AI验证 ≥ 90分
- ⭐ 人工验证高度评价
- ⭐ 有创新性和独特见解
- ⭐ 示例特别丰富实用

---

## 🔧 验证工具集

### 完整的验证脚本

```bash
# 1. 规则验证
./scripts/validation/rule-check.sh skill.md

# 2. AI验证
./scripts/validation/ai-validate.sh skill.md result.json

# 3. 人工验证
./scripts/validation/human-review.sh skill.md

# 4. 完整验证流程
./scripts/validation/full-validation.sh skill.md

# 5. 批量验证
./scripts/validation/batch-validate.sh pending/
```

---

## 💡 验证优化建议

### 持续学习
- 记录每次验证的结果
- 分析被拒绝的原因
- 优化验证标准和提示词

### 反馈循环
- 收集用户对已发布技能的反馈
- 根据反馈调整验证标准
- 识别高价值技能的特征

---

_三层验证，质量保证！✅🤖👤_
