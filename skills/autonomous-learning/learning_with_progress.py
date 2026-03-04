#!/usr/bin/env python3
"""
自主学习完整示例 - 带进度跟踪和时间保障

演示如何在子Agent中使用进度跟踪器
"""

import sys
import os
import json
import time
from datetime import datetime
from pathlib import Path

# 添加当前目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from learning_progress_tracker import LearningProgressTracker, create_tracker


class LearningTaskExecutor:
    """
    学习任务执行器
    
    负责：
    1. 执行实际的学习任务
    2. 管理时间预算
    3. 实时汇报进度
    4. 确保学满时间
    """
    
    def __init__(self, config: dict):
        """
        初始化学习执行器
        
        参数:
            config: 学习配置 {
                'topic': 主题,
                'depth': 深度,
                'time_limit': 时间限制（分钟）,
                'token_budget': Token预算
            }
        """
        self.config = config
        self.topic = config['topic']
        self.depth = config['depth']
        self.time_limit = config['time_limit']
        self.token_budget = config['token_budget']
        
        # 创建进度跟踪器
        self.tracker = create_tracker(self.time_limit, self.topic)
        
        # 学习结果
        self.collected_info = []
        self.organized_knowledge = {}
        self.generated_skill = None
    
    def execute(self):
        """执行完整的学习流程"""
        # 开始跟踪
        self.tracker.start()
        
        # 根据深度执行不同流程
        if self.depth == 'intro':
            self._execute_intro_learning()
        elif self.depth == 'systematic':
            self._execute_systematic_learning()
        elif self.depth == 'master':
            self._execute_master_learning()
        
        # 返回学习报告
        return self.tracker.get_report()
    
    def _execute_intro_learning(self):
        """快速学习模式（≤15分钟）"""
        # 阶段1: 信息搜索
        self._search_info(quick=True)
        
        # 阶段2: 知识整理
        self._organize_knowledge(quick=True)
        
        # 阶段3: 文档生成
        self._generate_document(quick=True)
    
    def _execute_systematic_learning(self):
        """系统学习模式（16-45分钟）"""
        # 阶段1: 信息搜索
        self._search_info()
        
        # 阶段2: 知识整理
        self._organize_knowledge()
        
        # 阶段3: 文档生成
        self._generate_document()
    
    def _execute_master_learning(self):
        """深度学习模式（>45分钟）"""
        # 阶段1: 信息搜索
        self._search_info(deep=True)
        
        # 阶段2: 深度分析
        self._analyze_deeply()
        
        # 阶段3: 知识整理
        self._organize_knowledge(deep=True)
        
        # 阶段4: 文档生成
        self._generate_document(deep=True)
    
    def _search_info(self, quick=False, deep=False):
        """
        搜索信息阶段
        
        时间保障机制：
        1. 预留搜索时间
        2. 定期检查进度
        3. 如果时间不够，智能跳过次要资源
        """
        print(f"🔍 开始搜索: {self.topic}")
        
        # 模拟搜索过程（实际应调用agent-browser）
        search_queries = self._generate_search_queries()
        
        total_queries = len(search_queries)
        for i, query in enumerate(search_queries):
            # 更新进度
            progress = int((i + 1) / total_queries * 100)
            self.tracker.update_progress(progress, f"搜索: {query}")
            
            # 模拟搜索耗时
            time.sleep(0.3)
            
            # 收集信息
            info = self._simulate_search(query)
            self.collected_info.append(info)
            
            # 时间检查：如果剩余时间不足，提前结束
            if self._should_stop_early():
                self.tracker.update_progress(100, "时间有限，提前结束搜索")
                break
        
        self.tracker.complete_current_phase(f"已收集{len(self.collected_info)}个资源")
    
    def _organize_knowledge(self, quick=False, deep=False):
        """
        整理知识阶段
        
        时间保障机制：
        1. 按重要性排序知识点
        2. 优先处理核心概念
        3. 时间不够时保留核心内容
        """
        print(f"📚 开始整理知识...")
        
        # 提取核心概念
        core_concepts = self._extract_core_concepts()
        total_concepts = len(core_concepts)
        
        for i, concept in enumerate(core_concepts):
            # 更新进度
            progress = int((i + 1) / total_concepts * 100)
            self.tracker.update_progress(progress, f"整理: {concept}")
            
            # 模拟整理过程
            time.sleep(0.2)
            
            # 存储整理结果
            self.organized_knowledge[concept] = self._organize_concept(concept)
        
        self.tracker.complete_current_phase(f"已整理{len(self.organized_knowledge)}个核心概念")
    
    def _analyze_deeply(self):
        """深度分析阶段（仅master模式）"""
        print(f"🔬 开始深度分析...")
        
        analysis_tasks = [
            "对比分析不同实现方案",
            "验证核心概念准确性",
            "探索最佳实践案例",
            "总结常见问题和陷阱"
        ]
        
        for i, task in enumerate(analysis_tasks):
            progress = int((i + 1) / len(analysis_tasks) * 100)
            self.tracker.update_progress(progress, task)
            time.sleep(0.3)
        
        self.tracker.complete_current_phase("深度分析完成")
    
    def _generate_document(self, quick=False, deep=False):
        """
        生成文档阶段
        
        时间保障机制：
        1. 根据剩余时间调整文档详细程度
        2. 优先保证核心章节完整
        3. 时间不够时生成精简版本
        """
        print(f"📝 开始生成文档...")
        
        # 确定文档结构
        if quick:
            sections = ["简介", "核心概念", "快速示例"]
        elif deep:
            sections = ["简介", "核心概念", "原理详解", "最佳实践", "高级技巧", "常见问题", "进阶资源"]
        else:
            sections = ["简介", "核心概念", "实践方法", "最佳实践", "常见问题"]
        
        # 逐章节生成
        for i, section in enumerate(sections):
            progress = int((i + 1) / len(sections) * 100)
            self.tracker.update_progress(progress, f"生成章节: {section}")
            time.sleep(0.2)
        
        # 生成最终文档
        self.generated_skill = self._create_skill_document(sections)
        
        self.tracker.complete_current_phase("文档生成完成")
    
    # ==================== 辅助方法 ====================
    
    def _generate_search_queries(self) -> list:
        """生成搜索查询列表"""
        base_queries = [
            f"{self.topic} 教程",
            f"{self.topic} 最佳实践",
            f"{self.topic} 实例"
        ]
        
        if self.depth in ['systematic', 'master']:
            base_queries.extend([
                f"{self.topic} 原理",
                f"{self.topic} 源码分析"
            ])
        
        if self.depth == 'master':
            base_queries.extend([
                f"{self.topic} 性能优化",
                f"{self.topic} 高级技巧"
            ])
        
        return base_queries
    
    def _simulate_search(self, query: str) -> dict:
        """模拟搜索（实际应调用agent-browser）"""
        return {
            "query": query,
            "results": [
                {"title": f"{query} - 结果1", "url": "https://example.com/1"},
                {"title": f"{query} - 结果2", "url": "https://example.com/2"}
            ],
            "timestamp": datetime.now().isoformat()
        }
    
    def _should_stop_early(self) -> bool:
        """检查是否应该提前结束当前阶段"""
        # 这里可以实现时间检查逻辑
        # 例如：如果已用时间超过预算的90%，返回True
        return False
    
    def _extract_core_concepts(self) -> list:
        """提取核心概念"""
        # 从收集的信息中提取核心概念
        return ["概念1", "概念2", "概念3", "概念4", "概念5"]
    
    def _organize_concept(self, concept: str) -> dict:
        """整理单个概念"""
        return {
            "name": concept,
            "description": f"{concept}的详细说明",
            "examples": [f"{concept}示例1", f"{concept}示例2"]
        }
    
    def _create_skill_document(self, sections: list) -> str:
        """创建技能文档"""
        doc = f"""---
name: {self.topic}
description: {self.topic}学习技能
metadata:
  emoji: "📚"
  author: "LearnerAgent"
  version: "1.0"
---

# {self.topic}

"""
        
        for section in sections:
            doc += f"\n## {section}\n\n{section}的内容...\n"
        
        return doc


# ==================== 使用示例 ====================

def example_usage():
    """演示如何使用学习执行器"""
    print("=" * 60)
    print("🎓 自主学习示例 - 带进度跟踪")
    print("=" * 60)
    print()
    
    # 配置学习任务
    config = {
        'topic': 'Python装饰器',
        'depth': 'systematic',
        'time_limit': 30,
        'token_budget': 5000
    }
    
    # 创建执行器
    executor = LearningTaskExecutor(config)
    
    # 执行学习
    report = executor.execute()
    
    # 打印报告
    print("\n" + "=" * 60)
    print("📊 学习报告")
    print("=" * 60)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    
    # 保存技能文档
    if executor.generated_skill:
        output_dir = Path.home() / ".openclaw" / "learner-workspace" / "skills"
        output_dir.mkdir(parents=True, exist_ok=True)
        
        output_file = output_dir / f"{config['topic'].replace(' ', '-')}.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(executor.generated_skill)
        
        print(f"\n✅ 技能文档已保存: {output_file}")


if __name__ == "__main__":
    example_usage()
