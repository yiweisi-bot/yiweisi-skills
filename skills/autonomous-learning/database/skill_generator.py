#!/usr/bin/env python3
"""
自主学习系统 - 技能内容生成器
"""

import os
from typing import Dict, List, Optional, Any
from datetime import datetime
from pathlib import Path


class SkillGenerator:
    """技能内容生成器"""
    
    def __init__(self):
        self.skills_dir = None
        self._init_skills_dir()
    
    def _init_skills_dir(self):
        """初始化技能目录"""
        # 获取当前文件所在目录
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # 技能目录是父目录下的 skills 文件夹
        self.skills_dir = os.path.join(os.path.dirname(current_dir), 'generated-skills')
        os.makedirs(self.skills_dir, exist_ok=True)
    
    def generate_skill_content(self, 
                                 outline: Dict[str, Any],
                                 collected_data: Optional[Dict] = None,
                                 author: str = '乙维斯') -> str:
        """
        生成完整的技能内容（SKILL.md 格式）
        
        参数:
            outline: 技能大纲
            collected_data: 收集到的信息
            author: 作者名称
        
        返回:
            完整的技能内容字符串
        """
        # 生成 Frontmatter
        frontmatter = self._generate_frontmatter(outline, author)
        
        # 生成正文内容
        content = self._generate_body(outline, collected_data)
        
        # 合并
        full_content = frontmatter + '\n' + content
        
        return full_content
    
    def _generate_frontmatter(self, outline: Dict[str, Any], author: str) -> str:
        """生成 Frontmatter"""
        title = outline.get('title', '技能')
        description = outline.get('description', '')
        
        # 提取标签
        tags = self._extract_tags(title)
        
        frontmatter = f"""---
name: {title}
description: {description}
read_when:
  - 需要使用 {title.split()[0]}
metadata: {{"emoji":"📚","author":"{author}"}}
---

"""
        return frontmatter
    
    def _extract_tags(self, title: str) -> List[str]:
        """从标题提取标签"""
        tag_keywords = {
            'React': ['React', '前端'],
            'TypeScript': ['TypeScript', '前端', 'JavaScript'],
            'Python': ['Python', '后端'],
            'Docker': ['Docker', 'DevOps'],
            'Tailwind': ['Tailwind', 'CSS', '前端'],
            'Git': ['Git', '工具'],
        }
        
        tags = []
        for keyword, tag_list in tag_keywords.items():
            if keyword in title:
                tags.extend(tag_list)
        
        return tags if tags else ['技能']
    
    def _generate_body(self, outline: Dict[str, Any], 
                        collected_data: Optional[Dict] = None) -> str:
        """生成正文内容"""
        sections = outline.get('sections', [])
        body_parts = []
        
        # 添加标题
        title = outline.get('title', '技能')
        body_parts.append(f"# {title}\n")
        
        # 添加描述
        description = outline.get('description', '')
        if description:
            body_parts.append(f"\n{description}\n")
        
        # 生成各个章节
        for section in sections:
            section_title = section.get('title', '')
            section_description = section.get('description', '')
            content_type = section.get('content_type', 'text')
            
            body_parts.append(f"\n## {section_title}\n")
            
            # 根据内容类型生成不同的内容
            if content_type == 'list':
                body_parts.append(self._generate_list_section(section_title, section_description, collected_data))
            elif content_type == 'steps_with_code':
                body_parts.append(self._generate_steps_section(section_title, collected_data))
            elif content_type == 'code_examples':
                body_parts.append(self._generate_examples_section(section_title, collected_data))
            elif content_type == 'faq':
                body_parts.append(self._generate_faq_section(section_title, collected_data))
            else:
                body_parts.append(self._generate_text_section(section_title, section_description, collected_data))
        
        return '\n'.join(body_parts)
    
    def _generate_text_section(self, title: str, description: str,
                                collected_data: Optional[Dict] = None) -> str:
        """生成文本章节"""
        content = ""
        
        if '核心概念' in title:
            content += """### 核心概念

本章节详细讲解核心概念和原理，帮助你理解技术的本质。

#### 概念1：基础概念
这是技术的基础核心概念，理解这个概念是掌握整个技术的关键。

#### 概念2：进阶概念
在基础概念之上，这个概念提供了更深入的理解。

#### 概念3：高级概念
这个概念涉及到技术的高级特性和用法。
"""
        else:
            content = f"{description}\n\n本章节提供详细的内容讲解。"
        
        return content
    
    def _generate_list_section(self, title: str, description: str,
                               collected_data: Optional[Dict] = None) -> str:
        """生成列表章节"""
        content = ""
        
        if '什么时候使用' in title:
            content += """### 典型使用场景

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
        elif '最佳实践' in title:
            content += """### 最佳实践

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
        
        return content
    
    def _generate_steps_section(self, title: str,
                                collected_data: Optional[Dict] = None) -> str:
        """生成步骤章节"""
        return """### 快速开始

#### 步骤1：安装依赖
```bash
# 安装基础依赖
npm install
# 或
pip install -r requirements.txt
```

#### 步骤2：基础配置
```javascript
// 配置文件示例
const config = {
  apiUrl: 'https://api.example.com',
  timeout: 5000
};
```

#### 步骤3：运行项目
```bash
# 启动开发服务器
npm run dev
# 或
python main.py
```
"""
    
    def _generate_examples_section(self, title: str,
                                    collected_data: Optional[Dict] = None) -> str:
        """生成示例章节"""
        return """### 实用示例

#### 示例1：基础用法
```javascript
// 基础用法示例
function greet(name) {
  return `Hello, ${name}!`;
}

console.log(greet('World'));
```

#### 示例2：高级用法
```javascript
// 高级用法示例
class Example {
  constructor(options) {
    this.options = options;
  }
  
  async execute() {
    // 实现逻辑
  }
}
```
"""
    
    def _generate_faq_section(self, title: str,
                             collected_data: Optional[Dict] = None) -> str:
        """生成FAQ章节"""
        faqs = collected_data.get('faqs', []) if collected_data else []
        
        content = "### 常见问题\n\n"
        
        if faqs:
            for i, faq in enumerate(faqs[:5], 1):
                content += f"#### Q{i}: {faq}\n"
                content += "A: 这是一个常见问题的解答。\n\n"
        else:
            content += """#### Q1: 如何开始使用？
A: 按照"快速开始"章节，3步即可上手。

#### Q2: 遇到问题怎么办？
A: 查看"常见问题"和"最佳实践"章节，或搜索 issue。

#### Q3: 如何贡献代码？
A: Fork 仓库，提交 PR 即可。

#### Q4: 支持哪些平台？
A: 支持主流浏览器和 Node.js 环境。

#### Q5: 有性能问题吗？
A: 参考"最佳实践"章节中的性能优化建议。
"""
        
        return content
    
    def save_skill_to_file(self, 
                         skill_content: str, 
                         title: str) -> str:
        """
        保存技能到文件
        
        返回: 文件路径
        """
        # 生成文件名
        safe_title = title.replace(' ', '-').replace('/', '-')
        filename = f"{safe_title}.md"
        filepath = os.path.join(self.skills_dir, filename)
        
        # 确保目录存在
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        # 写入文件
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(skill_content)
        
        return filepath
    
    def get_skills_list(self) -> List[str]:
        """获取已生成的技能列表"""
        if not os.path.exists(self.skills_dir):
            return [f for f in os.listdir(self.skills_dir) 
                   if f.endswith('.md')]
        return []


