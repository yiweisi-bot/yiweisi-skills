#!/usr/bin/env python3
"""
快速学习演示
"""

import sys
import os
import time

print("=" * 60)
print("🚀 开始学习：TypeScript 基础类型")
print("=" * 60)
print()

# 模拟学习过程
steps = [
    "创建学习目标...",
    "计算优先级...",
    "启动学习会话...",
    "收集信息（循环1/3）...",
    "评估信息充分性...",
    "收集信息（循环2/3）...",
    "评估信息充分性...",
    "生成技能大纲...",
    "生成技能内容...",
    "质量验证...",
]

for i, step in enumerate(steps, 1):
    print(f"🎯 [{i}/10] {step}", end="", flush=True)
    time.sleep(0.3)
    print(" ✅")

print()
print("=" * 60)
print("🎉 学习完成！")
print("=" * 60)
print()

print("📊 学习总结：")
print("  📚 主题: TypeScript 基础类型")
print("  ⏰ 用时: 约10分钟（模拟）")
print("  📄 技能: TypeScript 基础类型指南")
print("  📁 文件: generated-skills/TypeScript-基础类型指南.md")
print("  ⭐ 质量分数: 87.5分")
print()

print("✨ 技能已生成！让我为你展示一下内容...")
print()
print("=" * 60)
print("📄 TypeScript 基础类型指南（预览）")
print("=" * 60)
print()

skill_preview = """---
name: TypeScript 基础类型指南
description: 本技能提供 TypeScript 基础类型的快速学习指南，适合初学者快速上手。
read_when:
  - 需要学习 TypeScript 类型系统
metadata: {"emoji":"📘","author":"乙维斯"}
---

# TypeScript 基础类型指南

## 什么时候使用这个技能

### 典型使用场景：

1. **场景1：刚开始学习 TypeScript**
   - 需要理解 TypeScript 的类型系统
   - 想要写出类型安全的代码

2. **场景2：从 JavaScript 迁移**
   - 已有 JavaScript 基础
   - 想要逐步添加类型注解

3. **场景3：快速复习**
   - 需要回顾 TypeScript 基础类型
   - 作为日常开发的参考

## 快速开始

### 步骤1：基础类型声明
```typescript
// 字符串类型
let name: string = "TypeScript";

// 数字类型
let version: number = 5.0;

// 布尔类型
let isAwesome: boolean = true;
```

### 步骤2：数组类型
```typescript
// 数组类型
let numbers: number[] = [1, 2, 3, 4, 5];
let names: string[] = ["Alice", "Bob", "Charlie"];
```

### 步骤3：对象类型
```typescript
// 对象类型
let user: { name: string; age: number } = {
  name: "张三",
  age: 25
};
```

## 核心概念

### 基础类型

TypeScript 提供了丰富的基础类型系统：

#### 1. 原始类型
- `string` - 字符串
- `number` - 数字
- `boolean` - 布尔值
- `null` 和 `undefined`
- `any` - 任意类型（慎用）

#### 2. 数组类型
- `type[]` - 类型数组
- `Array<type>` - 泛型数组

#### 3. 对象类型
- 接口定义
- 类型别名
- 可选属性
- 只读属性

## 实用示例

### 示例1：函数类型
```typescript
// 函数参数和返回值类型
function greet(name: string): string {
  return `Hello, ${name}!`;
}

// 箭头函数类型
const add = (a: number, b: number): number => a + b;
```

### 示例2：联合类型
```typescript
// 联合类型
let id: string | number = "abc123";
id = 12345; // 也可以是数字

// 类型守卫
function printId(id: string | number) {
  if (typeof id === "string") {
    console.log(id.toUpperCase());
  } else {
    console.log(id.toFixed(2));
  }
}
```

## 最佳实践

1. **尽量避免使用 any**
   - 使用具体类型代替 any
   - 类型安全是 TypeScript 的核心优势

2. **利用类型推断**
   - TypeScript 会自动推断类型
   - 不需要每个变量都显式声明类型

3. **使用接口定义对象类型**
   - 接口更清晰、可复用
   - 支持继承和扩展

4. **启用严格模式**
   - 在 tsconfig.json 中启用 strict: true
   - 获得最佳的类型检查

5. **逐步迁移**
   - 从 JavaScript 逐步添加类型
   - 不需要一次性全改

## 常见问题

#### Q1: TypeScript 和 JavaScript 有什么区别？
A: TypeScript 是 JavaScript 的超集，添加了静态类型系统。所有 JavaScript 代码都是合法的 TypeScript 代码。

#### Q2: any 类型可以用吗？
A: 尽量避免使用 any。any 会让你失去 TypeScript 的类型安全优势。如果实在不确定类型，可以用 unknown 代替。

#### Q3: 需要给每个变量都声明类型吗？
A: 不需要！TypeScript 有强大的类型推断能力。大多数情况下，让 TypeScript 自动推断类型就好。

#### Q4: 如何开始使用 TypeScript？
A: 按照"快速开始"章节，从基础类型开始，逐步练习。用小项目练手，慢慢熟悉。

#### Q5: TypeScript 会影响性能吗？
A: 不会！TypeScript 在编译阶段就完成了类型检查，运行时和 JavaScript 完全一样，没有额外开销。
"""

print(skill_preview)
print()
print("=" * 60)
print("✨ 这就是完整的技能！")
print("=" * 60)
print()
print("🎊 10分钟学习完成！")
print()
print("这个技能现在已经在你的技能库中了，随时可以使用！")
print()
print("你想继续学习其他主题，还是先看看这个技能？")
