#!/usr/bin/env python3
"""
NocoDB API 测试脚本
测试 NocoDB API 的基本功能，包括创建记录、获取记录等操作
"""

import httpx
import json
import asyncio
import os
from typing import Dict, List, Any
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 从环境变量读取配置信息
NOCODB_HOST = os.getenv("NOCODB_HOST", "https://app.nocodb.com")
NOCODB_TOKEN = os.getenv("NOCODB_TOKEN")
TABLE_ID = "m1bb5qra85k6fw2"

# 检查必要的配置
if not NOCODB_TOKEN:
    raise ValueError("NOCODB_TOKEN 未在 .env 文件中配置")

# 测试数据
TEST_DATA = [
    {"Title": "123"},
    {"Title": "456"}
]

class NocoDBAPITester:
    def __init__(self, host: str, token: str):
        self.host = host.rstrip('/')
        self.token = token
        self.headers = {
            "xc-token": token,
            "Content-Type": "application/json"
        }
    
    async def create_records(self, table_id: str, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        创建表记录
        """
        url = f"{self.host}/api/v2/tables/{table_id}/records"
        
        # 对于localhost，禁用SSL验证
        verify_ssl = not ("localhost" in self.host or "127.0.0.1" in self.host)
        
        async with httpx.AsyncClient(verify=verify_ssl) as client:
            try:
                response = await client.post(
                    url,
                    headers=self.headers,
                    json=data,
                    timeout=30.0
                )
                
                print(f"创建记录请求: POST {url}")
                print(f"请求头: {json.dumps(self.headers, indent=2, ensure_ascii=False)}")
                print(f"请求数据: {json.dumps(data, indent=2, ensure_ascii=False)}")
                print(f"响应状态码: {response.status_code}")
                
                if response.status_code == 200:
                    result = response.json()
                    print(f"创建成功! 响应数据: {json.dumps(result, indent=2, ensure_ascii=False)}")
                    return result
                else:
                    print(f"创建失败! 错误信息: {response.text}")
                    return {"error": response.text, "status_code": response.status_code}
                    
            except Exception as e:
                print(f"请求异常: {str(e)}")
                return {"error": str(e)}
    
    async def get_records(self, table_id: str, limit: int = 10) -> Dict[str, Any]:
        """
        获取表记录
        """
        url = f"{self.host}/api/v2/tables/{table_id}/records"
        params = {"limit": limit}
        
        # 对于localhost，禁用SSL验证
        verify_ssl = not ("localhost" in self.host or "127.0.0.1" in self.host)
        
        async with httpx.AsyncClient(verify=verify_ssl) as client:
            try:
                response = await client.get(
                    url,
                    headers=self.headers,
                    params=params,
                    timeout=30.0
                )
                
                print(f"\n获取记录请求: GET {url}")
                print(f"请求参数: {params}")
                print(f"响应状态码: {response.status_code}")
                
                if response.status_code == 200:
                    result = response.json()
                    print(f"获取成功! 记录数量: {len(result.get('list', []))}")
                    print(f"响应数据: {json.dumps(result, indent=2, ensure_ascii=False)}")
                    return result
                else:
                    print(f"获取失败! 错误信息: {response.text}")
                    return {"error": response.text, "status_code": response.status_code}
                    
            except Exception as e:
                print(f"请求异常: {str(e)}")
                return {"error": str(e)}
    
    async def test_connection(self) -> bool:
        """
        测试连接和认证
        """
        url = f"{self.host}/api/v2/tables/{TABLE_ID}/records"
        
        # 对于localhost，禁用SSL验证
        verify_ssl = not ("localhost" in self.host or "127.0.0.1" in self.host)
        
        async with httpx.AsyncClient(verify=verify_ssl) as client:
            try:
                response = await client.get(
                    url,
                    headers=self.headers,
                    params={"limit": 1},
                    timeout=10.0
                )
                
                print(f"连接测试: GET {url}")
                print(f"SSL验证: {verify_ssl}")
                print(f"响应状态码: {response.status_code}")
                
                if response.status_code == 200:
                    print("✅ 连接和认证成功!")
                    return True
                else:
                    print(f"❌ 连接失败: {response.text}")
                    return False
                    
            except Exception as e:
                print(f"❌ 连接异常: {str(e)}")
                return False

async def main():
    """
    主测试函数
    """
    print("=" * 60)
    print("NocoDB API 测试开始")
    print("=" * 60)
    
    # 初始化测试器
    tester = NocoDBAPITester(NOCODB_HOST, NOCODB_TOKEN)
    
    print(f"NocoDB 主机: {NOCODB_HOST}")
    print(f"Table ID: {TABLE_ID}")
    print(f"Token: {NOCODB_TOKEN[:10]}...{NOCODB_TOKEN[-10:]}")
    print()
    
    # 1. 测试连接
    print("1. 测试连接和认证...")
    if not await tester.test_connection():
        print("连接失败，请检查配置信息")
        return
    
    print()
    
    # 2. 创建记录
    print("2. 创建测试记录...")
    create_result = await tester.create_records(TABLE_ID, TEST_DATA)
    
    print()
    
    # 3. 获取记录
    print("3. 获取表记录...")
    get_result = await tester.get_records(TABLE_ID, limit=20)
    
    print()
    print("=" * 60)
    print("测试完成")
    print("=" * 60)

if __name__ == "__main__":
    # 运行测试
    asyncio.run(main())