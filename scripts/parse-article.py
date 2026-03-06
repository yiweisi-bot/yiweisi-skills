#!/usr/bin/env python3
"""
解析微信公众号文章
"""

import re
import html
import sys

def extract_article_content(html_file):
    """从HTML中提取文章内容"""
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 尝试提取js_content
        js_content_match = re.search(r'<div[^>]*id="js_content"[^>]*>(.*?)</div>\s*</div>\s*</div>', content, re.DOTALL)
        
        if js_content_match:
            article_html = js_content_match.group(1)
            
            # 简单清理HTML标签，只保留文本
            # 移除script标签
            article_html = re.sub(r'<script[^>]*>.*?</script>', '', article_html, flags=re.DOTALL)
            # 移除style标签
            article_html = re.sub(r'<style[^>]*>.*?</style>', '', article_html, flags=re.DOTALL)
            # 移除HTML标签，保留换行
            text = re.sub(r'<br\s*/?>', '\n', article_html)
            text = re.sub(r'<p[^>]*>', '\n', text)
            text = re.sub(r'</p>', '\n', text)
            text = re.sub(r'<[^>]+>', '', text)
            # 解码HTML实体
            text = html.unescape(text)
            # 清理多余的空行
            lines = [line.strip() for line in text.split('\n')]
            lines = [line for line in lines if line]
            text = '\n'.join(lines)
            
            return text
        else:
            return "未能找到文章内容"
            
    except Exception as e:
        return f"解析失败: {e}"

if __name__ == '__main__':
    html_file = '/tmp/article.html'
    print('正在解析文章...')
    print('=' * 60)
    content = extract_article_content(html_file)
    
    print(content[:15000])  # 只显示前15000字符
    if len(content) > 15000:
        print('\n... (内容已截断)')
