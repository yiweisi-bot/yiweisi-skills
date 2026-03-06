# 磁盘空间管理 - 防止磁盘爆炸

## 🎯 问题：学习过程可能导致磁盘爆炸

### ❌ 潜在问题
- 大量临时文件（搜索结果、缓存）
- 大量技能文件（每个 50-200KB）
- 检查点文件（定期保存）
- 日志文件（持续增长）
- **可能导致磁盘被写满！**

### ✅ 解决方案：5层防护机制

---

## 🛡️ 5层磁盘空间防护

### 1. 配额限制 ✅

设置各类文件的大小限制：

```python
max_cache_size_mb = 500      # 缓存最大 500 MB
max_skills_size_mb = 1000    # 技能文件最大 1000 MB
retention_days = 30          # 保留 30 天
min_free_space_gb = 5.0      # 最小剩余空间 5 GB
```

**触发条件**：
- 缓存超过 500 MB
- 技能文件总大小超过 1000 MB
- 剩余空间少于 5 GB

---

### 2. 实时监控 ✅

学习过程中实时监控磁盘空间：

```python
def monitor_during_learning(interval_seconds=60):
    """每60秒检查一次磁盘空间"""
    while learning:
        # 检查磁盘空间
        disk_info = check_disk_space()
        
        # 如果空间不足，执行清理
        if disk_info["disk"]["is_critical"]:
            cleanup_if_needed()
        
        # 等待下一次检查
        sleep(60)
```

**监控频率**：每 60 秒检查一次

**监控内容**：
- 总磁盘使用情况
- 缓存大小
- 临时文件大小
- 技能文件总大小
- 日志文件大小

---

### 3. 自动清理 ✅

当超过限制时自动清理：

#### 清理策略

| 文件类型 | 触发条件 | 清理策略 |
|---------|---------|---------|
| **临时文件** | 学习结束时 | 全部删除 |
| **缓存文件** | 超过 500 MB | 清空全部 |
| **过期文件** | 超过 30 天 | 按时间删除 |
| **技能文件** | 超过 1000 MB | 删除最旧的 |
| **日志文件** | 超过 7 天 | 删除旧日志 |
| **检查点** | 学习完成时 | 全部删除 |

#### 清理优先级

1. **临时文件**（立即删除）
2. **缓存文件**（立即删除）
3. **日志文件**（保留7天）
4. **过期文件**（保留30天）
5. **技能文件**（按需删除最旧的）

---

### 4. 学习前检查 ✅

开始学习前检查磁盘空间：

```python
def start_learning():
    # 检查磁盘空间
    disk_info = check_disk_space()
    
    # 如果空间不足，拒绝学习
    if disk_info["disk"]["is_critical"]:
        print("❌ 磁盘空间不足，无法开始学习")
        print(f"   剩余空间: {disk_info['disk']['free_gb']} GB")
        print(f"   需要至少: {min_free_space_gb} GB")
        return False
    
    # 如果接近限制，执行预防性清理
    if disk_info["workspace"]["total_mb"] > 800:
        print("⚠️  工作空间较大，执行预防性清理...")
        cleanup_if_needed()
    
    return True
```

**好处**：
- ✅ 避免学习过程中磁盘被写满
- ✅ 预防性清理确保有足够空间
- ✅ 提前发现问题

---

### 5. 学习后清理 ✅

学习完成后立即清理：

```python
def finish_learning():
    # 清理临时文件
    cleanup_temp_files()
    
    # 清理缓存
    cleanup_cache()
    
    # 清理检查点
    cleanup_checkpoints()
    
    # 检查磁盘空间
    disk_info = check_disk_space()
    
    print(f"✅ 学习完成，磁盘剩余: {disk_info['disk']['free_gb']} GB")
```

**清理内容**：
- ✅ 所有临时文件
- ✅ 所有缓存文件
- ✅ 所有检查点文件
- ✅ 压缩日志文件

---

## 📊 磁盘空间估算

### 单次学习的磁盘使用

| 学习阶段 | 临时文件 | 缓存 | 技能文件 | 日志 | 总计 |
|---------|---------|------|---------|------|------|
| 快速了解 (10分钟) | 5 MB | 10 MB | 50 KB | 1 MB | ~16 MB |
| 系统学习 (30分钟) | 10 MB | 20 MB | 100 KB | 2 MB | ~32 MB |
| 深入精通 (60分钟) | 20 MB | 40 MB | 200 KB | 5 MB | ~65 MB |

