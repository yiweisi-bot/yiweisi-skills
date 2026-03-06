#!/usr/bin/env python3
"""
乙维斯 邮件收取工具
使用POP3收取163邮箱邮件
"""

import poplib
from email.parser import Parser
from email.header import decode_header
from datetime import datetime

class EmailReceiver:
    """邮件收取器"""
    
    def __init__(self):
        # 163邮箱POP3配置
        self.pop3_server = 'pop.163.com'
        self.pop3_port = 995
        self.email_address = 'yiweisibot@163.com'
        self.email_password = 'LETRDkCf7PAipLeW'  # 授权码
    
    def decode_str(self, s):
        """解码邮件头字符串"""
        value, charset = decode_header(s)[0]
        if charset:
            value = value.decode(charset)
        return value
    
    def get_emails(self, count=5):
        """
        获取最新的邮件
        
        Args:
            count: 要获取的邮件数量
        """
        try:
            print(f'正在连接 {self.pop3_server}:{self.pop3_port}...')
            
            # 连接POP3服务器
            server = poplib.POP3_SSL(self.pop3_server, self.pop3_port)
            server.user(self.email_address)
            server.pass_(self.email_password)
            
            print('登录成功！')
            
            # 获取邮件统计
            msg_count, msg_size = server.stat()
            print(f'邮箱中共有 {msg_count} 封邮件，总大小 {msg_size} 字节')
            
            if msg_count == 0:
                print('邮箱中没有邮件')
                server.quit()
                return []
            
            # 获取最新的count封邮件
            emails = []
            start = max(1, msg_count - count + 1)
            
            for i in range(start, msg_count + 1):
                print(f'\n正在获取第 {i} 封邮件...')
                
                # 获取邮件
                resp, lines, octets = server.retr(i)
                
                # 解析邮件
                msg_content = b'\r\n'.join(lines).decode('utf-8', errors='ignore')
                msg = Parser().parsestr(msg_content)
                
                # 提取邮件信息
                subject = self.decode_str(msg['Subject'])
                from_addr = self.decode_str(msg['From'])
                to_addr = self.decode_str(msg['To'])
                date = msg['Date']
                
                print(f'  主题: {subject}')
                print(f'  发件人: {from_addr}')
                print(f'  收件人: {to_addr}')
                print(f'  日期: {date}')
                
                emails.append({
                    'index': i,
                    'subject': subject,
                    'from': from_addr,
                    'to': to_addr,
                    'date': date
                })
            
            server.quit()
            return emails
            
        except Exception as e:
            print(f'收取邮件失败: {e}')
            import traceback
            traceback.print_exc()
            return []

def main():
    """测试收取邮件"""
    print('=' * 50)
    print('乙维斯 邮件收取工具')
    print('=' * 50)
    
    # 创建邮件收取器
    receiver = EmailReceiver()
    
    # 收取最新的5封邮件
    print('\n准备收取最新的5封邮件...')
    print('-' * 50)
    
    emails = receiver.get_emails(count=5)
    
    if emails:
        print(f'\n✅ 成功收取 {len(emails)} 封邮件！')
    else:
        print('\n❌ 未能收取到邮件')

if __name__ == '__main__':
    main()
