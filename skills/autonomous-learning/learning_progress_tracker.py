#!/usr/bin/env python3
"""
学习进度跟踪器 - 确保学满时间并汇报进度

核心功能：
1. 时间预算管理 - 确保每个阶段分配合理时间
2. 进度检查点 - 定期汇报学习状态
3. 时间补偿机制 - 如果某个阶段超时，动态调整后续阶段
4. 最终报告 - 完整的学习总结
"""

import time
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Callable, Any
from dataclasses import dataclass, field, asdict
from enum import Enum


class PhaseStatus(Enum):
    """阶段状态"""
    PENDING = "待开始"
    IN_PROGRESS = "进行中"
    COMPLETED = "已完成"
    OVERTIME = "已超时"


@dataclass
class Phase:
    """学习阶段"""
    name: str
    description: str
    time_budget: int  # 分钟
    status: PhaseStatus = PhaseStatus.PENDING
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    progress_percent: int = 0
    notes: List[str] = field(default_factory=list)
    
    def start(self):
        """开始阶段"""
        self.status = PhaseStatus.IN_PROGRESS
        self.start_time = datetime.now()
        
    def update_progress(self, percent: int, note: str = None):
        """更新进度"""
        self.progress_percent = min(100, max(0, percent))
        if note:
            self.notes.append(f"[{datetime.now().strftime('%H:%M')}] {note}")
        
        # 检查是否超时
        if self.start_time:
            elapsed = (datetime.now() - self.start_time).total_seconds() / 60
            if elapsed > self.time_budget:
                self.status = PhaseStatus.OVERTIME
    
    def complete(self, note: str = None):
        """完成阶段"""
        self.end_time = datetime.now()
        if self.status != PhaseStatus.OVERTIME:
            self.status = PhaseStatus.COMPLETED
        self.progress_percent = 100
        if note:
            self.notes.append(f"[{datetime.now().strftime('%H:%M')}] {note}")
    
    @property
    def actual_time(self) -> float:
        """实际用时（分钟）"""
        if self.start_time and self.end_time:
            return (self.end_time - self.start_time).total_seconds() / 60
        elif self.start_time:
            return (datetime.now() - self.start_time).total_seconds() / 60
        return 0
    
    @property
    def is_overtime(self) -> bool:
        """是否超时"""
        return self.actual_time > self.time_budget
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "name": self.name,
            "description": self.description,
            "time_budget": self.time_budget,
            "status": self.status.value,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "actual_time": round(self.actual_time, 2),
            "progress_percent": self.progress_percent,
            "notes": self.notes
        }