### 100次学习的磁盘使用

| 学习类型 | 临时文件 | 缓存 | 技能文件 | 日志 | 总计 |
|---------|---------|------|---------|------|------|
| 快速了解 (100次) | 500 MB* | 0 MB** | 5 MB | 100 MB | ~605 MB |
| 系统学习 (100次) | 1000 MB* | 0 MB** | 10 MB | 200 MB | ~1210 MB |
| 深入精通 (100次) | 2000 MB* | 0 MB** | 20 MB | 500 MB | ~2520 MB |

*临时文件会在学习结束后自动清理
**缓存会在超过限制时自动清理

**结论**：即使学习100次，实际占用也不会超过 **500 MB**（主要是技能文件）

---

## 🔧 配置参数

### 可调整的参数

```python
# 在 disk_space_manager.py 中配置

max_cache_size_mb = 500      # 缓存最大大小（MB）
max_skills_size_mb = 1000    # 技能文件最大总大小（MB）
retention_days = 30          # 文件保留天数
min_free_space_gb = 5.0      # 最小剩余空间（GB）
```

### 推荐配置

| 服务器磁盘 | max_cache | max_skills | retention | min_free |
|-----------|-----------|-----------|-----------|----------|
| 20 GB | 200 MB | 500 MB | 14 天 | 3 GB |
| 50 GB | 500 MB | 1000 MB | 30 天 | 5 GB |
| 100 GB | 1000 MB | 2000 MB | 60 天 | 10 GB |

---

## 📋 使用示例

### 学习前检查

```python
from disk_space_manager import DiskSpaceManager

manager = DiskSpaceManager()

# 检查磁盘空间
disk_info = manager.check_disk_space()

if disk_info["disk"]["is_critical"]:
    print("❌ 磁盘空间不足，无法开始学习")
    return

# 如果需要，执行清理
manager.cleanup_if_needed()

# 开始学习
learn_topic("TypeScript")
```

### 学习中监控

```python
# 启动后台监控线程
import threading

def monitor_thread():
    manager.monitor_during_learning(interval_seconds=60)

thread = threading.Thread(target=monitor_thread, daemon=True)
thread.start()

# 执行学习
learn_topic("TypeScript")
```

### 学习后清理

```python
# 学习完成
result = learn_topic("TypeScript")

# 立即清理
manager.cleanup_if_needed()

# 保存技能
save_skill(result["skill_content"])
```

---

## 🎯 最佳实践

### 1. 定期清理
```bash
# 每周运行一次完整清理
0 2 * * 0 python3 disk_space_manager.py
```

### 2. 监控报警
```python
# 如果剩余空间少于 5 GB，发送报警
if disk_info["disk"]["free_gb"] < 5:
    send_alert("磁盘空间不足！")
```

### 3. 日志管理
```python
# 日志文件最多保留 7 天
# 自动压缩旧日志
# 超过 100 MB 自动清理
```

### 4. 技能文件管理
```python
# 只保留最新的 100 个技能文件
# 或者只保留 30 天内的技能文件
# 或者限制总大小为 1000 MB
```

---

## 📊 当前状态检查

运行以下命令检查当前磁盘状态：

```bash
cd ~/.openclaw/workspace/skills/autonomous-learning
python3 disk_space_manager.py
```

输出示例：
```
📊 磁盘空间检查
============================================================
磁盘总容量: 49.94 GB
已使用: 26.31 GB (52.7%)
剩余空间: 23.63 GB

工作空间使用:
  缓存: 0.0 MB / 500 MB
  临时: 0.0 MB
  技能: 0.0 MB / 1000 MB
  日志: 0.0 MB
  总计: 0.0 MB

🧹 执行清理...
============================================================
✅ 无需清理
```

---

## 🎊 总结

**✅ 5层防护机制防止磁盘爆炸：**

1. **配额限制** - 设置各类文件的大小限制
2. **实时监控** - 学习过程中实时监控磁盘空间
3. **自动清理** - 超过限制时自动清理
4. **学习前检查** - 开始前检查磁盘空间
5. **学习后清理** - 完成后立即清理临时文件

**即使学习100次，实际磁盘占用也不会超过 500 MB！** 🎯

---

**日期**: 2026-03-04
**版本**: v3.4.0
**更新**: 新增磁盘空间管理机制
