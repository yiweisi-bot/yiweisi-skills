
#!/bin/bash
# Batch import memory files

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
MEMORY_DIR="/root/.openclaw/workspace/memory"

echo "📚 开始批量导入记忆文件..."
echo ""

cd "$SCRIPT_DIR"

imported=0
errors=0

for file in "$MEMORY_DIR"/20*.md; do
    if [ ! -f "$file" ]; then
        continue
    fi
    
    filename=$(basename "$file")
    
    # Skip non-daily memory files
    if [[ ! "$filename" =~ ^20[0-9]{2}-[0-9]{2}-[0-9]{2}\.md$ ]]; then
        continue
    fi
    
    # Check file size
    filesize=$(wc -c < "$file")
    if [ "$filesize" -lt 100 ]; then
        continue
    fi
    
    # Calculate importance (more recent = more important)
    date_str="${filename%.md}"
    days_ago=$(( ( $(date +%s) - $(date -d "$date_str" +%s 2>/dev/null || echo 0) ) / 86400 ))
    if [ $days_ago -lt 0 ]; then
        days_ago=0
    fi
    
    # Calculate importance: 1.0 - (days_ago * 0.1), minimum 0.3
    importance=$(awk -v days="$days_ago" 'BEGIN { imp=1.0-(days*0.1); if(imp<0.3) imp=0.3; printf "%.2f", imp }')
    
    echo "📄 导入 $filename (重要性：$importance)..."
    
    # Read file content (limit to 10000 chars to avoid too long entries)
    content=$(head -c 10000 "$file")
    
    # Store the memory
    result=$(python3 "$SCRIPT_DIR/mem.py" store "$content" \
        --type semantic \
        --source "memory_file:$filename" \
        --importance "$importance" 2>&1)
    
    if echo "$result" | grep -q "✓ Stored"; then
        echo "   ✅ 成功"
        ((imported++))
    else
        echo "   ❌ 失败"
        ((errors++))
    fi
    
    echo ""
done

echo "============================================================"
echo "📊 导入完成：成功 $imported, 错误 $errors"
echo "============================================================"

