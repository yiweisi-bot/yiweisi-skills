#!/usr/bin/env python3
"""
自主学习系统 - 主CLI入口
"""

import sys
import os
import argparse
import json
from pathlib import Path

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db import get_db


def print_banner():
    """打印欢迎横幅"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║                    🧠 自主学习系统                           ║
║              OpenClaw Agent Autonomous Learning                      ║
╚══════════════════════════════════════════════════════════════╝
    """)


def show_help():
    """显示帮助信息"""
    print("""
可用命令:

  基础命令:
    help              - 显示帮助信息
    status            - 查看学习系统状态
    learn now         - 立即开始学习（手动触发）
    learn topic <topic> - 学习指定主题
    learn github       - 只学习 GitHub 内容

  目标管理:
    goal add <goal>   - 添加学习目标
    goal list         - 列出所有学习目标
    goal remove <id>   - 移除学习目标

  学习历史:
    history show      - 显示学习历史
    history skills    - 显示生成的技能
    history topics    - 显示已学主题

  技能管理:
    skills list       - 列出所有自动生成的技能
    skills review    - 审核待确认的技能

示例:
  autonomous-learning help
  autonomous-learning status
  autonomous-learning learn now
  autonomous-learning goal add "学习 React 19"
  autonomous-learning learn topic "Python 异步编程"
    """)


def show_status():
    """显示学习系统状态"""
    print("📊 学习系统状态\n")
    
    db = get_db()
    
    # 学习目标统计
    goals = db.list_goals()
    pending_goals = [g for g in goals if g['status'] == 'pending']
    in_progress_goals = [g for g in goals if g['status'] == 'in_progress']
    completed_goals = [g for g in goals if g['status'] == 'completed']
    
    print(f"📚 学习目标:")
    print(f"   • 待开始: {len(pending_goals)}")
    print(f"   • 进行中: {len(in_progress_goals)}")
    print(f"   • 已完成: {len(completed_goals)}")
    print(f"   • 总计: {len(goals)}")
    
    # 生成的技能统计
    skills = db.list_skills()
    pending_skills = [s for s in skills if s['validation_status'] == 'pending']
    approved_skills = [s for s in skills if s['validation_status'] == 'human_approved']
    
    print(f"\n✨ 生成技能:")
    print(f"   • 待审核: {len(pending_skills)}")
    print(f"   • 已通过: {len(approved_skills)}")
    print(f"   • 总计: {len(skills)}")
    
    # 待学习列表
    backlog = db.list_backlog()
    print(f"\n📋 待学习列表: {len(backlog)} 项")
    
    # 数据库位置
    print(f"\n💾 数据库: {db.db_path}")


def list_goals():
    """列出学习目标"""
    db = get_db()
    goals = db.list_goals()
    
    if not goals:
        print("📚 暂无学习目标")
        return
    
    print("📚 学习目标列表:\n")
    
    for goal in goals:
        status_emoji = {
            'pending': '⏳',
            'in_progress': '🔄',
            'completed': '✅',
            'paused': '⏸️',
            'cancelled': '❌'
        }.get(goal['status'], '❓')
        
        priority_emoji = {
            1: '🟢',
            2: '🟡',
            3: '🔴'
        }.get(goal['priority'], '⚪')
        
        print(f"{status_emoji} [{goal['id']}. {priority_emoji} {goal['title']}")
        print(f"    状态: {goal['status']} | 优先级: {goal['priority']}")
        print(f"    创建: {goal['created_at']}")
        if goal['description']:
            print(f"    描述: {goal['description']}")
        print()


def add_goal(title: str, description: str = None):
    """添加学习目标"""
    db = get_db()
    goal_id = db.create_goal(
        title=title,
        description=description,
        priority=2  # 默认中优先级
    )
    print(f"✅ 已添加学习目标: {title} (ID: {goal_id})")


def remove_goal(goal_id: int):
    """移除学习目标"""
    # 注意：这里我们只更新状态为 cancelled，而不是真正删除
    db = get_db()
    success = db.update_goal_status(goal_id, 'cancelled')
    if success:
        print(f"✅ 已取消学习目标 (ID: {goal_id})")
    else:
        print(f"❌ 未找到学习目标 (ID: {goal_id})")


def list_skills():
    """列出生成的技能"""
    db = get_db()
    skills = db.list_skills()
    
    if not skills:
        print("✨ 暂无生成的技能")
        return
    
    print("✨ 生成的技能列表:\n")
    
    for skill in skills:
        status_emoji = {
            'pending': '⏳',
            'rule_passed': '✅',
            'ai_approved': '🤖',
            'human_approved': '🎉',
            'rejected': '❌'
        }.get(skill['validation_status'], '❓')
        
        print(f"{status_emoji} [{skill['id']}. {skill['title']}")
        print(f"    状态: {skill['validation_status']}")
        print(f"    文件: {skill['file_path']}")
        print(f"    创建: {skill['created_at']}")
        if skill['quality_score']:
            print(f"    质量分: {skill['quality_score']}/100")
        print()


