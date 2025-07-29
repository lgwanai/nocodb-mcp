#!/bin/bash

# NocoDB MCP Server 管理脚本
# 支持启动、停止、重启和状态检查

set -e

# 配置
PID_FILE=".nocodb-mcp.pid"
LOG_FILE="nocodb-mcp.log"
SERVER_SCRIPT="server.py"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 打印带颜色的消息
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查 Python 环境
check_python() {
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 is not installed or not in PATH"
        exit 1
    fi
    
    python_version=$(python3 --version 2>&1 | cut -d' ' -f2 | cut -d'.' -f1,2)
    print_info "Found Python $python_version"
}

# 检查依赖
check_dependencies() {
    if [ ! -f "requirements.txt" ]; then
        print_error "requirements.txt not found"
        exit 1
    fi
    
    print_info "Checking dependencies..."
    
    # 检查是否需要安装依赖
    if ! python3 -c "import fastmcp, httpx, dotenv" &> /dev/null; then
        print_warning "Some dependencies are missing. Installing..."
        pip3 install -r requirements.txt
        print_success "Dependencies installed"
    else
        print_success "All dependencies are available"
    fi
}

# 检查配置文件
check_config() {
    if [ ! -f ".env" ]; then
        print_error ".env file not found. Please create it with your NocoDB configuration."
        print_info "Example .env content:"
        echo "NOCODB_HOST=https://your-nocodb-host.com"
        echo "NOCODB_TOKEN=your-api-token-here"
        echo "MCP_PORT=8000"
        exit 1
    fi
    
    # 检查必要的环境变量
    source .env
    
    if [ -z "$NOCODB_HOST" ] || [ -z "$NOCODB_TOKEN" ]; then
        print_error "NOCODB_HOST and NOCODB_TOKEN must be set in .env file"
        exit 1
    fi
    
    print_success "Configuration file validated"
}

# 检查服务状态
check_status() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p "$PID" > /dev/null 2>&1; then
            return 0  # 服务正在运行
        else
            rm -f "$PID_FILE"  # 清理无效的PID文件
            return 1  # 服务未运行
        fi
    else
        return 1  # 服务未运行
    fi
}

# 启动服务
start_service() {
    local mode="$1"
    
    if [ "$mode" = "stdio" ]; then
        # stdio模式直接前台运行，不支持后台
        print_info "Starting NocoDB MCP Server in stdio mode (foreground)..."
        print_warning "stdio mode runs in foreground. Use Ctrl+C to stop."
        print_info "For background operation, use SSE mode: ./start.sh start --sse"
        exec python3 "$SERVER_SCRIPT"
    fi
    
    # SSE模式支持后台运行
    if check_status; then
        PID=$(cat "$PID_FILE")
        print_warning "Service is already running (PID: $PID)"
        return 1
    fi
    
    print_info "Starting NocoDB MCP Server in $mode mode..."
    
    source .env
    print_info "Server will be available at http://localhost:${MCP_PORT:-8000}"
    nohup python3 "$SERVER_SCRIPT" --sse > "$LOG_FILE" 2>&1 &
    
    PID=$!
    echo $PID > "$PID_FILE"
    
    # 等待一下确保服务启动
    sleep 2
    
    if check_status; then
        print_success "Service started successfully (PID: $PID)"
        print_info "Log file: $LOG_FILE"
    else
        print_error "Failed to start service"
        if [ -f "$LOG_FILE" ]; then
            print_info "Last few lines from log:"
            tail -n 10 "$LOG_FILE"
        fi
        return 1
    fi
}

# 停止服务
stop_service() {
    if ! check_status; then
        print_warning "Service is not running"
        return 1
    fi
    
    PID=$(cat "$PID_FILE")
    print_info "Stopping NocoDB MCP Server (PID: $PID)..."
    
    # 尝试优雅停止
    kill "$PID" 2>/dev/null || true
    
    # 等待进程结束
    local count=0
    while [ $count -lt 10 ] && ps -p "$PID" > /dev/null 2>&1; do
        sleep 1
        count=$((count + 1))
    done
    
    # 如果还在运行，强制杀死
    if ps -p "$PID" > /dev/null 2>&1; then
        print_warning "Force killing process..."
        kill -9 "$PID" 2>/dev/null || true
        sleep 1
    fi
    
    rm -f "$PID_FILE"
    print_success "Service stopped successfully"
}

# 重启服务
restart_service() {
    local mode="$1"
    
    if [ "$mode" = "stdio" ]; then
        print_error "Restart is not supported for stdio mode"
        print_info "stdio mode runs in foreground and cannot be managed as a background service"
        print_info "Use SSE mode for background operation: ./start.sh restart --sse"
        return 1
    fi
    
    print_info "Restarting NocoDB MCP Server..."
    
    if check_status; then
        stop_service
    fi
    
    sleep 1
    start_service "$mode"
}

