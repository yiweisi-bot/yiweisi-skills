#!/usr/bin/env python3
"""
自主学习系统 - 学习流程管理器（已更新集成 agent-browser）
"""

import sys
import os
from typing import Optional, Dict, List, Any
from datetime import datetime

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db import get_db
from database.priority import calculate_goal_priority
from database.information_scorer import InformationScorer, InformationScore


class LearningManager:
    """学习流程管理器"""
    
    def __init__(self):
        self.db = get_db()
        self.scorer = InformationScorer()
    
    # ============================================
    # 目标管理
    # ============================================
    
    def create_learning_goal(self, title: str, description: Optional[str] = None,
                       source: Optional[str] = None) -> Dict[str, Any]:
        """
        创建学习目标（带优先级计算）
        
        返回: 目标信息字典
        """
        # 计算优先级
        priority_result = calculate_goal_priority(title, description)
        
        # 创建目标
        goal_id = self.db.create_goal(
            title=title,
            description=description,
            priority=priority_result['level'],
            source=source
        )
        
        # 获取目标信息
        goal = self.db.get_goal(goal_id)
        
        return {
            'goal_id': goal_id,
            'goal': goal,
            'priority_score': priority_result['score'],
            'priority_level': priority_result['level'],
            'priority_details': priority_result['details']
        }
    
    def start_learning(self, goal_id: int) -> Dict[str, Any]:
        """
        开始学习
        
        返回: 会话信息
        """
        # 更新目标状态
        self.db.update_goal_status(goal_id, 'in_progress')
        
        # 创建学习会话
        session_id = self.db.create_session(
            goal_id=goal_id,
            session_type='learning'
        )
        
        return {
            'session_id': session_id,
            'goal_id': goal_id,
            'started_at': datetime.now().isoformat()
        }
    
    # ============================================
    # Action-Reflection-Iteration 循环
    # ============================================
    
    def start_iteration_cycle(self, goal_id: int, session_id: int,
                         collected_data: Dict,
                         iteration: int = 1) -> Dict[str, Any]:
        """
        执行一次 Action-Reflection-Iteration 循环
        
        参数:
            goal_id: 学习目标ID
            session_id: 学习会话ID
            collected_data: 已收集的数据
            iteration: 当前循环次数 (1-3)
        
        返回: 循环结果
        """
        print(f"🔄 开始循环 {iteration}/3")
        
        # 1. Action: 收集信息（使用 agent-browser）
        action_result = self._action_collect_info(goal_id, collected_data, iteration)
        
        # 2. Reflection: 评估信息充分性
        reflection_result = self._reflection_assess(action_result['collected_data'], iteration)
        
        # 3. Iteration: 决策是否继续
        iteration_decision = self._iteration_decide(reflection_result['score'], iteration)
        
        return {
            'iteration': iteration,
            'action': action_result,
            'reflection': reflection_result,
            'decision': iteration_decision
        }
    
    def _action_collect_info(self, goal_id: int, existing_data: Dict, iteration: int) -> Dict[str, Any]:
        """
        Action 阶段：收集信息（使用 agent-browser 集成）
        """
        print(f"   📡 Action: 收集信息...")
        
        # 获取目标信息
        goal = self.db.get_goal(goal_id)
        if not goal:
            return {
                'status': 'error',
                'collected_data': existing_data
            }
        
        # 提取主题（去掉"学习"前缀）
        topic = goal['title'].replace('学习', '').strip()
        
        # 使用 agent-browser 集成模块
        from database.agent_browser_integration import collect_information_with_agent_browser
        print(f"   🔍 使用 agent-browser 搜索: {topic}")
        
        new_data = collect_information_with_agent_browser(topic, iteration)
        
        # 合并已有数据
        collected_data = existing_data.copy()
        
        # 合并概念
        if 'concepts' in new_data:
            existing_concepts = collected_data.setdefault('concepts', [])
            for concept in new_data['concepts']:
                if concept not in existing_concepts:
                    existing_concepts.append(concept)
        
        # 合并其他字段
        for key in ['examples_count', 'has_best_practices', 'has_faqs', 'sources_quality', 'search_results']:
            if key in new_data:
                collected_data[key] = new_data[key]
        
        print(f"   ✅ 信息收集完成（agent-browser）")
        
        return {
            'status': 'completed',
            'collected_data': collected_data
        }
    
    def _reflection_assess(self, collected_data: Dict, iteration: int) -> Dict[str, Any]:
        """
        Reflection 阶段：评估信息充分性
        """
        print(f"   🤔 Reflection: 评估信息...")
        
        # 使用 InformationScorer 评估
        score_result = self.scorer.score_information(collected_data, iteration)
        
        print(f"   📊 总分: {score_result.total_score}分")
        print(f"   ✅ 充分: {score_result.is_sufficient}")
        
        return {
            'score': score_result.total_score,
            'is_sufficient': score_result.is_sufficient,
            'dimension_scores': score_result.dimension_scores,
            'feedback': score_result.feedback,
            'missing_items': score_result.missing_items,
            'score_object': score_result
        }
    
    def _iteration_decide(self, current_score: float, iteration: int) -> Dict[str, Any]:
        """
        Iteration 阶段：决策是否继续
        """
        print(f"   🔄 Iteration: 决策...")
        
        # 使用 scorer 的决策逻辑
        should_continue = self.scorer.should_continue(current_score, iteration)
        
        decision = 'continue' if should_continue else 'exit'
        reason = ''
        
        if current_score >= 70:
            reason = '信息充分（≥70分）'
        elif iteration >= 3:
            reason = '达到最大循环次数（3次）'
        elif not should_continue:
            reason = '判断无需继续'
        
        print(f"   🎯 决策: {decision} - {reason}")
        
        return {
            'should_continue': should_continue,
            'decision': decision,
            'reason': reason
        }
    
    # ============================================
    # 技能生成
    # ============================================
    
    def generate_skill(self, goal_id: int, collected_data: Dict,
                     topic: Optional[str] = None,
                     depth: str = 'systematic') -> Dict[str, Any]:
        """
        生成技能（集成大纲设计器和内容生成器）
        """
        print(f"✨ 开始生成技能...")
        
        # 1. 检查重复
        from database.skill_versioning import get_version_manager
        version_manager = get_version_manager()
        
        # 获取目标信息
        goal = self.db.get_goal(goal_id)
        if not goal:
            return {'status': 'error', 'message': '目标不存在'}
        
        skill_title = topic or goal['title']
        
        # 检查重复
        has_dup, similar_skills = version_manager.check_duplicate(skill_title)
        
        if has_dup:
            print(f"   ⚠️  检测到 {len(similar_skills)} 个相似技能")
            # 这里简化处理，直接新建版本
            # 实际项目中可以交互让用户选择
        
        # 2. 生成大纲
        from database.skill_outliner import generate_skill_outline
        print(f"   📋 生成技能大纲...")
        
        outline = generate_skill_outline(skill_title, collected_data, depth)
        print(f"   ✅ 大纲生成: {outline['title']}")
        print(f"   📊 章节数: {len(outline['sections'])}")
        
        # 3. 生成内容（使用真实LLM集成）
        print(f"   ✍️  生成技能内容...")
        
        from database.real_llm_integration import get_real_llm_integration
        llm = get_real_llm_integration()
        
        # 生成内容
        content = llm.generate_skill_content_with_llm(outline, collected_data)
        
        # 保存文件
        import re
        safe_title = re.sub(r'[\\/*?:"<>|]', '', skill_title)
        safe_title = safe_title.replace(' ', '-')
        
        skills_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            'generated-skills'
        )
        os.makedirs(skills_dir, exist_ok=True)
        
        filepath = os.path.join(skills_dir, f"{safe_title}.md")
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        result = {
            'title': skill_title,
            'content': content,
            'filepath': filepath
        }
        
        print(f"   📝 技能标题: {result['title']}")
        print(f"   📁 文件: {result['filepath']}")
        print(f"   ✅ 技能生成完成！")
        
        # 4. 记录到数据库
        db_skill_id = self.db.create_skill(
            goal_id=goal_id,
            title=result['title'],
            file_path=result['filepath'],
            tokens_used=outline.get('estimated_tokens', 0)
        )
        
        print(f"   💾 已记录到数据库: ID={db_skill_id}")
        
        # 5. 质量验证（使用真实LLM集成）
        print()
        print("🛡️  开始质量验证...")
        
        from database.quality_validator import validate_skill_updated
        validation_result = validate_skill_updated(result['filepath'])
        
        # 更新技能验证状态
        if validation_result.get('overall', {}).get('status') == 'pending_human':
            self.db.update_skill_validation(
                db_skill_id,
                validation_status='rule_passed',
                quality_score=int(validation_result['overall']['overall_score'])
            )
        
        return {
            'status': 'completed',
            'skill_id': db_skill_id,
            'skill_title': result['title'],
            'filepath': result['filepath'],
            'outline': outline,
            'collected_data': collected_data,
            'validation': validation_result
        }


