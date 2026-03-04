#!/usr/bin/env python3
"""
自主学习技能 - 自动设置钩子
当 OpenClaw 加载此技能时，会自动执行此脚本
"""

import json
import os
import sys
from pathlib import Path


def check_learner_agent():
    """检查 Learner Agent 是否存在"""
    config_file = Path.home() / ".openclaw" / "openclaw.json"
    
    if not config_file.exists():
        print("⚠️  OpenClaw 配置文件不存在")
        return False
    
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # 检查 agents.list 中是否有 learner
        for agent in config.get('agents', {}).get('list', []):
            if agent.get('id') == 'learner':
                print("✅ Learner Agent 已存在")
                return True
        
        return False
    except Exception as e:
        print(f"❌ 检查失败: {e}")
        return False


def create_learner_agent():
    """创建 Learner Agent"""
    config_file = Path.home() / ".openclaw" / "openclaw.json"
    
    try:
        # 读取配置
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # 备份原配置
        backup_file = config_file.with_suffix('.json.backup')
        with open(backup_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        # 添加 learner agent
        learner_agent = {
            "id": "learner",
            "workspace": str(Path.home() / ".openclaw" / "learner-workspace"),
            "model": {
                "primary": "doubao/ark-code-latest",
                "fallbacks": ["zhipu/glm-5", "deepseek/deepseek-chat"]
            },
            "identity": {
                "name": "LearnerBot",
                "theme": "自主学习专家",
                "emoji": "📚"
            },
            "groupChat": {
                "mentionPatterns": ["@learner", "@学习", "@learn"]
            }
        }
        
        # 检查是否已存在
        exists = False
        for agent in config['agents']['list']:
            if agent['id'] == 'learner':
                exists = True
                break
        
        if not exists:
            config['agents']['list'].append(learner_agent)
            print("✅ Learner Agent 已添加到配置")
        
        # 更新 main agent 的 allowAgents
        for agent in config['agents']['list']:
            if agent['id'] == 'main':
                if 'subagents' not in agent:
                    agent['subagents'] = {}
                if 'allowAgents' not in agent['subagents']:
                    agent['subagents']['allowAgents'] = []
                
                # 添加 learner 到 allowAgents（如果不存在）
                if 'learner' not in agent['subagents']['allowAgents']:
                    agent['subagents']['allowAgents'].append('learner')
                    print("✅ Learner Agent 已添加到 main agent 的 allowAgents")
        
        # 保存配置
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        print("✅ OpenClaw 配置已更新")
        return True
        
    except Exception as e:
        print(f"❌ 创建失败: {e}")
        return False


def create_workspace():
    """创建 Learner Agent 工作空间"""
    workspace = Path.home() / ".openclaw" / "learner-workspace"
    
    if not workspace.exists():
        workspace.mkdir(parents=True)
        (workspace / "skills").mkdir()
        (workspace / "memory").mkdir()
        
        # 创建 AGENTS.md
        agents_md = workspace / "AGENTS.md"
        agents_md.write_text("""# AGENTS.md - LearnerBot Workspace

这是 LearnerBot 的工作空间。

## 工作流程

1. 接收学习任务
2. 使用 agent-browser 搜索信息
3. 生成技能内容
4. 执行质量验证
5. 返回结果

## 输出目录

- `skills/` - 生成的技能
- `memory/` - 学习记忆
""")
        
        print("✅ 工作空间已创建")
    else:
        print("✅ 工作空间已存在")


def main():
    """主函数"""
    print("=" * 50)
    print("🧠 自主学习技能 - 自动设置")
    print("=" * 50)
    print()
    
    # 检查 Learner Agent
    if check_learner_agent():
        print("✅ Learner Agent 已配置，无需操作")
        return 0
    
    print("⚠️  Learner Agent 不存在，开始创建...")
    print()
    
    # 创建 Learner Agent
    if not create_learner_agent():
        print("❌ 创建 Learner Agent 失败")
        return 1
    
    print()
    
    # 创建工作空间
    create_workspace()
    
    print()
    print("=" * 50)
    print("✅ 自主学习技能设置完成！")
    print("=" * 50)
    print()
    print("⚠️  重要：需要重启 OpenClaw 使配置生效")
    print("   重启命令: openclaw gateway restart")
    print()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
