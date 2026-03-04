#!/usr/bin/env python3
"""
自主学习系统 - 启动交互流程
"""

import sys
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass


@dataclass
class LearningConfig:
    """学习配置"""
    topic: str
    depth: str  # intro, systematic, mastery
    time_limit: int  # 分钟
    token_budget: int  # token数量
    auto_continue: bool = True


class InteractiveSetup:
    """启动交互流程"""
    
    # 学习深度选项
    DEPTH_OPTIONS = {
        '1': {'key': 'intro', 'name': '入门了解', 'tokens': 5000, 'time': 60},
        '2': {'key': 'systematic', 'name': '系统学习', 'tokens': 20000, 'time': 120},
        '3': {'key': 'mastery', 'name': '深入精通', 'tokens': 50000, 'time': 240}
    }
    
    # 智能推荐主题
    RECOMMENDED_TOPICS = [
        'React 19 Server Components',
        'TypeScript 5.5 新特性',
        'Python 异步编程',
        'Docker 容器化',
        'Tailwind CSS v4'
    ]
    
    def __init__(self):
        pass
    
    def run_setup(self, initial_topic: Optional[str] = None) -> Optional[LearningConfig]:
        """
        运行完整的启动交互流程
        
        参数:
            initial_topic: 初始主题（可选）
        
        返回: LearningConfig 或 None（用户取消）
        """
        print("=" * 60)
        print("🧠 自主学习系统 - 配置向导")
        print("=" * 60)
        print()
        
        # 步骤1：选择学习主题
        topic = self._select_topic(initial_topic)
        if not topic:
            print("已取消")
            return None
        
        print()
        
        # 步骤2：选择学习深度
        depth = self._select_depth()
        if not depth:
            print("已取消")
            return None
        
        print()
        
        # 步骤3：设置时间限制
        time_limit = self._set_time_limit(depth)
        
        print()
        
        # 步骤4：设置Token预算
        token_budget = self._set_token_budget(depth)
        
        print()
        
        # 步骤5：确认配置
        config = LearningConfig(
            topic=topic,
            depth=depth['key'],
            time_limit=time_limit,
            token_budget=token_budget
        )
        
        confirmed = self._confirm_config(config, depth)
        
        if confirmed:
            print()
            print("✅ 配置确认完成！")
            return config
        else:
            print()
            print("已取消")
            return None
    
    def _select_topic(self, initial_topic: Optional[str] = None) -> Optional[str]:
        """选择学习主题"""
        if initial_topic:
            print(f"📚 学习主题: {initial_topic}")
            return initial_topic
        
        print("📚 请选择学习主题：")
        print()
        
        # 显示推荐主题
        print("智能推荐主题：")
        for i, topic in enumerate(self.RECOMMENDED_TOPICS, 1):
            print(f"  {i}. {topic}")
        
        print()
        print("或者，输入你想学习的主题...")
        
        choice = input("请输入数字或自定义主题: ").strip()
        
        if not choice:
            return None
        
        # 检查是否是数字
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(self.RECOMMENDED_TOPICS):
                return self.RECOMMENDED_TOPICS[idx]
            else:
                print("无效的选择")
                return None
        else:
            return choice
    
    def _select_depth(self) -> Optional[Dict]:
        """选择学习深度"""
        print("🎯 请选择学习深度：")
        print()
        
        for key, option in self.DEPTH_OPTIONS.items():
            print(f"  {key}. {option['name']}")
            print(f"     预估 Token: {option['tokens']:,}")
            print(f"     预估时间: {option['time']} 分钟")
            print()
        
        choice = input("请选择 (1/2/3, 默认: 2): ").strip() or "2"
        
        return self.DEPTH_OPTIONS.get(choice)
    
    def _set_time_limit(self, depth: Dict) -> int:
        """设置时间限制"""
        recommended = depth['time']
        
        print("⏰ 设置学习时间限制：")
        print(f"  推荐: {recommended} 分钟")
        print()
        
        choice = input(f"请输入时间限制（分钟，默认: {recommended}）: ").strip()
        
        if not choice:
            return recommended
        
        try:
            limit = int(choice)
            if limit <= 0:
                print("  ⚠️  时间限制必须大于0，使用推荐值")
                return recommended
            return limit
        except ValueError:
            print("  ⚠️  无效输入，使用推荐值")
            return recommended
    
    def _set_token_budget(self, depth: Dict) -> int:
        """设置Token预算"""
        recommended = depth['tokens']
        
        # 估算成本（简化版）
        cost_estimate = self._estimate_cost(recommended)
        
        print("💰 设置Token预算：")
        print(f"  推荐: {recommended:,} tokens")
        print(f"  预估成本: {cost_estimate}")
        print()
        
        choice = input(f"请输入Token预算（默认: {recommended}）: ").strip()
        
        if not choice:
            return recommended
        
        try:
            budget = int(choice.replace(',', ''))
            if budget <= 0:
                print("  ⚠️  Token预算必须大于0，使用推荐值")
                return recommended
            return budget
        except ValueError:
            print("  ⚠️  无效输入，使用推荐值")
            return recommended
    
    def _estimate_cost(self, tokens: int) -> str:
        """估算成本（简化版）"""
        # 简化估算：$0.01 per 1K tokens
        cost = (tokens / 1000) * 0.01
        return f"约 ${cost:.2f} USD"
    
    def _confirm_config(self, config: LearningConfig, depth: Dict) -> bool:
        """确认配置"""
        print("📋 配置摘要：")
        print()
        print(f"  📚 学习主题: {config.topic}")
        print(f"  🎯 学习深度: {depth['name']}")
        print(f"  ⏰ 时间限制: {config.time_limit} 分钟")
        print(f"  💰 Token预算: {config.token_budget:,} tokens")
        print()
        
        choice = input("确认开始学习？(Y/n): ").strip().lower()
        
        return choice in ['', 'y', 'yes']


def run_interactive_setup(initial_topic: Optional[str] = None) -> Optional[LearningConfig]:
    """
    便捷函数：运行交互配置
    
    返回: LearningConfig 或 None
    """
    setup = InteractiveSetup()
    return setup.run_setup(initial_topic)


if __name__ == '__main__':
    # 测试
    print("🧪 启动交互流程测试\n")
    
    config = run_interactive_setup()
    
    if config:
        print()
        print("✅ 配置完成！")
        print(f"   主题: {config.topic}")
        print(f"   深度: {config.depth}")
        print(f"   时间: {config.time_limit} 分钟")
        print(f"   Token: {config.token_budget:,}")
    else:
        print()
        print("❌ 已取消")
