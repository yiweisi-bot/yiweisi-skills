
#!/bin/bash
# sync-memories.sh - 智能同步记忆文件到向量数据库

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
MEMORY_DIR="/root/.openclaw/workspace/memory"
STATE_FILE="$SCRIPT_DIR/../memory-sync-state.json"
LOG_DIR="/root/.openclaw/workspace/logs"

echo "🧠 记忆同步检查..."
echo "📅 时间: $(date)"
echo ""

# 确保日志目录存在
mkdir -p "$LOG_DIR"

# 设置代理（如果需要）
export HTTP_PROXY=http://127.0.0.1:7892
export HTTPS_PROXY=http://127.0.0.1:7892

# 初始化状态文件
if [ ! -f "$STATE_FILE" ]; then
    echo '{"imported_files":{}, "last_sync":""}' > "$STATE_FILE"
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
    stored_hash=$(cat "$STATE_FILE" 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('imported_files',{}).get('$filename',''))" 2>/dev/null)
    
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
    importance=$(awk -v days="$days_ago" 'BEGIN { imp=1.0-(days*0.1); if(imp<0.3) imp=0.3; printf "%.2f", imp }')
    
    # 导入文件
    if [ "$stored_hash" ]; then
        echo "🔄 $filename - 检测到变更，重新导入..."
        ((updated++))
    else
        echo "📄 $filename - 新文件，导入中..."
        ((imported++))
    fi
    
    # 读取文件内容（限制大小避免过长）
    content=$(head -c 50000 "$file")
    
    # 存储记忆
    result=$(python3 "$SCRIPT_DIR/mem.py" store "$content" \
        --type semantic \
        --source "memory_file:$filename" \
        --importance "$importance" 2>&1)
    
    if echo "$result" | grep -q "✓ Stored"; then
        echo "   ✅ 成功 (重要性：$importance)"
        
        # 更新状态文件
        python3 -c "
import json
import os
state_file = '$STATE_FILE'
if os.path.exists(state_file):
    with open(state_file, 'r') as f:
        state = json.load(f)
else:
    state = {'imported_files': {}, 'last_sync': ''}
if 'imported_files' not in state:
    state['imported_files'] = {}
state['imported_files']['$filename'] = '$file_hash'
state['last_sync'] = '$(date -Iseconds)'
with open(state_file, 'w') as f:
    json.dump(state, f, indent=2, ensure_ascii=False)
" 2>/dev/null
    else
        echo "   ❌ 失败: $result"
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