# 显示服务状态
show_status() {
    if check_status; then
        PID=$(cat "$PID_FILE")
        print_success "Service is running (PID: $PID)"
        
        # 显示进程信息
        if command -v ps &> /dev/null; then
            print_info "Process details:"
            ps -p "$PID" -o pid,ppid,cmd,etime 2>/dev/null || true
        fi
        
        # 显示日志文件大小
        if [ -f "$LOG_FILE" ]; then
            LOG_SIZE=$(wc -c < "$LOG_FILE" 2>/dev/null || echo "0")
            print_info "Log file size: $LOG_SIZE bytes"
        fi
    else
        print_warning "Service is not running"
    fi
}

# 显示日志
show_logs() {
    local lines="${1:-50}"
    
    if [ ! -f "$LOG_FILE" ]; then
        print_warning "Log file not found: $LOG_FILE"
        return 1
    fi
    
    print_info "Showing last $lines lines from $LOG_FILE:"
    echo "----------------------------------------"
    tail -n "$lines" "$LOG_FILE"
    echo "----------------------------------------"
}

# 显示帮助信息
show_help() {
    echo "NocoDB MCP Server 管理脚本"
    echo ""
    echo "用法: $0 <命令> [选项]"
    echo ""
    echo "命令:"
    echo "  start       启动服务"
    echo "  stop        停止服务 (仅SSE模式)"
    echo "  restart     重启服务 (仅SSE模式)"
    echo "  status      显示服务状态"
    echo "  logs        显示服务日志"
    echo "  check       检查环境和配置"
    echo "  example     运行使用示例"
    echo ""
    echo "选项:"
    echo "  --stdio     以 stdio 模式运行 (前台运行，默认)"
    echo "  --sse       以 SSE 模式运行 (后台运行)"
    echo "  --lines N   显示日志的行数 (默认: 50)"
    echo "  --help      显示此帮助信息"
    echo ""
    echo "模式说明:"
    echo "  stdio模式:  前台运行，适合开发调试，使用Ctrl+C停止"
    echo "  SSE模式:    后台运行，适合生产环境，支持start/stop/restart管理"
    echo ""
    echo "示例:"
    echo "  $0 start           # 以 stdio 模式启动 (前台)"
    echo "  $0 start --sse     # 以 SSE 模式启动 (后台)"
    echo "  $0 stop            # 停止后台服务"
    echo "  $0 restart --sse   # 重启后台服务"
    echo "  $0 status          # 查看服务状态"
    echo "  $0 logs --lines 100 # 显示最后100行日志"
    echo "  $0 check           # 检查环境配置"
}

# 主函数
main() {
    # 如果没有参数，显示帮助
    if [ $# -eq 0 ]; then
        show_help
        exit 1
    fi
    
    # 检查是否是帮助请求
    if [ "$1" = "--help" ] || [ "$1" = "-h" ] || [ "$1" = "help" ]; then
        show_help
        exit 0
    fi
    
    # 解析命令
    COMMAND="$1"
    shift
    
    # 解析选项
    MODE="stdio"
    LOG_LINES=50
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            --stdio)
                MODE="stdio"
                shift
                ;;
            --sse)
                MODE="sse"
                shift
                ;;
            --lines)
                if [ -n "$2" ] && [ "$2" -eq "$2" ] 2>/dev/null; then
                    LOG_LINES="$2"
                    shift 2
                else
                    print_error "--lines requires a numeric argument"
                    exit 1
                fi
                ;;
            --help)
                show_help
                exit 0
                ;;
            *)
                print_error "Unknown option: $1"
                show_help
                exit 1
                ;;
        esac
    done
    
    # 执行命令
    case "$COMMAND" in
        start)
            print_info "NocoDB MCP Server 管理脚本"
            print_info "=============================="
            check_python
            check_dependencies
            check_config
            start_service "$MODE"
            ;;
        stop)
            stop_service
            ;;
        restart)
            print_info "NocoDB MCP Server 管理脚本"
            print_info "=============================="
            check_python
            check_dependencies
            check_config
            restart_service "$MODE"
            ;;
        status)
            show_status
            ;;
        logs)
            show_logs "$LOG_LINES"
            ;;
        check)
            print_info "NocoDB MCP Server 环境检查"
            print_info "=============================="
            check_python
            check_dependencies
            check_config
            print_success "All checks passed!"
            ;;
        example)
            print_info "Running usage example..."
            if [ ! -f "example.py" ]; then
                print_error "example.py not found"
                exit 1
            fi
            python3 example.py
            ;;
        *)
            print_error "Unknown command: $COMMAND"
            show_help
            exit 1
            ;;
    esac
}

# 捕获中断信号
trap 'print_info "\nShutting down server..."; exit 0' INT TERM

# 运行主函数
main "$@"