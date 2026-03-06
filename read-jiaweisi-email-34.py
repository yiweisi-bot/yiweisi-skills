
import poplib
import email
from email.header import decode_header
import os

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
    
    # 读取第34封邮件（最新的甲维斯邮件）
    print('读取第34封邮件（甲维斯发送的新邮件）...')
    print('=' * 80)
    
    _, msg_lines, _ = mail.retr(34)
    msg_content = b'\r\n'.join(msg_lines)
    msg = email.message_from_bytes(msg_content)
    
    # 解析主题
    subject, encoding = decode_header(msg['Subject'])[0]
    if isinstance(subject, bytes):
        subject = subject.decode(encoding or 'utf-8')
    
    print(f'主题: {subject}')
    print(f'发件人: {msg["From"]}')
    print(f'时间: {msg["Date"]}')
    print('=' * 80)
    
    # 检查附件和内容
    if msg.is_multipart():
        print('发现多部分邮件，检查附件和内容...')
        print('-' * 80)
        
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))
            
            print(f'内容类型: {content_type}')
            print(f'内容处置: {content_disposition}')
            
            # 如果是附件
            if "attachment" in content_disposition:
                filename = part.get_filename()
                if filename:
                    print(f'\n🎁 发现附件: {filename}')
                    
                    # 解码文件名
                    if filename and '=?' in filename:
                        filename = decode_header(filename)[0][0]
                        if isinstance(filename, bytes):
                            filename = filename.decode()
                    
                    print(f'保存文件名: {filename}')
                    
                    # 保存附件
                    payload = part.get_payload(decode=True)
                    if payload:
                        with open(filename, 'wb') as f:
                            f.write(payload)
                        print(f'✅ 附件已保存到: {os.path.abspath(filename)}')
                        
                        # 如果是压缩文件，尝试解压
                        if filename.endswith('.zip'):
                            print('\n尝试解压 ZIP 文件...')
                            import zipfile
                            with zipfile.ZipFile(filename, 'r') as zip_ref:
                                zip_ref.extractall('.')
                            print(f'✅ ZIP 文件已解压到当前目录')
                        elif filename.endswith('.tar.gz') or filename.endswith('.tgz'):
                            print('\n尝试解压 TAR.GZ 文件...')
                            import tarfile
                            with tarfile.open(filename, 'r:gz') as tar:
                                tar.extractall('.')
                            print(f'✅ TAR.GZ 文件已解压到当前目录')
            elif content_type == "text/plain":
                print('\n📄 文本内容:')
                print('-' * 80)
                try:
                    body = part.get_payload(decode=True).decode()
                    print(body)
                except Exception as e:
                    print(f'解码文本失败: {e}')
                    pass
            elif content_type == "text/html":
                print('\n📄 HTML内容 (跳过显示)')
            print()
    else:
        print('这不是一封多部分邮件')
        # 尝试获取文本内容
        if msg.get_content_type() == "text/plain":
            print('\n📄 文本内容:')
            print('-' * 80)
            try:
                body = msg.get_payload(decode=True).decode()
                print(body)
            except Exception as e:
                print(f'解码文本失败: {e}')
    
    mail.quit()
    print('\n✅ 邮件读取完成！')
    
except Exception as e:
    print(f'错误: {e}')
    import traceback
    traceback.print_exc()

