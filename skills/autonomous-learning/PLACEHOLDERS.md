# 自主学习系统 - 占位符清单

**当前状态**: 基础框架完成，需要集成真实功能

---

## 📋 占位符清单

### 1. Action 阶段（信息收集）- `learning_manager.py`
**当前状态**: 占位符，模拟数据
**需要实现**: 真实的 agent-browser 搜索

**位置**: `database/learning_manager.py` - `collect_information()`

**当前代码**:
```python
def collect_information(self, goal_id: int, iteration: int) -> Dict:
    # 占位符：实际项目中这里会调用 agent-browser 搜索
    collected_data = {
        'concepts': ['概念1', '概念2', '概念3', '概念4', '概念5'],
        'examples_count': 3,
        'has_best_practices': iteration > 1,
        'has_faqs': iteration > 2,
        'sources_quality': 0.7
    }
    return collected_data
```

**需要改成**:
- 调用 agent-browser 真实搜索
- 提取网页内容
- 结构化信息

---

### 2. AI验证器 - `quality_validator.py`
**当前状态**: 占位符，返回模拟数据
**需要实现**: 真实的 LLM 调用

**位置**: `database/quality_validator.py` - `AIValidator.validate()`

**当前代码**:
```python
def validate(self, filepath: str) -> ValidationResult:
    # 占位符，实际会调用LLM进行验证
    return ValidationResult(
        passed=True,
        score=85.0,
        issues=[],
        strengths=['实用性强', '示例完整', '文档清晰'],
        details={...}
    )
```

**需要改成**:
- 读取技能文件
- 调用 LLM 进行验证
- 返回真实的评分和反馈

---

### 3. 技能内容生成 - `skill_generator.py`
**当前状态**: 模板化内容，占位符
**需要实现**: 真实的 LLM 内容生成

**位置**: `database/skill_generator.py` - 各个内容生成方法

**当前代码**:
- 所有内容都是预写好的模板
- 没有真实的 LLM 调用

**需要改成**:
- 根据收集的信息
- 调用 LLM 生成真实内容
- 生成个性化的技能

---

### 4. 大纲设计优化 - `skill_outliner.py`
**当前状态**: 固定模板，不根据收集的数据调整
**需要实现**: 根据收集的数据智能调整大纲

**位置**: `database/skill_outliner.py`

**当前代码**:
- 固定的章节模板
- 不根据实际收集的信息调整

**需要改成**:
- 分析收集的数据
- 智能调整章节
- 突出重点内容

---

### 5. 人工验证流程 - `quality_validator.py`
**当前状态**: 只有状态标记，没有交互流程
**需要实现**: 真实的人工验证交互

**位置**: 需要新增

**需要添加**:
- 展示技能给用户
- 接受用户反馈
- 处理修改、通过、拒绝

---

## 🎯 实现优先级

### 🔴 高优先级（核心功能）
1. **Action 阶段** - 集成 agent-browser 真实搜索
2. **技能内容生成** - 集成 LLM 真实生成
3. **AI验证器** - 集成 LLM 真实验证

### 🟡 中优先级（增强功能）
4. **大纲设计优化** - 智能调整大纲
5. **人工验证流程** - 用户交互验证

### 🟢 低优先级（锦上添花）
6. **更多优化** - 错误处理、重试机制等

---

## 🛠️ 实现步骤

### Phase A: 集成 agent-browser
1. 创建信息收集模块
2. 集成 agent-browser 搜索
3. 网页内容提取和清洗
4. 信息结构化

### Phase B: 集成 LLM
1. 创建 LLM 调用模块
2. 技能内容生成
3. AI验证器实现
4. 大纲优化

### Phase C: 完善交互
1. 人工验证流程
2. 用户反馈处理
3. 完整端到端测试

---

## 📝 备注

- 当前所有核心框架都已完成
- 只需要替换占位符为真实实现
- agent-browser 技能已存在
- LLM 可以通过 OpenClaw 调用
