#!/usr/bin/env python3
"""
自主学习系统 - 优先级计算模块
"""

import re
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta


class PriorityCalculator:
    """优先级计算器"""
    
    # 时效性关键词（新技术）
    RECENT_KEYWORDS = [
        'React 19', 'React 18', 'Vue 4', 'Vue 3.4',
        'Tailwind CSS v4', 'Tailwind v4',
        'Next.js 15', 'Next.js 14',
        'Vite 6', 'Vite 5',
        'TypeScript 5.5', 'TypeScript 5.4',
        'Python 3.13', 'Python 3.12',
        'Rust 1.80', 'Rust 1.79',
        'Node.js 22', 'Node.js 21',
        'Server Components', 'RSC',
        'Suspense', 'Streaming SSR',
    ]
    
    # 成熟技术关键词
    MATURE_KEYWORDS = [
        'Python', 'JavaScript', 'Java', 'C++', 'Go', 'Rust',
        'Docker', 'Kubernetes', 'Linux', 'Git',
        'MySQL', 'PostgreSQL', 'MongoDB', 'Redis',
        'REST API', 'GraphQL',
    ]
    
    # 用户偏好关键词
    URGENCY_KEYWORDS = ['急用', '紧急', '马上', '现在', '尽快', '急需']
    CASUAL_KEYWORDS = ['了解一下', '看看', '随便', '有空']
    
    def __init__(self):
        self.base_score = 50
    
    def calculate_priority(self, title: str, description: Optional[str] = None,
                          existing_skills: Optional[List[str]] = None,
                          is_dependency: bool = False,
                          depends_on_others: bool = False) -> Tuple[int, str]:
        """
        计算优先级分数
        
        返回: (分数, 优先级等级: 1=低, 2=中, 3=高)
        """
        score = self.base_score
        details = []
        
        # 1. 时效性加成
        recency_score, recency_detail = self._calculate_recency(title, description)
        score += recency_score
        details.append(recency_detail)
        
        # 2. 技能缺口加成
        skill_gap_score, skill_gap_detail = self._calculate_skill_gap(
            title, existing_skills
        )
        score += skill_gap_score
        details.append(skill_gap_detail)
        
        # 3. 用户偏好加成
        preference_score, preference_detail = self._calculate_preference(
            title, description
        )
        score += preference_score
        details.append(preference_detail)
        
        # 4. 依赖关系加成
        dependency_score, dependency_detail = self._calculate_dependency(
            is_dependency, depends_on_others
        )
        score += dependency_score
        details.append(dependency_detail)
        
        # 确保分数在合理范围内
        score = max(0, min(100, score))
        
        # 确定优先级等级
        if score >= 71:
            level = 3
        elif score >= 41:
            level = 2
        else:
            level = 1
        
        detail_text = f"总分: {score} | " + " | ".join(details)
        
        return score, level, detail_text
    
    def _calculate_recency(self, title: str, description: Optional[str] = None) -> Tuple[int, str]:
        """计算时效性加成"""
        text = f"{title} {description or ''}".lower()
        
        # 检查是否是新技术
        for keyword in self.RECENT_KEYWORDS:
            if keyword.lower() in text:
                return 20, f"时效性(新技术<6个月): +20"
        
        # 检查是否是成熟技术
        for keyword in self.MATURE_KEYWORDS:
            if keyword.lower() in text:
                return 0, f"时效性(成熟技术): +0"
        
        # 默认中等时效性
        return 10, f"时效性(较新技术<1年): +10"
    
    def _calculate_skill_gap(self, title: str, 
                             existing_skills: Optional[List[str]] = None) -> Tuple[int, str]:
        """计算技能缺口加成"""
        if not existing_skills:
            return 15, "技能缺口(无相关技能): +15"
        
        title_lower = title.lower()
        
        # 检查是否已有相关技能
        has_related = False
        has_outdated = False
        
        for skill in existing_skills:
            skill_lower = skill.lower()
            
            # 简单的关键词匹配
            if any(keyword in skill_lower and keyword in title_lower 
                  for keyword in ['react', 'vue', 'python', 'docker', 'tailwind']):
                has_related = True
                
                # 检查版本是否过时
                if self._is_outdated(skill, title):
                    has_outdated = True
        
        if has_outdated:
            return 10, "技能缺口(版本过时): +10"
        elif has_related:
            return -10, "技能缺口(已有技能): -10"
        else:
            return 15, "技能缺口(无相关技能): +15"
    
    def _is_outdated(self, skill_name: str, target_title: str) -> bool:
        """检查技能是否过时"""
        # 简单的版本比较逻辑
        # 实际项目中可以更复杂
        return False
    
    def _calculate_preference(self, title: str, description: Optional[str] = None) -> Tuple[int, str]:
        """计算用户偏好加成"""
        text = f"{title} {description or ''}".lower()
        
        # 检查是否紧急
        for keyword in self.URGENCY_KEYWORDS:
            if keyword in text:
                return 20, f"用户偏好(急用): +20"
        
        # 检查是否随便看看
        for keyword in self.CASUAL_KEYWORDS:
            if keyword in text:
                return -10, f"用户偏好(随便看看): -10"
        
        return 0, "用户偏好(正常): +0"
    
    def _calculate_dependency(self, is_dependency: bool, 
                              depends_on_others: bool) -> Tuple[int, str]:
        """计算依赖关系加成"""
        if is_dependency:
            return 15, "依赖关系(是其他目标的依赖): +15"
        elif depends_on_others:
            return -10, "依赖关系(依赖其他目标): -10"
        else:
            return 0, "依赖关系(无): +0"


def calculate_goal_priority(title: str, description: Optional[str] = None,
                            existing_skills: Optional[List[str]] = None) -> dict:
    """
    便捷函数：计算学习目标优先级
    
    返回: {
        'score': 分数,
        'level': 优先级等级 (1-3),
        'details': 详细说明
    }
    """
    calculator = PriorityCalculator()
    score, level, details = calculator.calculate_priority(
        title, description, existing_skills
    )
    
    return {
        'score': score,
        'level': level,
        'details': details
    }


if __name__ == '__main__':
    # 测试
    test_cases = [
        "学习 React 19 Server Components",
        "学习 Python 异步编程",
        "学习 Docker 容器化（急用）",
        "了解一下 Tailwind CSS v4",
    ]
    
    print("🧪 优先级计算测试\n")
    
    for i, title in enumerate(test_cases, 1):
        result = calculate_goal_priority(title)
        level_emoji = {1: '🟢', 2: '🟡', 3: '🔴'}[result['level']]
        print(f"测试 {i}: {title}")
        print(f"  分数: {result['score']} {level_emoji}")
        print(f"  等级: {result['level']}")
        print(f"  说明: {result['details']}")
        print()
