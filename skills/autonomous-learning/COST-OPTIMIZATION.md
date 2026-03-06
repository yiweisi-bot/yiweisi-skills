# Token消耗优化指南 💰

## ⚠️ 重要提示

**自主学习技能会显著消耗模型Token！** 请合理控制使用频率和时长。

---

## 📊 Token消耗估算

### 单次学习会话的Token消耗

| 操作 | 估算Token | 说明 |
|------|----------|------|
| **学习规划** | 2,000-5,000 | 分析目标、制定计划 |
| **GitHub探索** | 5,000-15,000 | 浏览Trending、提取内容 |
| **知识整理** | 3,000-8,000 | 结构化学习笔记 |
| **技能生成** | 8,000-20,000 | 生成完整SKILL.md |
| **质量审核** | 5,000-12,000 | LLM多维度评估 |
| **进度汇报** | 1,000-3,000 | 自然语言总结 |
| **交互对话** | 2,000-5,000 | 与主Agent沟通 |

**总计（单次2小时学习）: 26,000-68,000 tokens**

---

### 月度消耗估算

| 使用频率 | 月度Token消耗 | 估算成本（参考） |
|---------|-------------|-----------------|
| **轻度** (每周1次) | 100K-270K | $0.10-$0.50 |
| **中度** (每周3次) | 300K-800K | $0.30-$1.50 |
| **重度** (每天1次) | 800K-2M | $0.80-$4.00 |
| **极重度** (持续运行) | 3M-10M+ | $3.00-$20.00+ |

*注：成本估算基于混合使用不同模型的大致价格*

---

## 💰 成本优化策略

### 策略1: 选择合适的模型 ⭐⭐⭐

**推荐模型优先级：**

| 模型 | 用途 | 成本 | 质量 | 推荐度 |
|------|------|------|------|--------|
| **doubao/ark-code-latest** | 主要学习 | 低 | 高 | ⭐⭐⭐⭐⭐ |
| **zhipu/glm-4.7** | 质量审核 | 中 | 高 | ⭐⭐⭐⭐ |
| **deepseek/deepseek-chat** | 技能生成 | 低 | 中 | ⭐⭐⭐ |
| **zhipu/glm-5** | 复杂任务 | 高 | 最高 | ⭐⭐⭐ (谨慎使用) |

**配置建议：**
```json
{
  "agents": {
    "learner": {
      "model": "doubao/ark-code-latest",
      "fallbackModels": ["zhipu/glm-4.7", "deepseek/deepseek-chat"]
    }
  }
}
```

---

### 策略2: 限制学习时长 ⭐⭐⭐

**配置学习时间窗口：**
```bash
# 编辑配置，限制单次学习时长
autonomous-learning config set duration 60    # 每次最多60分钟
autonomous-learning config set cooldown 120   # 冷却2小时
```

**推荐时间配置：**

| 使用场景 | 单次时长 | 冷却时间 | 每日次数 |
|---------|---------|---------|---------|
| **测试体验** | 30分钟 | 4小时 | 1-2次 |
| **轻度使用** | 60分钟 | 2小时 | 2-3次 |
| **中度使用** | 90分钟 | 1小时 | 3-4次 |
| **重度使用** | 120分钟 | 30分钟 | 4-6次 |

---

### 策略3: 智能降级策略 ⭐⭐⭐

**不同任务使用不同模型：**

| 任务类型 | 推荐模型 | 原因 |
|---------|---------|------|
| **简单学习规划** | doubao/ark-code-latest | 成本低，够用 |
| **GitHub内容提取** | deepseek/deepseek-chat | 不需要超强理解 |
| **技能生成** | zhipu/glm-4.7 | 质量较好，成本适中 |
| **简单质量审核** | doubao/ark-code-latest | 规则性强，成本低 |
| **复杂质量审核** | zhipu/glm-5 | 需要深度理解（少用） |

---

