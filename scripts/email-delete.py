#!/usr/bin/env python3
"""
乙维斯 邮件删除工具
删除无用的退信邮件
"""

import poplib
from email.parser import Parser
from email.header import decode_header

class EmailDeleter:
    """邮件删除器"""
    
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
    
    def delete_emails(self):
        """删除退信邮件"""
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
            
            # 遍历所有邮件，标记要删除的
            to_delete = []
            
            print(f'\n正在扫描邮件...')
            print('-' * 50)
            
            for i in range(1, msg_count + 1):
                # 获取邮件
                resp, lines, octets = server.retr(i)
                
                # 解析邮件
                msg_content = b'\r\n'.join(lines).decode('utf-8', errors='ignore')
                msg = Parser().parsestr(msg_content)
                
                # 提取邮件信息
                subject = self.decode_str(msg['Subject'])
                from_addr = self.decode_str(msg['From'])
                
                # 判断是否是退信
                is_bounce = (
                    '系统退信' in subject or 
                    'Postmaster' in from_addr or
                    'MAILER-DAEMON' in from_addr or
                    'Undelivered' in subject
                )
                
                if is_bounce:
                    print(f'✓ 标记删除: 第 {i} 封 - {subject} - {from_addr}')
                    to_delete.append(i)
                else:
                    print(f'  保留: 第 {i} 封 - {subject} - {from_addr}')
            
            if not to_delete:
                print('\n没有需要删除的邮件')
                server.quit()
                return
            
            # 确认删除
            print(f'\n准备删除 {len(to_delete)} 封邮件...')
            print(f'邮件编号: {to_delete}')
            
            # 执行删除（标记为删除）
            for i in to_delete:
                server.dele(i)
            
            # 真正删除（退出时会执行）
            print('\n正在提交删除...')
            server.quit()
            
            print(f'✅ 成功删除 {len(to_delete)} 封邮件！')
            
        except Exception as e:
            print(f'删除邮件失败: {e}')
            import traceback
            traceback.print_exc()

def main():
    """删除退信邮件"""
    print('=' * 50)
    print('乙维斯 邮件删除工具')
    print('=' * 50)
    
    # 创建邮件删除器
    deleter = EmailDeleter()
    
    # 删除退信邮件
    deleter.delete_emails()

if __name__ == '__main__':
    main()
