#!/usr/bin/env python3
"""
乙维斯 心跳邮件检查工具
简单快速地检查邮件，用于心跳任务
⚠️ 安全版本：只读取邮件头，不读取邮件内容！
"""

import poplib
from email.header import decode_header

def decode_str(s):
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

def check_emails():
    """检查邮件 - 安全版本：只读取邮件头"""
    try:
        # 163邮箱POP3配置
        pop3_server = 'pop.163.com'
        pop3_port = 995
        email_address = 'yiweisibot@163.com'
        email_password = 'LETRDkCf7PAipLeW'
        
        # 连接POP3服务器
        server = poplib.POP3_SSL(pop3_server, pop3_port)
        server.user(email_address)
        server.pass_(email_password)
        
        # 获取邮件统计
        msg_count, msg_size = server.stat()
        
        print(f"📧 邮件检查完成：")
        print(f"   - 邮箱状态: 正常")
        print(f"   - 邮件数量: {msg_count} 封")
        print(f"   - 安全模式: 只读取邮件头，不读取内容")
        
        if msg_count > 0:
            # 只读取最新邮件的邮件头（TOP命令，不获取完整内容）
            latest_count = min(3, msg_count)
            print(f"   - 最新邮件:")
            
            for i in range(msg_count - latest_count + 1, msg_count + 1):
                # 使用TOP命令只获取邮件头（0表示只获取头，不获取内容）
                resp, lines, octets = server.top(i, 0)
                
                # 只解析邮件头部分
                from_header = ''
                subject_header = ''
                date_header = ''
                
                for line in lines:
                    line_str = line.decode('utf-8', errors='ignore')
                    if line_str.lower().startswith('from:'):
                        from_header = decode_str(line_str[5:].strip())
                    elif line_str.lower().startswith('subject:'):
                        subject_header = decode_str(line_str[8:].strip())
                    elif line_str.lower().startswith('date:'):
                        date_header = line_str[5:].strip()[:40]
                
                print(f"     * {date_header} - {from_header[:30]}")
                print(f"       主题: {subject_header[:50]}")
        
        server.quit()
        return True
        
    except Exception as e:
        print(f"📧 邮件检查：无法连接（{e}）")
        return False

if __name__ == "__main__":
    check_emails()
