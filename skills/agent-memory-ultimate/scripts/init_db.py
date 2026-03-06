
#!/usr/bin/env python3
"""
Initialize the memory database
"""
import sqlite3
import os
import sys

# Get the database path directly
DB_PATH = '/root/.openclaw/workspace/db/memory.db'

# Ensure db directory exists
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

print(f"📦 Initializing database at: {DB_PATH}")

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Create memories table
cursor.execute('''
CREATE TABLE IF NOT EXISTS memories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL,
    memory_type TEXT DEFAULT 'semantic',
    source TEXT DEFAULT 'manual',
    importance REAL DEFAULT 0.5,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted INTEGER DEFAULT 0
)
''')

# Create full-text search virtual table
cursor.execute('''
CREATE VIRTUAL TABLE IF NOT EXISTS memories_fts USING fts5(
    content,
    content=memories,
    content_rowid=id
)
''')

# Create indexes
cursor.execute('''
CREATE INDEX IF NOT EXISTS idx_memories_type ON memories(memory_type)
''')
cursor.execute('''
CREATE INDEX IF NOT EXISTS idx_memories_importance ON memories(importance)
''')
cursor.execute('''
CREATE INDEX IF NOT EXISTS idx_memories_created ON memories(created_at)
''')

# Create triggers for FTS sync
cursor.execute('''
CREATE TRIGGER IF NOT EXISTS memories_ai AFTER INSERT ON memories BEGIN
    INSERT INTO memories_fts(rowid, content) VALUES (new.id, new.content);
END;
''')
cursor.execute('''
CREATE TRIGGER IF NOT EXISTS memories_ad AFTER DELETE ON memories BEGIN
    INSERT INTO memories_fts(memories_fts, rowid, content) VALUES('delete', old.id, old.content);
END;
''')
cursor.execute('''
CREATE TRIGGER IF NOT EXISTS memories_au AFTER UPDATE ON memories BEGIN
    INSERT INTO memories_fts(memories_fts, rowid, content) VALUES('delete', old.id, old.content);
    INSERT INTO memories_fts(rowid, content) VALUES (new.id, new.content);
END;
''')

conn.commit()
conn.close()

print("✅ Database initialized successfully!")
print(f"📊 Database location: {DB_PATH}")

