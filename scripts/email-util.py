#!/usr/bin/env python3
"""
乙维斯 邮箱管理工具
使用163邮箱SMTP服务发送邮件
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from datetime import datetime

class EmailManager:
    """邮箱管理器"""
    
    def __init__(self):
        # 163邮箱SMTP配置
        self.smtp_server = 'smtp.163.com'
        self.smtp_port = 465  # SSL端口
        self.email_address = 'yiweisibot@163.com'
        self.email_password = 'LETRDkCf7PAipLeW'  # 授权码
        self.sender_name = '乙维斯'
    
    def send_email(self, to_email, subject, content, html_content=None):
        """
        发送邮件
        
        Args:
            to_email: 收件人邮箱
            subject: 邮件主题
            content: 邮件正文（纯文本）
            html_content: 邮件正文（HTML格式，可选）
        """
        try:
            # 创建邮件对象
            msg = MIMEMultipart()
            msg['From'] = f'{self.sender_name} <{self.email_address}>'
            msg['To'] = to_email
            msg['Subject'] = Header(subject, 'utf-8')
            
            # 添加纯文本内容
            text_part = MIMEText(content, 'plain', 'utf-8')
            msg.attach(text_part)
            
            # 如果有HTML内容，也添加
            if html_content:
                html_part = MIMEText(html_content, 'html', 'utf-8')
                msg.attach(html_part)
            
            # 连接SMTP服务器并发送
            print(f'正在连接 {self.smtp_server}:{self.smtp_port}...')
            
            with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port) as server:
                server.login(self.email_address, self.email_password)
                print('登录成功！')
                
                server.sendmail(self.email_address, [to_email], msg.as_string())
                print(f'邮件发送成功！To: {to_email}')
                
            return True
            
        except Exception as e:
            print(f'邮件发送失败: {e}')
            return False

def main():
    """测试邮件发送"""
    print('=' * 50)
    print('乙维斯 邮箱管理工具')
    print('=' * 50)
    
    # 创建邮箱管理器
    email_manager = EmailManager()
    
    # 测试邮件内容
    to_email = 'wwzhen1083728594@gmail.com'
    subject = '你好'
    
    # 邮件正文
    content = f'''你好，

我是乙维斯。

这是我从 yiweisibot@163.com 发送的邮件。

祝好，
乙维斯
{datetime.now().strftime('%Y-%m-%d')}
'''
    
    # 发送邮件
    print(f'\n准备发送邮件到: {to_email}')
    print(f'主题: {subject}')
    print('-' * 50)
    
    success = email_manager.send_email(to_email, subject, content)
    
    if success:
        print('\n✅ 邮件发送成功！')
    else:
        print('\n❌ 邮件发送失败，请检查配置。')

if __name__ == '__main__':
    main()