def generate_skill(outline: Dict[str, Any],
                    collected_data: Optional[Dict] = None,
                    author: str = '乙维斯') -> Dict[str, Any]:
    """
    便捷函数：生成技能
    
    返回: { 'content': 内容, 'filepath': 文件路径 }
    """
    generator = SkillGenerator()
    
    # 生成内容
    content = generator.generate_skill_content(outline, collected_data, author)
    
    # 保存文件
    filepath = generator.save_skill_to_file(content, outline.get('title', 'skill'))
    
    return {
        'content': content,
        'filepath': filepath,
        'title': outline.get('title', 'skill')
    }


if __name__ == '__main__':
    # 测试
    print("🧪 技能生成器测试\n")
    
    # 测试大纲
    test_outline = {
        'title': 'React 19 Server Components 指南',
        'description': '本技能提供 React 19 Server Components 的完整学习指南。',
        'sections': [
            {'title': '什么时候使用这个技能', 'description': '3个典型使用场景'},
            {'title': '快速开始', 'description': '3个步骤'},
            {'title': '核心概念', 'description': '详细讲解'},
            {'title': '实用示例', 'description': '2个完整示例'},
            {'title': '最佳实践', 'description': '5条最佳实践'},
            {'title': '常见问题', 'description': '5个常见问题'},
        ]
    }
    
    print("📝 生成技能...")
    result = generate_skill(test_outline)
    
    print(f"✅ 技能生成完成！")
    print(f"   📄 标题: {result['title']}")
    print(f"   📁 文件: {result['filepath']}")
    print(f"   📊 大小: {len(result['content'])} 字符")
    print()
    print("📋 技能内容预览:")
    print(result['content'][:500] + "..." if len(result['content']) > 500 else result['content'])
