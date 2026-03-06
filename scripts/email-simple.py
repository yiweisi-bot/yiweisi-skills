#!/usr/bin/env python3
"""
乙维斯 简单邮件发送工具
使用最简单的方式，避免编码问题
"""

import smtplib
from email.mime.text import MIMEText
from datetime import datetime

def send_simple_email():
    """发送简单邮件"""
    print('=' * 50)
    print('乙维斯 简单邮件发送工具')
    print('=' * 50)
    
    # 配置
    smtp_server = 'smtp.163.com'
    smtp_port = 465
    email_address = 'yiweisibot@163.com'
    email_password = 'LETRDkCf7PAipLeW'
    sender_name = '乙维斯'
    
    to_email = 'wwzhen1083728594@gmail.com'
    subject = '你好'
    
    # 邮件内容
    content = f'''你好，

我是乙维斯。

这是我从 yiweisibot@163.com 发送的邮件。

祝好，
乙维斯
{datetime.now().strftime('%Y-%m-%d')}
'''
    
    print(f'\n准备发送邮件到: {to_email}')
    print(f'主题: {subject}')
    print('-' * 50)
    
    try:
        # 创建简单的文本邮件
        msg = MIMEText(content, 'plain', 'utf-8')
        msg['From'] = f'{sender_name} <{email_address}>'
        msg['To'] = to_email
        msg['Subject'] = subject
        
        print(f'正在连接 {smtp_server}:{smtp_port}...')
        
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(email_address, email_password)
            print('登录成功！')
            
            server.sendmail(email_address, [to_email], msg.as_string())
            print(f'邮件发送成功！To: {to_email}')
            
        print('\n✅ 邮件发送成功！')
        return True
        
    except Exception as e:
        print(f'\n❌ 邮件发送失败: {e}')
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    send_simple_email()
