# 自主学习系统 - 完整设计文档 v2.0

**文档版本**: v2.0
**更新日期**: 2026-03-04
**作者**: 乙维斯

---

## 📋 目录

1. [系统架构总览](#1-系统架构总览)
2. [完整流程详解](#2-完整流程详解)
3. [启动交互流程](#3-启动交互流程)
4. [Action-Reflection-Iteration 循环](#4-action-reflection-iteration-循环)
5. [技能生成流程](#5-技能生成流程)
6. [三层质量验证](#6-三层质量验证)
7. [数据库设计](#7-数据库设计)
8. [Token消耗优化](#8-token消耗优化)
9. [错误处理机制](#9-错误处理机制)
10. [状态机设计](#10-状态机设计)
11. [文件结构](#11-文件结构)
12. [下一步实现计划](#12-下一步实现计划)

---

## 1. 系统架构总览

### 1.1 架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                      用户交互层                                  │
│  用户输入学习目标 → 查看进度 → 反馈评价                         │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                   LearnerAgent (主控制器)                       │
│  • 目标解析与拆解    • 优先级排序    • 任务调度                 │
│  • 进度监控          • 用户交互    • Token监控                  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    任务管理层                                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │  目标管理    │  │  任务拆解    │  │  优先级排序  │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│               Action-Reflection-Iteration 循环                  │
│                                                                 │
│    ┌──────────┐      ┌──────────────┐      ┌───────────┐       │
│    │  Action  │ ───▶ │  Reflection  │ ───▶ │ Iteration │       │
│    │  (执行)   │      │   (反思)     │      │  (迭代)    │       │
│    └──────────┘      └──────────────┘      └───────────┘       │
│         ▲                    │                    │             │
│         └────────────────────┴────────────────────┘             │
│                    (最大3次循环)                                 │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    技能生成层                                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │  大纲设计    │─▶│  内容生成    │─▶│  自我检查    │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                   质量验证层 (三层)                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │  规则验证    │─▶│  AI验证      │─▶│  人工验证    │          │
│  │  (自动化)    │  │  (LLM)       │  │  (最终把关)  │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                  数据持久化层 (SQLite)                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │learning_goals│  │learning_tasks│  │learning_sess │          │
│  │  (学习目标)  │  │  (学习任务)  │  │  (学习会话)  │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│  ┌──────────────┐  ┌──────────────┐                             │
│  │generated_sk. │  │learning_back.│                             │
│  │  (生成技能)  │  │  (待学习列表)│                             │
│  └──────────────┘  └──────────────┘                             │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. 完整流程详解

### 2.1 阶段1: 用户目标输入

**输入示例**:
```
用户: "帮我学习一下React 19、Python、还有Docker"
```

**处理流程**:
```
1. 解析用户输入
   │
   ▼
2. 拆分为3个独立目标
   - 目标1: 学习 React 19
   - 目标2: 学习 Python
   - 目标3: 学习 Docker
   │
   ▼
3. 自动评估优先级 (详见 2.2 优先级规则)
   - React 19: 高优先级（新技术、用户可能需要）
   - Python: 中优先级
   - Docker: 中优先级
   │
   ▼
4. 存入数据库 (learning_goals表)
   │
   ▼
5. 开始执行第一个目标 (React 19)
```

### 2.2 优先级计算规则

**自动评估公式**:
```
优先级分数 = 基础分 + 时效性加成 + 技能缺口加成 + 用户偏好加成

优先级等级:
  1 = 低优先级 (分数 0-40)
  2 = 中优先级 (分数 41-70)
  3 = 高优先级 (分数 71-100)
```

**评分细则**:

| 维度 | 条件 | 加分 |
|------|------|------|
| **基础分** | 所有目标 | 50 |
| **时效性** | 发布<6个月的新技术 | +20 |
| | 发布<1年的技术 | +10 |
| | 发布>2年的成熟技术 | +0 |
| **技能缺口** | 系统中无相关技能 | +15 |
| | 有相关但版本过时 | +10 |
| | 已有相关技能 | -10 |
| **用户偏好** | 用户明确提到"急用" | +20 |
| | 用户明确提到"了解一下" | -10 |
| **依赖关系** | 是其他目标的依赖 | +15 |
| | 依赖其他目标 | -10 |

**示例计算**:
```
React 19:
  基础分: 50
  + 时效性(新发布<6个月): 20
  + 技能缺口(无相关技能): 15
  = 85 → 高优先级

Python:
  基础分: 50
  + 时效性(成熟技术): 0
  + 技能缺口(无相关技能): 15
  = 65 → 中优先级
```

---

## 3. 启动交互流程

### 3.1 场景1: 用户没有明确主题

```
用户: @learner 开始学习吧

LearnerAgent:
🎯 好的！让我帮你规划一下学习~

我看了一下，我们可以学习这些内容：

📚 推荐主题（基于技能缺口）：
1. React 19 Server Components - 最新技术，我们还没有相关技能
2. GitHub Actions 最佳实践 - CI/CD必备，很实用
3. Tailwind CSS v4 - 新版本，有很多改进
4. Docker 容器化 - 通用性强，应用广泛
5. Rust 入门 - 越来越热门的系统语言

💡 或者，你有想学习的特定主题吗？

请告诉我：
- 选一个上面的推荐（1-5）
- 或者告诉我你想学习的主题
```

### 3.2 场景2: 用户有明确主题 - 三个必问问题

#### 问题1: 学习深度
```
你想学习到什么程度？

A. 入门了解（快速上手，30-60分钟）
   - 适合: 想快速了解，不需要深入
   - 内容: 核心概念 + 1个简单示例
   - Token预估: 5K-10K

B. 系统学习（全面掌握，2-3小时）⭐推荐
   - 适合: 真正想掌握这个技能
   - 内容: 完整教程 + 多个示例 + 最佳实践
   - Token预估: 20K-40K

C. 深入精通（深度研究，4小时+）
   - 适合: 需要成为专家
   - 内容: 深度原理 + 高级技巧 + 实战案例
   - Token预估: 50K-100K

你的选择（A/B/C）：
```

#### 问题2: 学习时间
```
⏰ 设置学习时间限制

推荐时长（根据学习深度）:
- 入门了解: 60分钟
- 系统学习: 120分钟 ⭐
- 深入精通: 240分钟

你想设置多少分钟？
- 直接输入数字（如: 90）
- 按回车使用推荐值
- 输入 0 表示不限制

💡 提示:
- 如果时间到了但没学完，我会通知你
- 询问是否需要继续
- 如果5分钟没有回复，自动保存并加入待学习列表
```

#### 问题3: Token预算
```
💰 设置Token消耗预算

推荐预算（根据学习深度）:
- 入门了解: 10K tokens
- 系统学习: 30K tokens ⭐
- 深入精通: 50K tokens

当前模型价格参考（估算）:
- doubao/ark-code-latest: ~$0.01/10K tokens
- zhipu/glm-4.7: ~$0.03/10K tokens
- zhipu/glm-5: ~$0.10/10K tokens

你想设置多少？
- 直接输入数字（如: 25000）
- 按回车使用推荐值
- 输入 0 表示不限制

⚠️ 提示: 达到预算会自动终止，避免超支！
```

### 3.3 配置确认摘要

```
✅ 学习计划确认

📚 学习主题: React 19
🎯 学习深度: 系统学习（全面掌握）
⏰ 时间限制: 120分钟
💰 Token预算: 30K tokens
🎨 学习风格: 平衡型

📊 预估:
- 预计时间: 90-120分钟
- 预计Token: 20K-30K
- 可能生成: 1-2个技能

如果没问题，我现在就开始！
(回复"开始"或直接回车确认，或告诉我需要调整)
```

---

## 4. Action-Reflection-Iteration 循环

### 4.1 配置参数

| 参数 | 值 | 说明 |
|------|-----|------|
| 最大循环次数 | 3次 | 防止无限循环 |
| 信息充分阈值 | 70分 | 达到即退出循环 |
| 单次循环超时 | 10分钟 | 防止单次卡住 |

### 4.2 评分维度与权重

**信息充分性评分表**:

| 维度 | 权重 | 评分标准 |
|------|------|----------|
| 核心概念覆盖 | 25% | 主要概念是否都有覆盖 |
| 实用示例数量 | 25% | 是否有足够的代码示例 |
| 最佳实践 | 20% | 是否包含行业最佳实践 |
| 常见问题 | 15% | 是否覆盖常见坑点 |
| 信息来源质量 | 15% | 来源是否权威可靠 |

**评分计算**:
```
总分 = Σ(维度得分 × 权重)

示例:
  核心概念: 80分 × 25% = 20
  实用示例: 60分 × 25% = 15
  最佳实践: 70分 × 20% = 14
  常见问题: 50分 × 15% = 7.5
  来源质量: 90分 × 15% = 13.5
  ────────────────────────
  总分: 70分 (刚好达到阈值)
```

### 4.3 循环终止条件

```
终止条件（满足任一）:
┌─────────────────────────────────────────────────────┐
│ 1. 总分 ≥ 70分 (信息充分)                           │
│ 2. 循环次数 = 3次 (达到上限)                        │
│ 3. 连续2次总分无提升 (陷入停滞)                     │
│ 4. Token预算剩余 < 20% (资源不足)                   │
│ 5. 用户手动终止                                     │
└─────────────────────────────────────────────────────┘

未达阈值的处理:
- 如果循环3次后总分 < 70分:
  → 提示用户当前信息有限
  → 询问是否继续或接受当前质量
  → 记录到日志供后续改进
```

### 4.4 循环1: 广泛收集

**Action (执行)**:
```
任务: 广泛搜索
- 打开 GitHub Trending
- 浏览 react.dev 官方文档
- 搜索 GitHub Blog 相关文章
- 收集初步信息

工具: agent-browser
```

**Reflection (反思)**:
```
评估信息充分性:

维度                    得分    加权分
─────────────────────────────────────
核心概念覆盖            80分    20.0  ✓
实用示例数量            30分     7.5  ✗ (只有1个简单示例)
最佳实践               60分     12.0  ⚠️
常见问题                0分      0.0  ✗ (完全没有)
信息来源质量            90分     13.5  ✓
─────────────────────────────────────
总分: 53分 < 70分阈值

判断: 信息不够，需要继续搜索

缺失项:
- 完整的代码示例（需要2-3个）
- 常见问题解答
- 更多最佳实践

建议搜索:
- "React 19 Server Components 完整示例"
- "React 19 常见问题 FAQ"
- "React 19 最佳实践 2026"
```

**Iteration (迭代决策)**:
```
判断: 继续循环2
原因: 53分 < 70分阈值，且未达最大循环次数
```

### 4.5 循环2: 针对性补充

**Action (执行)**:
```
任务: 针对性搜索（基于循环1的缺失项）
- 搜索 "React 19 Server Components 完整示例"
- 搜索 "React 19 常见问题 FAQ"
- 搜索 "React 19 最佳实践 2026"
- 深入阅读官方文档的示例章节

工具: agent-browser
```

**Reflection (反思)**:
```
评估信息充分性:

维度                    得分    加权分
─────────────────────────────────────
核心概念覆盖            85分    21.25  ✓
实用示例数量            75分    18.75  ✓ (找到3个完整示例)
最佳实践               80分     16.00  ✓
常见问题               70分     10.50  ✓ (收集到5个FAQ)
信息来源质量            90分     13.50  ✓
─────────────────────────────────────
总分: 80分 ≥ 70分阈值 ✓

判断: 信息充分，可以进入技能生成阶段

收集到的资源:
- 官方文档: 3篇
- 社区教程: 5篇
- 代码示例: 4个
- FAQ: 8个
- 最佳实践: 12条
```

**Iteration (迭代决策)**:
```
判断: 退出循环
原因: 80分 ≥ 70分阈值，信息已充分
下一步: 进入技能生成流程
```

---

## 5. 技能生成流程

### 5.1 技能去重与更新逻辑

**检查流程**:
```
生成技能前检查:
┌─────────────────────────────────────────┐
│ 1. 查询 generated_skills 表             │
│    条件: title LIKE '%主题关键词%'      │
│                                         │
│ 2. 如果存在同名技能:                    │
│    → 检查版本差异                       │
│    → 询问用户: 覆盖/新建版本/取消       │
│                                         │
│ 3. 如果存在相似技能:                    │
│    → 显示相似度                         │
│    → 询问用户: 合并/新建/取消           │
└─────────────────────────────────────────┘
```

**版本管理**:
```sql
-- 技能版本字段
ALTER TABLE generated_skills ADD COLUMN version INTEGER DEFAULT 1;
ALTER TABLE generated_skills ADD COLUMN parent_skill_id INTEGER;
ALTER TABLE generated_skills ADD COLUMN is_latest BOOLEAN DEFAULT 1;

-- 新建版本时:
-- 1. 将旧版本的 is_latest 设为 0
-- 2. 新版本 parent_skill_id 指向旧版本
-- 3. version = 旧版本 + 1
```

**用户交互示例**:
```
⚠️ 检测到已存在相似技能

已有技能:
  - "React Server Components" (v1, 创建于 2025-06-15)
  - "React 18 新特性" (v1, 创建于 2025-03-20)

请选择:
A. 覆盖 "React Server Components" (创建新版本)
B. 新建独立技能 "React 19 Server Components"
C. 合并到 "React Server Components" (扩展内容)
D. 取消

你的选择:
```

### 5.2 步骤1: 大纲设计（LLM）

```json
{
  "title": "React 19 Server Components 指南",
  "sections": [
    {
      "title": "什么时候使用这个技能",
      "content": "3个典型使用场景"
    },
    {
      "title": "快速开始",
      "content": "3个步骤，每个步骤有代码示例"
    },
    {
      "title": "核心概念",
      "content": "Server Components vs Client Components"
    },
    {
      "title": "实用示例",
      "content": "2个完整示例"
    },
    {
      "title": "最佳实践",
      "content": "5条最佳实践"
    },
    {
      "title": "常见问题",
      "content": "5个FAQ"
    }
  ]
}
```

### 5.3 步骤2: 内容生成（LLM）
按照大纲生成完整的SKILL.md文件。

### 5.4 步骤3: 自我检查（LLM）
自我检查完整性、实用性、示例、准确性，发现问题直接修改。

---

## 6. 三层质量验证

### 6.1 第一层: 规则验证（自动化）

**检查清单**:
- [ ] Frontmatter 完整
- [ ] 结构完整（标题、章节≥3）
- [ ] 内容充足（≥2KB, ≥800字）
- [ ] 有代码块（≥1个）
- [ ] 无占位符、无垃圾关键词

### 6.2 第二层: AI验证（LLM）

**评分维度**:
| 维度 | 权重 |
|------|------|
| 实用性 | 25% |
| 完整性 | 20% |
| 示例质量 | 20% |
| 文档清晰 | 15% |
| 准确性 | 15% |
| 创新性 | 5% |

**输出示例**:
```json
{
  "overallScore": 87,
  "status": "approved",
  "strengths": ["实用性强", "示例完整"],
  "suggestions": ["增加真实项目示例", "补充性能优化技巧"]
}
```

### 6.3 第三层: 人工验证（最终把关）

**验证清单**:
- [ ] 整体印象
- [ ] 实用性（我自己会用吗？）
- [ ] 准确性
- [ ] 完整性
- [ ] 与AI验证一致吗？

---

## 7. 数据库设计

### 7.1 数据库选择
- SQLite（轻量级、文件型、无需服务器）
- 位置: `~/.openclaw/skills/autonomous-learning/data/learning.db`

### 7.2 核心表设计

#### 表1: learning_goals (学习目标)

```sql
CREATE TABLE learning_goals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    priority INTEGER NOT NULL DEFAULT 2,
    status TEXT NOT NULL DEFAULT 'pending',
    source TEXT,
    estimated_hours REAL,
    actual_hours REAL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    deadline TIMESTAMP,
    parent_id INTEGER,
    metadata TEXT,
    FOREIGN KEY (parent_id) REFERENCES learning_goals(id)
);

-- 状态枚举: pending, in_progress, completed, paused, cancelled
-- 优先级: 1=低, 2=中, 3=高
```

#### 表2: learning_tasks (学习任务)

```sql
CREATE TABLE learning_tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    goal_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    task_type TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending',
    priority INTEGER NOT NULL DEFAULT 2,
    estimated_minutes INTEGER,
    actual_minutes INTEGER,
    tokens_used INTEGER DEFAULT 0,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    retry_count INTEGER DEFAULT 0,
    error_message TEXT,
    result_summary TEXT,
    metadata TEXT,
    FOREIGN KEY (goal_id) REFERENCES learning_goals(id) ON DELETE CASCADE
);

-- 任务类型: search, analyze, generate, validate
-- 状态: pending, in_progress, completed, failed, skipped
```

#### 表3: learning_sessions (学习会话)

```sql
CREATE TABLE learning_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    goal_id INTEGER NOT NULL,
    session_type TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'active',
    started_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ended_at TIMESTAMP,
    duration_minutes INTEGER,
    tokens_used INTEGER DEFAULT 0,
    tokens_budget INTEGER,
    time_budget_minutes INTEGER,
    checkpoints TEXT,
    summary TEXT,
    metadata TEXT,
    FOREIGN KEY (goal_id) REFERENCES learning_goals(id) ON DELETE CASCADE
);

-- 会话类型: learning, iteration, generation, validation
-- 状态: active, paused, completed, timeout, cancelled
```

#### 表4: generated_skills (生成的技能)

```sql
CREATE TABLE generated_skills (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    goal_id INTEGER NOT NULL,
    task_id INTEGER,
    title TEXT NOT NULL,
    file_path TEXT NOT NULL,
    version INTEGER DEFAULT 1,
    parent_skill_id INTEGER,
    is_latest BOOLEAN DEFAULT 1,
    quality_score INTEGER,
    validation_status TEXT NOT NULL DEFAULT 'pending',
    tokens_used INTEGER DEFAULT 0,
    file_size_bytes INTEGER,
    word_count INTEGER,
    code_block_count INTEGER,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    validated_at TIMESTAMP,
    validated_by TEXT,
    feedback TEXT,
    metadata TEXT,
    FOREIGN KEY (goal_id) REFERENCES learning_goals(id) ON DELETE SET NULL,
    FOREIGN KEY (task_id) REFERENCES learning_tasks(id) ON DELETE SET NULL,
    FOREIGN KEY (parent_skill_id) REFERENCES generated_skills(id) ON DELETE SET NULL
);

-- 验证状态: pending, rule_passed, ai_approved, human_approved, rejected
```

#### 表5: learning_backlog (待学习列表)

```sql
CREATE TABLE learning_backlog (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    source_goal_id INTEGER,
    source_session_id INTEGER,
    priority INTEGER NOT NULL DEFAULT 2,
    reason TEXT NOT NULL,
    saved_progress TEXT,
    tokens_already_used INTEGER DEFAULT 0,
    time_already_spent_minutes INTEGER DEFAULT 0,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_attempted_at TIMESTAMP,
    attempt_count INTEGER DEFAULT 0,
    metadata TEXT,
    FOREIGN KEY (source_goal_id) REFERENCES learning_goals(id) ON DELETE SET NULL,
    FOREIGN KEY (source_session_id) REFERENCES learning_sessions(id) ON DELETE SET NULL
);

-- 加入原因: timeout, user_paused, token_budget_exceeded, manual_save
```

#### 索引设计

```sql
-- 性能优化索引
CREATE INDEX idx_goals_status ON learning_goals(status);
CREATE INDEX idx_goals_priority ON learning_goals(priority DESC);
CREATE INDEX idx_tasks_goal_id ON learning_tasks(goal_id);
CREATE INDEX idx_tasks_status ON learning_tasks(status);
CREATE INDEX idx_sessions_goal_id ON learning_sessions(goal_id);
CREATE INDEX idx_skills_goal_id ON generated_skills(goal_id);
CREATE INDEX idx_skills_validation ON generated_skills(validation_status);
CREATE INDEX idx_backlog_priority ON learning_backlog(priority DESC);
CREATE INDEX idx_backlog_created ON learning_backlog(created_at DESC);
```

---

## 8. Token消耗优化

### 8.1 实时监控机制

**监控点**:
```python
class TokenMonitor:
    def __init__(self, budget: int, warning_threshold: float = 0.8):
        self.budget = budget
        self.used = 0
        self.warning_threshold = warning_threshold
        self.checkpoints = []  # 安全中断点列表

    def check_before_action(self, estimated_tokens: int) -> bool:
        """执行前检查是否有足够预算"""
        if self.used + estimated_tokens > self.budget:
            return False
        return True

    def record_usage(self, actual_tokens: int):
        """记录实际消耗"""
        self.used += actual_tokens
        if self.used / self.budget >= self.warning_threshold:
            self.emit_warning()

    def can_continue(self) -> bool:
        """检查是否还能继续"""
        return self.used < self.budget * 0.95  # 留5%缓冲

    def get_remaining(self) -> int:
        """获取剩余预算"""
        return max(0, self.budget - self.used)
```

**安全中断点**:
```
┌─────────────────────────────────────────────────────┐
│ 安全中断点（可在这些点暂停而不影响质量）:            │
│                                                     │
│ 1. 循环之间 - Action-Reflection-Iteration          │
│ 2. 技能生成前 - 收集完信息后                        │
│ 3. 验证层之间 - 规则验证后、AI验证后                │
│ 4. 章节之间 - 生成大纲后可逐章节生成                │
└─────────────────────────────────────────────────────┘
```

### 8.2 预算不足处理

```
Token预算即将耗尽时的处理:

if remaining < budget * 0.2:
    1. 检查当前是否在安全中断点
    2. 如果是:
       → 暂停并保存进度到 learning_backlog
       → 通知用户并询问是否增加预算
    3. 如果不是:
       → 继续到下一个安全中断点
       → 然后暂停
```

### 8.3 优化策略

1. LLM全程介入，但每一步都明确目标
2. 先决策、再设计、最后生成 - 避免盲目生成
3. 自我检查、自我改进 - 减少来回迭代
4. 规则验证先做 - 低成本快速过滤
5. AI验证后再人工 - 节省人工成本

### 8.4 预期效率
- 相比"脚本生成 + LLM审核"，节省 **~70% token**
- 质量显著提升
- 循环架构确保信息充分

---

## 9. 错误处理机制

### 9.1 错误分类与处理

| 错误类型 | 场景 | 处理策略 |
|----------|------|----------|
| **网络错误** | 搜索/爬取失败 | 重试3次，间隔递增(5s, 15s, 30s) |
| **LLM超时** | 生成/验证超时 | 检查点恢复，分段生成 |
| **LLM错误** | 返回格式错误 | 重试并给出更明确提示 |
| **数据库错误** | 写入失败 | 内存缓存+异步重试 |
| **Token超限** | 达到预算上限 | 安全中断点暂停 |
| **时间超限** | 达到时间限制 | 安全中断点暂停 |

### 9.2 重试策略

```python
class RetryStrategy:
    def __init__(self, max_retries: int = 3):
        self.max_retries = max_retries
        self.delays = [5, 15, 30]  # 秒

    async def execute_with_retry(self, action, error_types):
        for attempt in range(self.max_retries):
            try:
                return await action()
            except error_types as e:
                if attempt == self.max_retries - 1:
                    raise  # 最后一次重试失败，抛出异常
                await asyncio.sleep(self.delays[attempt])

        # 所有重试失败后的处理
        self.handle_final_failure(e)

    def handle_final_failure(self, error):
        """最终失败处理"""
        # 1. 记录详细错误日志
        # 2. 保存当前进度
        # 3. 更新任务状态为 failed
        # 4. 通知用户并提供选项
```

### 9.3 错误恢复流程

```
错误发生后的恢复流程:

┌─────────────────────────────────────────┐
│ 1. 捕获错误并分类                        │
│    ↓                                    │
│ 2. 记录错误详情到日志                    │
│    ↓                                    │
│ 3. 保存当前进度到数据库                  │
│    ↓                                    │
│ 4. 判断是否可重试                        │
│    ├─ 可重试 → 执行重试策略              │
│    └─ 不可重试 → 进入恢复流程            │
│         ↓                               │
│ 5. 通知用户并提供选项:                   │
│    A. 从检查点继续                       │
│    B. 跳过当前步骤                       │
│    C. 保存到待学习列表                   │
│    D. 放弃本次学习                       │
└─────────────────────────────────────────┘
```

### 9.4 超时处理细节

**时间超时处理**:
```
学习时间达到限制时:

1. 检查当前阶段:
   - 信息收集阶段 → 保存已收集信息
   - 技能生成阶段 → 保存已生成部分
   - 质量验证阶段 → 保存验证进度

2. 通知用户:
   ⏰ 学习时间已达到设定的 120 分钟

   当前进度:
   - 阶段: 技能生成 (60%)
   - 已生成: 大纲 + 3个章节
   - 剩余: 2个章节 + 验证

   请选择:
   A. 继续学习 (追加时间)
   B. 保存进度，稍后继续
   C. 接受当前结果 (跳过剩余内容)

3. 等待用户响应 (5分钟超时):
   - 有响应 → 执行用户选择
   - 无响应 → 自动保存到 learning_backlog
```

**Token超时处理**:
```
Token预算达到80%时预警:
   💰 Token使用提醒

   已使用: 24,000 / 30,000 (80%)
   剩余: 6,000 tokens

   当前正在进行: AI验证
   预计完成需要: ~3,000 tokens

   建议: 可以完成当前步骤

Token预算达到95%时强制暂停:
   ⚠️ Token预算即将耗尽

   已使用: 28,500 / 30,000 (95%)

   已自动保存当前进度。
   请增加预算或从待学习列表继续。
```

---

## 10. 状态机设计

### 10.1 学习目标状态机

```
                    ┌──────────────┐
                    │   pending    │
                    │   (待开始)   │
                    └──────┬───────┘
                           │ 用户启动
                           ▼
                    ┌──────────────┐
           ┌───────│ in_progress  │───────┐
           │       │   (进行中)   │       │
           │       └──────┬───────┘       │
           │              │               │
     用户暂停            完成所有任务      用户取消
           │              │               │
           ▼              ▼               ▼
    ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
    │   paused     │ │  completed   │ │  cancelled   │
    │   (已暂停)   │ │   (已完成)   │ │   (已取消)   │
    └──────┬───────┘ └──────────────┘ └──────────────┘
           │
      用户继续
           │
           ▼
    ┌──────────────┐
    │ in_progress  │
    └──────────────┘
```

### 10.2 学习任务状态机

```
┌──────────────┐
│   pending    │
│   (待执行)   │
└──────┬───────┘
       │ 开始执行
       ▼
┌──────────────┐
│ in_progress  │◀─────────────┐
│   (执行中)   │              │
└──────┬───────┘              │
       │                      │
       ├──── 执行成功 ──▶ ┌──────────────┐
       │                  │  completed   │
       │                  │   (已完成)   │
       │                  └──────────────┘
       │
       ├──── 执行失败 ──▶ ┌──────────────┐
       │                  │   failed     │
       │                  │   (失败)     │
       │                  └──────┬───────┘
       │                         │
       │                    重试次数 < 3
       │                         │
       └─────────────────────────┘
                             │
                        重试次数 ≥ 3
                             │
                             ▼
                      ┌──────────────┐
                      │   skipped    │
                      │   (已跳过)   │
                      └──────────────┘
```

### 10.3 技能验证状态机

```
┌──────────────┐
│   pending    │
│  (待验证)    │
└──────┬───────┘
       │ 规则验证
       ▼
┌──────────────┐
│ rule_check   │
│  (规则检查)  │
└──────┬───────┘
       │
       ├──── 不通过 ──▶ 返回修改
       │
       ▼ 通过
┌──────────────┐
│ rule_passed  │
│ (规则通过)   │
└──────┬───────┘
       │ AI验证
       ▼
┌──────────────┐
│ ai_validating│
│ (AI验证中)   │
└──────┬───────┘
       │
       ├──── 分数<60 ──▶ ┌──────────────┐
       │                 │  rejected    │
       │                 │  (已拒绝)    │
       │                 └──────────────┘
       │
       ▼ 分数≥60
┌──────────────┐
│ ai_approved  │
│ (AI通过)     │
└──────┬───────┘
       │ 人工验证
       ▼
┌──────────────┐
│ human_review │
│ (人工审核)   │
└──────┬───────┘
       │
       ├──── 不通过 ──▶ 返回修改
       │
       ▼ 通过
┌──────────────┐
│human_approved│
│ (人工通过)   │
└──────────────┘
```

---

## 11. 文件结构

```
autonomous-learning/
├── SKILL.md                    # 技能主文档
├── README.md                   # 用户快速开始
├── SETUP.md                    # 安装指南
├── COST-OPTIMIZATION.md        # Token优化指南
├── LEARNING-LOGIC.md           # 学习逻辑
├── INFO-TO-SKILL.md           # 信息到技能流程
├── QUALITY-VALIDATION.md      # 质量验证系统
├── AGENT-ENHANCEMENT.md        # 子Agent设计
├── OPENSOURCE-PLAN.md          # 开源方案
├── STARTUP-INTERACTION.md      # 启动交互流程
├── COMPLETE-ARCHITECTURE.md    # 完整架构
├── 完整设计文档.md             # 本文档
├── templates/
│   └── learner-agent-prompt.md # LearnerAgent提示词
├── database/
│   ├── schema.sql              # 数据库建表SQL
│   ├── db.py                   # Python数据库类
│   └── queries.py             # SQL查询封装
├── scripts/
│   ├── setup.sh                # 一键安装
│   ├── validation/             # 验证脚本
│   └── ...
└── data/
    ├── learning.db            # SQLite数据库
    └── backups/               # 数据库备份
```

---

## 12. 下一步实现计划

### Phase 1: 基础框架
1. 创建数据库表结构 (schema.sql)
2. 实现Python数据库类 (db.py)
3. 创建LearnerAgent提示词

### Phase 2: 核心流程
1. 实现目标拆解与优先级计算
2. 实现Action-Reflection-Iteration循环
3. 实现技能生成

### Phase 3: 质量验证
1. 实现规则验证脚本
2. 实现AI验证提示词
3. 实现人工验证流程

### Phase 4: 完善优化
1. 启动交互流程
2. 超时处理与错误恢复
3. 待学习列表管理
4. Token监控与优化
5. 用户界面

---

## 🎯 关键特性总结

| 特性 | 状态 |
|------|------|
| 目标拆解与优先级排序 | ✅ 含计算规则 |
| Action-Reflection-Iteration 循环 | ✅ 含终止条件 |
| LLM全程介入（决策→设计→生成→自检） | ✅ |
| 三层质量验证（规则→AI→人工） | ✅ |
| SQLite数据库（完整状态持久化） | ✅ 5表完整DDL |
| 启动交互流程（推荐→确认→配置） | ✅ |
| 超时处理（智能暂停/继续/待学习） | ✅ 含详细流程 |
| 待学习列表（优先级管理） | ✅ |
| Token优化（高效使用资源） | ✅ 含监控机制 |
| 错误处理机制 | ✅ 含重试策略 |
| 状态机设计 | ✅ 3个状态机图 |
| 技能去重/版本管理 | ✅ |

---

**文档结束**

_自主学习系统设计 v2.0 完成！_
