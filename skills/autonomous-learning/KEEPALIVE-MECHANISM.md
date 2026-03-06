# LearnerBot 长时间任务保活机制

## 🎯 问题：如何确保学满 1 小时？

### ❌ 旧版问题
- sessions_spawn 默认超时：5分钟
- 学习任务可能几分钟就结束
- 无法完成深入精通级别的学习（60分钟）

### ✅ 新版解决方案

---

## 📋 保活机制（5层保障）

### 1. 任务分解 ✅

将长时间任务分解为多个阶段：

```python
# 深入精通（60分钟）分解为10个阶段
stages = [
    {"name": "全面搜索", "duration": 15, "weight": 20},
    {"name": "深度挖掘", "duration": 10, "weight": 15},
    {"name": "架构设计", "duration": 5, "weight": 8},
    {"name": "核心原理", "duration": 8, "weight": 12},
    {"name": "高级示例", "duration": 7, "weight": 10},
    {"name": "性能优化", "duration": 5, "weight": 8},
    {"name": "最佳实践", "duration": 5, "weight": 8},
    {"name": "故障排查", "duration": 3, "weight": 5},
    {"name": "全面验证", "duration": 2, "weight": 4},
    {"name": "最终润色", "duration": 2, "weight": 2}
]
```

**好处**：
- ✅ 每个阶段独立执行
- ✅ 定期检查和保活
- ✅ 可以中断和恢复

---

### 2. 心跳机制 ✅

定期发送心跳保持活跃：

```python
def _send_heartbeat(self, stage: str, current: int, total: int):
    """发送心跳（保活）"""
    heartbeat = {
        "type": "heartbeat",
        "timestamp": datetime.now().isoformat(),
        "elapsed_minutes": int(elapsed),
        "remaining_minutes": int(self.time_limit - elapsed),
        "progress": self.progress,
        "current_stage": stage,
        "tokens_used": self.tokens_used,
        "status": "running"
    }
    
    # 发送到父 session
    sessions_send(sessionKey=parent_session, message=json.dumps(heartbeat))
```

**频率**：每个阶段结束时发送一次（约5-15分钟一次）

**好处**：
- ✅ 保持任务活跃
- ✅ 防止被系统终止
- ✅ 实时反馈进度

---

### 3. 检查点保存 ✅

定期保存进度，支持中断恢复：

```python
def _save_checkpoint(self, stage: str):
    """保存检查点（用于恢复）"""
    checkpoint = {
        "timestamp": datetime.now().isoformat(),
        "stage": stage,
        "progress": self.progress,
        "tokens_used": self.tokens_used,
        "elapsed_minutes": elapsed
    }
    
    # 保存到文件
    with open(checkpoint_file, 'w') as f:
        json.dump(checkpoint, f)
```

**频率**：每个阶段结束时保存一次

**好处**：
- ✅ 中断后可以恢复
- ✅ 不会丢失进度
- ✅ 安全可靠

---

### 4. 时间和 Token 监控 ✅

实时监控时间和 Token 使用：

```python
def _is_timeout(self) -> bool:
    """检查是否超时"""
    elapsed = (datetime.now() - self.start_time).total_seconds() / 60
    return elapsed >= self.time_limit

def _is_token_exceeded(self) -> bool:
    """检查是否超过 Token 预算"""
    return self.tokens_used >= self.token_budget
```

**检查频率**：每5秒检查一次

**好处**：
- ✅ 精确控制时间
- ✅ 避免超过预算
- ✅ 及时终止任务

---

### 5. sessions_spawn 超时设置 ✅

设置足够的超时时间：

```python
# 启动子 Agent 时设置超时
result = sessions_spawn(
    task=task,
    agent="learner",
    mode="run",
    timeout=7200  # 2小时超时（足够长）
)
```

**推荐值**：
- 快速了解（10分钟）：timeout=900（15分钟）
- 系统学习（30分钟）：timeout=3600（1小时）
- 深入精通（60分钟）：timeout=7200（2小时）

**好处**：
- ✅ 不会因为超时而终止
- ✅ 有足够的缓冲时间
- ✅ 确保任务完成

---

## 🔄 完整流程（60分钟深入精通）

