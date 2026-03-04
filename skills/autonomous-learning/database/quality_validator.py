#!/usr/bin/env python3
"""
自主学习系统 - 质量验证器（已更新集成 LLM）
"""

import os
import re
from typing import Dict, List, Optional, Any
from dataclasses import dataclass


@dataclass
class ValidationResult:
    """验证结果"""
    passed: bool
    score: float
    issues: List[str]
    strengths: List[str]
    details: Dict[str, Any]


class RuleValidator:
    """规则验证器"""
    
    def __init__(self):
        self.checks = [
            self._check_frontmatter,
            self._check_title,
            self._check_sections,
            self._check_examples,
            self._check_read_when,
            self._check_content_length
        ]
    
    def validate(self, filepath: str) -> ValidationResult:
        """验证文件"""
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        issues = []
        strengths = []
        total_score = 0
        
        for check in self.checks:
            result = check(content)
            if result['passed']:
                total_score += result['weight']
                if 'strength' in result:
                    strengths.append(result['strength'])
            else:
                issues.append(result['issue'])
        
        # 计算总分（100分制）
        overall_score = (total_score / 6) * 100
        
        return ValidationResult(
            passed=len(issues) == 0,
            score=overall_score,
            issues=issues,
            strengths=strengths,
            details={'checks_passed': 6 - len(issues), 'total_checks': 6}
        )
    
    def _check_frontmatter(self, content: str) -> Dict:
        """检查 Frontmatter"""
        has_frontmatter = content.startswith('---') and '---' in content[3:]
        if has_frontmatter:
            return {'passed': True, 'weight': 1, 'strength': '有正确的 Frontmatter'}
        return {'passed': False, 'weight': 1, 'issue': '缺少 Frontmatter'}
    
    def _check_title(self, content: str) -> Dict:
        """检查标题"""
        has_title = '# ' in content
        if has_title:
            return {'passed': True, 'weight': 1, 'strength': '有主标题'}
        return {'passed': False, 'weight': 1, 'issue': '缺少主标题'}
    
    def _check_sections(self, content: str) -> Dict:
        """检查章节"""
        sections = content.count('## ')
        if sections >= 3:
            return {'passed': True, 'weight': 1, 'strength': f'有 {sections} 个章节'}
        return {'passed': False, 'weight': 1, 'issue': '章节不足（需要至少3个）'}
    
    def _check_examples(self, content: str) -> Dict:
        """检查示例"""
        has_examples = '```' in content
        if has_examples:
            return {'passed': True, 'weight': 1, 'strength': '有代码示例'}
        return {'passed': False, 'weight': 1, 'issue': '缺少代码示例'}
    
    def _check_read_when(self, content: str) -> Dict:
        """检查 read_when"""
        has_read_when = 'read_when:' in content
        if has_read_when:
            return {'passed': True, 'weight': 1, 'strength': '有 read_when 部分'}
        return {'passed': False, 'weight': 1, 'issue': '缺少 read_when 部分'}
    
    def _check_content_length(self, content: str) -> Dict:
        """检查内容长度"""
        length = len(content)
        if length >= 1000:
            return {'passed': True, 'weight': 1, 'strength': f'内容充足（{length} 字符）'}
        return {'passed': False, 'weight': 1, 'issue': '内容太短（需要至少1000字符）'}


class AIValidator:
    """AI验证器（使用真实LLM集成）"""
    
    def validate(self, filepath: str) -> ValidationResult:
        """验证文件（使用真实LLM）"""
        from database.real_llm_integration import get_real_llm_integration
        llm = get_real_llm_integration()
        
        # 使用 LLM 验证
        result = llm.validate_skill_with_llm(filepath)
        
        return ValidationResult(
            passed=result.get('passed', True),
            score=result.get('score', 85),
            issues=result.get('issues', []),
            strengths=result.get('strengths', []),
            details=result.get('details', {})
        )


def validate_skill_updated(filepath: str) -> Dict[str, Any]:
    """
    验证技能（三层验证，已更新集成LLM）
    
    返回: 验证结果字典
    """
    print(f"🛡️  开始质量验证（已更新）...")
    
    # 第一层：规则验证
    print(f"   1️⃣  规则验证...")
    rule_validator = RuleValidator()
    rule_result = rule_validator.validate(filepath)
    print(f"      规则: {'✅ 通过' if rule_result.passed else '❌ 失败'}")
    print(f"      分数: {rule_result.score:.1f}")
    
    if not rule_result.passed:
        print(f"      问题: {rule_result.issues}")
        return {
            'overall': {
                'status': 'rule_failed',
                'overall_score': rule_result.score
            },
            'rule': rule_result,
            'ai': None,
            'human': None
        }
    
    # 第二层：AI验证（使用真实LLM）
    print(f"   2️⃣  AI验证（真实LLM）...")
    ai_validator = AIValidator()
    ai_result = ai_validator.validate(filepath)
    print(f"      AI: {'✅ 通过' if ai_result.passed else '❌ 失败'}")
    print(f"      分数: {ai_result.score:.1f}")
    print(f"      优点: {ai_result.strengths[:3]}")
    
    if ai_result.score < 70:
        print(f"      AI分数不足70分，需要改进")
        return {
            'overall': {
                'status': 'ai_failed',
                'overall_score': (rule_result.score + ai_result.score) / 2
            },
            'rule': rule_result,
            'ai': ai_result,
            'human': None
        }
    
    # 第三层：人工验证
    print(f"   3️⃣  人工验证...")
    print(f"      ⏳ 等待人工确认")
    
    overall_score = (rule_result.score * 0.3 + ai_result.score * 0.7)
    
    return {
        'overall': {
            'status': 'pending_human',
            'overall_score': overall_score
        },
        'rule': rule_result,
        'ai': ai_result,
        'human': {
            'status': 'pending',
            'result': None,
            'feedback': None
        }
    }


if __name__ == '__main__':
    # 测试
    print("🧪 更新版质量验证器测试\n")
    
    # 需要一个测试文件
    import tempfile
    test_content = """---
name: 测试技能
description: 这是一个测试技能
read_when:
  - 需要测试
metadata: {"emoji":"🧪","author":"乙维斯"}
---

# 测试技能

## 什么时候使用

1. 场景1：测试用
2. 场景2：验证用

## 快速开始

```bash
echo "test"
```

## 核心概念

这是核心概念章节。

内容足够长，超过1000字符...
"""
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
        f.write(test_content)
        temp_file = f.name
    
    try:
        result = validate_skill_updated(temp_file)
        print(f"\n✅ 验证完成！")
        print(f"   总体状态: {result['overall']['status']}")
        print(f"   总体分数: {result['overall']['overall_score']:.1f}")
    finally:
        import os
        os.unlink(temp_file)