def learn_now():
    """立即开始学习"""
    from database.learning_manager import get_learning_manager
    
    print("\n🚀 开始学习流程...\n")
    
    manager = get_learning_manager()
    
    # 检查是否有待开始的目标
    goals = manager.db.list_goals(status='pending')
    
    if not goals:
        print("❌ 没有待开始的学习目标")
        print("请先运行: autonomous-learning goal add \"学习主题\"")
        return
    
    # 选择第一个目标
    goal = goals[0]
    print(f"📚 选择目标: {goal['title']}")
    print()
    
    # 开始学习
    print("🎯 启动学习会话...")
    session_result = manager.start_learning(goal['id'])
    print(f"   ✅ 会话创建: ID={session_result['session_id']}")
    print()
    
    # 执行循环
    print("🔄 执行 Action-Reflection-Iteration 循环...")
    collected_data = {}
    
    for i in range(1, 4):
        cycle_result = manager.start_iteration_cycle(
            goal_id=goal['id'],
            session_id=session_result['session_id'],
            collected_data=collected_data,
            iteration=i
        )
        
        collected_data = cycle_result['action']['collected_data']
        
        if not cycle_result['decision']['should_continue']:
            print()
            print(f"🎯 循环结束: {cycle_result['decision']['reason']}")
            break
    
    print()
    
    # 4. 生成技能
    print("✨ 开始技能生成...")
    goal = manager.db.get_goal(goal['id'])
    
    skill_result = manager.generate_skill(
        goal_id=goal['id'],
        collected_data=collected_data,
        topic=goal['title'],
        depth='systematic'
    )
    
    print()
    print("🎉 技能生成完成！")
    print(f"   📄 技能标题: {skill_result['skill_title']}")
    print(f"   📁 文件位置: {skill_result['filepath']}")
    print(f"   💾 数据库ID: {skill_result['skill_id']}")
    
    # 显示质量验证结果
    validation = skill_result.get('validation', {})
    if validation:
        print()
        print("🛡️  质量验证结果:")
        overall = validation.get('overall', {})
        print(f"   整体状态: {overall.get('status', 'unknown')}")
        print(f"   总体分数: {overall.get('overall_score', 0):.1f}分")
        
        if 'rule' in validation:
            rule = validation['rule']
            print(f"   规则验证: {'✅ 通过' if rule['passed'] else '❌ 失败'} ({rule['score']:.1f}分)")
        
        if 'ai' in validation:
            ai = validation['ai']
            print(f"   AI验证: {'✅ 通过' if ai['passed'] else '❌ 失败'} ({ai['score']:.1f}分)")
    
    print()
    print("✅ Phase 4 质量验证演示完成！")


def learn_topic(topic: str):
    """学习指定主题"""
    print(f"\n📚 准备学习: {topic}\n")
    print("💡 提示：完整的学习流程即将推出！")
    print(f"已记录学习目标...")
    
    # 添加到学习目标
    db = get_db()
    goal_id = db.create_goal(
        title=f"学习 {topic}",
        description=f"自主学习: {topic}",
        priority=2
    )
    
    print(f"✅ 已创建学习目标 (ID: {goal_id})")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='自主学习系统 - OpenClaw Agent Autonomous Learning',
        add_help=False
    )
    parser.add_argument('command', nargs='?', help='命令')
    parser.add_argument('subcommand', nargs='?', help='子命令')
    parser.add_argument('args', nargs='*', help='参数')
    
    # 解析已知参数
    args = parser.parse_args()
    
    # 打印横幅
    print_banner()
    
    # 处理命令
    if not args.command:
        show_help()
        return
    
    command = args.command.lower()
    
    if command == 'help':
        show_help()
    
    elif command == 'status':
        show_status()
    
    elif command == 'learn':
        if args.subcommand == 'now':
            learn_now()
        elif args.subcommand == 'topic' and args.args:
            topic = ' '.join(args.args)
            learn_topic(topic)
        elif args.subcommand == 'github':
            print("\n🔍 GitHub 学习 GitHub 内容（即将推出）")
        else:
            print("\n❓ 未知的 learn 子命令")
            print("可用: learn now, learn topic <topic>, learn github")
    
    elif command == 'goal':
        if args.subcommand == 'add' and args.args:
            title = ' '.join(args.args)
            add_goal(title)
        elif args.subcommand == 'list':
            list_goals()
        elif args.subcommand == 'remove' and args.args:
            try:
                goal_id = int(args.args[0])
                remove_goal(goal_id)
            except ValueError:
                print("❌ 请提供有效的目标ID")
        else:
            print("\n❓ 未知的 goal 子命令")
            print("可用: goal add <goal>, goal list, goal remove <id>")
    
    elif command == 'history':
        if args.subcommand == 'show':
            print("\n📜 学习历史（即将推出）")
        elif args.subcommand == 'skills':
            list_skills()
        elif args.subcommand == 'topics':
            print("\n📚 已学主题（即将推出）")
        else:
            print("\n❓ 未知的 history 子命令")
            print("可用: history show, history skills, history topics")
    
    elif command == 'skills':
        if args.subcommand == 'list':
            list_skills()
        elif args.subcommand == 'review':
            print("\n🔍 技能审核（即将推出）")
        else:
            print("\n❓ 未知的 skills 子命令")
            print("可用: skills list, skills review")
    
    else:
        print(f"\n❓ 未知命令: {command}")
        show_help()


if __name__ == '__main__':
    main()
