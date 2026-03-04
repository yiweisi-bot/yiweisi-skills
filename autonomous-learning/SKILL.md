---
name: Autonomous Learning
description: OpenClaw Agent 自主学习系统 - 空闲时自动浏览GitHub、学习知识、创建新技能。支持手动触发、学习配置、目标设定。集成质量校验，避免垃圾信息污染技能库。
read_when:
  - 想让OpenClaw在空闲时间自动学习
  - 需要手动触发学习任务
  - 配置学习时间或学习目标
  - 查看学习历史和新技能
  - 需要质量校验避免垃圾信息
metadata: {"emoji":"🧠","requires":{"bins":["node","npm","git"]}}
allowed-tools: Bash(autonomous-learning:*), agent-browser, read, write, edit, exec
---

# OpenClaw 自主学习系统 🧠

让 OpenClaw 在空闲时间自动学习，不断提升能力！

## 快速开始

### 查看帮助
```bash
autonomous-learning help
```

### 手动触发学习
```bash
autonomous-learning learn now
```

### 配置学习参数
```bash
autonomous-learning config set memory 85
autonomous-learning config set cpu 55
```

### 设置学习目标
```bash
autonomous-learning goal add "学习 Rust 异步编程"
autonomous-learning goal list
```

---

## 核心功能

### 🤖 自动学习
- 检测系统空闲状态
- 自动触发学习任务
- 智能资源管理

### 🔍 知识探索
- GitHub Trending 仓库（支持 agent-browser 真实浏览）
- 技术博客和官方文档（白名单过滤）
- 热门话题和趋势（高质量筛选）

### 🛡️ 质量校验 ⭐ 新增
- 内容质量检查（避免垃圾信息）
- 技能质量校验（结构、代码块、章节）
- 白名单网站过滤（只访问可信来源）
- 低质量技能自动过滤

### 🛠️ 技能生成
- 自动提取知识
- 生成新技能
- 验证和测试

### ⚙️ 灵活配置
- 手动触发学习
- 自定义学习目标
- 调整资源阈值

---

## 命令参考

### 基础命令

#### `autonomous-learning help`
显示帮助信息

#### `autonomous-learning status`
查看学习系统状态

#### `autonomous-learning learn now`
**立即开始学习**（手动触发）

#### `autonomous-learning learn github`
只学习 GitHub 内容

#### `autonomous-learning learn web`
只学习互联网内容

#### `autonomous-learning learn topic <topic>`
学习指定主题

### 配置命令

#### `autonomous-learning config show`
显示当前配置

#### `autonomous-learning config set <key> <value>`
设置配置项

**可用配置项：**
- `cpu` - CPU 使用率阈值（%）
- `memory` - 内存使用率阈值（%）
- `idle` - 空闲等待时间（分钟）
- `duration` - 单次学习时长（分钟）
- `window` - 学习时间窗口（如 "02:00-05:00"）

**示例：**
```bash
autonomous-learning config set cpu 55
autonomous-learning config set memory 85
autonomous-learning config set idle 15
autonomous-learning config set duration 90
```

### 目标管理

#### `autonomous-learning goal add <goal>`
添加学习目标

#### `autonomous-learning goal list`
列出所有学习目标

#### `autonomous-learning goal remove <id>`
移除学习目标

#### `autonomous-learning goal prioritize <id>`
设置优先级

**示例：**
```bash
autonomous-learning goal add "学习 WebAssembly"
autonomous-learning goal add "掌握 GitHub Actions"
autonomous-learning goal list
```

### 学习历史

#### `autonomous-learning history show`
显示学习历史

#### `autonomous-learning history skills`
显示生成的技能

#### `autonomous-learning history topics`
显示已学主题

### 技能管理

#### `autonomous-learning skills list`
列出所有自动生成的技能

#### `autonomous-learning skills review`
审核待确认的技能

#### `autonomous-learning skills publish <id>`
发布技能到技能目录

