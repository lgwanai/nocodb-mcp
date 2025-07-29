# NocoDB MCP Server

一个基于 FastMCP 的 Model Context Protocol (MCP) 服务器，提供对 NocoDB API 的访问功能。支持 stdio 和 SSE 两种传输方式。

## 功能特性

- 🚀 支持 stdio 和 SSE 两种启动方式
- 📊 完整的 NocoDB 表记录 CRUD 操作
- 🔧 基于 FastMCP 框架构建
- 🌐 异步 HTTP 客户端支持
- ⚙️ 环境变量配置管理
- 📝 详细的错误处理和响应

## 安装依赖

```bash
pip install -r requirements.txt
```

## 配置

1. 复制 `.env` 文件并配置你的 NocoDB 信息：

```bash
cp .env .env.local
```

2. 编辑 `.env` 文件：

```env
# NocoDB Configuration
NOCODB_HOST=https://your-nocodb-host.com
NOCODB_TOKEN=your-api-token-here

# MCP Server Configuration
MCP_PORT=8000
```

### 获取 NocoDB API Token

1. 登录你的 NocoDB 实例
2. 进入 `Account Settings` > `Tokens`
3. 创建新的 API Token
4. 复制 token 到 `.env` 文件中

## 启动方式

### Stdio 模式（默认）

```bash
python server.py
```

### SSE 模式

```bash
python server.py --sse
```

SSE 模式将在指定端口启动 HTTP 服务器（默认 8000）。

## 可用工具

### 1. create_table_records

在指定表中创建新记录。

**参数：**
- `table_id` (string): 表 ID
- `records` (object|array): 单个记录对象或记录对象数组

**示例：**
```python
# 创建单个记录
result = await create_table_records(
    table_id="tbl_abc123",
    records={
        "SingleLineText": "John Doe",
        "Email": "john@example.com",
        "Number": 42
    }
)

# 创建多个记录
result = await create_table_records(
    table_id="tbl_abc123",
    records=[
        {"SingleLineText": "Alice", "Email": "alice@example.com"},
        {"SingleLineText": "Bob", "Email": "bob@example.com"}
    ]
)
```

### 2. get_table_records

从指定表中检索记录。

**参数：**
- `table_id` (string): 表 ID
- `limit` (int, 可选): 最大记录数，默认 25
- `offset` (int, 可选): 跳过的记录数，默认 0

**示例：**
```python
result = await get_table_records(
    table_id="tbl_abc123",
    limit=50,
    offset=0
)
```

### 3. update_table_record

更新指定记录。

**参数：**
- `table_id` (string): 表 ID
- `record_id` (string): 记录 ID
- `data` (object): 要更新的字段数据

**示例：**
```python
result = await update_table_record(
    table_id="tbl_abc123",
    record_id="rec_xyz789",
    data={
        "SingleLineText": "Updated Name",
        "Email": "updated@example.com"
    }
)
```

### 4. delete_table_record

删除指定记录。

**参数：**
- `table_id` (string): 表 ID
- `record_id` (string): 记录 ID

**示例：**
```python
result = await delete_table_record(
    table_id="tbl_abc123",
    record_id="rec_xyz789"
)
```

### 5. get_server_info

获取服务器配置信息。

**示例：**
```python
result = await get_server_info()
```

## 支持的字段类型

### 可编辑字段类型
- **文本类型**: SingleLineText, LongText, Email, PhoneNumber, URL
- **数值类型**: Number, Decimal, Currency, Percent, Duration, Rating
- **布尔类型**: Checkbox
- **日期时间**: Date, DateTime, Time, Year
- **选择类型**: SingleSelect, MultiSelect
- **复杂类型**: JSON, Geometry, Attachment

### 只读字段类型（请求中会被忽略）
- Look Up, Roll Up, Formula, Auto Number
- Created By, Updated By, Created At, Updated At
- Barcode, QR Code

## 响应格式

所有工具都返回统一的响应格式：

```json
{
  "success": true|false,
  "data": {...},           // 成功时的数据
  "message": "...",        // 操作消息
  "error": {...},          // 错误时的错误信息
  "status_code": 200|400   // HTTP 状态码
}
```

## 示例用法

查看 `example.py` 文件了解详细的使用示例：

```bash
python example.py
```

## 错误处理

服务器包含完整的错误处理机制：

- **网络错误**: 连接超时、网络不可达等
- **认证错误**: 无效的 API Token
- **请求错误**: 无效的表 ID、记录 ID 或数据格式
- **服务器错误**: NocoDB 服务器内部错误

## 开发

### 项目结构

```
nocodb-mcp/
├── server.py          # 主服务器文件
├── example.py         # 使用示例
├── requirements.txt   # Python 依赖
├── .env              # 环境变量配置
├── nocodb.md         # NocoDB API 文档
└── README.md         # 项目说明
```

### 扩展功能

要添加新的 NocoDB API 功能：

1. 在 `NocoDBClient` 类中添加新方法
2. 使用 `@mcp.tool()` 装饰器创建对应的 MCP 工具
3. 添加适当的错误处理和文档

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！