def get_learning_manager() -> LearningManager:
    """获取学习管理器实例"""
    return LearningManager()


if __name__ == '__main__':
    # 简单测试
    print("🧪 学习管理器（已更新）测试\n")
    
    manager = get_learning_manager()
    
    # 1. 创建学习目标
    print("1. 创建学习目标")
    result = manager.create_learning_goal(
        title="学习 TypeScript 基础类型",
        description="学习 TypeScript 的基础类型系统"
    )
    print(f"   ✅ 目标创建成功: ID={result['goal_id']}")
    print(f"   🎯 优先级: {result['priority_score']}分 (等级 {result['priority_level']})")
    print()
    
    # 2. 开始学习
    print("2. 开始学习")
    session_result = manager.start_learning(result['goal_id'])
    print(f"   ✅ 学习会话创建: ID={session_result['session_id']}")
    print()
    
    # 3. 执行循环
    print("3. 执行循环")
    collected_data = {}
    
    for i in range(1, 4):
        cycle_result = manager.start_iteration_cycle(
            goal_id=result['goal_id'],
            session_id=session_result['session_id'],
            collected_data=collected_data,
            iteration=i
        )
        
        collected_data = cycle_result['action']['collected_data']
        
        if not cycle_result['decision']['should_continue']:
            print(f"   🎯 循环结束")
            break
    
    print()
    print("4. 生成技能")
    skill_result = manager.generate_skill(
        goal_id=result['goal_id'],
        collected_data=collected_data
    )
    print(f"   ✅ 技能生成: {skill_result['skill_title']}")
    print(f"   📁 文件: {skill_result['filepath']}")
    
    print()
    print("✅ 测试完成！")
