# FastMCP 使用指南

## 问题说明

用户遇到的问题是使用了错误的 FastMCP 启动方式。以下是正确和错误的对比：

### ❌ 错误的方式

```python
# 错误：在构造函数中传入端口参数
mcp = FastMCP("PDF MCP Server", port=config.mcp_port)

if len(sys.argv) > 1 and sys.argv[1] == "--sse":
    mcp.run(transport="sse")
else:
    mcp.run()
```

### ✅ 正确的方式

```python
# 正确：FastMCP 构造函数只需要服务器名称
mcp = FastMCP("NocoDB MCP Server")

if len(sys.argv) > 1 and sys.argv[1] == "--sse":
    # 正确：使用 run() 方法，传入 transport 和 port 参数
    mcp.run(transport="sse", port=MCP_PORT)
else:
    # 正确：使用 run() 方法，默认为 stdio 模式
    mcp.run()
```

## FastMCP API 说明

### 构造函数

```python
FastMCP(name: str)
```

- `name`: 服务器名称，用于标识 MCP 服务器
- **注意**: 构造函数不接受 `port` 参数

### 运行方法

#### 统一运行方法

```python
mcp.run(transport: str = "stdio", port: int = None, **kwargs)
```

- `transport`: 传输模式，可选值："stdio"（默认）、"sse"
- `port`: 服务器监听端口（仅在 SSE 模式下需要）
- **stdio 模式**: `mcp.run()` 或 `mcp.run(transport="stdio")`
- **SSE 模式**: `mcp.run(transport="sse", port=8000)`

## 完整示例

```python
#!/usr/bin/env python3
import os
import sys
from fastmcp import FastMCP
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 配置
MCP_PORT = int(os.getenv("MCP_PORT", "8000"))

# 创建 FastMCP 实例
mcp = FastMCP("My MCP Server")

@mcp.tool()
async def example_tool(message: str) -> str:
    """示例工具"""
    return f"Hello: {message}"

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--sse":
        # SSE 模式
        print(f"Starting server in SSE mode on port {MCP_PORT}", file=sys.stderr)
        mcp.run_sse(port=MCP_PORT)
    else:
        # stdio 模式（默认）
        print("Starting server in stdio mode", file=sys.stderr)
        mcp.run_stdio()
```

## 环境变量配置

在 `.env` 文件中配置：

```env
# MCP 服务器配置
MCP_PORT=8000

# 其他配置...
NOCODB_HOST=https://your-nocodb-host.com
NOCODB_TOKEN=your-api-token
```

## 启动方式

### stdio 模式

```bash
python server.py
```

### SSE 模式

```bash
python server.py --sse
```

## 调试技巧

1. **日志输出**: 使用 `file=sys.stderr` 确保日志不干扰 stdio 通信
2. **错误处理**: 在工具函数中添加 try-catch 块
3. **环境检查**: 启动前验证必要的环境变量

## 常见错误

1. **AttributeError: 'FastMCP' object has no attribute 'run'**
   - 原因: 使用了不存在的 `run()` 方法
   - 解决: 使用 `run_stdio()` 或 `run_sse()`

2. **TypeError: FastMCP() missing required argument**
   - 原因: 构造函数参数错误
   - 解决: 只传入服务器名称字符串

3. **端口占用错误**
   - 原因: SSE 模式下端口已被占用
   - 解决: 更改端口或停止占用端口的进程

## 最佳实践

1. 使用环境变量管理配置
2. 添加适当的错误处理
3. 在 stderr 输出日志信息
4. 提供清晰的工具文档字符串
5. 使用类型提示提高代码可读性