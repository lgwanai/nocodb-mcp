#!/usr/bin/env python3
"""
NocoDB MCP Server

A Model Context Protocol server that provides access to NocoDB API functionality.
Supports both stdio and SSE transport methods.
"""

import os
import json
import asyncio
import copy
from typing import Any, Dict, List, Optional, Union
from dotenv import load_dotenv
import httpx
from fastmcp import FastMCP

# Load environment variables
load_dotenv()

# Configuration
NOCODB_HOST = os.getenv("NOCODB_HOST", "")
NOCODB_TOKEN = os.getenv("NOCODB_TOKEN", "")
MCP_PORT = int(os.getenv("MCP_PORT", "8000"))

if not NOCODB_HOST or not NOCODB_TOKEN:
    raise ValueError("NOCODB_HOST and NOCODB_TOKEN must be set in environment variables")

# 只读字段列表 - 这些字段在更新时需要被过滤掉
READONLY_FIELDS = {
    'CreatedAt', 'UpdatedAt', 'Created By', 'Updated By',
    'createdAt', 'updatedAt', 'created_by', 'updated_by',
    'nc_created_at', 'nc_updated_at', 'nc_created_by', 'nc_updated_by'
}

def filter_readonly_fields(records: Union[Dict[str, Any], List[Dict[str, Any]]]) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
    """
    过滤掉只读字段，防止更新时出错
    
    Args:
        records: 单个记录字典或记录列表
        
    Returns:
        过滤后的记录
    """
    def filter_single_record(record: Dict[str, Any]) -> Dict[str, Any]:
        # 深拷贝记录以避免修改原始数据
        filtered_record = copy.deepcopy(record)
        
        # 删除只读字段
        for field in READONLY_FIELDS:
            if field in filtered_record:
                del filtered_record[field]
                
        return filtered_record
    
    if isinstance(records, list):
        return [filter_single_record(record) for record in records]
    else:
        return filter_single_record(records)

# Initialize FastMCP
mcp = FastMCP("NocoDB MCP Server")

class NocoDBClient:
    """NocoDB API client wrapper"""
    
    def __init__(self, host: str, token: str):
        self.host = host.rstrip('/')
        self.token = token
        self.headers = {
            "xc-token": token,
            "Content-Type": "application/json"
        }
    
    async def create_records(self, table_id: str, records: Union[Dict, List[Dict]]) -> Dict[str, Any]:
        """Create new records in a table"""
        url = f"{self.host}/api/v2/tables/{table_id}/records"
        
        # Ensure records is a list
        if isinstance(records, dict):
            records = [records]
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                headers=self.headers,
                json=records,
                timeout=30.0
            )
            
            if response.status_code == 200:
                return {
                    "success": True,
                    "data": response.json(),
                    "message": f"Successfully created {len(records)} record(s)"
                }
            else:
                error_data = response.json() if response.headers.get("content-type", "").startswith("application/json") else {"msg": response.text}
                return {
                    "success": False,
                    "error": error_data,
                    "status_code": response.status_code
                }
    
    async def get_records(self, table_id: str, limit: int = 25, offset: int = 0) -> Dict[str, Any]:
        """Get records from a table"""
        url = f"{self.host}/api/v2/tables/{table_id}/records"
        params = {
            "limit": limit,
            "offset": offset
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                url,
                headers=self.headers,
                params=params,
                timeout=30.0
            )
            
            if response.status_code == 200:
                return {
                    "success": True,
                    "data": response.json(),
                    "message": f"Successfully retrieved records from table {table_id}"
                }
            else:
                error_data = response.json() if response.headers.get("content-type", "").startswith("application/json") else {"msg": response.text}
                return {
                    "success": False,
                    "error": error_data,
                    "status_code": response.status_code
                }
    
    async def update_records(self, table_id: str, records: Union[Dict, List[Dict]]) -> Dict[str, Any]:
        """Update records in a table (batch update)"""
        url = f"{self.host}/api/v2/tables/{table_id}/records"
        
        # Ensure records is a list
        if isinstance(records, dict):
            records = [records]
        
        async with httpx.AsyncClient() as client:
            response = await client.patch(
                url,
                headers=self.headers,
                json=records,
                timeout=30.0
            )
            
            if response.status_code == 200:
                return {
                    "success": True,
                    "data": response.json(),
                    "message": f"Successfully updated {len(records)} record(s)"
                }
            else:
                error_data = response.json() if response.headers.get("content-type", "").startswith("application/json") else {"msg": response.text}
                return {
                    "success": False,
                    "error": error_data,
                    "status_code": response.status_code
                }
    
    async def delete_record(self, table_id: str, record_id: str) -> Dict[str, Any]:
        """Delete a specific record"""
        url = f"{self.host}/api/v2/tables/{table_id}/records/{record_id}"
        
        async with httpx.AsyncClient() as client:
            response = await client.delete(
                url,
                headers=self.headers,
                timeout=30.0
            )
            
            if response.status_code == 200:
                return {
                    "success": True,
                    "message": f"Successfully deleted record {record_id}"
                }
            else:
                error_data = response.json() if response.headers.get("content-type", "").startswith("application/json") else {"msg": response.text}
                return {
                    "success": False,
                    "error": error_data,
                    "status_code": response.status_code
                }

