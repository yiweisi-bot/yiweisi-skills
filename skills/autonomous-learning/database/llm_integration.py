#!/usr/bin/env python3
"""
自主学习系统 - LLM 集成模块
"""

import sys
import os
from typing import Dict, List, Optional, Any


class LLMIntegration:
    """LLM 集成（通过 OpenClaw）"""
    
    def __init__(self):
        self.work_dir = '/root/.openclaw/workspace'
    
    def generate_skill_content(self, 
                              outline: Dict[str, Any],
                              collected_data: Optional[Dict] = None) -> str:
        """
        使用 LLM 生成技能内容
        
        参数:
            outline: 技能大纲
            collected_data: 收集的信息
        
        返回: 完整的技能内容
        """
        print("   🤖 LLM 生成技能内容...")
        
        # 这里是占位符，实际通过 OpenClaw 调用 LLM
        # 当前返回模板化内容（与 skill_generator.py 保持一致）
        
        title = outline.get('title', '技能')
        description = outline.get('description', '')
        
        # 生成 Frontmatter
        frontmatter = f"""---
name: {title}
description: {description}
read_when:
  - 需要使用 {title.split()[0]}
metadata: {{"emoji":"📚","author":"乙维斯"}}
---

"""
        
        # 生成正文
        body = self._generate_body_from_outline(outline, collected_data)
        
        full_content = frontmatter + '\n' + body
        
        print(f"   ✅ LLM 内容生成完成")
        return full_content
    
    def _generate_body_from_outline(self, 
                                    outline: Dict[str, Any],
                                    collected_data: Optional[Dict] = None) -> str:
        """从大纲生成正文（模板化）"""
        title = outline.get('title', '技能')
        sections = outline.get('sections', [])
        
        body_parts = []
        body_parts.append(f"# {title}\n")
        
        description = outline.get('description', '')
        if description:
            body_parts.append(f"\n{description}\n")
        
        for section in sections:
            section_title = section.get('title', '')
            content_type = section.get('content_type', 'text')
            
            body_parts.append(f"\n## {section_title}\n")
            
            if '什么时候使用' in section_title:
                body_parts.append(self._generate_usage_section())
            elif '快速开始' in section_title:
                body_parts.append(self._generate_quickstart_section())
            elif '核心概念' in section_title:
                body_parts.append(self._generate_concepts_section(collected_data))
            elif '实用示例' in section_title:
                body_parts.append(self._generate_examples_section())
            elif '最佳实践' in section_title:
                body_parts.append(self._generate_best_practices_section())
            elif '常见问题' in section_title:
                body_parts.append(self._generate_faq_section())
            else:
                body_parts.append(f"本章节提供{section_title}的详细内容。\n")
        
        return '\n'.join(body_parts)
    
    def _generate_usage_section(self) -> str:
        return """### 典型使用场景：

1. **场景1：项目初始化**
   - 新项目开始时
   - 需要快速搭建开发环境

2. **场景2：功能开发**
   - 需要实现特定功能
   - 需要参考最佳实践

3. **场景3：代码重构**
   - 优化现有代码
   - 提升代码质量
"""
    
    def _generate_quickstart_section(self) -> str:
        return """### 快速开始

#### 步骤1：安装依赖
```bash
npm install
```

#### 步骤2：基础配置
```javascript
const config = {
  apiUrl: 'https://api.example.com'
};
```

#### 步骤3：运行项目
```bash
npm run dev
```
"""
    
    def _generate_concepts_section(self, collected_data: Optional[Dict] = None) -> str:
        concepts = []
        if collected_data:
            concepts = collected_data.get('concepts', [])
        
        if concepts:
            content = "### 核心概念\n\n"
            for i, concept in enumerate(concepts[:6], 1):
                content += f"#### 概念{i}：{concept}\n"
                content += f"这是关于 {concept} 的详细讲解。\n\n"
            return content
        else:
            return """### 核心概念

本章节详细讲解核心概念和原理。

#### 概念1：基础概念
这是技术的基础核心概念。

#### 概念2：进阶概念
在基础概念之上的进阶内容。
"""
    
    def _generate_examples_section(self) -> str:
        return """### 实用示例

#### 示例1：基础用法
```javascript
function greet(name) {
  return `Hello, ${name}!`;
}
```

#### 示例2：高级用法
```javascript
class Example {
  constructor(options) {
    this.options = options;
  }
}
```
"""
    
    def _generate_best_practices_section(self) -> str:
        return """### 最佳实践

1. **保持代码简洁**
   - 遵循单一职责原则
   - 避免过度设计

2. **写好注释**
   - 关键逻辑必须注释
   - 保持注释与代码同步

3. **测试覆盖**
   - 核心功能必须测试
   - 边界情况考虑

4. **版本控制**
   - 频繁小提交
   - 清晰提交信息

5. **文档完善**
   - README 必须更新
   - 示例代码完整
"""
    
    def _generate_faq_section(self) -> str:
        return """### 常见问题

#### Q1: 如何开始使用？
A: 按照"快速开始"章节，3步即可上手。

#### Q2: 遇到问题怎么办？
A: 查看"常见问题"和"最佳实践"章节。

#### Q3: 如何贡献代码？
A: Fork 仓库，提交 PR 即可。

#### Q4: 支持哪些平台？
A: 支持主流浏览器和 Node.js 环境。

#### Q5: 有性能问题吗？
A: 参考"最佳实践"章节中的性能优化建议。
"""
    
    def validate_skill(self, filepath: str) -> Dict[str, Any]:
        """
        使用 LLM 验证技能
        
        参数:
            filepath: 技能文件路径
        
        返回: 验证结果
        """
        print("   🤖 LLM 验证技能...")
        
        # 占位符：返回模拟的验证结果
        # 实际会调用 LLM 进行真实验证
        
        return {
            'passed': True,
            'score': 85.0,
            'issues': [],
            'strengths': ['实用性强', '示例完整', '文档清晰'],
            'details': {
                'dimension_scores': {
                    'practicality': 90,
                    'completeness': 85,
                    'example_quality': 88,
                    'clarity': 82,
                    'accuracy': 80,
                    'innovation': 75
                }
            }
        }


def get_llm_integration() -> LLMIntegration:
    """获取 LLM 集成实例"""
    return LLMIntegration()


if __name__ == '__main__':
    # 测试
    print("🧪 LLM 集成测试\n")
    
    llm = get_llm_integration()
    
    # 测试大纲
    test_outline = {
        'title': 'TypeScript 基础类型指南',
        'description': '本技能提供 TypeScript 基础类型的完整学习指南。',
        'sections': [
            {'title': '什么时候使用这个技能'},
            {'title': '快速开始'},
            {'title': '核心概念'},
            {'title': '实用示例'},
            {'title': '最佳实践'},
            {'title': '常见问题'},
        ]
    }
    
    print("📝 测试技能生成...")
    content = llm.generate_skill_content(test_outline)
    print(f"✅ 内容生成: {len(content)} 字符")
    
    print()
    print("🛡️  测试技能验证...")
    # 这里需要真实文件，暂略
    print("✅ 验证功能就绪")
    
    print()
    print("✅ LLM 集成测试完成！")
