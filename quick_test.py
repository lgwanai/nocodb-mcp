#!/usr/bin/env python3
"""
快速NocoDB API测试脚本
用于快速验证API连接和基本功能
"""

import httpx
import json
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 配置
HOST = os.getenv("NOCODB_HOST", "http://localhost:8080")
TOKEN = os.getenv("NOCODB_TOKEN")
TABLE_ID = "m1bb5qra85k6fw2"

if not TOKEN:
    print("❌ 错误: NOCODB_TOKEN 未配置")
    exit(1)

headers = {
    "xc-token": TOKEN,
    "Content-Type": "application/json"
}

# 禁用SSL验证（用于localhost）
verify_ssl = not ("localhost" in HOST or "127.0.0.1" in HOST)

def test_api():
    print(f"🔗 测试连接: {HOST}")
    print(f"📋 Table ID: {TABLE_ID}")
    print(f"🔑 Token: {TOKEN[:10]}...{TOKEN[-10:]}")
    print(f"🔒 SSL验证: {verify_ssl}")
    print("-" * 50)
    
    with httpx.Client(verify=verify_ssl) as client:
        # 1. 测试连接
        try:
            url = f"{HOST}/api/v2/tables/{TABLE_ID}/records"
            response = client.get(url, headers=headers, params={"limit": 1})
            
            if response.status_code == 200:
                print("✅ 连接成功")
            else:
                print(f"❌ 连接失败: {response.status_code} - {response.text}")
                return
                
        except Exception as e:
            print(f"❌ 连接异常: {e}")
            return
        
        # 2. 创建记录测试
        try:
            test_data = [{"Title": "快速测试记录"}]
            response = client.post(url, headers=headers, json=test_data)
            
            if response.status_code == 200:
                result = response.json()
                record_id = result[0].get("Id")
                print(f"✅ 创建记录成功: ID={record_id}")
            else:
                print(f"❌ 创建记录失败: {response.status_code} - {response.text}")
                
        except Exception as e:
            print(f"❌ 创建记录异常: {e}")
        
        # 3. 获取记录测试
        try:
            response = client.get(url, headers=headers, params={"limit": 5})
            
            if response.status_code == 200:
                result = response.json()
                count = len(result.get("list", []))
                print(f"✅ 获取记录成功: 共{count}条记录")
                
                # 显示最新的几条记录
                for record in result.get("list", [])[:3]:
                    print(f"   - ID: {record.get('Id')}, Title: {record.get('Title')}")
            else:
                print(f"❌ 获取记录失败: {response.status_code} - {response.text}")
                
        except Exception as e:
            print(f"❌ 获取记录异常: {e}")
    
    print("-" * 50)
    print("🎉 测试完成")

if __name__ == "__main__":
    test_api()