# Initialize NocoDB client
nocodb_client = NocoDBClient(NOCODB_HOST, NOCODB_TOKEN)

@mcp.tool()
async def create_table_records(
    table_id: str,
    records: Union[Dict[str, Any], List[Dict[str, Any]], str]
) -> Dict[str, Any]:
    """
    Create new records in a NocoDB table.
    
    Args:
        table_id: The ID of the table to create records in
        records: A single record object, array of record objects, or JSON string to create
    
    Returns:
        Dictionary containing success status, created record IDs, and any error messages
    """
    try:
        # 处理records参数的保护逻辑
        processed_records = records
        
        # 如果records是字符串，尝试解析为JSON
        if isinstance(records, str):
            try:
                import json
                processed_records = json.loads(records)
            except json.JSONDecodeError as json_error:
                return {
                    "success": False,
                    "error": f"Invalid JSON string: {str(json_error)}",
                    "message": "Failed to parse records JSON string"
                }
        
        # 验证解析后的数据类型
        if not isinstance(processed_records, (dict, list)):
            return {
                "success": False,
                "error": "Records must be a dictionary, list, or valid JSON string",
                "message": "Invalid records data type"
            }
        
        result = await nocodb_client.create_records(table_id, processed_records)
        return result
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to create records due to an unexpected error"
        }

@mcp.tool()
async def get_table_records(
    table_id: str,
    limit: int = 25,
    offset: int = 0
) -> Dict[str, Any]:
    """
    Retrieve records from a NocoDB table.
    
    Args:
        table_id: The ID of the table to retrieve records from
        limit: Maximum number of records to retrieve (default: 25)
        offset: Number of records to skip (default: 0)
    
    Returns:
        Dictionary containing success status, retrieved records, and any error messages
    """
    try:
        result = await nocodb_client.get_records(table_id, limit, offset)
        return result
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to retrieve records due to an unexpected error"
        }

@mcp.tool()
async def update_table_records(
    table_id: str,
    records: Union[Dict[str, Any], List[Dict[str, Any]], str]
) -> Dict[str, Any]:
    """
    Update records in a NocoDB table (batch update).
    
    Args:
        table_id: The ID of the table containing the records
        records: A single record object (must include id), array of record objects, or JSON string
    
    Returns:
        Dictionary containing success status, updated record data, and any error messages
    """
    try:
        # 处理records参数的保护逻辑
        processed_records = records
        
        # 如果records是字符串，尝试解析为JSON
        if isinstance(records, str):
            try:
                import json
                processed_records = json.loads(records)
            except json.JSONDecodeError as json_error:
                return {
                    "success": False,
                    "error": f"Invalid JSON string: {str(json_error)}",
                    "message": "Failed to parse records JSON string"
                }
        
        # 验证解析后的数据类型
        if not isinstance(processed_records, (dict, list)):
            return {
                "success": False,
                "error": "Records must be a dictionary, list, or valid JSON string",
                "message": "Invalid records data type"
            }
        
        # 验证记录必须包含id字段（支持'id'或'Id'）
        records_to_check = processed_records if isinstance(processed_records, list) else [processed_records]
        for record in records_to_check:
            if not isinstance(record, dict) or ('id' not in record and 'Id' not in record):
                return {
                    "success": False,
                    "error": "Each record must be a dictionary containing an 'id' or 'Id' field",
                    "message": "Invalid record format - missing id/Id field"
                }
        
        # 过滤只读字段，防止更新失败
        filtered_records = filter_readonly_fields(processed_records)
        
        result = await nocodb_client.update_records(table_id, filtered_records)
        return result
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to update records due to an unexpected error"
        }

@mcp.tool()
async def delete_table_record(
    table_id: str,
    record_id: str
) -> Dict[str, Any]:
    """
    Delete a specific record from a NocoDB table.
    
    Args:
        table_id: The ID of the table containing the record
        record_id: The ID of the record to delete
    
    Returns:
        Dictionary containing success status and any error messages
    """
    try:
        result = await nocodb_client.delete_record(table_id, record_id)
        return result
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to delete record due to an unexpected error"
        }

@mcp.tool()
async def get_server_info() -> Dict[str, Any]:
    """
    Get information about the NocoDB MCP server configuration.
    
    Returns:
        Dictionary containing server configuration information
    """
    return {
        "server_name": "NocoDB MCP Server",
        "nocodb_host": NOCODB_HOST,
        "mcp_port": MCP_PORT,
        "available_tools": [
            "create_table_records",
            "get_table_records", 
            "update_table_records",
            "delete_table_record",
            "get_server_info"
        ]
    }

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--sse":
        # SSE mode
        print(f"Starting NocoDB MCP Server in SSE mode on port {MCP_PORT}", file=sys.stderr)
        mcp.run(transport="sse", port=MCP_PORT)
    else:
        # stdio mode (default)
        print("Starting NocoDB MCP Server in stdio mode", file=sys.stderr)
        mcp.run()