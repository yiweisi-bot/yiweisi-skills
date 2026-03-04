#!/usr/bin/env python3
"""
自主学习系统 - 完整启动流程

流程：
1. 【交互阶段】主Agent与用户交互，明确学习目标
2. 【确认阶段】用户确认配置
3. 【执行阶段】启动子Agent执行学习（无需交互）

使用方法:
    python3 start_learning.py [主题]
    
示例:
    python3 start_learning.py "Python装饰器"
    python3 start_learning.py "Docker容器化"
    python3 start_learning.py  # 不带参数将询问主题
"""

import sys
import os
import subprocess
import json
from typing import Dict, Optional, Any
from pathlib import Path

# 添加当前目录到Python路径
sys.path.insert(0, str(Path(__file__).parent))

from autonomous_learning_interactive import start_interactive_learning


def spawn_learner_agent(config: Dict[str, Any]) -> bool:
    """
    启动Learner Agent执行学习（非交互式）
    
    参数:
        config: 学习配置
    
    返回: 是否成功启动
    """
    topic = config['topic']
    depth = config['depth']
    time_limit = config['time_limit']
    token_budget = config['token_budget']
    
    # 构建任务描述
    task = f"""执行自主学习任务

## 学习配置（已通过交互式配置确认）
- 主题: {topic}
- 深度: {depth}
- 时间限制: {time_limit} 分钟
- Token预算: {token_budget} tokens

## 学习任务

请执行以下自主学习流程：

### Phase 1: 信息收集（使用agent-browser）
1. 搜索与「{topic}」相关的高质量资料
2. 访问权威网站，收集技术文档、最佳实践、案例分析
3. 记录关键信息点和核心概念

### Phase 2: 知识整理与提炼
1. 整理收集到的信息，去重和筛选
2. 提炼核心概念和关键知识点
3. 组织成结构化的知识体系

### Phase 3: 生成技能文档（SKILL.md格式）
请生成一份高质量的博客写作技能文档，包含以下章节：

```markdown
---
name: [技能名称]
description: [简短描述]
read_when:
  - [使用场景1]
  - [使用场景2]
metadata:
  emoji: "📝"
  author: "LearnerAgent"
  version: "1.0"
---

# [技能标题]

## 简介
[技能的整体介绍]

## 使用场景
- 场景1
- 场景2

## 核心概念/原理
[详细解释核心概念]

## 实践方法/步骤
1. 步骤一
2. 步骤二
3. 步骤三

## 最佳实践
- 实践建议1
- 实践建议2

## 常见问题与解决方案
**Q1: [常见问题]**  
A: [解决方案]

## 进阶资源
- [资源名称](链接)

## 总结
[技能要点总结]
```

### 质量要求
1. 内容准确性：技术概念准确，示例可运行
2. 结构清晰：章节逻辑清晰，易于阅读
3. 实用性强：包含实际案例和最佳实践
4. 格式规范：符合SKILL.md标准格式

### 输出要求
1. 将生成的技能文档保存到：`~/.openclaw/learner-workspace/skills/`
2. 文件名格式：`[主题].md`，使用英文小写和连字符
3. 返回学习结果摘要，包括：
   - 学习主题
   - 学习深度
   - 生成的技能文件路径
   - 内容概要（200字以内）

## 重要提醒

⚠️ **质量优先**：宁可内容精简，也要确保准确性和实用性  
⚠️ **格式规范**：严格遵循SKILL.md格式，便于后续使用  
⚠️ **来源可靠**：优先参考官方文档和权威资源  
⚠️ **实践导向**：多提供实际可操作的示例和建议

现在开始执行自主学习任务！
"""
    
    print("\n" + "=" * 60)
    print("🚀 启动 Learner Agent 执行学习...")
    print("=" * 60)
    print()
    print("📋 任务摘要:")
    print(f"   📚 主题: {topic}")
    print(f"   🎯 深度: {depth}")
    print(f"   ⏰ 时间: {time_limit} 分钟")
    print(f"   💰 Token: {token_budget}")
    print()
    
    # 检查是否可以使用 openclaw sessions_spawn
    try:
        # 构建命令
        cmd = [
            "openclaw", "sessions", "spawn",
            "--runtime", "subagent",
            "--agent", "learner",
            "--mode", "run",
            "--task", task
        ]
        
        print("🤖 执行命令:")
        print(f"   {' '.join(cmd[:8])}...")
        print()
        
        # 执行命令
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=3600  # 1小时超时
        )
        
        if result.returncode == 0:
            print("✅ Learner Agent 执行成功！")
            if result.stdout:
                print("\n📤 输出:")
                print(result.stdout)
            return True
        else:
            print(f"❌ Learner Agent 执行失败 (返回码: {result.returncode})")
            if result.stderr:
                print("\n📥 错误信息:")
                print(result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print("⏰ Learner Agent 执行超时（超过1小时）")
        return False
    except FileNotFoundError:
        print("⚠️  openclaw 命令未找到，尝试使用 Python 直接调用...")
        return _spawn_with_python(task)
    except Exception as e:
        print(f"❌ 启动 Learner Agent 时出错: {e}")
        return False


def _spawn_with_python(task: str) -> bool:
    """使用 Python 直接调用 sessions_spawn 模块"""
    try:
        # 这里可以实现直接调用 OpenClaw 的 Python API
        # 暂时返回失败，让上层处理
        print("⚠️  Python 直接调用暂未实现")
        return False
    except Exception as e:
        print(f"❌ Python 调用失败: {e}")
        return False


def main():
    """主函数"""
    # 获取命令行参数（可选的学习主题）
    initial_topic = sys.argv[1] if len(sys.argv) > 1 else None
    
    print("=" * 60)
    print("🎓 自主学习系统")
    print("=" * 60)
    print()
    print("流程: 交互配置 → 确认 → 启动Learner Agent")
    print()
    
    # 步骤1: 交互式配置（主Agent与用户对话）
    config = start_interactive_learning(initial_topic)
    
    if not config:
        print("\n❌ 学习已取消")
        return 1
    
    # 步骤2: 启动 Learner Agent 执行学习（非交互式）
    success = spawn_learner_agent(config)
    
    if success:
        print("\n" + "=" * 60)
        print("✅ 自主学习完成！")
        print("=" * 60)
        print()
        print("📄 生成的技能文档已保存到:")
        print(f"   ~/.openclaw/learner-workspace/skills/")
        print()
        return 0
    else:
        print("\n" + "=" * 60)
        print("❌ 学习执行失败")
        print("=" * 60)
        return 1


if __name__ == "__main__":
    sys.exit(main())
