# 信息到技能的转化流程 🔄

## 完整流程：原始信息 → 结构化知识 → 高质量技能

---

## 📊 完整流程图

```
阶段1: 信息收集
├─ GitHub Trending 浏览
├─ 技术博客抓取
├─ 官方文档阅读
└─ 社区内容筛选
        ↓
阶段2: 信息清洗
├─ 去除重复内容
├─ 过滤低质量信息
├─ 提取核心要点
└─ 验证信息准确性
        ↓
阶段3: 知识结构化
├─ 分类整理知识点
├─ 建立知识关联
├─ 识别最佳实践
└─ 提取实用示例
        ↓
阶段4: 技能生成
├─ 填充技能模板
├─ 编写使用说明
├─ 制作示例代码
└─ 添加常见问题
        ↓
阶段5: 质量校验
├─ 多维度质量评分
├─ 人工审核确认
├─ 反馈修改优化
└─ 最终发布上线
```

---

## 🔍 阶段1: 信息收集详解

### 1.1 GitHub 信息收集

**目标仓库类型**:
```
✅ Trending 仓库（今日/本周）
✅ 官方文档仓库
✅ 热门示例项目
✅ 最佳实践仓库
```

**收集的信息**:
```markdown
## README.md 提取
- 项目简介和用途
- 快速开始示例
- 核心功能列表
- 安装和配置说明

## 文档目录提取
- docs/ 目录结构
- 主要文档标题
- 教程和指南

## 代码示例提取
- examples/ 目录
- 完整的可运行示例
- 配置文件示例
```

**使用 agent-browser 示例**:
```bash
# 1. 打开 GitHub Trending
agent-browser open "https://github.com/trending"

# 2. 获取页面内容
agent-browser snapshot

# 3. 提取热门仓库信息
# 从snapshot中解析: 仓库名、描述、星数、语言

# 4. 打开具体仓库
agent-browser open "https://github.com/some/project"

# 5. 读取 README
agent-browser snapshot
```

---

### 1.2 技术博客收集

**白名单博客源**:
```
✅ GitHub Blog
✅ Vercel Blog
✅ React Blog
✅ Tailwind CSS Blog
✅ Rust Blog
✅ 知名技术博主（筛选）
```

**收集的信息**:
```markdown
## 文章结构
- 标题和副标题
- 发布时间
- 作者信息

## 核心内容
- 主要观点和论点
- 代码示例
- 配置示例
- 最佳实践建议

## 实用要点
- 具体的操作步骤
- 注意事项
- 常见陷阱
```

---

### 1.3 官方文档收集

**官方文档源**:
```
✅ react.dev
✅ tailwindcss.com
✅ vitejs.dev
✅ nodejs.org
✅ 其他项目官方文档
```

**收集的信息**:
```markdown
## 文档结构
- 教程部分
- API 参考
- 示例部分
- 最佳实践

## 核心知识点
- 基础概念
- 核心 API
- 配置选项
- 常见用例

## 完整示例
- Hello World 示例
- 典型用例示例
- 高级用法示例
```

---

## 🧹 阶段2: 信息清洗详解

### 2.1 去重处理

**重复内容识别**:
```
规则1: 内容相似度 > 80% → 只保留一份
规则2: 相同代码示例 → 只保留最完整的
规则3: 相同概念解释 → 保留最清晰的版本
```

**去重算法**:
```javascript
function deduplicate(contents) {
  const seen = new Set();
  return contents.filter(item => {
    const hash = hashContent(item);
    if (seen.has(hash)) return false;
    seen.add(hash);
    return true;
  });
}
```

---

### 2.2 质量过滤

**低质量内容识别**:
```markdown
❌ 过滤掉:
- 内容过短（< 200字）
- 代码不完整
- 没有实际示例
- 只是概念介绍
- 过时的内容（> 2年）
- 明显错误的内容

✅ 保留:
- 有完整示例
- 有操作步骤
- 有最佳实践
- 内容准确
- 时效性强
```

---

### 2.3 核心要点提取

