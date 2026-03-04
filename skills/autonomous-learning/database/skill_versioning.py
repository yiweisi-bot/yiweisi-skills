#!/usr/bin/env python3
"""
自主学习系统 - 技能去重与版本管理
"""

import os
import re
from typing import Dict, List, Optional, Tuple
from difflib import SequenceMatcher
from datetime import datetime

# 添加父目录到路径
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db import get_db


class SkillVersionManager:
    """技能版本管理器"""
    
    def __init__(self):
        self.db = get_db()
    
    def check_duplicate(self, title: str, 
                       description: Optional[str] = None) -> Tuple[bool, List[Dict]]:
        """
        检查是否已存在相似技能
        
        返回: (是否有重复, 相似技能列表)
        """
        # 获取所有最新技能
        all_skills = self.db.list_skills(is_latest=True)
        
        similar_skills = []
        
        for skill in all_skills:
            # 标题相似度
            title_sim = self._calculate_similarity(title, skill['title'])
            
            # 如果标题相似度高，加入列表
            if title_sim > 0.7:
                similar_skills.append({
                    'skill': skill,
                    'similarity': title_sim,
                    'match_type': 'title'
                })
            # 如果标题包含相同关键词
            elif self._has_common_keywords(title, skill['title']):
                similar_skills.append({
                    'skill': skill,
                    'similarity': 0.5,
                    'match_type': 'keywords'
                })
        
        # 按相似度排序
        similar_skills.sort(key=lambda x: x['similarity'], reverse=True)
        
        return len(similar_skills) > 0, similar_skills
    
    def _calculate_similarity(self, str1: str, str2: str) -> float:
        """计算两个字符串的相似度"""
        return SequenceMatcher(None, str1.lower(), str2.lower()).ratio()
    
    def _has_common_keywords(self, title1: str, title2: str) -> bool:
        """检查是否有共同关键词"""
        # 技术关键词
        tech_keywords = [
            'React', 'Vue', 'TypeScript', 'JavaScript', 'Python',
            'Docker', 'Kubernetes', 'Git', 'Tailwind', 'CSS',
            'Server Components', 'Async', 'API', 'REST', 'GraphQL'
        ]
        
        title1_lower = title1.lower()
        title2_lower = title2.lower()
        
        for keyword in tech_keywords:
            keyword_lower = keyword.lower()
            if keyword_lower in title1_lower and keyword_lower in title2_lower:
                return True
        
        return False
    
    def create_new_version(self, existing_skill_id: int, 
                         new_file_path: str,
                         change_description: str) -> int:
        """
        创建新版本
        
        返回: 新技能ID
        """
        # 获取旧技能信息
        old_skill = self.db.get_skill(existing_skill_id)
        if not old_skill:
            raise ValueError(f"技能不存在: {existing_skill_id}")
        
        # 将旧版本标记为非最新
        self._update_is_latest(existing_skill_id, False)
        
        # 获取文件信息
        import os
        file_size = os.path.getsize(new_file_path) if os.path.exists(new_file_path) else 0
        
        # 创建新版本
        new_skill_id = self.db.create_skill(
            goal_id=old_skill['goal_id'],
            task_id=old_skill.get('task_id'),
            title=old_skill['title'],
            file_path=new_file_path,
            tokens_used=old_skill.get('tokens_used', 0)
        )
        
        # 更新新版本的版本号
        conn = self.db._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE generated_skills 
                SET version = ?, parent_skill_id = ?
                WHERE id = ?
            ''', (old_skill.get('version', 1) + 1, existing_skill_id, new_skill_id))
            conn.commit()
        finally:
            conn.close()
        
        return new_skill_id
    
    def _update_is_latest(self, skill_id: int, is_latest: bool):
        """更新 is_latest 标志"""
        conn = self.db._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE generated_skills 
                SET is_latest = ?
                WHERE id = ?
            ''', (1 if is_latest else 0, skill_id))
            conn.commit()
        finally:
            conn.close()
    
    def get_version_history(self, skill_id: int) -> List[Dict]:
        """获取技能的版本历史"""
        skill = self.db.get_skill(skill_id)
        if not skill:
            return []
        
        # 查找所有相关版本
        conn = self.db._get_connection()
        try:
            cursor = conn.cursor()
            
            # 查找根技能
            root_id = skill_id
            current = skill
            while current.get('parent_skill_id'):
                root_id = current['parent_skill_id']
                current = self.db.get_skill(root_id)
                if not current:
                    break
            
            # 获取所有版本
            cursor.execute('''
                SELECT * FROM generated_skills 
                WHERE id = ? OR parent_skill_id = ? OR 
                      (parent_skill_id IN (SELECT id FROM generated_skills WHERE parent_skill_id = ?))
                ORDER BY version ASC
            ''', (root_id, root_id, root_id))
            
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        finally:
            conn.close()
    
    def get_user_choice(self, similar_skills: List[Dict]) -> str:
        """
        获取用户选择（交互式）
        
        返回: 'overwrite', 'new', 'merge', 'cancel'
        """
        print("\n⚠️  检测到已存在相似技能：\n")
        
        for i, item in enumerate(similar_skills[:5], 1):
            skill = item['skill']
            sim = item['similarity']
            match_type = item['match_type']
            
            print(f"  {i}. 📄 {skill['title']}")
            print(f"     相似度: {int(sim * 100)}% ({match_type})")
            print(f"     版本: v{skill.get('version', 1)}")
            print(f"     创建: {skill['created_at']}")
            print()
        
        print("请选择:")
        print("  A. 覆盖（创建新版本）")
        print("  B. 新建独立技能")
        print("  C. 合并（扩展现有技能）")
        print("  D. 取消")
        
        choice = input("\n你的选择 (A/B/C/D): ").strip().upper()
        
        choice_map = {
            'A': 'overwrite',
            'B': 'new',
            'C': 'merge',
            'D': 'cancel'
        }
        
        return choice_map.get(choice, 'cancel')


def get_version_manager() -> SkillVersionManager:
    """获取版本管理器实例"""
    return SkillVersionManager()


if __name__ == '__main__':
    # 测试
    print("🧪 技能版本管理测试\n")
    
    manager = get_version_manager()
    
    # 测试检查重复
    test_title = "React 19 Server Components 指南"
    has_dup, similar = manager.check_duplicate(test_title)
    
    print(f"🔍 检查: {test_title}")
    print(f"   有重复: {has_dup}")
    print(f"   相似技能数: {len(similar)}")
    
    for item in similar[:3]:
        skill = item['skill']
        print(f"   - {skill['title']} (相似度: {int(item['similarity'] * 100)}%)")
    
    print()
    print("✅ 测试完成！")
