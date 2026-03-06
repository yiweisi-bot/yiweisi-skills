#!/usr/bin/env python3
"""
乙维斯 邮件附件下载工具
读取特定邮件并下载附件
"""

import poplib
from email.parser import Parser
from email.header import decode_header
import email
import os
import sys

class EmailAttachmentDownloader:
    """邮件附件下载器"""
    
    def __init__(self):
        # 163邮箱POP3配置
        self.pop3_server = 'pop.163.com'
        self.pop3_port = 995
        self.email_address = 'yiweisibot@163.com'
        self.email_password = 'LETRDkCf7PAipLeW'  # 授权码
        
        # 附件保存目录
        self.attachment_dir = '/root/.openclaw/workspace/email-attachments'
        os.makedirs(self.attachment_dir, exist_ok=True)
    
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
    
    def save_attachments(self, msg, email_num):
        """保存邮件附件"""
        attachments = []
        
        if msg.is_multipart():
            for part in msg.walk():
                # 检查是否是附件
                filename = part.get_filename()
                if filename:
                    # 解码文件名
                    filename = self.decode_str(filename)
                    
                    # 保存附件
                    attachment_path = os.path.join(self.attachment_dir, f'email-{email_num}-{filename}')
                    
                    try:
                        payload = part.get_payload(decode=True)
                        with open(attachment_path, 'wb') as f:
                            f.write(payload)
                        attachments.append({
                            'filename': filename,
                            'path': attachment_path,
                            'size': len(payload)
                        })
                        print(f'  ✅ 已保存附件: {filename} ({len(payload)} bytes)')
                    except Exception as e:
                        print(f'  ❌ 保存附件失败 {filename}: {e}')
        
        return attachments
    
    def read_email_with_attachments(self, email_num):
        """读取特定邮件并下载附件"""
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
            
            if email_num < 1 or email_num > msg_count:
                print(f'错误: 邮件编号 {email_num} 超出范围 (1-{msg_count})')
                server.quit()
                return
            
            print(f'\n正在读取邮件 {email_num}...')
            print('=' * 60)
            
            # 获取邮件
            resp, lines, octets = server.retr(email_num)
            
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
                print(content)
                print()
            
            # 保存附件
            print('--- 附件 ---')
            attachments = self.save_attachments(msg, email_num)
            
            if not attachments:
                print('  此邮件没有附件')
            else:
                print(f'\n共保存 {len(attachments)} 个附件到: {self.attachment_dir}')
            
            server.quit()
            
            return attachments
            
        except Exception as e:
            print(f'读取邮件失败: {e}')
            import traceback
            traceback.print_exc()
            return None

def main():
    """主函数"""
    print('=' * 60)
    print('乙维斯 邮件附件下载工具')
    print('=' * 60)
    
    # 检查参数
    if len(sys.argv) < 2:
        print('\n用法: python3 email-attachments.py <邮件编号>')
        print('示例: python3 email-attachments.py 34  (读取第34封邮件)')
        print()
        
        # 列出最近的邮件
        print('最近的邮件:')
        downloader = EmailAttachmentDownloader()
        
        try:
            server = poplib.POP3_SSL(downloader.pop3_server, downloader.pop3_port)
            server.user(downloader.email_address)
            server.pass_(downloader.email_password)
            
            msg_count, _ = server.stat()
            
            # 显示最近10封邮件
            start = max(1, msg_count - 9)
            for i in range(msg_count, start - 1, -1):
                resp, lines, octets = server.retr(i)
                msg_content = b'\r\n'.join(lines).decode('utf-8', errors='ignore')
                msg = Parser().parsestr(msg_content)
                subject = downloader.decode_str(msg['Subject'])
                from_addr = downloader.decode_str(msg['From'])
                print(f'  [{i}] {subject} - {from_addr}')
            
            server.quit()
        except Exception as e:
            print(f'获取邮件列表失败: {e}')
        
        return
    
    email_num = int(sys.argv[1])
    
    # 创建邮件下载器
    downloader = EmailAttachmentDownloader()
    
    # 读取邮件并下载附件
    downloader.read_email_with_attachments(email_num)

if __name__ == '__main__':
    main()