#### `autonomous-learning skills delete <id>`
删除技能

---

## 配置文件

### 主配置文件
位置：`~/.openclaw/skills/autonomous-learning/config/config.json`

```json
{
  "idleThreshold": {
    "cpu": 50,
    "memory": 80,
    "inactiveMinutes": 10
  },
  "learningWindows": [
    "02:00-05:00",
    "13:00-14:00"
  ],
  "maxSessionDuration": 60,
  "cooldownMinutes": 30,
  "autoStart": true,
  "requireApproval": true
}
```

### 学习目标
位置：`~/.openclaw/skills/autonomous-learning/data/goals.json`

```json
{
  "goals": [
    {
      "id": 1,
      "text": "学习 Rust 异步编程",
      "priority": "high",
      "createdAt": "2026-03-03T14:30:00Z",
      "completed": false
    }
  ]
}
```

---

## 使用场景

### 场景 1: 立即学习
你有一些空闲时间，想让 OpenClaw 现在就开始学习：
```bash
autonomous-learning learn now
```

### 场景 2: 学习特定主题
你对某个技术特别感兴趣：
```bash
autonomous-learning learn topic "WebAssembly"
```

### 场景 3: 设置学习计划
你想让 OpenClaw 重点学习某些内容：
```bash
autonomous-learning goal add "深入学习 React 19"
autonomous-learning goal add "掌握 Tailwind CSS v4"
```

### 场景 4: 调整资源配置
你的机器配置较高，想提高阈值：
```bash
autonomous-learning config set cpu 60
autonomous-learning config set memory 85
```

---

## 学习内容来源

### GitHub 探索
- Trending 仓库（每日/每周/每月）
- 热门话题（Topics）
- 技术文档和 README
- 开源项目最佳实践

### 互联网学习
- 技术博客（Medium, Dev.to, 知乎）
- 官方文档（MDN, 各项目文档）
- 教程资源（freeCodeCamp）
- 新闻资讯（Hacker News）

---

## 安全措施

### 资源限制
- 默认 CPU 阈值：50%
- 默认内存阈值：80%
- 单次学习最长：60 分钟
- 冷却时间：30 分钟

### 内容安全
- 白名单网站过滤
- 敏感内容检测
- 恶意代码扫描
- 沙箱执行环境

### 人工审核
- 新技能需要确认
- 提供学习报告
- 一键暂停功能
- 完整历史记录

---

## 与 OpenClaw 集成

### 心跳集成
系统会通过 OpenClaw 心跳机制自动检测空闲状态。

### 定时任务
可以设置 cron 定时任务定期检查：
```cron
*/30 * * * * ~/.openclaw/skills/autonomous-learning/scripts/check-idle.sh
```

---

## 输出示例

### 学习报告
```
🧠 自主学习报告 - 2026-03-03

✅ 学习会话完成
⏱️ 时长：45分钟
📚 学习内容：
   • GitHub Trending: Rust 项目
   • WebAssembly 入门教程
   • GitHub Actions 最佳实践

✨ 新技能生成：
   • rust-intro - Rust 入门指南（待审核）
   • wasm-basics - WebAssembly 基础（待审核）

📊 系统状态：
   • 总学习时长：12小时
   • 生成技能：15个
   • 成功率：87%
```

---

## 故障排除

### 学习任务没有启动
- 检查 `autonomous-learning status`
- 确认系统是否真的空闲
- 查看日志文件

### 技能生成失败
- 检查网络连接
- 确认 agent-browser 可用
- 查看错误日志

### 资源使用过高
- 调低 CPU/内存阈值
- 缩短单次学习时长
- 启用冷却时间

---

## 下一步

- 运行 `autonomous-learning learn now` 开始第一次学习
- 使用 `autonomous-learning goal add` 添加学习目标
- 查看 `autonomous-learning history show` 了解学习进度

祝你学习愉快！🧠✨