### 策略4: 缓存和复用 ⭐⭐

**复用已有成果：**
- 缓存已探索的GitHub仓库信息
- 复用之前生成的学习笔记
- 避免重复学习相同主题

**配置示例：**
```bash
# 启用缓存
autonomous-learning config set cacheEnabled true
autonomous-learning config set cacheTTL 72  # 缓存72小时
```

---

### 策略5: 手动审核代替自动审核 ⭐⭐

**节省审核Token：**

| 方式 | Token消耗 | 优点 | 缺点 |
|------|----------|------|------|
| **LLM自动审核** | 5K-12K/次 | 全自动，客观 | Token消耗大 |
| **人工审核** | 0 | 免费，准确 | 需要时间 |
| **混合审核** | 2K-5K/次 | 平衡 | 需要简单配置 |

**推荐：混合审核策略**
- 先用简单规则快速筛选
- 只对边缘案例使用LLM审核
- 最终由人工确认

---

## 🎛️ 成本控制模式

### 模式1: 经济型模式 💰💰
**适合：预算有限，想尝试功能**

```bash
autonomous-learning config set duration 30
autonomous-learning config set cooldown 240
autonomous-learning config set model doubao/ark-code-latest
autonomous-learning config set autoReview false
```

**预计消耗：** 3K-8K tokens/次

---

### 模式2: 平衡模式 ⚖️
**适合：日常使用，成本适中**

```bash
autonomous-learning config set duration 60
autonomous-learning config set cooldown 120
autonomous-learning config set model zhipu/glm-4.7
autonomous-learning config set autoReview true
autonomous-learning config set reviewModel doubao/ark-code-latest
```

**预计消耗：** 15K-30K tokens/次

---

### 模式3: 质量优先模式 ✨
**适合：追求质量，预算充足**

```bash
autonomous-learning config set duration 120
autonomous-learning config set cooldown 60
autonomous-learning config set model zhipu/glm-5
autonomous-learning config set autoReview true
autonomous-learning config set reviewModel zhipu/glm-4.7
```

**预计消耗：** 40K-80K tokens/次

---

## 📊 成本监控

### 启用Token统计
```bash
# 查看当前会话消耗
autonomous-learning stats current

# 查看历史消耗
autonomous-learning stats history

# 查看月度报告
autonomous-learning stats monthly
```

### 设置预算提醒
```bash
# 设置月度预算提醒
autonomous-learning budget set monthly 500000  # 500K tokens

# 设置单次提醒
autonomous-learning budget set session 30000    # 30K tokens
```

### 预警阈值配置
```json
{
  "budget": {
    "monthlyLimit": 500000,
    "sessionLimit": 30000,
    "warningThreshold": 0.8,    # 80%时警告
    "stopThreshold": 0.95        # 95%时停止
  }
}
```

---

## 💡 省钱小贴士

### 1. 集中学习
不要零散学习，集中时间一次学完，减少上下文重复。

### 2. 利用非高峰时段
有些模型提供商在非高峰时段有折扣（如果支持）。

### 3. 复用已有技能
先看看有没有现成的技能，不要重复造轮子。

### 4. 人工审核质量
用你的眼睛代替LLM审核，节省大量token！

### 5. 设置自动停止
配置好预算限制，避免超支。

---

## ⚠️ 重要警告

### 使用前必读
1. **先测试再重度使用** - 先用经济型模式试试水
2. **设置预算限制** - 一定要配置预算提醒
3. **监控使用情况** - 定期查看token消耗
4. **随时可以暂停** - 学习过程中可以随时停止
5. **理解成本结构** - 不同模型价格差异很大

---

## 📞 需要帮助？

如果对成本有疑问：
- 查看 `autonomous-learning help cost`
- 运行 `autonomous-learning stats estimate` 估算消耗
- 查看模型提供商的定价文档

---

_记住：智能学习很强大，但要理性消费！💰✨_
