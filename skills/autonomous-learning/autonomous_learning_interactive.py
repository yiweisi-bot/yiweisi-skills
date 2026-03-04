#!/usr/bin/env3
"""
自主学习系统 - 交互式版本（先与主Agent交互，再启动子Agent）

流程：
1. 主Agent与用户交互，明确学习目标和配置
2. 用户确认配置
3. 启动子Agent执行学习（无需交互）
"""

import sys
import os
import json
from typing import Dict, List, Optional, Any
from pathlib import Path


class InteractiveLearningConfigurator:
    """交互式学习配置器 - 与用户对话，收集学习需求"""
    
    def __init__(self):
        self.topic = None
        self.depth = None
        self.time_limit = None
        self.token_budget = None
        self.depth_map = {
            "1": ("intro", "快速了解", 10),
            "2": ("systematic", "系统学习", 30),
            "3": ("master", "深入精通", 60)
        }
    
    def start_interaction(self, initial_topic: Optional[str] = None) -> Dict[str, Any]:
        """
        开始交互式配置对话
        
        返回: 学习配置字典
        """
        print("=" * 60)
        print("🎯 自主学习配置向导")
        print("=" * 60)
        print()
        print("你好！我是乙维斯，让我们一起配置你的学习计划。")
        print()
        
        # 步骤1: 明确学习主题
        self.topic = self._ask_topic(initial_topic)
        print()
        
        # 步骤2: 选择学习深度
        self.depth = self._ask_depth()
        print()
        
        # 步骤3: 确认时间限制
        self.time_limit = self._ask_time_limit()
        print()
        
        # 步骤4: 选择Token预算
        self.token_budget = self._ask_token_budget()
        print()
        
        # 步骤5: 最终确认
        config = self._confirm_and_start()
        
        return config
    
    def _ask_topic(self, initial_topic: Optional[str]) -> str:
        """询问学习主题"""
        print("📝 步骤 1/4: 学习主题")
        print("-" * 60)
        
        if initial_topic:
            print(f"我注意到你想学习: 「{initial_topic}」")
            print()
            print("选项:")
            print(f"  1. ✅ 就学习 「{initial_topic}」")
            print("  2. 🔍 我想更具体/换个角度...")
            print("  3. 🔄 换一个完全不同的主题")
            print()
            
            while True:
                choice = input("请选择 (1/2/3) [默认: 1]: ").strip() or "1"
                
                if choice == "1":
                    return initial_topic
                elif choice == "2":
                    specific = input(f"好的，请告诉我更具体的角度或子主题: ").strip()
                    return specific if specific else initial_topic
                elif choice == "3":
                    new_topic = input("没问题！请告诉我你想学习的新主题: ").strip()
                    if new_topic:
                        return new_topic
                    else:
                        print("⚠️ 主题不能为空，让我为你推荐一个...")
                        return "通用编程最佳实践"
                else:
                    print("⚠️ 请输入 1、2 或 3")
        else:
            print("你想学习什么主题呢？")
            print()
            print("💡 示例主题:")
            print("  • Python 异步编程")
            print("  • React Hooks 深度解析")
            print("  • Docker 容器化实践")
            print("  • Kubernetes 入门指南")
            print("  • 机器学习基础概念")
            print()
            
            while True:
                topic = input("请输入你想学习的主题: ").strip()
                if topic:
                    return topic
                else:
                    print("⚠️  主题不能为空，请重新输入")
    
    def _ask_depth(self) -> str:
        """询问学习深度"""
        print("🎚️  步骤 2/4: 学习深度")
        print("-" * 60)
        print("你想花多少时间来深入学习这个主题？")
        print()
        print("选项:")
        print()
        print("  1. 🚀 快速了解 (10分钟)")
        print("     • 适合: 快速浏览、初步了解")
        print("     • 产出: 概览性的知识框架")
        print()
        print("  2. 📚 系统学习 (30分钟) [推荐]")
        print("     • 适合: 建立完整的知识体系")
        print("     • 产出: 详细的技能文档 + 实践案例")
        print()
        print("  3. 🎓 深入精通 (60分钟)")
        print("     • 适合: 复杂主题、专业深度")
        print("     • 产出: 全面的技能文档 + 高级技巧")
        print()
        
        while True:
            choice = input("请选择 (1/2/3) [默认: 2]: ").strip() or "2"
            
            if choice in self.depth_map:
                depth_key, depth_name, default_time = self.depth_map[choice]
                print(f"   ✅ 已选择: {depth_name} ({default_time}分钟)")
                return depth_key
            else:
                print("⚠️  请输入 1、2 或 3")
    
    def _ask_time_limit(self) -> int:
        """询问时间限制 - 显示默认推荐时间"""
        print("⏰ 步骤 3/4: 时间限制")
        print("-" * 60)
        
        # 根据已选择的深度获取推荐时间
        recommended_time = {
            "intro": 10,
            "systematic": 30,
            "master": 60
        }.get(self.depth, 30)
        
        print(f"根据你选择的「{self._get_depth_name(self.depth)}」深度，推荐学习时间为: {recommended_time} 分钟")
        print()
        print("选项:")
        print(f"  1. ✅ 使用推荐时间 ({recommended_time} 分钟)")
        print("  2. 📝 自定义时间")
        print()
        
        choice = input("请选择 (1/2) [默认: 1]: ").strip() or "1"
        
        if choice == "1":
            print(f"   ✅ 时间设置为: {recommended_time} 分钟")
            return recommended_time
        elif choice == "2":
            while True:
                custom_input = input(f"请输入自定义时间（分钟，默认{recommended_time}）: ").strip()
                if not custom_input:
                    print(f"   ✅ 使用默认时间: {recommended_time} 分钟")
                    return recommended_time
                try:
                    time_val = int(custom_input)
                    if time_val > 0:
                        print(f"   ✅ 时间设置为: {time_val} 分钟")
                        return time_val
                    else:
                        print("⚠️  时间必须大于0，请重新输入")
                except ValueError:
                    print("⚠️  请输入有效的数字")
        else:
            print(f"   ✅ 使用默认时间: {recommended_time} 分钟")
            return recommended_time
    
    def _ask_token_budget(self) -> int:
        """询问Token预算"""
        print("💰 步骤 4/4: Token预算")
        print("-" * 60)
        print("Token预算决定了学习的质量和详细程度。选择适合你的预算：")
        print()
        print("选项:")
        print()
        print("  1. 💵 经济型 (2000 tokens)")
        print("     • 适合: 简单主题，快速了解")
        print("     • 成本: 最低")
        print("     • 产出: 简洁的技能概览")
        print()
        print("  2. ⚖️  平衡型 (5000 tokens) [推荐]")
        print("     • 适合: 大多数学习场景")
        print("     • 成本: 适中")
       以后继续补充代码，提供完整的交互式配置流程，让用户可以自主设定学习目标、选择学习深度、调整时间限制和Token预算，确保学习过程既个性化又高效。print("     • 产出: 详细的技能文档 + 实用示例")
        print()
        print("  3. 💎 质量型 (10000 tokens)")
        print("     • 适合: 复杂主题，追求高质量输出")
        print("     • 成本: 较高")
        print("     • 产出: 全面的技能文档 + 高级技巧 + 最佳实践")
        print()
        
        while True:
            choice = input("请选择 (1/2/3) [默认: 2]: ").strip() or "2"
            
            budget_map = {
                "1": (2000, "经济型"),
                "2": (5000, "平衡型"),
                "3": (10000, "质量型")
            }
            
            if choice in budget_map:
                budget, name = budget_map[choice]
                print(f"   ✅ 已选择: {name} ({budget} tokens)")
                return budget
            else:
                print("⚠️  请输入 1、2 或 3")
    
    def _confirm_and_start(self) -> Dict[str, Any]:
        """最终确认并返回配置"""
        print()
        print("=" * 60)
        print("📋 学习配置确认")
        print("=" * 60)
        print()
        print(f"📚 学习主题: {self.topic}")
        print(f"🎚️  学习深度: {self._get_depth_name(self.depth)}")
        print(f"⏰ 时间限制: {self.time_limit} 分钟")
        print(f"💰 Token预算: {self.token_budget} tokens")
        print()
        
        # 根据深度给出学习产出预期
        depth_expectations = {
            "intro": "概览性的知识框架，适合快速了解",
            "systematic": "详细的技能文档 + 实用示例 + 最佳实践",
            "master": "全面的技能文档 + 高级技巧 + 深入案例分析"
        }
        
        print(f"📖 预期产出: {depth_expectations.get(self.depth, '标准技能文档')}")
        print()
        print("确认开始学习吗？")
        print("  1. ✅ 确认，开始学习")
        print("  2. 🔄 重新配置")
        print("  3. ❌ 取消")
        print()
        
        while True:
            choice = input("请选择 (1/2/3) [默认: 1]: ").strip() or "1"
            
            if choice == "1":
                print()
                print("✅ 配置已确认！启动学习...")
                print()
                return {
                    "topic": self.topic,
                    "depth": self.depth,
                    "time_limit": self.time_limit,
                    "token_budget": self.token_budget,
                    "confirmed": True
                }
            elif choice == "2":
                print()
                print("🔄 重新配置...")
                print()
                # 重新启动交互
                return self.start_interaction(self.topic)
            elif choice == "3":
                print()
                print("❌ 已取消学习")
                print()
                return {"confirmed": False}
            else:
                print("⚠️  请输入 1、2 或 3")
    
    def _get_depth_name(self, depth: str) -> str:
        """获取深度的中文名称"""
        depth_names = {
            "intro": "快速了解 (10分钟)",
            "systematic": "系统学习 (30分钟)",
            "master": "深入精通 (60分钟)"
        }
        return depth_names.get(depth, depth)


def start_interactive_learning(initial_topic: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """
    启动交互式学习配置（便捷函数）
    
    参数:
        initial_topic: 用户最初提到的主题
    
    返回: 学习配置字典，如果用户取消则返回None
    """
    configurator = InteractiveLearningConfigurator()
    config = configurator.start_interaction(initial_topic)
    
    if not config.get('confirmed'):
        return None
    
    return config


if __name__ == "__main__":
    # 测试交互式配置
    print("🧪 交互式学习配置测试")
    print()
    
    config = start_interactive_learning("Python编程")
    
    if config:
        print()
        print("=" * 60)
        print("📊 最终配置:")
        print("=" * 60)
        print(f"主题: {config['topic']}")
        print(f"深度: {config['depth']}")
        print(f"时间: {config['time_limit']} 分钟")
        print(f"Token: {config['token_budget']}")
    else:
        print("\n❌ 用户取消了配置")