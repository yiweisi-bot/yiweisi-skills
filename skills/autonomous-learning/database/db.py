#!/usr/bin/env python3
"""
自主学习系统 - 数据库操作类
"""

import sqlite3
import json
import os
from typing import Optional, List, Dict, Any
from datetime import datetime


class LearningDatabase:
    """学习数据库操作类"""
    
    def __init__(self, db_path: Optional[str] = None):
        """初始化数据库连接"""
        if db_path is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            db_path = os.path.join(base_dir, 'data', 'learning.db')
        
        self.db_path = db_path
        self._ensure_data_dir()
        self._init_database()
    
    def _ensure_data_dir(self):
        """确保数据目录存在"""
        data_dir = os.path.dirname(self.db_path)
        os.makedirs(data_dir, exist_ok=True)
    
    def _init_database(self):
        """初始化数据库表结构"""
        schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
        
        if os.path.exists(schema_path):
            with open(schema_path, 'r', encoding='utf-8') as f:
                schema = f.read()
            
            with self._get_connection() as conn:
                conn.executescript(schema)
    
    def _get_connection(self):
        """获取数据库连接"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def _to_dict(self, row: sqlite3.Row) -> Dict[str, Any]:
        """将Row转换为字典"""
        return dict(row)
    
    def _to_list(self, rows: List[sqlite3.Row]) -> List[Dict[str, Any]]:
        """将Row列表转换为字典列表"""
        return [self._to_dict(row) for row in rows]
    
    # ============================================
    # 学习目标操作
    # ============================================
    
    def create_goal(self, title: str, description: Optional[str] = None,
                   priority: int = 2, source: Optional[str] = None,
                   estimated_hours: Optional[float] = None,
                   parent_id: Optional[int] = None,
                   metadata: Optional[Dict] = None) -> int:
        """创建学习目标"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO learning_goals 
                (title, description, priority, source, estimated_hours, parent_id, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (title, description, priority, source, estimated_hours, 
                  parent_id, json.dumps(metadata) if metadata else None))
            return cursor.lastrowid
    
    def get_goal(self, goal_id: int) -> Optional[Dict[str, Any]]:
        """获取单个学习目标"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM learning_goals WHERE id = ?', (goal_id,))
            row = cursor.fetchone()
            return self._to_dict(row) if row else None
    
    def list_goals(self, status: Optional[str] = None, 
                   limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """列出学习目标"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            if status:
                cursor.execute('''
                    SELECT * FROM learning_goals 
                    WHERE status = ? 
                    ORDER BY priority DESC, created_at DESC
                ''', (status,))
            else:
                cursor.execute('''
                    SELECT * FROM learning_goals 
                    ORDER BY priority DESC, created_at DESC
                ''')
            
            if limit:
                rows = cursor.fetchmany(limit)
            else:
                rows = cursor.fetchall()
            
            return self._to_list(rows)
    
    def update_goal_status(self, goal_id: int, status: str) -> bool:
        """更新学习目标状态"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            update_data = {'status': status}
            if status == 'in_progress':
                update_data['started_at'] = datetime.now().isoformat()
            elif status == 'completed':
                update_data['completed_at'] = datetime.now().isoformat()
            
            set_clause = ', '.join([f'{k} = ?' for k in update_data.keys()])
            values = list(update_data.values()) + [goal_id]
            
            cursor.execute(f'''
                UPDATE learning_goals 
                SET {set_clause}
                WHERE id = ?
            ''', values)
            
            return cursor.rowcount > 0
    
    # ============================================
    # 学习任务操作
    # ============================================
    
    def create_task(self, goal_id: int, title: str, task_type: str,
                   description: Optional[str] = None, priority: int = 2,
                   estimated_minutes: Optional[int] = None,
                   metadata: Optional[Dict] = None) -> int:
        """创建学习任务"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO learning_tasks 
                (goal_id, title, description, task_type, priority, estimated_minutes, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (goal_id, title, description, task_type, priority, 
                  estimated_minutes, json.dumps(metadata) if metadata else None))
            return cursor.lastrowid
    
    def get_task(self, task_id: int) -> Optional[Dict[str, Any]]:
        """获取单个学习任务"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM learning_tasks WHERE id = ?', (task_id,))
            row = cursor.fetchone()
            return self._to_dict(row) if row else None
    
    def list_tasks(self, goal_id: Optional[int] = None,
                   status: Optional[str] = None) -> List[Dict[str, Any]]:
        """列出学习任务"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            if goal_id and status:
                cursor.execute('''
                    SELECT * FROM learning_tasks 
                    WHERE goal_id = ? AND status = ?
                    ORDER BY priority DESC, created_at ASC
                ''', (goal_id, status))
            elif goal_id:
                cursor.execute('''
                    SELECT * FROM learning_tasks 
                    WHERE goal_id = ?
                    ORDER BY priority DESC, created_at ASC
                ''', (goal_id,))
            else:
                cursor.execute('''
                    SELECT * FROM learning_tasks 
                    ORDER BY created_at DESC
                ''')
            
            rows = cursor.fetchall()
            return self._to_list(rows)
    
    def update_task_status(self, task_id: int, status: str,
                          tokens_used: Optional[int] = None,
                          result_summary: Optional[str] = None,
                          error_message: Optional[str] = None) -> bool:
        """更新学习任务状态"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            update_data = {'status': status}
            if status == 'in_progress':
                update_data['started_at'] = datetime.now().isoformat()
            elif status == 'completed':
                update_data['completed_at'] = datetime.now().isoformat()
            elif status == 'failed':
                update_data['retry_count'] = 1  # 简化处理
            
            if tokens_used is not None:
                update_data['tokens_used'] = tokens_used
            if result_summary:
                update_data['result_summary'] = result_summary
            if error_message:
                update_data['error_message'] = error_message
            
            set_clause = ', '.join([f'{k} = ?' for k in update_data.keys()])
            values = list(update_data.values()) + [task_id]
            
            cursor.execute(f'''
                UPDATE learning_tasks 
                SET {set_clause}
                WHERE id = ?
            ''', values)
            
            return cursor.rowcount > 0
    
    # ============================================
    # 学习会话操作
    # ============================================
    
    def create_session(self, goal_id: int, session_type: str,
                      tokens_budget: Optional[int] = None,
                      time_budget_minutes: Optional[int] = None,
                      metadata: Optional[Dict] = None) -> int:
        """创建学习会话"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO learning_sessions 
                (goal_id, session_type, tokens_budget, time_budget_minutes, metadata)
                VALUES (?, ?, ?, ?, ?)
            ''', (goal_id, session_type, tokens_budget, 
                  time_budget_minutes, json.dumps(metadata) if metadata else None))
            return cursor.lastrowid
    
    def get_active_session(self, goal_id: int) -> Optional[Dict[str, Any]]:
        """获取目标的活跃会话"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM learning_sessions 
                WHERE goal_id = ? AND status = 'active'
                ORDER BY started_at DESC 
                LIMIT 1
            ''', (goal_id,))
            row = cursor.fetchone()
            return self._to_dict(row) if row else None
    
    def update_session(self, session_id: int, status: Optional[str] = None,
                      tokens_used: Optional[int] = None,
                      summary: Optional[str] = None,
                      checkpoints: Optional[Dict] = None) -> bool:
        """更新学习会话"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            update_data = {}
            if status:
                update_data['status'] = status
                if status != 'active':
                    update_data['ended_at'] = datetime.now().isoformat()
            if tokens_used is not None:
                update_data['tokens_used'] = tokens_used
            if summary:
                update_data['summary'] = summary
            if checkpoints:
                update_data['checkpoints'] = json.dumps(checkpoints)
            
            if not update_data:
                return False
            
            set_clause = ', '.join([f'{k} = ?' for k in update_data.keys()])
            values = list(update_data.values()) + [session_id]
            
            cursor.execute(f'''
                UPDATE learning_sessions 
                SET {set_clause}
                WHERE id = ?
            ''', values)
            
            return cursor.rowcount > 0
    
    # ============================================
    # 生成技能操作
    # ============================================
    
    def create_skill(self, goal_id: int, title: str, file_path: str,
                    task_id: Optional[int] = None,
                    tokens_used: Optional[int] = None,
                    metadata: Optional[Dict] = None) -> int:
        """创建生成的技能记录"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # 获取文件信息
            file_size = os.path.getsize(file_path) if os.path.exists(file_path) else 0
            
            cursor.execute('''
                INSERT INTO generated_skills 
                (goal_id, task_id, title, file_path, tokens_used, file_size_bytes, validation_status)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (goal_id, task_id, title, file_path, tokens_used, 
                  file_size, 'pending'))
            return cursor.lastrowid
    
    def get_skill(self, skill_id: int) -> Optional[Dict[str, Any]]:
        """获取单个技能"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM generated_skills WHERE id = ?', (skill_id,))
            row = cursor.fetchone()
            return self._to_dict(row) if row else None
    
    def list_skills(self, goal_id: Optional[int] = None,
                   validation_status: Optional[str] = None,
                   is_latest: bool = True) -> List[Dict[str, Any]]:
        """列出生成的技能"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            conditions = []
            params = []
            
            if goal_id:
                conditions.append('goal_id = ?')
                params.append(goal_id)
            if validation_status:
                conditions.append('validation_status = ?')
                params.append(validation_status)
            if is_latest:
                conditions.append('is_latest = 1')
            
            where_clause = ' AND '.join(conditions) if conditions else '1=1'
            
            cursor.execute(f'''
                SELECT * FROM generated_skills 
                WHERE {where_clause}
                ORDER BY created_at DESC
            ''', params)
            
            rows = cursor.fetchall()
            return self._to_list(rows)
    
    def update_skill_validation(self, skill_id: int, validation_status: str,
                               quality_score: Optional[int] = None,
                               feedback: Optional[str] = None,
                               validated_by: Optional[str] = None) -> bool:
        """更新技能验证状态"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            update_data = {
                'validation_status': validation_status,
                'validated_at': datetime.now().isoformat()
            }
            if quality_score is not None:
                update_data['quality_score'] = quality_score
            if feedback:
                update_data['feedback'] = feedback
            if validated_by:
                update_data['validated_by'] = validated_by
            
            set_clause = ', '.join([f'{k} = ?' for k in update_data.keys()])
            values = list(update_data.values()) + [skill_id]
            
            cursor.execute(f'''
                UPDATE generated_skills 
                SET {set_clause}
                WHERE id = ?
            ''', values)
            
            return cursor.rowcount > 0
    
    # ============================================
    # 待学习列表操作
    # ============================================
    
    def add_to_backlog(self, title: str, reason: str,
                      description: Optional[str] = None,
                      source_goal_id: Optional[int] = None,
                      source_session_id: Optional[int] = None,
                      priority: int = 2,
                      saved_progress: Optional[Dict] = None,
                      tokens_already_used: int = 0,
                      time_already_spent_minutes: int = 0) -> int:
        """添加到待学习列表"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO learning_backlog 
                (title, description, reason, source_goal_id, source_session_id, 
                 priority, saved_progress, tokens_already_used, time_already_spent_minutes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (title, description, reason, source_goal_id, source_session_id,
                  priority, json.dumps(saved_progress) if saved_progress else None,
                  tokens_already_used, time_already_spent_minutes))
            return cursor.lastrowid
    
    def list_backlog(self, priority: Optional[int] = None,
                    limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """列出待学习列表"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            if priority:
                cursor.execute('''
                    SELECT * FROM learning_backlog 
                    WHERE priority = ?
                    ORDER BY priority DESC, created_at DESC
                ''', (priority,))
            else:
                cursor.execute('''
                    SELECT * FROM learning_backlog 
                    ORDER BY priority DESC, created_at DESC
                ''')
            
            if limit:
                rows = cursor.fetchmany(limit)
            else:
                rows = cursor.fetchall()
            
            return self._to_list(rows)
    
    def remove_from_backlog(self, backlog_id: int) -> bool:
        """从待学习列表移除"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM learning_backlog WHERE id = ?', (backlog_id,))
            return cursor.rowcount > 0


# 便捷函数
def get_db() -> LearningDatabase:
    """获取数据库实例"""
    return LearningDatabase()


if __name__ == '__main__':
    # 简单测试
    db = get_db()
    print('数据库初始化完成:', db.db_path)
