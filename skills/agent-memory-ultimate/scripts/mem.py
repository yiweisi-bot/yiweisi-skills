
#!/usr/bin/env python3
"""
Simple memory management tool
"""
import sqlite3
import os
import sys
import argparse
from datetime import datetime

# Get the database path directly
DB_PATH = '/root/.openclaw/workspace/db/memory.db'

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def store_memory(content, memory_type='semantic', source='manual', importance=0.5):
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO memories (content, memory_type, source, importance)
    VALUES (?, ?, ?, ?)
    ''', (content, memory_type, source, importance))
    
    memory_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    print("✓ Stored memory #{} (semantic, importance={})".format(memory_id, importance))
    return memory_id

def recall_memories(query, limit=10):
    conn = get_connection()
    cursor = conn.cursor()
    
    if query == "*":
        cursor.execute('''
        SELECT id, content, memory_type, source, importance, created_at
        FROM memories
        WHERE deleted = 0
        ORDER BY importance DESC, created_at DESC
        LIMIT ?
        ''', (limit,))
    else:
        cursor.execute('''
        SELECT m.id, m.content, m.memory_type, m.source, m.importance, m.created_at
        FROM memories m
        JOIN memories_fts fts ON m.id = fts.rowid
        WHERE memories_fts MATCH ?
        AND m.deleted = 0
        ORDER BY m.importance DESC, m.created_at DESC
        LIMIT ?
        ''', (query, limit))
    
    memories = cursor.fetchall()
    conn.close()
    
    return memories

def show_stats():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(*) as total FROM memories WHERE deleted = 0')
    total = cursor.fetchone()['total']
    
    cursor.execute('SELECT COUNT(*) as with_content FROM memories WHERE deleted = 0')
    with_content = cursor.fetchone()['with_content']
    
    cursor.execute('SELECT COUNT(*) as deleted FROM memories WHERE deleted = 1')
    deleted = cursor.fetchone()['deleted']
    
    conn.close()
    
    print("╔══════════════════════════════════════╗")
    print("║       COGNITIVE MEMORY STATS         ║")
    print("╠══════════════════════════════════════╣")
    print(f"║  Active memories:       {total:<12}║")
    print(f"║  Deleted (soft):        {deleted:<12}║")
    print("╚══════════════════════════════════════╝")

def main():
    parser = argparse.ArgumentParser(description='Memory management tool')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Store command
    store_parser = subparsers.add_parser('store', help='Store a memory')
    store_parser.add_argument('content', help='Memory content')
    store_parser.add_argument('--type', default='semantic', help='Memory type')
    store_parser.add_argument('--source', default='manual', help='Memory source')
    store_parser.add_argument('--importance', type=float, default=0.5, help='Importance (0-1)')
    
    # Recall command
    recall_parser = subparsers.add_parser('recall', help='Recall memories')
    recall_parser.add_argument('query', help='Search query (* for all)')
    recall_parser.add_argument('--limit', type=int, default=10, help='Max results')
    
    # Stats command
    subparsers.add_parser('stats', help='Show statistics')
    
    args = parser.parse_args()
    
    if args.command == 'store':
        store_memory(args.content, args.type, args.source, args.importance)
    elif args.command == 'recall':
        memories = recall_memories(args.query, args.limit)
        print(f"Found {len(memories)} memories:")
        print()
        for mem in memories:
            print(f"#{mem['id']} [{mem['memory_type']}]  importance={mem['importance']}")
            print(f"  {mem['content'][:200]}...")
            print()
    elif args.command == 'stats':
        show_stats()

if __name__ == '__main__':
    main()

