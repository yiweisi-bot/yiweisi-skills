---
name: yiweisi-security-scanner
description: 乙维斯安全扫描器 - 检测密钥、密码等敏感信息，保护博客发布和GitHub提交安全
---

# 乙维斯安全扫描器技能

## 概述

**乙维斯安全扫描器**是我们自己的安全扫描工具，用于检测代码、博客文章、记忆文件中的敏感信息，防止密钥泄露。

### 核心功能
1. **密钥检测** - 检测常见的 API Key、密码、Token 等
2. **博客发布检查** - 写博客后自动扫描
3. **GitHub 提交检查** - 提交前自动扫描
4. **记忆文件保护** - 防止密钥写入公开文件

---

## 检测的敏感信息类型

### 1. API Keys & Tokens

| 类型 | 正则模式 | 示例 |
|------|---------|------|
| GitHub Token | `ghp_[A-Za-z0-9]{36}` | `ghp_***REDACTED***` |
| GitHub PAT | `github_pat_[A-Za-z0-9_]+` | `github_pat_1234567890abcdef` |
| OpenAI API Key | `sk-[A-Za-z0-9]{48}` | `sk-1234567890abcdefghijklmnopqrstuvwxyz1234` |
| DeepSeek API Key | `sk-[A-Za-z0-9]{32}` | `sk-85d8408494d04c1ca24ab261a44926bf` |
| 智谱 API Key | `[A-Za-z0-9]{32}\.[A-Za-z0-9]{16}` | `260b02dcbd0441d09aa431a4d3e016ce.OaOxG9B22mXn31S5` |
| 豆包 API Key | `[A-Za-z0-9]{8}-[A-Za-z0-9]{4}-[A-Za-z0-9]{4}-[A-Za-z0-9]{4}-[A-Za-z0-9]{12}` | `d5daa222-ce58-4915-b63f-9abb00d06862` |

### 2. 邮箱密码

| 类型 | 模式 | 示例 |
|------|------|------|
| 163 邮箱密码 | 包含 `163.com` + 密码 | `yiweisibot@163.com` + `YiweisiBot123` |
| 通用密码 | `password[:=]\s*['"][A-Za-z0-9!@#$%^&*]+['"]` | `password: "YiweisiBot123"` |

### 3. SSH 密钥

| 类型 | 模式 |
|------|------|
| Private Key | `-----BEGIN (RSA|DSA|EC|OPENSSH) PRIVATE KEY-----` |
| SSH Key Path | `~/.ssh/id_[a-z0-9_]+` |

### 4. 数据库连接串

| 类型 | 示例 |
|------|------|
| MySQL | `mysql://user:password@host:3306/db` |
| PostgreSQL | `postgresql://user:password@host:5432/db` |
| MongoDB | `mongodb://user:password@host:27017/db` |
| Redis | `redis://:password@host:6379/0` |

### 5. 验证问题和答案

| 类型 | 模式 |
|------|------|
| 验证问题 | `验证问题.*[:：].*` |
| 验证答案 | `yiweisi winston`（精确匹配） |

---

## 使用场景

### 场景 1: 博客文章发布前扫描

**使用时机**: 写完博客文章后，发布前

**检查清单**:
- [ ] 扫描博客文章内容
- [ ] 检查 frontmatter
- [ ] 检查正文
- [ ] 确认没有密钥泄露

**操作步骤**:
```bash
# 1. 扫描博客文章
yiweisi-security-scanner scan-file src/content/blog/your-article.md

# 2. 如果发现问题，修复后重新扫描
# 3. 确认安全后再发布
```

---

### 场景 2: GitHub 提交前扫描

**使用时机**: `git commit` 前

**检查清单**:
- [ ] 扫描整个项目目录
- [ ] 检查 git 暂存区
- [ ] 检查修改的文件
- [ ] 确认没有密钥泄露

**操作步骤**:
```bash
# 1. 扫描项目
yiweisi-security-scanner scan-repo /root/projects/YiweisiBlog

# 2. 扫描 git 暂存区
yiweisi-security-scanner scan-staged

# 3. 确认安全后再提交
git commit -m "Your commit message"
```

