---
name: brave-search
description: Web search and content extraction using Brave Search via agent-browser
read_when:
  - Searching the web for information
  - Extracting content from search results
  - Getting real-time web data
metadata:
  clawdbot:
    emoji: "🔍"
    requires:
      bins:
        - agent-browser
allowed-tools:
  - Bash(agent-browser:*)
---

# Brave Search Skill

使用 Brave Search 进行网页搜索和内容提取。

## 功能

- 通过 Brave Search 搜索网页
- 提取搜索结果内容
- 支持中文和英文搜索
- 无需 API 密钥

## 使用方法

### 基本搜索流程

```bash
# 1. 打开 Brave Search
agent-browser open https://search.brave.com/search?q=你的搜索词

# 2. 等待页面加载
agent-browser wait 3000

# 3. 获取搜索结果
agent-browser snapshot -i

# 4. 提取结果内容
agent-browser get text @ref
```

### 示例：搜索新闻

```bash
# 搜索最新科技新闻
agent-browser open "https://search.brave.com/search?q=2026+最新科技新闻"
agent-browser wait 3000
agent-browser snapshot -i
```

### 示例：搜索技术文档

```bash
# 搜索 OpenClaw 文档
agent-browser open "https://search.brave.com/search?q=OpenClaw+多Agent系统"
agent-browser wait 3000
agent-browser snapshot -i
```

## Brave Search 优势

- ✅ 隐私保护：不追踪用户
- ✅ 无需 API 密钥
- ✅ 搜索结果质量高
- ✅ 支持多种语言

## 注意事项

1. 使用 URL 编码处理搜索词中的特殊字符
2. 等待页面完全加载后再获取结果
3. 可以多次 snapshot 获取更多结果
4. 建议使用 agent-browser 的其他功能（截图、PDF）保存搜索结果

## 高级用法

### 组合使用

```bash
# 搜索并截图保存
agent-browser open "https://search.brave.com/search?q=关键词"
agent-browser wait 3000
agent-browser screenshot search-result.png
agent-browser snapshot -i
```

### 提取特定结果

```bash
# 获取第一个搜索结果的标题
agent-browser get text @e1

# 点击第一个结果查看详情
agent-browser click @e1
agent-browser wait 2000
agent-browser snapshot
```

## 依赖

- agent-browser 技能（必需）
- Node.js 环境

## 故障排查

如果搜索失败：
1. 检查 agent-browser 是否正确安装
2. 确认网络连接正常
3. 尝试增加等待时间
4. 使用 `--headed` 参数查看浏览器窗口调试
