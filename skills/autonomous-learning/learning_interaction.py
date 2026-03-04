#!/usr/bin/env python3
"""
自主学习系统 - 交互式学习启动器
在开始学习前，通过几轮反问明确学习目标
"""

import sys
import os
from typing import Dict, Any, Optional


class LearningInteraction:
    """学习前的交互式对话"""
    
    def __init__(self):
        self.topic = None
        self.depth = None
        self.time_limit = None
        self.token_budget = None
    
    def start_interaction(self, initial_topic: Optional[str] = None) -> Dict[str, Any]:
        """
        开始交互式对话
        
        参数:
            initial_topic: 用户最初提到的主题（可能不明确）
        
        返回: 学习配置
        """
        print("🎯 自主学习启动向导")
        print("=" * 50)
        print()
        
        # 问题1: 明确学习主题
        self.topic = self._ask_topic(initial_topic)
        print()
        
        # 问题2: 选择学习深度
        self.depth = self._ask_depth()
        print()
        
        # 问题3: 确认时间限制
        self.time_limit = self._ask_time_limit()
        print()
        
        # 问题4: 选择 Token 预算
        self.token_budget = self._ask_token_budget()
        print()
        
        # 最终确认
        config = self._confirm_config()
        
        return config
    
    def _ask_topic(self, initial_topic: Optional[str]) -> str:
        """问题1: 明确学习主题"""
        print("📝 问题 1/4: 学习主题")
        print("-" * 50)
        
        if initial_topic:
            print(f"你提到想学习: {initial_topic}")
            print()
            print("请确认或细化学习主题：")
            print(f"  1. 直接学习「{initial_topic}」")
            print("  2. 我想更具体一点...")
            print("  3. 我想换个主题")
            print()
            
            choice = input("请选择 (1/2/3) [默认: 1]: ").strip() or "1"
            
            if choice == "1":
                return initial_topic
            elif choice == "2":
                specific = input(f"请输入更具体的主题 (例如: {initial_topic} 的高级特性): ").strip()
                return specific if specific else initial_topic
            elif choice == "3":
                new_topic = input("请输入你想学习的主题: ").strip()
                return new_topic if new_topic else initial_topic
            else:
                return initial_topic
        else:
            print("请告诉我你想学习什么？")
            print()
            print("示例:")
            print("  - TypeScript 基础类型")
            print("  - React Hooks")
            print("  - Python 装饰器")
            print("  - Docker 容器化")
            print()
            
            topic = input("学习主题: ").strip()
            
            if not topic:
                print("⚠️  未输入主题，使用默认: 通用编程基础")
                return "通用编程基础"
            
            return topic
    
    def _ask_depth(self) -> str:
        """问题2: 选择学习深度"""
        print("📚 问题 2/4: 学习深度")
        print("-" * 50)
        print("请选择学习深度：")
        print()
        print("  1. 🚀 快速了解 (intro)")
        print("     - 时间: 10 分钟")
        print("     - 适合: 快速了解概念，建立基本认知")
        print("     - 输出: 简明扼要的入门指南")
        print()
        print("  2. 📖 系统学习 (systematic) [推荐]")
        print("     - 时间: 30 分钟")
        print("     - 适合: 系统掌握某个技术")
        print("     - 输出: 完整的技能文档")
        print()
        print("  3. 🎓 深入精通 (master)")
        print("     - 时间: 60 分钟")
        print("     - 适合: 深入理解原理和最佳实践")
        print("     - 输出: 详尽的高级指南")
        print()
        
        choice = input("请选择 (1/2/3) [默认: 2]: ").strip() or "2"
        
        depth_map = {
            "1": "intro",
            "2": "systematic",
            "3": "master"
        }
        
        return depth_map.get(choice, "systematic")
    
    def _ask_time_limit(self) -> int:
        """问题3: 确认时间限制"""
        print("⏰ 问题 3/4: 时间限制")
        print("-" * 50)
        
        # 根据深度推荐时间
        recommended_time = {
            "intro": 10,
            "systematic": 30,
            "master": 60
        }
        
        default_time = recommended_time.get(self.depth, 30)
        
        print(f"当前深度「{self.depth}」推荐时间: {default_time} 分钟")
        print()
        print("请选择时间限制：")
        print(f"  1. 使用推荐时间 ({default_time} 分钟)")
        print("  2. 自定义时间")
        print()
        
        choice = input("请选择 (1/2) [默认: 1]: ").strip() or "1"
        
        if choice == "1":
            return default_time
        elif choice == "2":
            while True:
                try:
                    custom_time = input(f"请输入时间限制（分钟）[默认: {default_time}]: ").strip()
                    if not custom_time:
                        return default_time
                    time_int = int(custom_time)
                    if time_int > 0:
                        return time_int
                    else:
                        print("⚠️  时间必须大于 0")
                except ValueError:
                    print("⚠️  请输入有效的数字")
        else:
            return default_time
    
    def _ask_token_budget(self) -> int:
        """问题4: 选择 Token 预算"""
        print("💰 问题 4/4: Token 预算")
        print("-" * 50)
        print("请选择 Token 预算：")
        print()
        print("  1. 💵 经济型 (2000 tokens)")
        print("     - 适合: 简单主题，快速了解")
        print("     - 成本: 最低")
        print()
        print("  2. ⚖️  平衡型 (5000 tokens) [推荐]")
        print("     - 适合: 大多数学习场景")
        print("     - 成本: 适中")
        print()
        print("  3. 💎 质量型 (10000 tokens)")
        print("     - 适合: 复杂主题，高质量输出")
        print("     - 成本: 较高")
        print()
        
        choice = input("请选择 (1/2/3) [默认: 2]: ").strip() or "2"
        
        budget_map = {
            "1": 2000,
            "2": 5000,
            "3": 10000
        }
        
        return budget_map.get(choice, 5000)
    
    def _confirm_config(self) -> Dict[str, Any]:
        """最终确认配置"""
        print("=" * 50)
        print("📋 学习配置确认")
        print("=" * 50)
        print()
        print(f"📚 学习主题: {self.topic}")
        print(f"🎯 学习深度: {self._get_depth_name(self.depth)}")
        print(f"⏰ 时间限制: {self.time_limit} 分钟")
        print(f"💰 Token预算: {self.token_budget}")
        print()
        
        print("确认开始学习吗？")
        print("  1. ✅ 确认，开始学习")
        print("  2. 🔄 重新配置")
        print("  3. ❌ 取消")
        print()
        
        choice = input("请选择 (1/2/3) [默认: 1]: ").strip() or "1"
        
        if choice == "1":
            print()
            print("✅ 配置已确认！")
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
            return self.start_interaction(self.topic)
        else:
            print()
            print("❌ 已取消")
            print()
            return {
                "confirmed": False
            }
    
    def _get_depth_name(self, depth: str) -> str:
        """获取深度的中文名称"""
        depth_names = {
            "intro": "快速了解 (intro)",
            "systematic": "系统学习 (systematic)",
            "master": "深入精通 (master)"
        }
        return depth_names.get(depth, depth)


def interactive_learning_start(initial_topic: Optional[str] = None) -> Dict[str, Any]:
    """
    交互式学习启动（便捷函数）
    
    参数:
        initial_topic: 用户最初提到的主题
    
    返回: 学习配置
    """
    interaction = LearningInteraction()
    return interaction.start_interaction(initial_topic)


if __name__ == "__main__":
    # 测试
    print("🧪 交互式学习启动器测试")
    print()
    
    config = interactive_learning_start("TypeScript")
    
    print()
    print("=" * 50)
    print("📊 最终配置:")
    print("=" * 50)
    for key, value in config.items():
        print(f"  {key}: {value}")
