#!/usr/bin/env python3
"""
乙维斯安全扫描器 - 检测密钥、密码等敏感信息
"""

import re
import sys
import os
import json
from pathlib import Path
from typing import List, Dict, Tuple


class SecurityScanner:
    """安全扫描器"""

    def __init__(self):
        # 定义敏感信息模式
        self.patterns = {
            # GitHub Tokens
            'github_token': r'ghp_[A-Za-z0-9]{36}',
            'github_pat': r'github_pat_[A-Za-z0-9_]+',

            # API Keys
            'openai_key': r'sk-[A-Za-z0-9]{48}',
            'deepseek_key': r'sk-[A-Za-z0-9]{32}',
            'zhipu_key': r'[A-Za-z0-9]{32}\.[A-Za-z0-9]{16}',
            'doubao_key': r'[A-Za-z0-9]{8}-[A-Za-z0-9]{4}-[A-Za-z0-9]{4}-[A-Za-z0-9]{4}-[A-Za-z0-9]{12}',

            # 密码模式
            'password': r'password[:=]\s*[\'"][A-Za-z0-9!@#$%^&*]+[\'"]',

            # SSH Keys
            'ssh_private_key': r'-----BEGIN (RSA|DSA|EC|OPENSSH) PRIVATE KEY-----',
            'ssh_key_path': r'~/.ssh/id_[a-z0-9_]+',

            # 数据库连接串
            'database_url': r'(mysql|postgresql|mongodb|redis)://[^\s]+',

            # 邮箱
            'email': r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
        }

        # 白名单：公开的、安全的信息
        self.whitelist = {
            # 公开的联系邮箱（可以在博客上展示）
            'yiweisibot@163.com',
        }

        # 已知的密钥（从记忆中获取，用于黑名单）
        self.known_secrets = {
            # 163 邮箱密码
            'YiweisiBot123',
            'LETRDkCf7PAipLeW',

            # GitHub
            'ghp_***REDACTED***',

            # 验证答案
            'yiweisi winston',

            # API Keys
            'd5daa222-ce58-4915-b63f-9abb00d06862',
            '260b02dcbd0441d09aa431a4d3e016ce.OaOxG9B22mXn31S5',
            'sk-85d8408494d04c1ca24ab261a44926bf',
        }

    def scan_text(self, text: str) -> List[Dict]:
        """扫描文本中的敏感信息"""
        findings = []

        # 使用正则模式扫描
        for pattern_name, pattern in self.patterns.items():
            # 跳过 email 模式（普通邮箱不是敏感信息）
            if pattern_name == 'email':
                continue
                
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                findings.append({
                    'type': pattern_name,
                    'match': match.group(),
                    'position': match.start(),
                    'line': text.count('\n', 0, match.start()) + 1
                })

        # 检查已知密钥
        for secret in self.known_secrets:
            if secret in text:
                findings.append({
                    'type': 'known_secret',
                    'match': secret[:4] + '****' + secret[-4:],  # 部分隐藏
                    'position': text.find(secret),
                    'line': text.count('\n', 0, text.find(secret)) + 1
                })

        # 过滤白名单
        filtered_findings = []
        for finding in findings:
            # 检查是否在白名单中
            in_whitelist = False
            for whitelisted in self.whitelist:
                if whitelisted in finding.get('match', ''):
                    in_whitelist = True
                    break
            if not in_whitelist:
                filtered_findings.append(finding)

        return filtered_findings

    def scan_file(self, file_path: str) -> Tuple[bool, List[Dict]]:
        """扫描单个文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            findings = self.scan_text(content)

            if findings:
                print(f"❌ 发现 {len(findings)} 个问题在 {file_path}:")
                for finding in findings:
                    print(f"  - 第 {finding['line']} 行: {finding['type']}")
                return False, findings
            else:
                print(f"✅ {file_path} - 未发现敏感信息")
                return True, []

        except Exception as e:
            print(f"❌ 扫描文件失败: {e}")
            return False, []

    def scan_directory(self, dir_path: str, extensions: List[str] = None) -> Tuple[bool, List[Dict]]:
        """扫描整个目录"""
        if extensions is None:
            extensions = ['.md', '.ts', '.tsx', '.js', '.jsx', '.json', '.env', '.yaml', '.yml']

        all_findings = []
        all_clean = True

        dir_path = Path(dir_path)
        if not dir_path.exists():
            print(f"❌ 目录不存在: {dir_path}")
            return False, []

        for file_path in dir_path.rglob('*'):
            if file_path.is_file() and file_path.suffix in extensions:
                # 跳过 node_modules, .git 等目录
                if any(part in ['.git', 'node_modules', '__pycache__'] for part in file_path.parts):
                    continue

                clean, findings = self.scan_file(str(file_path))
                if not clean:
                    all_clean = False
                    all_findings.extend([{'file': str(file_path), **f} for f in findings])

        return all_clean, all_findings


def main():
    """主函数"""
    scanner = SecurityScanner()

    if len(sys.argv) < 2:
        print("""
乙维斯安全扫描器

使用方法:
  python scan.py scan-file <文件路径>    - 扫描单个文件
  python scan.py scan-repo <目录路径>     - 扫描整个目录
  python scan.py scan-text <文本>          - 扫描文本
        """)
        return

    command = sys.argv[1]

    if command == 'scan-file' and len(sys.argv) == 3:
        scanner.scan_file(sys.argv[2])
    elif command == 'scan-repo' and len(sys.argv) == 3:
        clean, findings = scanner.scan_directory(sys.argv[2])
        if clean:
            print("\n✅ 扫描完成，未发现敏感信息！")
        else:
            print(f"\n❌ 扫描完成，发现 {len(findings)} 个问题！")
            sys.exit(1)
    elif command == 'scan-text' and len(sys.argv) == 3:
        findings = scanner.scan_text(sys.argv[2])
        if findings:
            print(f"❌ 发现 {len(findings)} 个问题:")
            for finding in findings:
                print(f"  - {finding['type']}")
        else:
            print("✅ 文本安全！")
    else:
        print("❌ 参数错误，请查看帮助")


if __name__ == '__main__':
    main()
