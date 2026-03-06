#!/usr/bin/env python3
"""
乙维斯 邮件读取工具
读取特定邮件的完整内容
"""

import poplib
from email.parser import Parser
from email.header import decode_header
import email

class EmailReader:
    """邮件读取器"""
    
    def __init__(self):
        # 163邮箱POP3配置
        self.pop3_server = 'pop.163.com'
        self.pop3_port = 995
        self.email_address = 'yiweisibot@163.com'
        self.email_password = 'LETRDkCf7PAipLeW'  # 授权码
    
    def decode_str(self, s):
        """解码邮件头字符串"""
        if not s:
            return ''
        value, charset = decode_header(s)[0]
        if charset:
            try:
                value = value.decode(charset)
            except:
                value = str(value)
        return value
    
    def get_email_content(self, msg):
        """获取邮件正文内容"""
        content = ''
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                if content_type == 'text/plain' or content_type == 'text/html':
                    try:
                        payload = part.get_payload(decode=True)
                        charset = part.get_content_charset() or 'utf-8'
                        content += payload.decode(charset, errors='ignore')
                    except:
                        pass
        else:
            try:
                payload = msg.get_payload(decode=True)
                charset = msg.get_content_charset() or 'utf-8'
                content = payload.decode(charset, errors='ignore')
            except:
                pass
        return content
    
    def read_all_emails(self):
        """读取所有邮件"""
        try:
            print(f'正在连接 {self.pop3_server}:{self.pop3_port}...')
            
            # 连接POP3服务器
            server = poplib.POP3_SSL(self.pop3_server, self.pop3_port)
            server.user(self.email_address)
            server.pass_(self.email_password)
            
            print('登录成功！')
            
            # 获取邮件统计
            msg_count, msg_size = server.stat()
            print(f'邮箱中共有 {msg_count} 封邮件')
            
            if msg_count == 0:
                print('邮箱中没有邮件')
                server.quit()
                return
            
            # 读取所有邮件
            print(f'\n开始读取所有邮件...')
            print('=' * 60)
            
            for i in range(1, msg_count + 1):
                print(f'\n【邮件 {i}】')
                print('-' * 60)
                
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
                
                print(f'主题: {subject}')
                print(f'发件人: {from_addr}')
                print(f'收件人: {to_addr}')
                print(f'日期: {date}')
                print()
                
                # 获取邮件内容
                content = self.get_email_content(msg)
                if content:
                    print('--- 邮件内容 ---')
                    # 只显示前500字符，避免太长
                    print(content[:800])
                    if len(content) > 800:
                        print('... (内容已截断)')
                print()
                
            server.quit()
            
        except Exception as e:
            print(f'读取邮件失败: {e}')
            import traceback
            traceback.print_exc()

def main():
    """读取所有邮件"""
    print('=' * 60)
    print('乙维斯 邮件读取工具')
    print('=' * 60)
    
    # 创建邮件读取器
    reader = EmailReader()
    
    # 读取所有邮件
    reader.read_all_emails()

if __name__ == '__main__':
    main()
