#!/usr/bin/env python3
"""
测试修复后的 update_table_records 函数对大小写 id 字段的支持
"""

import json
import asyncio
from typing import Dict, Any, Union

# 模拟修复后的 update_table_records 函数的核心验证逻辑
async def test_update_table_record_validation(
    table_id: str,
    records: Union[Dict[str, Any], str]
) -> Dict[str, Any]:
    """
    测试修复后的验证逻辑
    """
    try:
        # 处理records参数的保护逻辑
        processed_records = records
        
        # 如果records是字符串，尝试解析为JSON
        if isinstance(records, str):
            try:
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
        
        # 如果验证通过，返回成功
        return {
            "success": True,
            "message": "Validation passed",
            "processed_records": processed_records
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to validate records due to an unexpected error"
        }

async def test_id_case_scenarios():
    """
    测试不同的id字段大小写场景
    """
    print("测试修复后的 update_table_records id字段验证逻辑")
    print("=" * 60)
    
    # 测试用的参数
    test_table_id = "memv33ksx429pnq"
    
    # 测试案例1: 使用大写的 'Id' 字段（用户的实际数据）
    print("\n1. 测试大写 'Id' 字段（用户实际数据）:")
    user_data = {
        "Id": 2, 
        "CreatedAt": "2025-10-07 04:17:57+00:00", 
        "UpdatedAt": "2025-10-08 15:22:27+00:00", 
        "Title": "任务2: 沉睡用户分层模型设计",
        "project": None, 
        "status": "done"
    }
    user_json_str = json.dumps(user_data)
    print(f"输入: {user_json_str}")
    result = await test_update_table_record_validation(test_table_id, user_json_str)
    print(f"结果: {result}")
    
    # 测试案例2: 使用小写的 'id' 字段
    print("\n2. 测试小写 'id' 字段:")
    lowercase_data = {"id": 1, "name": "test"}
    lowercase_json_str = json.dumps(lowercase_data)
    print(f"输入: {lowercase_json_str}")
    result = await test_update_table_record_validation(test_table_id, lowercase_json_str)
    print(f"结果: {result}")
    
    # 测试案例3: 没有id字段
    print("\n3. 测试没有id字段:")
    no_id_data = {"name": "test", "value": 123}
    no_id_json_str = json.dumps(no_id_data)
    print(f"输入: {no_id_json_str}")
    result = await test_update_table_record_validation(test_table_id, no_id_json_str)
    print(f"结果: {result}")
    
    # 测试案例4: 同时有id和Id字段
    print("\n4. 测试同时有 'id' 和 'Id' 字段:")
    both_id_data = {"id": 1, "Id": 2, "name": "test"}
    both_id_json_str = json.dumps(both_id_data)
    print(f"输入: {both_id_json_str}")
    result = await test_update_table_record_validation(test_table_id, both_id_json_str)
    print(f"结果: {result}")
    
    # 测试案例5: 批量更新（数组）
    print("\n5. 测试批量更新（包含大写Id）:")
    batch_data = [
        {"Id": 1, "name": "test1"},
        {"id": 2, "name": "test2"}
    ]
    batch_json_str = json.dumps(batch_data)
    print(f"输入: {batch_json_str}")
    result = await test_update_table_record_validation(test_table_id, batch_json_str)
    print(f"结果: {result}")

if __name__ == "__main__":
    asyncio.run(test_id_case_scenarios())