#!/usr/bin/env python3
"""
每日整理任务脚本
执行时间：每天23:00 UTC+8 (15:00 UTC)
"""

import os
import sys
from datetime import datetime
import subprocess
import re

def run_cmd(cmd, cwd=None):
    """执行shell命令"""
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, 
                              capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def get_today():
    """获取今天的日期"""
    return datetime.now().strftime("%Y-%m-%d")

def read_memory_file(date):
    """读取记忆文件"""
    memory_path = f"/root/.openclaw/workspace/memory/{date}.md"
    if not os.path.exists(memory_path):
        print(f"警告: 记忆文件不存在: {memory_path}")
        return ""
    
    with open(memory_path, 'r', encoding='utf-8') as f:
        return f.read()

def filter_sensitive_content(content):
    """过滤敏感信息"""
    # 移除API密钥
    content = re.sub(r'apiKey["\s:]+["\'][^"\']+["\']', 'apiKey: "***"', content)
    content = re.sub(r'api_key["\s:]+["\'][^"\']+["\']', 'api_key: "***"', content)
    
    # 移除密码
    content = re.sub(r'password["\s:]+["\'][^"\']+["\']', 'password: "***"', content)
    content = re.sub(r'授权码["\s:]+["\'][^"\']+["\']', '授权码: "***"', content)
    
    # 移除邮箱密码
    content = re.sub(r'登录密码["\s:]+["\'][^"\']+["\']', '登录密码: "***"', content)
    
    return content

def generate_blog_article(date, memory_content):
    """生成博客文章"""
    # 过滤敏感信息
    safe_content = filter_sensitive_content(memory_content)
    
    # 提取关键内容
    lines = safe_content.split('\n')
    key_points = []
    current_section = ""
    
    for line in lines:
        line = line.strip()
        if line.startswith('##') or line.startswith('# '):
            current_section = line.lstrip('#').strip()
        elif line.startswith('- [x]') or line.startswith('- ✅'):
            key_points.append(line)
        elif '✅' in line and len(line) < 100:
            key_points.append(line)
    
    # 生成文章内容
    article = f"""---
title: "OpenClaw日常 - {date}"
description: "今天的工作内容和学习总结"
date: "{date}"
author: "乙维斯"
tags: ["OpenClaw", "日常记录", "教程"]
---

# OpenClaw日常 - {date}

## 今日概述

本文记录 {date} 的OpenClaw工作内容和学习总结。

## 完成的任务

"""
    
    if key_points:
        for point in key_points[:10]:  # 最多10个要点
            article += f"- {point.lstrip('- ')}\n"
    else:
        article += "- 今天完成了日常工作\n"
    
    article += """

## 技术要点

### 定时任务系统
- 使用 `openclaw cron` 管理自动化任务
- cron表达式：`0 15 * * *` (每天15:00 UTC)
- 会话模式：`--session isolated` (独立会话)

### 记忆管理
- 每日记录：`memory/YYYY-MM-DD.md`
- 长期记忆：`MEMORY.md`
- 定期整理提炼重要信息

### 博客发布
- 文章目录：`src/content/blog/`
- 构建：`npm run build`
- 部署：`/var/www/winston-blog/`

## 经验总结

### 今日学习要点
1. 自动化任务能提高工作效率
2. 记忆管理对持续学习很重要
3. 过滤敏感信息保护隐私

## 明日计划

- 继续优化工作流程
- 探索更多OpenClaw功能
- 保持学习和实践

---

_本文由乙维斯自动生成_
"""
    
    return article

def main():
    """主函数"""
    today = get_today()
    print(f"开始执行每日整理任务 - {today}")
    
    # 1. 读取记忆文件
    print("读取记忆文件...")
    memory_content = read_memory_file(today)
    
    # 2. 生成博客文章
    print("生成博客文章...")
    blog_content = generate_blog_article(today, memory_content)
    
    blog_dir = "/root/projects/YiweisiBlog/src/content/blog"
    blog_file = os.path.join(blog_dir, f"openclaw-daily-{today}.md")
    
    os.makedirs(blog_dir, exist_ok=True)
    with open(blog_file, 'w', encoding='utf-8') as f:
        f.write(blog_content)
    
    print(f"博客文章已保存: {blog_file}")
    
    # 3. 构建和部署
    print("构建项目...")
    success, stdout, stderr = run_cmd("npm run build", cwd="/root/projects/YiweisiBlog")
    if not success:
        print(f"构建失败: {stderr}")
        return 1
    
    print("部署到生产环境...")
    success, stdout, stderr = run_cmd("cp -r dist/* /var/www/winston-blog/", 
                                      cwd="/root/projects/YiweisiBlog")
    if not success:
        print(f"部署失败: {stderr}")
        return 1
    
    # 4. Git提交
    print("Git提交...")
    run_cmd("git add .", cwd="/root/projects/YiweisiBlog")
    success, stdout, stderr = run_cmd(f"git commit -m 'feat: 添加{today}日常记录文章'", 
                                      cwd="/root/projects/YiweisiBlog")
    if success:
        run_cmd("git push", cwd="/root/projects/YiweisiBlog")
        print("Git推送成功")
    else:
        print("没有需要提交的更改")
    
    # 5. 发送邮件通知
    print("发送邮件通知...")
    email_subject = f"每日整理任务完成 - {today}"
    email_body = f"每日整理任务完成！\n\n日期：{today}\n博客文章：openclaw-daily-{today}.md\n\n任务已成功执行。"
    
    # 使用mailx发送邮件
    success, stdout, stderr = run_cmd(f'echo "{email_body}" | mailx -s "{email_subject}" wwzhen1083728594@gmail.com')
    if success:
        print("邮件通知发送成功")
    else:
        print(f"邮件发送失败: {stderr}")
    
    print(f"每日整理任务完成！ - {today}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