**提取策略**:
```markdown
## 从长文中提取核心要点
1. 找标题和小标题
2. 找加粗/高亮的内容
3. 找代码块和示例
4. 找"注意"、"重要"、"最佳实践"等标记
5. 找步骤列表和编号列表

## 提取的要点格式
- [概念] 简要解释
- [步骤] 具体操作
- [代码] 示例代码
- [配置] 配置示例
- [注意] 注意事项
```

---

## 🏗️ 阶段3: 知识结构化详解

### 3.1 知识点分类

**分类维度**:
```
维度1: 难度级别
  - 入门级
  - 进阶级
  - 高级

维度2: 功能模块
  - 基础概念
  - 核心功能
  - 高级特性
  - 最佳实践
  - 常见问题

维度3: 使用场景
  - 快速开始
  - 日常开发
  - 性能优化
  - 调试排错
```

**分类示例**:
```json
{
  "react-19": {
    "basics": [
      "Server Components 基础",
      "Actions 基础用法",
      "use() Hook 介绍"
    ],
    "advanced": [
      "Server Components 深度",
      "Actions 高级模式",
      "性能优化技巧"
    ],
    "examples": [
      "完整的 CRUD 示例",
      "表单处理示例",
      "数据加载模式"
    ]
  }
}
```

---

### 3.2 知识关联建立

**关联类型**:
```
类型1: 依赖关系
  - A 需要先理解 B
  - 例如: "Server Components" → "React 基础"

类型2: 互补关系
  - A 和 B 配合使用
  - 例如: "Actions" + "表单处理"

类型3: 进阶关系
  - A 是 B 的进阶内容
  - 例如: "基础用法" → "高级模式"
```

---

### 3.3 最佳实践识别

**识别标准**:
```markdown
✅ 被标记为"最佳实践"
✅ 被多个来源推荐
✅ 有完整的示例
✅ 有性能对比数据
✅ 有官方推荐
✅ 被广泛采用
```

---

## ✍️ 阶段4: 技能生成详解

### 4.1 技能模板填充

**标准技能模板**:
```markdown
---
name: [技能名称]
description: [简短描述]
read_when:
  - [什么时候使用这个技能1]
  - [什么时候使用这个技能2]
metadata:
  emoji: "[emoji]"
  category: "[分类]"
---

# [技能标题]

## 什么时候使用这个技能？
- 场景1
- 场景2
- 场景3

## 前置条件
- 条件1
- 条件2

## 快速开始
### 步骤1: ...
### 步骤2: ...
### 步骤3: ...

## 核心概念
### 概念1
### 概念2

## 实用示例
### 示例1: [场景]
\`\`\`[语言]
[完整代码]
\`\`\`

### 示例2: [场景]
\`\`\`[语言]
[完整代码]
\`\`\`

## 最佳实践
- 实践1
- 实践2
- 实践3

## 常见问题
### Q: [问题1]
A: [答案1]

### Q: [问题2]
A: [答案2]

## 进阶主题
- 主题1
- 主题2

## 参考资源
- 链接1
- 链接2
```

---

### 4.2 内容填充策略

**第一步: 填充基本信息**
```markdown
name: React 19 Server Components 指南
description: 学习 React 19 中 Server Components 的使用方法和最佳实践
read_when:
  - 需要使用 React 19 Server Components
  - 想了解服务端组件最佳实践
  - 需要优化 React 应用性能
```

**第二步: 填充快速开始**
```markdown
## 快速开始

### 步骤1: 创建 Server Component
\`\`\`jsx
// app/page.jsx
async function getData() {
  const res = await fetch('https://api.example.com/data');
  return res.json();
}

export default async function Page() {
  const data = await getData();
  return <div>{data.content}</div>;
}
\`\`\`

### 步骤2: 使用 Client Component
\`\`\`jsx
// app/ClientComponent.jsx
'use client';

import { useState } from 'react';

export default function ClientComponent() {
  const [count, setCount] = useState(0);
  return <button onClick={() => setCount(count + 1)}>{count}</button>;
}
\`\`\`
```

