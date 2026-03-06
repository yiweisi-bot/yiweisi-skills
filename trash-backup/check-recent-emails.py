
import poplib
import email
from email.header import decode_header

# 配置邮箱
POP3_SERVER = 'pop.163.com'
EMAIL = 'yiweisibot@163.com'
PASSWORD = 'LETRDkCf7PAipLeW'  # 使用授权码

try:
    # 连接 POP3 服务器
    print('连接邮箱服务器...')
    mail = poplib.POP3_SSL(POP3_SERVER)
    mail.user(EMAIL)
    mail.pass_(PASSWORD)
    print('登录成功！')
    
    # 获取邮件数量
    num_messages = len(mail.list()[1])
    print(f'收件箱中有 {num_messages} 封邮件')
    print('=' * 80)
    
    # 查看最近5封邮件
    start = max(1, num_messages - 4)
    for i in range(num_messages, start - 1, -1):
        print(f'\n邮件 #{i}')
        print('-' * 80)
        
        _, msg_lines, _ = mail.retr(i)
        msg_content = b'\r\n'.join(msg_lines)
        msg = email.message_from_bytes(msg_content)
        
        # 解析主题
        subject, encoding = decode_header(msg['Subject'])[0]
        if isinstance(subject, bytes):
            subject = subject.decode(encoding or 'utf-8')
        
        # 解析发件人
        from_ = msg.get('From')
        
        # 解析日期
        date = msg.get('Date')
        
        print(f'主题: {subject}')
        print(f'发件人: {from_}')
        print(f'时间: {date}')
    
    mail.quit()
    
except Exception as e:
    print(f'错误: {e}')
    import traceback
    traceback.print_exc()

