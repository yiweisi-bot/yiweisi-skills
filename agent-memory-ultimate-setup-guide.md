# 🧠 Agent Memory Ultimate 完整配置指南

**适用于：** OpenClaw Agent  
**版本：** 3.1.0  
**配置时间：** 2026-03-04  
**配置者：** 甲维斯

---

## 📋 概述

Agent Memory Ultimate 是一个基于向量数据库的长期记忆系统，让 AI Agent 能够：
- ✅ 记住用户偏好、项目上下文、重要决策
- ✅ 跨会话保持记忆（不怕 session 重置）
- ✅ 语义搜索（不只是关键词匹配）
- ✅ 自动记忆更新和同步
- ✅ 100% 本地运行，无需外部 API

---

## 🔧 安装步骤

### 1️⃣ 安装 Python 依赖

```bash
pip3 install numpy sentence-transformers onnxruntime
```

**说明：**
- `numpy` - 数值计算库
- `sentence-transformers` - 向量嵌入模型（用于语义理解）
- `onnxruntime` - 本地推理引擎（无需 GPU）

**预计时间：** 5-10 分钟  
**磁盘空间：** ~2-3 GB

---

### 2️⃣ 验证技能已安装

```bash
ls -la /root/.openclaw/workspace/skills/agent-memory-ultimate/
```

**应包含的文件：**
```
agent-memory-ultimate/
├── SKILL.md
├── run
├── package.json
├── scripts/
│   ├── mem.py          # 核心记忆管理
│   ├── query.py        # 查询工具
│   ├── init_db.py      # 数据库初始化
│   └── ...
└── lib/
    ├── memory_core.py  # 记忆核心逻辑
    └── embedder.py     # 向量嵌入
```

---

### 3️⃣ 初始化数据库

```bash
cd /root/.openclaw/workspace/skills/agent-memory-ultimate
python3 scripts/init_db.py
```

**成功后会创建：**
- `/root/.openclaw/workspace/db/memory.db` - SQLite 数据库
- 包含向量索引和全文搜索表

---

## 📥 导入现有记忆

### 4️⃣ 批量导入历史记忆文件

```bash
cd /root/.openclaw/workspace/skills/agent-memory-ultimate
bash scripts/batch-import.sh
```

**功能：**
- 导入 `memory/` 目录下的所有每日记忆文件
- 自动计算重要性（越近的文件越重要）
- 显示导入进度和统计

**预期输出：**
```
📚 开始批量导入记忆文件...

📄 导入 2026-03-01.md (重要性：0.6)...
   ✅ ✓ Stored memory #1 (semantic, importance=0.6)

📄 导入 2026-03-02.md (重要性：0.7)...
   ✅ ✓ Stored memory #2 (semantic, importance=0.7)

...

============================================================
📊 导入完成：成功 4, 错误 0
============================================================
```

---

## 🔄 配置自动同步

### 5️⃣ 创建智能同步脚本

文件：`/root/.openclaw/workspace/skills/agent-memory-ultimate/scripts/sync-memories.sh`

**功能：**
- 自动检测新增/变更的记忆文件
- MD5 哈希去重（避免重复导入）
- 状态追踪（`memory-sync-state.json`）
- 只导入有变化的文件

**脚本内容：** 见附录 A

---

### 6️⃣ 配置 cron 定时任务

```bash
# 编辑 crontab
crontab -e

# 添加以下行（每 3 小时同步一次）
0 */3 * * * /root/.openclaw/workspace/skills/agent-memory-ultimate/scripts/sync-memories.sh >> /root/.openclaw/workspace/logs/memory-sync.log 2>&1
```

**说明：**
- 每 3 小时自动运行
- 日志输出到 `logs/memory-sync.log`
- 自动补导入遗漏的记忆文件

---

## 📊 验证配置

### 7️⃣ 查看记忆统计

```bash
cd /root/.openclaw/workspace/skills/agent-memory-ultimate
python3 scripts/mem.py stats
```

**预期输出：**
```
╔══════════════════════════════════════╗
║       COGNITIVE MEMORY STATS         ║
╠══════════════════════════════════════╣
║  Active memories:       6            ║
║  Deleted (soft):        0            ║
║  With embeddings:       6            ║
║  DB size:             188 KB         ║
╚══════════════════════════════════════╝
```

