#!/usr/bin/env python3
"""
LearnerBot - 带实时进度反馈的学习 Agent
"""

import sys
import os
import time
import json
from typing import Dict, Any, List


class LearnerBotWithProgress:
    """带实时进度反馈的 LearnerBot"""
    
    def __init__(self):
        self.progress_steps = [
            {"stage": "信息收集", "step": "初始化学习任务", "progress": 0},
            {"stage": "信息收集", "step": "使用 agent-browser 搜索", "progress": 10},
            {"stage": "信息收集", "step": "提取搜索结果", "progress": 20},
            {"stage": "信息收集", "step": "分析关键信息", "progress": 30},
            {"stage": "技能生成", "step": "设计技能大纲", "progress": 40},
            {"stage": "技能生成", "step": "生成核心概念", "progress": 50},
            {"stage": "技能生成", "step": "生成实用示例", "progress": 60},
            {"stage": "技能生成", "step": "生成最佳实践", "progress": 70},
            {"stage": "质量验证", "step": "执行规则验证", "progress": 80},
            {"stage": "质量验证", "step": "执行 AI 验证", "progress": 90},
            {"stage": "完成", "step": "返回学习结果", "progress": 100}
        ]
        self.current_step = 0
        self.parent_session = None
    
    def set_parent_session(self, session_key: str):
        """设置父 session，用于发送进度更新"""
        self.parent_session = session_key
    
    def learn(self, topic: str, depth: str = 'systematic', 
             time_limit: int = 30, token_budget: int = 5000) -> Dict[str, Any]:
        """
        执行学习任务（带实时进度反馈）
        
        参数:
            topic: 学习主题
            depth: 学习深度
            time_limit: 时间限制（分钟）
            token_budget: Token 预算
        
        返回: 学习结果
        """
        print(f"📚 LearnerBot 开始学习: {topic}")
        print()
        
        # 阶段1: 信息收集
        self._report_progress("信息收集", "使用 agent-browser 搜索相关信息...", 0)
        time.sleep(2)
        
        self._report_progress("信息收集", "正在搜索 Google...", 10)
        collected_info = self._collect_information(topic)
        time.sleep(2)
        
        self._report_progress("信息收集", "提取关键信息...", 20)
        time.sleep(1)
        
        self._report_progress("信息收集", f"找到 {collected_info['sources_used']} 个来源", 30)
        time.sleep(1)
        
        # 阶段2: 技能生成
        self._report_progress("技能生成", "设计技能大纲...", 40)
        time.sleep(2)
        
        self._report_progress("技能生成", "生成核心概念...", 50)
        skill_content = self._generate_skill(topic, collected_info, depth)
        time.sleep(2)
        
        self._report_progress("技能生成", "生成实用示例...", 60)
        time.sleep(1)
        
        self._report_progress("技能生成", "生成最佳实践...", 70)
        time.sleep(1)
        
        # 阶段3: 质量验证
        self._report_progress("质量验证", "执行规则验证...", 80)
        validation_result = self._validate_skill(skill_content)
        time.sleep(1)
        
        self._report_progress("质量验证", f"AI 验证评分: {validation_result['ai_score']}/100", 90)
        time.sleep(1)
        
        # 完成
        self._report_progress("完成", "学习完成！", 100)
        time.sleep(1)
        
        # 返回最终结果
        result = {
            "status": "completed",
            "skill_title": f"{topic} 学习指南",
            "skill_content": skill_content,
            "collected_info": collected_info,
            "validation_result": validation_result
        }
        
        print()
        print("✅ 学习完成！")
        
        return result
    
    def _report_progress(self, stage: str, message: str, progress: int):
        """
        报告进度（实时反馈）
        
        参数:
            stage: 当前阶段
            message: 进度消息
            progress: 进度百分比 (0-100)
        """
        # 1. 在本地输出
        progress_bar = self._get_progress_bar(progress)
        print(f"\r{progress_bar} [{progress:3d}%] {stage}: {message}", end="", flush=True)
        
        # 2. 发送进度到父 session（如果设置了）
        if self.parent_session:
            self._send_progress_to_parent(stage, message, progress)
    
    def _get_progress_bar(self, progress: int, width: int = 20) -> str:
        """生成进度条"""
        filled = int(width * progress / 100)
        empty = width - filled
        return "█" * filled + "░" * empty
    
    def _send_progress_to_parent(self, stage: str, message: str, progress: int):
        """
        发送进度到父 session
        
        这需要使用 sessions_send 工具
        """
        try:
            # 使用 sessions_send 发送进度更新
            from tools import sessions_send
            
            progress_message = f"""
📊 学习进度更新

阶段: {stage}
进度: {progress}%
详情: {message}

{self._get_progress_bar(progress)}
"""
            
            sessions_send(
                sessionKey=self.parent_session,
                message=progress_message
            )
        except Exception as e:
            # 如果发送失败，只记录本地日志
            print(f"\n⚠️  进度发送失败: {e}")
    
    def _collect_information(self, topic: str) -> Dict[str, Any]:
        """收集信息（模拟）"""
        return {
            "sources_used": 8,
            "key_concepts": ["概念1", "概念2", "概念3", "概念4", "概念5"],
            "search_summary": f"通过 agent-browser 搜索了 {topic} 相关的 8 个高质量来源"
        }
    
    def _generate_skill(self, topic: str, info: Dict, depth: str) -> str:
        """生成技能（模拟）"""
        return f"""# {topic} 学习指南

## 使用场景
...

## 快速开始
...

## 核心概念
...

## 实用示例
...

## 最佳实践
...

## 常见问题
...
"""
    
    def _validate_skill(self, skill_content: str) -> Dict[str, Any]:
        """验证技能（模拟）"""
        return {
            "rule_check": "passed",
            "ai_score": 87.5,
            "overall": "passed"
        }


def learn_with_progress(topic: str, depth: str = 'systematic',
                       time_limit: int = 30, token_budget: int = 5000,
                       parent_session: str = None) -> Dict[str, Any]:
    """
    带进度反馈的学习（便捷函数）
    
    参数:
        topic: 学习主题
        depth: 学习深度
        time_limit: 时间限制
        token_budget: Token 预算
        parent_session: 父 session key（用于发送进度）
    
    返回: 学习结果
    """
    bot = LearnerBotWithProgress()
    
    if parent_session:
        bot.set_parent_session(parent_session)
    
    return bot.learn(topic, depth, time_limit, token_budget)


if __name__ == "__main__":
    # 测试
    print("🧪 LearnerBot 进度反馈测试")
    print()
    
    result = learn_with_progress(
        topic="TypeScript 基础类型",
        depth="systematic",
        time_limit=30,
        token_budget=5000
    )
    
    print()
    print("=" * 50)
    print("📊 学习结果:")
    print("=" * 50)
    print(f"状态: {result['status']}")
    print(f"技能: {result['skill_title']}")
    print(f"评分: {result['validation_result']['ai_score']}/100")
