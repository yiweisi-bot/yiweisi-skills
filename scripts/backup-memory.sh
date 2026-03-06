
#!/bin/bash
# backup-memory.sh - 备份记忆数据库

BACKUP_DIR="/root/.openclaw/backups/memory"
DB_PATH="/root/.openclaw/workspace/db/memory.db"

echo "💾 开始备份记忆数据库..."
echo "📅 时间: $(date)"
echo ""

# 创建备份目录
mkdir -p "$BACKUP_DIR"

# 检查数据库文件是否存在
if [ ! -f "$DB_PATH" ]; then
    echo "❌ 错误：数据库文件不存在: $DB_PATH"
    exit 1
fi

# 执行备份
BACKUP_FILE="$BACKUP_DIR/memory-$(date +%Y%m%d_%H%M%S).db"
cp "$DB_PATH" "$BACKUP_FILE"

if [ $? -eq 0 ]; then
    echo "✅ 备份成功：$BACKUP_FILE"
    
    # 显示备份文件大小
    BACKUP_SIZE=$(du -h "$BACKUP_FILE" | cut -f1)
    echo "📊 备份大小：$BACKUP_SIZE"
    
    # 清理7天前的旧备份
    echo ""
    echo "🧹 清理7天前的旧备份..."
    DELETED=$(find "$BACKUP_DIR" -name "memory-*.db" -mtime +7 -delete -print | wc -l)
    if [ "$DELETED" -gt 0 ]; then
        echo "🗑️  已删除 $DELETED 个旧备份"
    else
        echo "✅ 没有需要删除的旧备份"
    fi
    
    # 显示当前备份列表
    echo ""
    echo "📁 当前备份列表："
    ls -lh "$BACKUP_DIR" | tail -10
    
    echo ""
    echo "🎉 备份完成！"
else
    echo "❌ 备份失败！"
    exit 1
fi

