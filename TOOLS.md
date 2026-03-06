# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

## Local Configuration

### Environment

- OS: Linux 6.6.117-45.1.oc9.x86_64
- Node: v22.22.0
- Python: (待确认)
- Working directory: /root/.openclaw/workspace

### Available Skills

- agent-browser 🌐 - 浏览器自动化工具
- file-search 🔍 - 文件搜索（fd + ripgrep）
- rememberall - 提醒系统
- openclaw-auto-updater - 自动更新工具

### Channel Config

- 当前频道: dingtalk
- 能力: capabilities=none (待启用更多功能)

---

## Yiweisi Bot 邮箱配置

### 邮箱账号（重要！）
- **邮箱地址**: yiweisibot@163.com
- **登录密码**: YiweisiBot123
- **授权码**: LETRDkCf7PAipLeW
- **用途**: Git提交、服务通知、账号注册、发送邮件等

⚠️ **重要提醒**: 
- 此密码和授权码需要严格保密，不要泄露
- 如需修改密码请及时更新此文件
- 不要在公开仓库或对话中泄露此密码和授权码
- 授权码用于SMTP发送邮件，登录密码用于网页登录

### Git配置
- **Git用户名**: Yiweisi Bot
- **Git邮箱**: yiweisibot@163.com

---

## 甲维斯 邮箱配置

### 邮箱账号
- **邮箱地址**: jiaweisibot@163.com
- **用途**: 甲维斯（OpenClaw机器人2号）的专属邮箱

⚠️ **重要提醒**:
- 此邮箱用于甲维斯的相关操作
- 密码等敏感信息待后续配置后更新
