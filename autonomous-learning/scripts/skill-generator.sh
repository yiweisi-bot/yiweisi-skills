#!/bin/bash

# 技能生成脚本
# 从提取的知识生成新技能

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DATA_DIR="$SKILL_DIR/data"
SESSION_ID="$1"

mkdir -p "$DATA_DIR/skills"
mkdir -p "$DATA_DIR/skills/pending"

echo "   🛠️ 开始生成技能..."

# 检查知识目录
knowledge_dir="$DATA_DIR/knowledge"
if [ ! -d "$knowledge_dir" ]; then
  echo "   ⚠️ 未找到知识目录，跳过技能生成"
  exit 0
fi

# MVP 版本：从预定义的知识生成技能
# 后面可以扩展使用 LLM 生成更智能的技能

skills_generated=0

# 1. 扫描知识文件
for knowledge_file in "$knowledge_dir"/*.md; do
  if [ ! -f "$knowledge_file" ]; then
    continue
  fi
  
  filename=$(basename "$knowledge_file" .md)
  
  echo "   📝 处理: $filename"
  
  # 2. 生成技能文件
  skill_file="$DATA_DIR/skills/pending/${filename}-skill.md"
  
  # 根据不同的主题生成不同的技能
  case "$filename" in
    rust-intro)
      cat > "$skill_file" << 'EOF'
---
name: Rust 入门
description: Rust 编程语言入门指南 - 核心概念、学习资源、快速开始
read_when:
  - 想学习 Rust 编程语言
  - 需要 Rust 基础参考
  - 探索系统级编程
metadata: {"emoji":"🦀","requires":{"bins":["rustc","cargo"]}}
allowed-tools: Bash(cargo:*), Bash(rustc:*)
---

# Rust 入门指南 🦀

Rust 是一门系统级编程语言，以内存安全、高性能著称。

## 快速开始

### 安装 Rust
```bash
# 使用官方安装脚本
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# 重新加载环境变量
source $HOME/.cargo/env
```

### 第一个程序
```bash
# 创建新项目
cargo new hello_rust
cd hello_rust

# 运行
cargo run
```

## 核心概念

### 1. 所有权系统
- 每个值有一个所有者
- 同一时间只能有一个所有者
- 所有者离开作用域，值被释放

### 2. 借用检查器
- 不可变借用 `&T`
- 可变借用 `&mut T`
- 同一时间只能有一个可变借用

### 3. 模式匹配
```rust
match option {
    Some(value) => println!("值: {}", value),
    None => println!("无值"),
}
```

## 常用 Cargo 命令

```bash
cargo new <project>    # 创建新项目
cargo build             # 构建
cargo run               # 运行
cargo test              # 测试
cargo check             # 快速检查
cargo doc --open        # 生成文档并打开
```

## 学习资源

- 📖 [The Rust Programming Language](https://doc.rust-lang.org/book/)
- 🎓 [Rust by Example](https://doc.rust-lang.org/rust-by-example/)
- 🌐 [Rust 官方网站](https://www.rust-lang.org/learn)

## 适用场景

- WebAssembly 开发
- 系统工具和命令行工具
- 高性能后端服务
- 嵌入式系统开发

---
*本技能由自主学习系统自动生成*
EOF
      ;;
    webassembly-basics)
      cat > "$skill_file" << 'EOF'
---
name: WebAssembly 基础
description: WebAssembly 入门指南 - 核心概念、使用场景、学习资源
read_when:
  - 想学习 WebAssembly
  - 需要高性能 Web 应用
  - 探索跨平台技术
metadata: {"emoji":"⚡","requires":{"bins":[]}}
allowed-tools:
---

# WebAssembly 基础 ⚡

WebAssembly (Wasm) 是一种高性能二进制指令格式。

## 核心特性

- **near-native 性能** - 接近原生代码的执行速度
- **沙箱安全** - 隔离的执行环境
- **多语言支持** - Rust、C/C++、Go、TypeScript 等
- **跨平台** - 浏览器、服务器、边缘设备

## 快速开始

### 使用 Rust 编译到 Wasm
```bash
# 安装 wasm-pack
cargo install wasm-pack

# 创建项目
cargo new --lib hello-wasm
cd hello-wasm

# 编译
wasm-pack build --target web
```

### 在浏览器中使用
```html
<script type="module">
  import init, { greet } from './pkg/hello_wasm.js';
  
  async function run() {
    await init();
    greet('World');
  }
  
  run();
</script>
```

## 适用场景

1. **浏览器高性能应用**
   - 游戏引擎
   - 视频编辑
   - 3D 可视化

2. **边缘计算**
   - 服务器端 Wasm
   - 边缘函数
   - 微服务

3. **插件系统**
   - 可扩展应用
   - 安全的沙箱插件

## 学习资源

- 🌐 [WebAssembly 官网](https://webassembly.org/getting-started/)
- 📖 [MDN WebAssembly 文档](https://developer.mozilla.org/en-US/docs/WebAssembly)
- 🦀 [Rust and WebAssembly](https://rustwasm.github.io/docs/book/)

---
*本技能由自主学习系统自动生成*
EOF
      ;;
    github-actions-guide)
      cat > "$skill_file" << 'EOF'
---
name: GitHub Actions 指南
description: GitHub CI/CD 自动化工作流完整指南
read_when:
  - 需要自动化构建、测试、部署
  - 想学习 GitHub Actions
  - 配置项目 CI/CD 流水线
metadata: {"emoji":"🔄","requires":{"bins":["gh"]}}
allowed-tools: Bash(gh:*)
---

# GitHub Actions 指南 🔄

GitHub 的原生 CI/CD 工具，自动化你的开发工作流。

## 核心概念

### Workflow（工作流）
- 位于 `.github/workflows/` 目录
- YAML 格式配置
- 由 Events 触发

### Events（事件）
```yaml
on:
  push:
    branches: [main]
  pull_request:
  schedule:
    - cron: '0 2 * * *'
```

### Jobs（任务）
```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build
        run: npm run build
```

## 常用 Workflow 示例

### Node.js 项目 CI
```yaml
name: Node.js CI

on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run tests
        run: npm test
      
      - name: Build
        run: npm run build
```

### 自动发布到 GitHub Pages
```yaml
name: Deploy to Pages

on:
  push:
    branches: [main]

permissions:
  contents: read
  pages: write
  id-token: write

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Pages
        uses: actions/configure-pages@v4
      
      - name: Build
        run: npm run build
      
      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: ./dist
      
      - name: Deploy
        id: deployment
        uses: actions/deploy-pages@v4
```

## 常用 Actions

- `actions/checkout@v4` - 检出代码
- `actions/setup-node@v4` - 设置 Node.js
- `actions/cache@v4` - 缓存依赖
- `actions/upload-pages-artifact@v3` - 上传 Pages 构件

## 学习资源

- 📖 [GitHub Actions 文档](https://docs.github.com/en/actions)
- 🎯 [GitHub Marketplace](https://github.com/marketplace?type=actions)

---
*本技能由自主学习系统自动生成*
EOF
      ;;
    *)
      # 通用技能模板
      cat > "$skill_file" << EOF
---
name: $filename 知识
description: 关于 $filename 的基础知识和学习资源
read_when:
  - 想学习 $filename
  - 需要相关参考资料
metadata: {"emoji":"📚"}
allowed-tools:
---

# $filename 知识 📚

本技能由自主学习系统自动生成。

## 概述

这是关于 $filename 的基础知识集合。

## 学习资源

请查看相关官方文档和教程。

---
*本技能由自主学习系统自动生成*
EOF
      ;;
  esac
  
  echo "      ✓ 已生成: $filename"
  skills_generated=$((skills_generated + 1))
done

# 3. 记录生成的技能
generated_list="$DATA_DIR/skills/generated_${SESSION_ID:-latest}.txt"
ls -1 "$DATA_DIR/skills/pending/" 2>/dev/null > "$generated_list"

echo ""
echo "   ✅ 技能生成完成"
echo "      - 生成 $skills_generated 个新技能"
echo "      - 待审核目录: $DATA_DIR/skills/pending/"
echo ""
echo "   💡 提示: 运行 'autonomous-learning skills review' 审核技能"
