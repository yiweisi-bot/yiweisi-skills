#!/bin/bash
# 乙维斯安全扫描器 - Shell 包装器

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SCAN_SCRIPT="$SKILL_DIR/scripts/scan.py"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

print_banner() {
    echo -e "${YELLOW}"
    echo "╔═══════════════════════════════════════════════════════════════╗"
    echo "║                    乙维斯安全扫描器                              ║"
    echo "║              Yiweisi Security Scanner                           ║"
    echo "╚═══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

print_help() {
    print_banner
    echo "使用方法:"
    echo "  $0 scan-file <文件路径>    - 扫描单个文件"
    echo "  $0 scan-repo <目录路径>     - 扫描整个目录"
    echo "  $0 scan-text <文本>          - 扫描文本"
    echo "  $0 scan-blog                 - 扫描博客文章目录"
    echo "  $0 scan-staged               - 扫描 git 暂存区"
    echo "  $0 help                      - 显示帮助"
    echo ""
}

scan_file() {
    local file="$1"
    if [ ! -f "$file" ]; then
        echo -e "${RED}❌ 文件不存在: $file${NC}"
        return 1
    fi
    print_banner
    echo -e "${YELLOW}🔍 正在扫描文件: $file${NC}"
    echo ""
    python3 "$SCAN_SCRIPT" scan-file "$file"
}

scan_repo() {
    local dir="$1"
    if [ ! -d "$dir" ]; then
        echo -e "${RED}❌ 目录不存在: $dir${NC}"
        return 1
    fi
    print_banner
    echo -e "${YELLOW}🔍 正在扫描目录: $dir${NC}"
    echo ""
    python3 "$SCAN_SCRIPT" scan-repo "$dir"
}

scan_text() {
    local text="$1"
    print_banner
    echo -e "${YELLOW}🔍 正在扫描文本${NC}"
    echo ""
    python3 "$SCAN_SCRIPT" scan-text "$text"
}

scan_blog() {
    local blog_dir="/root/projects/YiweisiBlog/src/content/blog"
    if [ ! -d "$blog_dir" ]; then
        echo -e "${RED}❌ 博客目录不存在: $blog_dir${NC}"
        return 1
    fi
    print_banner
    echo -e "${YELLOW}🔍 正在扫描博客文章目录${NC}"
    echo ""
    python3 "$SCAN_SCRIPT" scan-repo "$blog_dir"
}

scan_staged() {
    # 检查是否在 git 仓库中
    if ! git rev-parse --git-dir > /dev/null 2>&1; then
        echo -e "${RED}❌ 当前不在 git 仓库中${NC}"
        return 1
    fi

    print_banner
    echo -e "${YELLOW}🔍 正在扫描 git 暂存区${NC}"
    echo ""

    # 创建临时文件
    local temp_file=$(mktemp)

    # 获取暂存区的文件
    git diff --cached --name-only > "$temp_file"

    if [ ! -s "$temp_file" ]; then
        echo -e "${GREEN}✅ git 暂存区为空${NC}"
        rm "$temp_file"
        return 0
    fi

    # 扫描每个暂存的文件
    local has_issues=0
    while IFS= read -r file; do
        if [ -f "$file" ]; then
            echo -e "${YELLOW}扫描: $file${NC}"
            if ! python3 "$SCAN_SCRIPT" scan-file "$file" > /dev/null 2>&1; then
                has_issues=1
                python3 "$SCAN_SCRIPT" scan-file "$file"
            fi
        fi
    done < "$temp_file"

    rm "$temp_file"

    if [ "$has_issues" -eq 1 ]; then
        echo ""
        echo -e "${RED}❌ 发现敏感信息，请修复后再提交！${NC}"
        return 1
    else
        echo ""
        echo -e "${GREEN}✅ git 暂存区安全，可以提交！${NC}"
        return 0
    fi
}

# 主程序
case "$1" in
    scan-file)
        if [ -z "$2" ]; then
            echo -e "${RED}❌ 请指定文件路径${NC}"
            print_help
            exit 1
        fi
        scan_file "$2"
        ;;
    scan-repo)
        if [ -z "$2" ]; then
            echo -e "${RED}❌ 请指定目录路径${NC}"
            print_help
            exit 1
        fi
        scan_repo "$2"
        ;;
    scan-text)
        if [ -z "$2" ]; then
            echo -e "${RED}❌ 请指定要扫描的文本${NC}"
            print_help
            exit 1
        fi
        scan_text "$2"
        ;;
    scan-blog)
        scan_blog
        ;;
    scan-staged)
        scan_staged
        ;;
    help|--help|-h)
        print_help
        ;;
    *)
        echo -e "${RED}❌ 未知命令: $1${NC}"
        print_help
        exit 1
        ;;
esac