---

### 8️⃣ 测试语义搜索

```bash
# 设置代理（如果需要）
export HTTP_PROXY=http://127.0.0.1:7892
export HTTPS_PROXY=http://127.0.0.1:7892

# 测试查询
python3 scripts/mem.py recall "聊天室"
python3 scripts/mem.py recall "时区"
python3 scripts/mem.py recall "小红书"
```

**预期输出：**
```
Found 1 memories (hybrid) [9996ms]:

  #   1  [semantic  ]  str=1.00  score=0.398
        用户 Winston 的时区是 Asia/Shanghai (UTC+8)
```

---

## 🛠️ 日常使用命令

### 添加记忆
```bash
python3 scripts/mem.py store "记忆内容" \
  --type semantic \
  --source "manual" \
  --importance 0.8
```

### 查询记忆
```bash
python3 scripts/mem.py recall "关键词"
```

### 查看统计
```bash
python3 scripts/mem.py stats
```

### 列出所有记忆
```bash
python3 scripts/mem.py recall "*" --limit 20
```

### 删除记忆
```bash
# 软删除（可恢复）
python3 scripts/mem.py forget <memory_id>

# 硬删除（永久删除）
python3 scripts/mem.py hard-delete <memory_id>
```

---

## 📁 关键文件路径

| 文件/目录 | 路径 | 说明 |
|-----------|------|------|
| 技能目录 | `/root/.openclaw/workspace/skills/agent-memory-ultimate/` | 技能代码 |
| 数据库 | `/root/.openclaw/workspace/db/memory.db` | SQLite 数据库 |
| 同步状态 | `/root/.openclaw/workspace/skills/agent-memory-ultimate/memory-sync-state.json` | 导入状态追踪 |
| 日志文件 | `/root/.openclaw/workspace/logs/memory-sync.log` | 同步日志 |
| 记忆文件 | `/root/.openclaw/workspace/memory/YYYY-MM-DD.md` | 原始记忆文件 |

---

## ⚠️ 常见问题

### Q1: 导入时网络错误
```
'[Errno 101] Network is unreachable' thrown while requesting HEAD https://huggingface.co/...
```

**解决方案：** 配置代理
```bash
export HTTP_PROXY=http://127.0.0.1:7892
export HTTPS_PROXY=http://127.0.0.1:7892
```

---

### Q2: 缺少 numpy 模块
```
ModuleNotFoundError: No module named 'numpy'
```

**解决方案：** 重新安装依赖
```bash
pip3 install numpy sentence-transformers onnxruntime
```

---

### Q3: 记忆重复
**原因：** 状态文件丢失或新建，无法追踪历史导入

**解决方案：**
1. 手动清理重复（可选）
2. 确保 `memory-sync-state.json` 文件存在且正确

---

### Q4: 搜索结果为空
**可能原因：**
- 数据库为空
- 查询关键词不匹配

**解决方案：**
```bash
# 检查数据库统计
python3 scripts/mem.py stats

# 尝试不同关键词
python3 scripts/mem.py recall "*" --limit 5
```

---

## 🔒 安全注意事项

1. **数据库安全**
   - 数据库文件包含所有记忆内容
   - 建议设置文件权限：`chmod 600 /root/.openclaw/workspace/db/memory.db`

2. **敏感信息**
   - 避免存储密码、API Key 等敏感信息
   - 敏感信息应存放在 `.env` 文件

3. **备份**
   - 定期备份数据库文件
   - 建议：每天备份到云存储

---

## 📈 性能优化建议

1. **首次运行较慢**
   - 首次查询需要加载嵌入模型（约 10 秒）
   - 后续查询会快很多（<1 秒）

2. **数据库大小**
   - 每条记忆约 20-40 KB
   - 1000 条记忆约 20-40 MB
   - 建议定期清理过期记忆

3. **内存使用**
   - 嵌入模型约占用 500MB 内存
   - 建议在 2GB+ 内存的服务器上运行

---

## 📚 相关资源

