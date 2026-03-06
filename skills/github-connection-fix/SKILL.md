---
name: github-connection-fix
description: 修复GitHub连接问题的完整解决方案。包括DNS解析问题、API访问失败、SSH认证问题等。当遇到curl卡住、gh CLI验证失败、GitHub API无法访问等问题时使用此技能。
---

# GitHub 连接问题修复技能

## 问题诊断

当遇到以下问题时，使用此技能：

1. **curl访问GitHub API卡住** - curl命令没有输出，卡在TLS握手
2. **gh CLI验证失败** - error validating token: HTTP 406
3. **GitHub API返回404或重定向** - API调用异常
4. **SSH认证失败** - Permission denied (publickey)

## 解决方案

### 1. DNS解析问题修复（最常见）

**问题表现**：
- curl访问api.github.com卡住
- wget可以正常访问
- 域名解析到错误的IP地址

**修复步骤**：

```bash
# 检查当前DNS解析
nslookup github.com 8.8.8.8
nslookup api.github.com 8.8.8.8

# 查看当前hosts文件
cat /etc/hosts
```

**正确的GitHub IP地址（2026-03-01）**：
```
github.com: 20.205.243.166
api.github.com: 20.205.243.168
gist.github.com: 20.205.243.166
raw.githubusercontent.com: 185.199.108.133, 185.199.109.133, 185.199.110.133, 185.199.111.133
```

**更新hosts文件**：
```bash
# 备份原始hosts
cp /etc/hosts /etc/hosts.backup

# 更新GitHub相关IP
sed -i 's/20.205.243.166 api.github.com/20.205.243.168 api.github.com/' /etc/hosts

# 或者直接编辑hosts文件添加：
# 20.205.243.166 github.com
# 20.205.243.166 gist.github.com
# 20.205.243.168 api.github.com
```

**验证修复**：
```bash
# 测试API访问
curl -s https://api.github.com/user | head -10

# 如果有token，测试认证
curl -s -H "Authorization: token YOUR_TOKEN" https://api.github.com/user
```

### 2. 使用wget替代curl（临时方案）

当curl无法工作时，wget通常可以正常工作：

```bash
# 测试GitHub API
wget -qO- https://api.github.com/user

# 带认证的API调用
wget --header="Authorization: token YOUR_TOKEN" -qO- https://api.github.com/user

# 创建仓库
wget --header="Authorization: token YOUR_TOKEN" \
     --header="Content-Type: application/json" \
     --post-data='{"name":"repo-name","private":false}' \
     -qO- https://api.github.com/user/repos
```

### 3. SSH密钥配置

**生成新的SSH密钥**：
```bash
# ED25519格式（推荐）
ssh-keygen -t ed25519 -C "your-email@example.com" -f ~/.ssh/id_ed25519_github

# RSA格式（兼容性更好）
ssh-keygen -t rsa -b 4096 -C "your-email@example.com" -f ~/.ssh/id_rsa_github
```

**配置SSH使用特定密钥**：

方法1：命令行指定
```bash
GIT_SSH_COMMAND="ssh -i ~/.ssh/id_ed25519_github -o IdentitiesOnly=yes" git clone git@github.com:user/repo.git
```

方法2：创建SSH配置文件 `~/.ssh/config`
```
Host github.com
  HostName github.com
  User git
  IdentityFile ~/.ssh/id_ed25519_github
  IdentitiesOnly yes
```

**测试SSH认证**：
```bash
ssh -i ~/.ssh/id_ed25519_github -T git@github.com
```

### 4. GitHub CLI配置

**手动配置gh CLI认证**：
```bash
# 创建配置目录
mkdir -p ~/.config/gh

# 创建hosts.yml文件
cat > ~/.config/gh/hosts.yml << 'EOF'
github.com:
  oauth_token: YOUR_TOKEN
  user: YOUR_USERNAME
EOF

# 验证配置
gh auth status
```

## 诊断脚本

使用提供的诊断脚本来快速检查和修复问题：

```bash
# 运行诊断脚本
bash /root/.openclaw/workspace/skills/github-connection-fix/scripts/diagnose.sh
```

## 快速修复清单

遇到GitHub连接问题时，按以下顺序检查：

1. ✅ 检查DNS解析（nslookup）
2. ✅ 检查hosts文件配置
3. ✅ 测试wget是否能访问（wget -qO- https://api.github.com）
4. ✅ 测试curl是否能访问（curl -s https://api.github.com）
5. ✅ 检查SSH密钥配置
6. ✅ 验证GitHub token有效性

## 常见错误及解决方案

| 错误 | 原因 | 解决方案 |
|------|------|---------|
| curl卡住无输出 | api.github.com IP错误 | 更新hosts文件，使用正确的IP |
| HTTP 406 Not Acceptable | token验证失败 | 检查token权限和格式 |
| 301 Moved Permanently | API端点重定向 | 检查请求URL和方法 |
| Permission denied (publickey) | SSH密钥错误 | 配置正确的SSH密钥 |

## 参考资源

- GitHub SSH密钥配置：https://docs.github.com/en/authentication/connecting-to-github-with-ssh
- GitHub API文档：https://docs.github.com/en/rest
- hosts文件配置指南：https://man7.org/linux/man-pages/man5/hosts.5.html
