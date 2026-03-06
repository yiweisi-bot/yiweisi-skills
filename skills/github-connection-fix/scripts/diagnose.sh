#!/bin/bash

# GitHub连接问题诊断脚本
# 用途：快速诊断和修复GitHub连接问题

echo "=========================================="
echo "GitHub 连接问题诊断工具"
echo "=========================================="
echo ""

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查函数
check_ok() {
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ 通过${NC}"
        return 0
    else
        echo -e "${RED}❌ 失败${NC}"
        return 1
    fi
}

# 1. 检查DNS解析
echo "1. 检查DNS解析..."
echo -n "   - github.com: "
nslookup github.com 8.8.8.8 2>/dev/null | grep "Address:" | tail -1
echo -n "   - api.github.com: "
nslookup api.github.com 8.8.8.8 2>/dev/null | grep "Address:" | tail -1
echo ""

# 2. 检查hosts文件
echo "2. 检查hosts文件配置..."
echo "   当前GitHub相关配置："
grep -E "(github|git)" /etc/hosts 2>/dev/null || echo "   （未找到GitHub相关配置）"
echo ""

# 3. 测试wget
echo "3. 测试wget连接..."
echo -n "   - 测试GitHub API: "
wget -qO- --timeout=5 https://api.github.com 2>/dev/null | head -5 > /dev/null
check_ok
echo ""

# 4. 测试curl
echo "4. 测试curl连接..."
echo -n "   - 测试GitHub API: "
curl -s --max-time 5 https://api.github.com 2>/dev/null | head -5 > /dev/null
check_ok
echo ""

# 5. 检查SSH密钥
echo "5. 检查SSH密钥..."
echo "   可用的SSH密钥："
ls -la ~/.ssh/ 2>/dev/null | grep -E "\.(pub|pem)$" || echo "   （未找到公钥文件）"
echo ""

# 6. 提供修复建议
echo "=========================================="
echo "诊断完成！"
echo "=========================================="
echo ""
echo "常见修复方案："
echo ""
echo "1. 如果curl失败但wget成功："
echo "   - 检查api.github.com的IP地址"
echo "   - 更新/etc/hosts文件"
echo ""
echo "2. 如果DNS解析有问题："
echo "   - 使用8.8.8.8或1.1.1.1作为DNS服务器"
echo ""
echo "3. 如果需要更新hosts文件："
echo "   sudo sed -i 's/20.205.243.166 api.github.com/20.205.243.168 api.github.com/' /etc/hosts"
echo ""
echo "4. 完整的hosts配置示例："
echo "   # GitHub"
echo "   20.205.243.166 github.com"
echo "   20.205.243.166 gist.github.com"
echo "   20.205.243.168 api.github.com"
echo ""
echo "详细说明请参考 SKILL.md 文件"
echo ""