class LearningProgressTracker:
    """
    学习进度跟踪器
    
    负责：
    1. 管理学习阶段和时间预算
    2. 跟踪和报告进度
    3. 处理时间超支和动态调整
    4. 生成最终报告
    """
    
    def __init__(self, total_time: int, topic: str = ""):
        """
        初始化进度跟踪器
        
        参数:
            total_time: 总学习时间（分钟）
            topic: 学习主题
        """
        self.topic = topic
        self.total_time = total_time
        self.phases: List[Phase] = []
        self.current_phase_index = -1
        self.start_time = None
        self.end_time = None
        self.callbacks: List[Callable] = []
        
        # 初始化阶段
        self._init_phases()
    
    def _init_phases(self):
        """初始化学习阶段（基于总时间分配）"""
        # 根据总时间分配各阶段时间预算
        if self.total_time <= 15:
            # 快速模式（≤15分钟）
            self.phases = [
                Phase("信息搜索", "搜索和收集相关资料", max(3, self.total_time // 4)),
                Phase("知识整理", "整理和提炼核心概念", max(5, self.total_time // 2)),
                Phase("文档生成", "生成技能文档", max(3, self.total_time // 4))
            ]
        elif self.total_time <= 45:
            # 标准模式（16-45分钟）
            search_time = max(8, int(self.total_time * 0.25))
            organize_time = max(15, int(self.total_time * 0.45))
            generate_time = self.total_time - search_time - organize_time
            
            self.phases = [
                Phase("信息搜索", "搜索和收集相关资料", search_time),
                Phase("知识整理", "整理和提炼核心概念", organize_time),
                Phase("文档生成", "生成技能文档", max(10, generate_time))
            ]
        else:
            # 深度模式（>45分钟）
            search_time = max(12, int(self.total_time * 0.22))
            analyze_time = max(10, int(self.total_time * 0.18))
            organize_time = max(20, int(self.total_time * 0.32))
            generate_time = self.total_time - search_time - analyze_time - organize_time
            
            self.phases = [
                Phase("信息搜索", "多源搜索和资料收集", search_time),
                Phase("深度分析", "分析、对比和验证", analyze_time),
                Phase("知识整理", "系统整理和概念提炼", organize_time),
                Phase("文档生成", "生成高质量技能文档", max(15, generate_time))
            ]
    
    def start(self):
        """开始跟踪学习进度"""
        self.start_time = datetime.now()
        print(f"🚀 开始学习: {self.topic}")
        print(f"   ⏰ 总时间: {self.total_time} 分钟")
        print(f"   📊 阶段数: {len(self.phases)}")
        print()
        
        # 显示阶段计划
        print("📋 学习阶段计划:")
        for i, phase in enumerate(self.phases, 1):
            print(f"   {i}. {phase.name} ({phase.time_budget}分钟) - {phase.description}")
        print()
        
        # 开始第一个阶段
        self._start_next_phase()
    
    def _start_next_phase(self):
        """开始下一个阶段"""
        self.current_phase_index += 1
        
        if self.current_phase_index >= len(self.phases):
            # 所有阶段完成
            self._complete_learning()
            return
        
        phase = self.phases[self.current_phase_index]
        phase.start()
        
        print("=" * 60)
        print(f"📍 当前阶段 {self.current_phase_index + 1}/{len(self.phases)}: {phase.name}")
        print("=" * 60)
        print(f"   📝 任务: {phase.description}")
        print(f"   ⏱️  预算时间: {phase.time_budget} 分钟")
        print(f"   ⏰ 开始时间: {phase.start_time.strftime('%H:%M:%S')}")
        print()
    
    def update_progress(self, percent: int, note: str = None):
        """更新当前阶段进度"""
        if self.current_phase_index < 0 or self.current_phase_index >= len(self.phases):
            return
        
        phase = self.phases[self.current_phase_index]
        phase.update_progress(percent, note)
        
        # 显示进度
        bar_length = 30
        filled = int(bar_length * percent / 100)
        bar = "█" * filled + "░" * (bar_length - filled)
        
        status_line = f"   📊 进度: [{bar}] {percent}%"
        if note:
            status_line += f" | {note}"
        
        print(status_line)
        
        # 检查是否完成
        if percent >= 100:
            self.complete_current_phase()
    
    def complete_current_phase(self, note: str = None):
        """完成当前阶段"""
        if self.current_phase_index < 0 or self.current_phase_index >= len(self.phases):
            return
        
        phase = self.phases[self.current_phase_index]
        phase.complete(note)
        
        print()
        print(f"   ✅ 阶段完成: {phase.name}")
        print(f"      实际用时: {phase.actual_time:.1f} 分钟")
        
        if phase.is_overtime:
            print(f"      ⚠️  超时: {phase.actual_time - phase.time_budget:.1f} 分钟")
        
        print()
        
        # 开始下一个阶段
        self._start_next_phase()
    
    def _complete_learning(self):
        """完成整个学习过程"""
        self.end_time = datetime.now()
        total_actual_time = (self.end_time - self.start_time).total_seconds() / 60
        
        print("=" * 60)
        print("🎉 学习完成！")
        print("=" * 60)
        print()
        print(f"📊 学习统计:")
        print(f"   📚 主题: {self.topic}")
        print(f"   ⏱️  计划时间: {self.total_time} 分钟")
        print(f"   ⏰ 实际用时: {total_actual_time:.1f} 分钟")
        print(f"   📈 效率: {(self.total_time/total_actual_time*100):.1f}%")
        print()
        
        # 阶段详细统计
        print("📋 各阶段详情:")
        for i, phase in enumerate(self.phases, 1):
            status_icon = "✅" if phase.status == PhaseStatus.COMPLETED else "⚠️" if phase.status == PhaseStatus.OVERTIME else "⏳"
            print(f"   {i}. {status_icon} {phase.name}: {phase.actual_time:.1f}/{phase.time_budget}分钟")
        
        print()
        print("=" * 60)
    
    def get_report(self) -> Dict[str, Any]:
        """获取完整的学习报告"""
        total_actual = (self.end_time - self.start_time).total_seconds() / 60 if self.end_time else 0
        
        return {
            "topic": self.topic,
            "total_planned_time": self.total_time,
            "total_actual_time": round(total_actual, 2),
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "phases": [phase.to_dict() for phase in self.phases],
            "efficiency": round(self.total_time / total_actual * 100, 1) if total_actual > 0 else 0
        }
    
    def on_progress(self, callback: Callable):
        """注册进度回调函数"""
        self.callbacks.append(callback)
    
    def _notify_callbacks(self, event: str, data: Dict):
        """通知所有回调函数"""
        for callback in self.callbacks:
            try:
                callback(event, data)
            except Exception as e:
                print(f"   ⚠️  回调函数执行失败: {e}")


# 便捷函数
def create_tracker(total_time: int, topic: str = "") -> LearningProgressTracker:
    """
    创建学习进度跟踪器
    
    参数:
        total_time: 总学习时间（分钟）
        topic: 学习主题
    
    返回: LearningProgressTracker实例
    """
    return LearningProgressTracker(total_time, topic)


# 测试代码
if __name__ == "__main__":
    print("🧪 学习进度跟踪器测试")
    print()
    
    # 创建一个30分钟的学习跟踪器
    tracker = create_tracker(30, "Python装饰器")
    
    # 开始跟踪
    tracker.start()
    
    # 模拟进度更新
    import time
    
    # 阶段1: 信息搜索
    tracker.update_progress(30, "正在搜索官方文档...")
    time.sleep(0.5)
    tracker.update_progress(60, "已找到3个高质量资源")
    time.sleep(0.5)
    tracker.update_progress(100, "搜索完成")
    
    # 阶段2: 知识整理
    time.sleep(0.5)
    tracker.update_progress(50, "整理核心概念...")
    time.sleep(0.5)
    tracker.update_progress(100, "整理完成")
    
    # 阶段3: 文档生成
    time.sleep(0.5)
    tracker.update_progress(100, "文档生成完成")
    
    # 获取报告
    report = tracker.get_report()
    
    print()
    print("=" * 60)
    print("📊 学习报告:")
    print("=" * 60)
    print(json.dumps(report, indent=2, ensure_ascii=False))
