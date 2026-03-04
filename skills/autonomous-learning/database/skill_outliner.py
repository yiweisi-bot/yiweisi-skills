#!/usr/bin/env python3
"""
自主学习系统 - 技能大纲设计器
"""

import json
from typing import Dict, List, Optional, Any
from dataclasses import dataclass


@dataclass
class SkillSection:
    """技能章节"""
    title: str
    description: str
    content_type: str = 'text'  # text, code, list, etc.


@dataclass
class SkillOutline:
    """技能大纲"""
    title: str
    description: str
    sections: List[SkillSection]
    estimated_tokens: int = 0


class SkillOutliner:
    """技能大纲设计器"""
    
    # 标准技能章节模板
    STANDARD_SECTIONS = [
        {
            'title': '什么时候使用这个技能',
            'description': '3个典型使用场景',
            'content_type': 'list'
        },
        {
            'title': '快速开始',
            'description': '3个步骤，每个步骤有代码示例',
            'content_type': 'steps_with_code'
        },
        {
            'title': '核心概念',
            'description': '详细讲解核心概念和原理',
            'content_type': 'text'
        },
        {
            'title': '实用示例',
            'description': '2-3个完整的代码示例',
            'content_type': 'code_examples'
        },
        {
            'title': '最佳实践',
            'description': '5条行业最佳实践',
            'content_type': 'list'
        },
        {
            'title': '常见问题',
            'description': '5个常见问题和解答',
            'content_type': 'faq'
        }
    ]
    
    # 不同学习深度的配置
    DEPTH_CONFIGS = {
        'intro': {
            'name': '入门了解',
            'sections_to_include': [0, 1, 2],  # 使用场景、快速开始、核心概念
            'estimated_tokens': 5000,
            'duration_minutes': 60
        },
        'systematic': {
            'name': '系统学习',
            'sections_to_include': [0, 1, 2, 3, 4, 5],  # 全部章节
            'estimated_tokens': 20000,
            'duration_minutes': 120
        },
        'mastery': {
            'name': '深入精通',
            'sections_to_include': [0, 1, 2, 3, 4, 5],  # 全部章节 + 深度内容
            'estimated_tokens': 50000,
            'duration_minutes': 240,
            'extra_sections': [
                {
                    'title': '高级技巧',
                    'description': '5个高级技巧',
                    'content_type': 'list'
                },
                {
                    'title': '实战案例',
                    'description': '1个完整的实战项目',
                    'content_type': 'project'
                }
            ]
        }
    }
    
    def __init__(self):
        pass
    
    def generate_outline(self, topic: str, 
                        collected_data: Optional[Dict] = None,
                        depth: str = 'systematic') -> SkillOutline:
        """
        生成技能大纲
        
        参数:
            topic: 学习主题
            collected_data: 收集到的信息数据
            depth: 学习深度 (intro, systematic, mastery)
        
        返回:
            SkillOutline 对象
        """
        config = self.DEPTH_CONFIGS.get(depth, self.DEPTH_CONFIGS['systematic'])
        
        # 选择章节
        sections = []
        for idx in config['sections_to_include']:
            if idx < len(self.STANDARD_SECTIONS):
                section_data = self.STANDARD_SECTIONS[idx]
                sections.append(SkillSection(
                    title=section_data['title'],
                    description=section_data['description'],
                    content_type=section_data['content_type']
                ))
        
        # 添加精通级别的额外章节
        if depth == 'mastery' and 'extra_sections' in config:
            for section_data in config['extra_sections']:
                sections.append(SkillSection(
                    title=section_data['title'],
                    description=section_data['description'],
                    content_type=section_data['content_type']
                ))
        
        # 生成技能标题
        skill_title = self._generate_skill_title(topic)
        
        # 生成技能描述
        skill_description = self._generate_skill_description(topic, collected_data)
        
        return SkillOutline(
            title=skill_title,
            description=skill_description,
            sections=sections,
            estimated_tokens=config['estimated_tokens']
        )
    
    def _generate_skill_title(self, topic: str) -> str:
        """生成技能标题"""
        # 清理主题
        clean_topic = topic.replace('学习', '').strip()
        
        # 常见主题的标准化标题
        title_map = {
            'react 19': 'React 19 Server Components 指南',
            'react': 'React 开发指南',
            'typescript': 'TypeScript 编程指南',
            'python': 'Python 开发指南',
            'docker': 'Docker 容器化指南',
            'tailwind': 'Tailwind CSS 实用指南',
        }
        
        for keyword, standard_title in title_map.items():
            if keyword.lower() in topic.lower():
                return standard_title
        
        # 默认标题
        return f"{clean_topic} 指南"
    
    def _generate_skill_description(self, topic: str, 
                                    collected_data: Optional[Dict] = None) -> str:
        """生成技能描述"""
        clean_topic = topic.replace('学习', '').strip()
        
        base_description = f"本技能提供 {clean_topic} 的完整学习指南，包含核心概念、实用示例和最佳实践。"
        
        if collected_data:
            # 根据收集到的数据补充描述
            concepts = collected_data.get('concepts', [])
            if concepts:
                base_description += f" 涵盖 {len(concepts)} 个核心概念。"
            
            examples = collected_data.get('examples', [])
            if examples:
                base_description += f" 包含 {len(examples)} 个实用示例。"
        
        return base_description
    
    def outline_to_dict(self, outline: SkillOutline) -> Dict[str, Any]:
        """将大纲转换为字典格式"""
        return {
            'title': outline.title,
            'description': outline.description,
            'sections': [
                {
                    'title': s.title,
                    'description': s.description,
                    'content_type': s.content_type
                }
                for s in outline.sections
            ],
            'estimated_tokens': outline.estimated_tokens
        }
    
    def outline_to_json(self, outline: SkillOutline) -> str:
        """将大纲转换为JSON字符串"""
        return json.dumps(self.outline_to_dict(outline), 
                        ensure_ascii=False, indent=2)


def generate_skill_outline(topic: str, 
                          collected_data: Optional[Dict] = None,
                          depth: str = 'systematic') -> Dict[str, Any]:
    """
    便捷函数：生成技能大纲
    
    返回: 大纲字典
    """
    outliner = SkillOutliner()
    outline = outliner.generate_outline(topic, collected_data, depth)
    return outliner.outline_to_dict(outline)


if __name__ == '__main__':
    # 测试
    print("🧪 技能大纲设计器测试\n")
    
    test_topics = [
        ("学习 React 19 Server Components", 'systematic'),
        ("学习 TypeScript 5.5", 'intro'),
        ("学习 Python 异步编程", 'mastery'),
    ]
    
    for topic, depth in test_topics:
        print(f"📚 主题: {topic}")
        print(f"   深度: {depth}")
        
        outline = generate_skill_outline(topic, depth=depth)
        
        print(f"   📝 标题: {outline['title']}")
        print(f"   📖 描述: {outline['description']}")
        print(f"   📊 章节数: {len(outline['sections'])}")
        print(f"   💰 预估Token: {outline['estimated_tokens']}")
        print("   📋 章节:")
        for i, section in enumerate(outline['sections'], 1):
            print(f"      {i}. {section['title']}")
        print()