```
用户: 深入学习 React 架构
    ↓
乙维斯: 🎯 交互式配置
    深度: 深入精通 (master)
    时间: 60 分钟
    Token: 10000
    ↓
启动 LearnerBot（timeout=7200秒）
    ↓
┌─────────────────────────────────────────────┐
│ 阶段 1/10: 全面搜索 (15分钟)               │
│   [████████░░░░░░░░░░] 45% 6:45/15:00     │
│   Token: 4500/10000                        │
│   💓 心跳: 已运行 6 分钟, 剩余 54 分钟     │
│   ✅ 检查点已保存                          │
├─────────────────────────────────────────────┤
│ 阶段 2/10: 深度挖掘 (10分钟)               │
│   [████████████░░░░░░] 60% 6:00/10:00     │
│   Token: 6000/10000                        │
│   💓 心跳: 已运行 21 分钟, 剩余 39 分钟    │
│   ✅ 检查点已保存                          │
├─────────────────────────────────────────────┤
│ ... (继续执行剩余阶段)                     │
├─────────────────────────────────────────────┤
│ 阶段 10/10: 最终润色 (2分钟)               │
│   [████████████████████] 100% 2:00/2:00   │
│   Token: 9800/10000                        │
│   💓 心跳: 已运行 60 分钟, 剩余 0 分钟     │
│   ✅ 检查点已保存                          │
└─────────────────────────────────────────────┘
    ↓
✅ 学习完成！
```

---

## 📊 时间分配示例

### 快速了解（10分钟）

| 阶段 | 时长 | 权重 | Token |
|------|------|------|-------|
| 快速搜索 | 3分钟 | 30% | 600 |
| 生成基础概念 | 3分钟 | 30% | 600 |
| 生成快速示例 | 2分钟 | 20% | 400 |
| 基础验证 | 2分钟 | 20% | 400 |
| **总计** | **10分钟** | **100%** | **2000** |

### 系统学习（30分钟）

| 阶段 | 时长 | 权重 | Token |
|------|------|------|-------|
| 广泛搜索 | 8分钟 | 25% | 1250 |
| 深度搜索 | 5分钟 | 15% | 750 |
| 设计完整大纲 | 3分钟 | 10% | 500 |
| 生成核心概念 | 5分钟 | 15% | 750 |
| 生成实用示例 | 4分钟 | 12% | 600 |
| 生成最佳实践 | 3分钟 | 10% | 500 |
| 三层质量验证 | 2分钟 | 8% | 400 |
| 优化和润色 | 2分钟 | 5% | 250 |
| **总计** | **30分钟** | **100%** | **5000** |

### 深入精通（60分钟）

| 阶段 | 时长 | 权重 | Token |
|------|------|------|-------|
| 全面搜索 | 15分钟 | 20% | 2000 |
| 深度挖掘 | 10分钟 | 15% | 1500 |
| 架构设计 | 5分钟 | 8% | 800 |
| 核心原理 | 8分钟 | 12% | 1200 |
| 高级示例 | 7分钟 | 10% | 1000 |
| 性能优化 | 5分钟 | 8% | 800 |
| 最佳实践 | 5分钟 | 8% | 800 |
| 故障排查 | 3分钟 | 5% | 500 |
| 全面验证 | 2分钟 | 4% | 400 |
| 最终润色 | 2分钟 | 2% | 200 |
| **总计** | **60分钟** | **100%** | **10000** |

---

## 🛡️ 安全保障

### 1. 时间限制保护
- ✅ 精确到分钟的计时
- ✅ 到达时间限制自动终止
- ✅ 不会超时运行

### 2. Token 预算保护
- ✅ 实时 Token 使用估算
- ✅ 到达预算限制自动终止
- ✅ 不会超支

### 3. 中断恢复保护
- ✅ 定期保存检查点
- ✅ 可以从中断处恢复
- ✅ 不丢失进度

### 4. 心跳保活保护
- ✅ 定期发送心跳
- ✅ 保持任务活跃
- ✅ 防止被系统终止

---

## 📋 使用示例

### 快速了解（10分钟）
```python
result = learn_with_keepalive(
    topic="TypeScript 基础类型",
    depth="intro",  # 10分钟
    time_limit=10,
    token_budget=2000
)
```

### 系统学习（30分钟）
```python
result = learn_with_keepalive(
    topic="React Hooks",
    depth="systematic",  # 30分钟
    time_limit=30,
    token_budget=5000
)
```

### 深入精通（60分钟）
```python
result = learn_with_keepalive(
    topic="React 架构设计",
    depth="master",  # 60分钟
    time_limit=60,
    token_budget=10000
)
```

---

## 🎊 总结

**✅ 5层保活机制确保学满指定时间：**

1. **任务分解** - 将长时间任务分解为多个阶段
2. **心跳机制** - 定期发送心跳保持活跃
3. **检查点保存** - 支持中断恢复
4. **时间监控** - 精确控制时间
5. **超时设置** - 设置足够的超时时间

**确保能学满1小时，不会几分钟就结束！** 🎯

---

**日期**: 2026-03-04
**版本**: v3.3.0
**更新**: 新增长时间任务保活机制
