#!/usr/bin/env python3
"""
自主学习系统 - 信息充分性评分模块
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass


@dataclass
class InformationScore:
    """信息充分性评分结果"""
    total_score: float
    dimension_scores: Dict[str, float]
    is_sufficient: bool
    feedback: str
    missing_items: List[str]


class InformationScorer:
    """信息充分性评分器"""
    
    # 评分维度与权重
    DIMENSIONS = {
        'core_concepts': {
            'name': '核心概念覆盖',
            'weight': 0.25,
            'description': '主要概念是否都有覆盖'
        },
        'examples': {
            'name': '实用示例数量',
            'weight': 0.25,
            'description': '是否有足够的代码示例'
        },
        'best_practices': {
            'name': '最佳实践',
            'weight': 0.20,
            'description': '是否包含行业最佳实践'
        },
        'faq': {
            'name': '常见问题',
            'weight': 0.15,
            'description': '是否覆盖常见坑点'
        },
        'source_quality': {
            'name': '信息来源质量',
            'weight': 0.15,
            'description': '来源是否权威可靠'
        }
    }
    
    # 阈值
    SUFFICIENT_THRESHOLD = 70.0
    MAX_ITERATIONS = 3
    
    def __init__(self):
        self.scores_history = []
    
    def score_information(self, 
                        collected_data: Dict,
                        iteration: int = 1) -> InformationScore:
        """
        评估信息充分性
        
        参数:
            collected_data: 收集到的信息数据
            iteration: 当前循环次数 (1-3)
        
        返回:
            InformationScore 对象
        """
        dimension_scores = {}
        
        # 1. 核心概念覆盖 (25%)
        dimension_scores['core_concepts'] = self._score_core_concepts(collected_data)
        
        # 2. 实用示例数量 (25%)
        dimension_scores['examples'] = self._score_examples(collected_data)
        
        # 3. 最佳实践 (20%)
        dimension_scores['best_practices'] = self._score_best_practices(collected_data)
        
        # 4. 常见问题 (15%)
        dimension_scores['faq'] = self._score_faq(collected_data)
        
        # 5. 信息来源质量 (15%)
        dimension_scores['source_quality'] = self._score_source_quality(collected_data)
        
        # 计算总分
        total_score = self._calculate_total_score(dimension_scores)
        
        # 判断是否充分
        is_sufficient = total_score >= self.SUFFICIENT_THRESHOLD
        
        # 生成反馈和缺失项
        feedback, missing_items = self._generate_feedback(
            dimension_scores, total_score, iteration
        )
        
        # 记录历史
        self.scores_history.append({
            'iteration': iteration,
            'total_score': total_score,
            'dimension_scores': dimension_scores.copy()
        })
        
        return InformationScore(
            total_score=total_score,
            dimension_scores=dimension_scores,
            is_sufficient=is_sufficient,
            feedback=feedback,
            missing_items=missing_items
        )
    
    def _score_core_concepts(self, data: Dict) -> float:
        """评分核心概念覆盖"""
        concepts = data.get('concepts', [])
        
        if not concepts:
            return 0.0
        
        # 评估概念覆盖程度
        concept_count = len(concepts)
        
        if concept_count >= 10:
            return 100.0
        elif concept_count >= 7:
            return 85.0
        elif concept_count >= 5:
            return 70.0
        elif concept_count >= 3:
            return 50.0
        else:
            return 30.0
    
    def _score_examples(self, data: Dict) -> float:
        """评分实用示例数量"""
        examples = data.get('examples', [])
        code_blocks = data.get('code_blocks', 0)
        
        example_count = len(examples) + code_blocks
        
        if example_count >= 5:
            return 100.0
        elif example_count >= 4:
            return 85.0
        elif example_count >= 3:
            return 70.0
        elif example_count >= 2:
            return 50.0
        elif example_count >= 1:
            return 30.0
        else:
            return 0.0
    
    def _score_best_practices(self, data: Dict) -> float:
        """评分最佳实践"""
        practices = data.get('best_practices', [])
        
        if not practices:
            return 0.0
        
        practice_count = len(practices)
        
        if practice_count >= 8:
            return 100.0
        elif practice_count >= 6:
            return 85.0
        elif practice_count >= 5:
            return 70.0
        elif practice_count >= 3:
            return 50.0
        elif practice_count >= 1:
            return 30.0
        else:
            return 0.0
    
    def _score_faq(self, data: Dict) -> float:
        """评分常见问题"""
        faqs = data.get('faqs', [])
        pitfalls = data.get('pitfalls', [])
        
        faq_count = len(faqs) + len(pitfalls)
        
        if faq_count >= 8:
            return 100.0
        elif faq_count >= 6:
            return 85.0
        elif faq_count >= 5:
            return 70.0
        elif faq_count >= 3:
            return 50.0
        elif faq_count >= 1:
            return 30.0
        else:
            return 0.0
    
    def _score_source_quality(self, data: Dict) -> float:
        """评分信息来源质量"""
        sources = data.get('sources', [])
        
        if not sources:
            return 50.0  # 基础分
        
        # 评估来源权威性
        authoritative_count = 0
        for source in sources:
            if self._is_authoritative_source(source):
                authoritative_count += 1
        
        if authoritative_count >= 3:
            return 100.0
        elif authoritative_count >= 2:
            return 85.0
        elif authoritative_count >= 1:
            return 70.0
        else:
            return 50.0
    
    def _is_authoritative_source(self, source: str) -> bool:
        """判断是否是权威来源"""
        authoritative_keywords = [
            'react.dev', 'vuejs.org', 'tailwindcss.com',
            'developer.mozilla.org', 'mdn.io',
            'docs.python.org', 'rust-lang.org',
            'nodejs.org', 'typescriptlang.org',
            'github.com', 'stackoverflow.com',
            'medium.com', 'dev.to', 'zhihu.com'
        ]
        
        source_lower = source.lower()
        return any(keyword in source_lower for keyword in authoritative_keywords)
    
    def _calculate_total_score(self, dimension_scores: Dict[str, float]) -> float:
        """计算总分"""
        total = 0.0
        
        for dim_name, dim_config in self.DIMENSIONS.items():
            score = dimension_scores.get(dim_name, 0.0)
            weight = dim_config['weight']
            total += score * weight
        
        return round(total, 1)
    
    def _generate_feedback(self, dimension_scores: Dict[str, float],
                          total_score: float, iteration: int) -> Tuple[str, List[str]]:
        """生成反馈和缺失项"""
        missing_items = []
        feedback_parts = []
        
        # 检查各个维度
        if dimension_scores.get('core_concepts', 0) < 70:
            missing_items.append('核心概念覆盖不足')
            feedback_parts.append('需要收集更多核心概念')
        
        if dimension_scores.get('examples', 0) < 70:
            missing_items.append('实用示例数量不足')
            feedback_parts.append('需要更多完整代码示例')
        
        if dimension_scores.get('best_practices', 0) < 70:
            missing_items.append('最佳实践不足')
            feedback_parts.append('需要收集行业最佳实践')
        
        if dimension_scores.get('faq', 0) < 70:
            missing_items.append('常见问题覆盖不足')
            feedback_parts.append('需要收集常见问题和坑点')
        
        if dimension_scores.get('source_quality', 0) < 70:
            missing_items.append('信息来源权威性不足')
            feedback_parts.append('建议参考更多权威来源')
        
        # 生成总体反馈
        if total_score >= 70:
            feedback = f"✅ 信息充分！总分: {total_score}分，可以进入技能生成阶段"
        elif iteration >= self.MAX_ITERATIONS:
            feedback = f"⚠️ 已达到最大循环次数({self.MAX_ITERATIONS})，总分: {total_score}分，建议接受当前质量"
        else:
            feedback = f"❌ 信息不足！总分: {total_score}分，需要继续搜索。缺失项: {', '.join(missing_items)}"
        
        return feedback, missing_items
    
    def should_continue(self, current_score: float, iteration: int) -> bool:
        """
        判断是否应该继续循环
        
        返回: True=继续, False=退出
        """
        # 检查是否达到阈值
        if current_score >= self.SUFFICIENT_THRESHOLD:
            return False
        
        # 检查是否达到最大循环次数
        if iteration >= self.MAX_ITERATIONS:
            return False
        
        # 检查是否陷入停滞（连续2次无提升）
        if len(self.scores_history) >= 2:
            prev1 = self.scores_history[-1]['total_score']
            prev2 = self.scores_history[-2]['total_score']
            if prev1 <= prev2:
                return False
        
        return True
    
    def get_search_suggestions(self, missing_items: List[str]) -> List[str]:
        """根据缺失项生成搜索建议"""
        suggestions = []
        
        suggestion_map = {
            '核心概念覆盖不足': [
                '{topic} 核心概念',
                '{topic} 完整教程',
                '{topic} 入门指南'
            ],
            '实用示例数量不足': [
                '{topic} 完整示例',
                '{topic} 代码示例',
                '{topic} 实战项目'
            ],
            '最佳实践不足': [
                '{topic} 最佳实践',
                '{topic} 最佳实践 2026',
                '{topic} 使用技巧'
            ],
            '常见问题覆盖不足': [
                '{topic} 常见问题',
                '{topic} FAQ',
                '{topic} 坑点'
            ],
            '信息来源权威性不足': [
                '{topic} 官方文档',
                'site:react.dev {topic}',
                'site:developer.mozilla.org {topic}'
            ]
        }
        
        for item in missing_items:
            if item in suggestion_map:
                suggestions.extend(suggestion_map[item])
        
        return suggestions


def score_information(collected_data: Dict, iteration: int = 1) -> InformationScore:
    """
    便捷函数：评估信息充分性
    
    返回: InformationScore 对象
    """
    scorer = InformationScorer()
    return scorer.score_information(collected_data, iteration)


if __name__ == '__main__':
    # 测试
    print("🧪 信息充分性评分测试\n")
    
    # 测试数据1：信息不足
    test_data1 = {
        'concepts': ['概念1', '概念2'],
        'examples': ['示例1'],
        'best_practices': [],
        'faqs': [],
        'sources': ['some-blog.com']
    }
    
    print("测试1：信息不足")
    result1 = score_information(test_data1, 1)
    print(f"  总分: {result1.total_score}")
    print(f"  充分: {result1.is_sufficient}")
    print(f"  反馈: {result1.feedback}")
    print()
    
    # 测试数据2：信息充分
    test_data2 = {
        'concepts': ['概念1', '概念2', '概念3', '概念4', '概念5', '概念6', '概念7'],
        'examples': ['示例1', '示例2', '示例3', '示例4'],
        'code_blocks': 2,
        'best_practices': ['实践1', '实践2', '实践3', '实践4', '实践5'],
        'faqs': ['问题1', '问题2', '问题3'],
        'pitfalls': ['坑1', '坑2'],
        'sources': ['react.dev', 'github.com', 'stackoverflow.com']
    }
    
    print("测试2：信息充分")
    result2 = score_information(test_data2, 2)
    print(f"  总分: {result2.total_score}")
    print(f"  充分: {result2.is_sufficient}")
    print(f"  反馈: {result2.feedback}")
    print()
