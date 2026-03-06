
#!/usr/bin/env python3
"""
清理重复的记忆数据
"""
import sqlite3
import os

DB_PATH = '/root/.openclaw/workspace/db/memory.db'

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def find_duplicates():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT source, GROUP_CONCAT(id) as ids, COUNT(*) as count
    FROM memories
    WHERE deleted = 0
    GROUP BY source
    HAVING count > 1
    ''')
    
    duplicates = cursor.fetchall()
    conn.close()
    
    return duplicates

def keep_latest_and_delete_others():
    conn = get_connection()
    cursor = conn.cursor()
    
    print("🧹 开始清理重复记忆...")
    print()
    
    # 找出所有重复的source
    cursor.execute('''
    SELECT source
    FROM memories
    WHERE deleted = 0
    GROUP BY source
    HAVING COUNT(*) > 1
    ''')
    
    sources = [row['source'] for row in cursor.fetchall()]
    
    total_deleted = 0
    
    for source in sources:
        print(f"处理来源: {source}")
        
        # 找出该source的所有记忆，按时间倒序
        cursor.execute('''
        SELECT id, created_at
        FROM memories
        WHERE source = ? AND deleted = 0
        ORDER BY created_at DESC
        ''', (source,))
        
        memories = cursor.fetchall()
        
        if len(memories) > 1:
            # 保留第一条（最新的），删除其他的
            latest_id = memories[0]['id']
            to_delete = [m['id'] for m in memories[1:]]
            
            print(f"   保留记忆 #{latest_id} (最新)")
            print(f"   删除记忆: {to_delete}")
            
            for mem_id in to_delete:
                cursor.execute('UPDATE memories SET deleted = 1 WHERE id = ?', (mem_id,))
                total_deleted += 1
            
            print(f"   已删除 {len(to_delete)} 条重复记忆")
        print()
    
    conn.commit()
    conn.close()
    
    print(f"✅ 清理完成！共删除 {total_deleted} 条重复记忆")
    return total_deleted

def show_stats():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(*) as total FROM memories WHERE deleted = 0')
    active = cursor.fetchone()['total']
    
    cursor.execute('SELECT COUNT(*) as deleted FROM memories WHERE deleted = 1')
    deleted = cursor.fetchone()['deleted']
    
    conn.close()
    
    print()
    print("📊 当前状态:")
    print(f"   活跃记忆: {active}")
    print(f"   已删除 (软删除): {deleted}")

if __name__ == '__main__':
    # 先显示重复数据
    duplicates = find_duplicates()
    
    if duplicates:
        print(f"发现 {len(duplicates)} 组重复数据:")
        for dup in duplicates:
            print(f"  {dup['source']}: {dup['ids']} (共 {dup['count']} 条)")
        print()
        
        # 执行清理
        keep_latest_and_delete_others()
    else:
        print("✅ 没有发现重复数据")
    
    # 显示统计
    show_stats()