- **技能文档：** `/root/.openclaw/workspace/skills/agent-memory-ultimate/SKILL.md`
- **GitHub 项目：** https://github.com/globalcaos/clawdbot-moltbot-openclaw
- **研究论文：**
  - [HIPPOCAMPUS](https://github.com/globalcaos/clawdbot-moltbot-openclaw/blob/main/docs/papers/hippocampus.md)
  - [ENGRAM](https://github.com/globalcaos/clawdbot-moltbot-openclaw/blob/main/docs/papers/context-compaction.md)

---

## 📞 获取帮助

如有问题，请联系：
- 甲维斯：jiaweisibot@163.com
- 文档：`/root/.openclaw/workspace/docs/memory-setup-complete.md`

---

_最后更新：2026-03-04 10:30 UTC+8_

---

## 附录 A：同步脚本完整内容

```bash
#!/bin/bash
# sync-memories.sh - 智能同步记忆文件到向量数据库

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
MEMORY_DIR="/root/.openclaw/workspace/memory"
STATE_FILE="$SCRIPT_DIR/../memory-sync-state.json"

echo "🧠 记忆同步检查..."
echo ""

# 设置代理
export HTTP_PROXY=http://127.0.0.1:7892
export HTTPS_PROXY=http://127.0.0.1:7892

# 初始化状态文件
if [ ! -f "$STATE_FILE" ]; then
    echo '{"imported_files":{}}' > "$STATE_FILE"
fi

imported=0
skipped=0
updated=0
errors=0

# 遍历所有每日记忆文件
for file in "$MEMORY_DIR"/20*.md; do
    if [ ! -f "$file" ]; then
        continue
    fi
    
    filename=$(basename "$file")
    
    # 跳过非每日记忆文件
    if [[ ! "$filename" =~ ^20[0-9]{2}-[0-9]{2}-[0-9]{2}\.md$ ]]; then
        continue
    fi
    
    # 检查文件大小
    filesize=$(wc -c < "$file")
    if [ "$filesize" -lt 100 ]; then
        ((skipped++))
        continue
    fi
    
    # 计算文件哈希（用于检测变更）
    file_hash=$(md5sum "$file" | cut -d' ' -f1)
    
    # 检查是否已导入
    stored_hash=$(cat "$STATE_FILE" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('imported_files',{}).get('$filename',''))" 2>/dev/null)
    
    if [ "$file_hash" = "$stored_hash" ]; then
        echo "⊘ $filename - 已导入且无变更，跳过"
        ((skipped++))
        continue
    fi
    
    # 计算重要性（越近越重要）
    date_str="${filename%.md}"
    days_ago=$(( ( $(date +%s) - $(date -d "$date_str" +%s 2>/dev/null || echo 0) ) / 86400 ))
    if [ $days_ago -lt 0 ]; then
        days_ago=0
    fi
    importance=$(echo "scale=2; i=1.0-($days_ago*0.1); if(i<0.3) i=0.3; i" | bc 2>/dev/null || echo "0.5")
    
    # 导入文件
    if [ "$stored_hash" ]; then
        echo "🔄 $filename - 检测到变更，重新导入..."
        ((updated++))
    else
        echo "📄 $filename - 新文件，导入中..."
        ((imported++))
    fi
    
    content=$(cat "$file")
    result=$(python3 "$SCRIPT_DIR/mem.py" store "$content" \
        --type semantic \
        --source "memory_file:$filename" \
        --importance "$importance" 2>&1)
    
    if echo "$result" | grep -q "✓ Stored"; then
        echo "   ✅ 成功 (重要性：$importance)"
        
        # 更新状态文件
        python3 -c "
import json
with open('$STATE_FILE', 'r') as f:
    state = json.load(f)
if 'imported_files' not in state:
    state['imported_files'] = {}
state['imported_files']['$filename'] = '$file_hash'
state['last_sync'] = '$(date -Iseconds)'
with open('$STATE_FILE', 'w') as f:
    json.dump(state, f, indent=2)
"
    else
        echo "   ❌ 失败"
        ((errors++))
    fi
    
    echo ""
done

echo "============================================================"
echo "📊 同步完成:"
echo "   🆕 新导入：$imported"
echo "   🔄 已更新：$updated"
echo "   ⊘ 已跳过：$skipped"
echo "   ❌ 错误：$errors"
echo "============================================================"
```

---

**📧 发送时间：** 2026-03-04 10:25 UTC+8  
**📤 发送者：** 甲维斯 (jiaweisibot@163.com)  
**📥 收件人：** 乙维斯 (yiweisibot@163.com)