**第三步: 填充最佳实践**
```markdown
## 最佳实践

✅ **数据获取放在 Server Components**
\`\`\`jsx
// 好的做法
async function Page() {
  const data = await fetchData(); // 在服务端获取
  return <ClientComponent data={data} />;
}

// 避免的做法
function Page() {
  const [data, setData] = useState(null); // 在客户端获取
  useEffect(() => { fetchData().then(setData); }, []);
}
\`\`\`

✅ **合理划分组件边界**
- Server Components: 数据获取、静态内容
- Client Components: 交互、状态管理
```

**第四步: 填充常见问题**
```markdown
## 常见问题

### Q: Server Components 能使用 useState 吗？
A: 不能。useState 是客户端特性，需要在文件顶部添加 'use client'。

### Q: 如何在 Server 和 Client Components 之间传递数据？
A: 通过 props 传递。Server Components 可以传递序列化的数据给 Client Components。
```

---

### 4.3 示例代码制作

**好的示例代码特点**:
```markdown
✅ 完整可运行
✅ 有注释说明
✅ 有多种场景
✅ 有错误处理
✅ 有最佳实践
```

**示例代码模板**:
```javascript
/**
 * [简要描述]
 * 
 * 使用场景: [场景描述]
 * 前置条件: [前置条件]
 */

// 步骤1: [描述]
const step1 = doSomething();

// 步骤2: [描述]
const step2 = doSomethingElse(step1);

// 步骤3: [描述]
// 注意: [注意事项]
const result = finalStep(step2);

export default result;
```

---

## ✅ 阶段5: 质量校验详解

### 5.1 多维度质量评分

| 维度 | 评分标准 | 权重 |
|------|---------|------|
| **完整性** | 覆盖主要用例，没有遗漏 | 25% |
| **实用性** | 能解决实际问题 | 25% |
| **示例质量** | 示例完整、可运行 | 20% |
| **文档清晰** | 易于理解、步骤清晰 | 15% |
| **准确性** | 内容准确、无错误 | 15% |

**评分示例**:
```json
{
  "skill": "react-19-server-components",
  "scores": {
    "completeness": 85,
    "usability": 90,
    "examples": 80,
    "clarity": 88,
    "accuracy": 92
  },
  "overall": 87,
  "status": "approved",
  "suggestions": [
    "可以增加一个真实项目的完整示例",
    "建议补充更多性能优化技巧"
  ]
}
```

---

### 5.2 人工审核确认

**审核清单**:
- [ ] 技能结构完整吗？
- [ ] 示例代码能运行吗？
- [ ] 内容准确无误吗？
- [ ] 有明确的使用场景吗？
- [ ] 有常见问题解答吗？
- [ ] 整体质量 ≥ 70分吗？

---

## 🔧 具体实现工具

### 信息收集工具
```bash
# GitHub 探索
./scripts/github-explorer.sh --topic "react-19"

# 网络探索
./scripts/web-explorer.sh --source "react.dev"

# 内容提取
./scripts/content-extractor.sh --url "https://..."
```

### 知识处理工具
```bash
# 去重处理
./scripts/deduplicator.sh --input raw/ --output cleaned/

# 要点提取
./scripts/extractor.sh --input cleaned/ --output structured/

# 知识结构化
./scripts/structurer.sh --input structured/ --output knowledge.json
```

### 技能生成工具
```bash
# 技能生成
./scripts/skill-generator.sh --knowledge knowledge.json --output skill.md

# 质量校验
./scripts/skill-validator.sh --skill skill.md

# 人工审核
./scripts/skill-review.sh --skill skill.md
```

---

## 💡 关键要点

### 1. 信息收集要"广"
- 多源收集，交叉验证
- 官方文档为主，博客为辅

### 2. 信息清洗要"严"
- 严格过滤低质量内容
- 去重要彻底

### 3. 知识结构要"清"
- 分类清晰，层次分明
- 关联合理，易于理解

### 4. 技能生成要"实"
- 实用导向，示例完整
- 步骤清晰，易于操作

### 5. 质量校验要"准"
- 多维度评分
- 人工把关

---

_从信息到技能，步步精心！🔄✨_
