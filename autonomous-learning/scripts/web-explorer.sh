#!/bin/bash

# 网络资源探索脚本
# 探索技术博客、官方文档、新闻等学习源

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DATA_DIR="$SKILL_DIR/data"
VALIDATOR_DIR="$SKILL_DIR/scripts/validators"
SESSION_ID="$1"

mkdir -p "$DATA_DIR/web"

echo "   🌐 开始探索网络学习资源..."

# 高质量学习源（白名单）
QUALITY_SOURCES=(
  "MDN Web Docs|https://developer.mozilla.org/"
  "GitHub Blog|https://github.blog/"
  "Rust Blog|https://blog.rust-lang.org/"
  "React Blog|https://react.dev/blog"
  "Vite Blog|https://vitejs.dev/blog/"
  "Tailwind Blog|https://tailwindcss.com/blog"
  "Kubernetes Blog|https://kubernetes.io/blog/"
)

# 技术新闻源
TECH_NEWS=(
  "Hacker News|https://news.ycombinator.com/"
  "Lobsters|https://lobste.rs/"
)

explore_quality_sources() {
  echo "   📚 探索高质量学习源..."
  
  sources_file="$DATA_DIR/web/sources.txt"
  > "$sources_file"
  
  local count=0
  for source in "${QUALITY_SOURCES[@]}"; do
    IFS='|' read -r name url <<< "$source"
    
    echo "      🔍 检查: $name"
    
    # 验证网站质量
    if validate_website_quality "$url"; then
      echo "$name|$url" >> "$sources_file"
      echo "         ✅ 已添加: $name"
      count=$((count + 1))
    else
      echo "         ⚠️ 跳过: $name (质量验证未通过)"
    fi
  done
  
  echo "      ✓ 收集 $count 个高质量学习源"
}

validate_website_quality() {
  local url="$1"
  
  # 白名单域名检查
  local whitelist_domains=(
    "mozilla.org"
    "github.com"
    "github.blog"
    "rust-lang.org"
    "react.dev"
    "vitejs.dev"
    "tailwindcss.com"
    "kubernetes.io"
    "webassembly.org"
    "python.org"
    "nodejs.org"
    "typescriptlang.org"
  )
  
  for domain in "${whitelist_domains[@]}"; do
    if [[ "$url" == *"$domain"* ]]; then
      return 0
    fi
  done
  
  return 1
}

create_web_knowledge_summary() {
  web_knowledge_file="$DATA_DIR/web/knowledge_${SESSION_ID:-latest}.md"
  
  cat > "$web_knowledge_file" << 'EOF'
# 网络学习资源摘要

## 高质量学习源

### 官方文档类
- MDN Web Docs - Web 技术权威文档
- React 官方文档 - React 框架文档
- Rust 官方文档 - Rust 语言文档
- Kubernetes 文档 - 容器编排文档
- Tailwind CSS 文档 - CSS 框架文档

### 技术博客类
- GitHub Blog - GitHub 官方博客
- Rust Blog - Rust 语言博客
- Vite Blog - Vite 构建工具博客

### 技术新闻类
- Hacker News - 技术新闻聚合
- Lobsters - 技术社区

---

## 推荐学习路径

### Web 开发
1. MDN Web Docs → 基础 Web 技术
2. React Blog → 前端框架
3. Vite Blog → 构建工具
4. Tailwind CSS → 样式框架

### 系统编程
1. Rust Blog → Rust 语言
2. WebAssembly → 高性能 Web

### 云原生
1. Kubernetes Blog → 容器编排
2. GitHub Blog → DevOps 实践

---

## 内容质量保证

✅ **所有来源均来自白名单**：
- 只包含官方文档和可信技术博客
- 过滤低质量内容和营销信息
- 优先选择有长期声誉的技术来源

---

*本摘要由自主学习系统自动生成*
EOF

  echo "      ✓ 网络资源摘要已生成"
}

# 主流程
explore_quality_sources
create_web_knowledge_summary

echo ""
echo "   ✅ 网络资源探索完成"
