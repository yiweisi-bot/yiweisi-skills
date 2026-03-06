#!/usr/bin/env python3
"""
乙维斯 最简单邮件测试
直接使用SMTP发送，避免任何编码问题
"""

import smtplib
from datetime import datetime

def send_test_email():
    """发送测试邮件"""
    print('=' * 50)
    print('乙维斯 最简单邮件测试')
    print('=' * 50)
    
    # 配置
    smtp_server = 'smtp.163.com'
    smtp_port = 465
    email_address = 'yiweisibot@163.com'
    email_password = 'LETRDkCf7PAipLeW'
    
    to_email = 'wwzhen1083728594@gmail.com'
    
    # 最简单的邮件内容 - 纯英文，避免编码
    subject = 'Hello'
    body = f'''Hello,

This is Yiweisi.

Sending from yiweisibot@163.com.

Best regards,
Yiweisi
{datetime.now().strftime('%Y-%m-%d')}
'''
    
    print(f'\nTo: {to_email}')
    print(f'Subject: {subject}')
    print('-' * 50)
    
    try:
        # 直接构建邮件 - 发件人用纯英文，避免编码
        message = f'''\
From: Yiweisi <{email_address}>
To: {to_email}
Subject: {subject}

{body}
'''
        
        print(f'正在连接 {smtp_server}:{smtp_port}...')
        
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(email_address, email_password)
            print('登录成功！')
            
            server.sendmail(email_address, [to_email], message.encode('utf-8'))
            print(f'邮件发送成功！To: {to_email}')
            
        print('\n✅ 邮件发送成功！')
        return True
        
    except Exception as e:
        print(f'\n❌ 邮件发送失败: {e}')
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    send_test_email()