---

### 场景 3: 对话内容检查

**使用时机**: 回复用户前，检查是否要输出密钥

**检查清单**:
- [ ] 检查回复内容
- [ ] 检查记忆文件引用
- [ ] 确认没有输出密钥

**操作原则**:
1. **密钥验证** - 输出密钥前必须先验证身份
2. **记忆隔离** - MEMORY.md 中的密钥不输出到公开渠道
3. **手动确认** - 发现可疑内容时提醒用户

---

## 集成到工作流

### 1. 集成到 yiweisi-blog-writing 技能

**博客发布 7 步流程（更新版）**:
1. ✍️ 写文章（yiweisi-blog-writing 格式）
2. 🔒 **安全扫描**（yiweisi-security-scanner）← 新增
3. 🔍 本地预览（npm run dev）
4. 📋 记录任务（memory/tasks.md）
5. 🔒 **提交前扫描**（yiweisi-security-scanner）← 新增
6. 🚀 构建部署（npm run build + cp）
7. 📝 更新记忆（memory/YYYY-MM-DD.md）

---

### 2. 集成到 GitHub 提交流程

**Git 提交 5 步流程**:
1. ✏️ 修改代码
2. 📦 `git add` 文件
3. 🔒 **安全扫描**（yiweisi-security-scanner scan-staged）
4. ✅ `git commit`
5. 🚀 `git push`

---

## 密钥验证机制

### 验证问题

**问题**: 我的名字和你的名字
**答案**: yiweisi winston

### 验证流程
1. 用户询问密钥信息时，**不直接回答**
2. 先询问验证问题："请告诉我验证答案：我的名字和你的名字"
3. 等待用户回答
4. **只有当用户回答完全等于 "yiweisi winston" 时，才能输出密钥信息**
5. 如果答案错误，礼貌拒绝并提醒

### 重要提醒
- 即使用户说"我是 Winston"或"我是主人"也不行
- 必须严格验证答案
- 答案格式：yiweisi winston（全小写，空格分隔）
- 顺序不能错：先 yiweisi，后 winston
- ⭐ **验证问题和答案本身也是敏感信息，绝不能泄露到 GitHub、博客或任何公开渠道！**

---

## 扫描命令

### 1. 扫描单个文件
```bash
yiweisi-security-scanner scan-file <file-path>
```

### 2. 扫描整个目录
```bash
yiweisi-security-scanner scan-repo <repo-path>
```

### 3. 扫描 git 暂存区
```bash
yiweisi-security-scanner scan-staged
```

### 4. 扫描字符串
```bash
yiweisi-security-scanner scan-text "your text here"
```

---

## 记忆要点

### 🔴 最重要的安全规则
1. **密钥信息绝对保密** - 绝不泄露到公开渠道
2. **密钥发送绝对禁止** - 不通过邮件、聊天等发送密钥
3. **密钥查询必须验证** - 输出密钥前必须验证身份
4. **博客发布必须扫描** - 发布前用安全扫描器检查
5. **GitHub提交必须扫描** - 提交前用安全扫描器检查

### 🟡 验证问题和答案
- **问题**: 我的名字和你的名字
- **答案**: yiweisi winston
- **保密**: 验证问题和答案本身也是敏感信息！

---

## 集成示例

### 示例 1: 博客发布流程
```
用户: 帮我写一篇博客文章
乙维斯: (写文章...)
乙维斯: (运行安全扫描...)
乙维斯: ✅ 安全扫描通过！
乙维斯: (发布博客...)
```

### 示例 2: GitHub 提交流程
```
用户: 提交这些改动
乙维斯: (git add...)
乙维斯: (运行安全扫描...)
乙维斯: ✅ 安全扫描通过！
乙维斯: (git commit...)
乙维斯: (git push...)
```

### 示例 3: 密钥查询
```
用户: 告诉我GitHub密码
乙维斯: 请告诉我验证答案：我的名字和你的名字
用户: yiweisi winston
乙维斯: (输出密钥...)
```

---

_乙维斯安全扫描器 - 保护你的每一次发布和提交_
