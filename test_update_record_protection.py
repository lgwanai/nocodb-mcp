#!/usr/bin/env python3
"""
测试 update_table_record 函数的 data 参数保护逻辑
"""

import json
import asyncio
from typing import Dict, Any, Union

# 模拟 update_table_record 函数的核心逻辑
async def test_update_table_record(
    table_id: str,
    record_id: str,
    data: Union[Dict[str, Any], str]
) -> Dict[str, Any]:
    """
    测试版本的 update_table_record 函数
    """
    try:
        # 处理data参数的保护逻辑
        processed_data = data
        
        # 如果data是字符串，尝试解析为JSON
        if isinstance(data, str):
            try:
                processed_data = json.loads(data)
            except json.JSONDecodeError as json_error:
                return {
                    "success": False,
                    "error": f"Invalid JSON string: {str(json_error)}",
                    "message": "Failed to parse data JSON string"
                }
        
        # 验证解析后的数据类型
        if not isinstance(processed_data, dict):
            return {
                "success": False,
                "error": "Data must be a dictionary or valid JSON string",
                "message": "Invalid data type"
            }
        
        # 模拟成功更新（实际中会调用 nocodb_client.update_record）
        return {
            "success": True,
            "data": processed_data,
            "message": f"Successfully updated record {record_id} in table {table_id}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to update record due to an unexpected error"
        }

async def test_data_protection():
    """
    测试不同类型的 data 参数
    """
    print("测试 update_table_record 的 data 参数保护逻辑")
    print("=" * 50)
    
    # 测试用的参数
    test_table_id = "test_table_123"
    test_record_id = "record_456"
    
    # 测试案例1: 正常的字典
    print("\n1. 测试正常的字典参数:")
    dict_data = {"Title": "Updated Record", "Number": 99}
    print(f"输入: {dict_data}")
    result = await test_update_table_record(test_table_id, test_record_id, dict_data)
    print(f"结果: {result}")
    
    # 测试案例2: 有效的JSON字符串
    print("\n2. 测试有效的JSON字符串:")
    json_data_str = json.dumps({"Title": "JSON Updated", "Status": "Active"})
    print(f"输入: {json_data_str}")
    result = await test_update_table_record(test_table_id, test_record_id, json_data_str)
    print(f"结果: {result}")
    
    # 测试案例3: 无效的JSON字符串
    print("\n3. 测试无效的JSON字符串:")
    invalid_json_str = '{"Title": "Invalid JSON", "Number": }'
    print(f"输入: {invalid_json_str}")
    result = await test_update_table_record(test_table_id, test_record_id, invalid_json_str)
    print(f"结果: {result}")
    
    # 测试案例4: 非字典的JSON字符串（列表）
    print("\n4. 测试非字典的JSON字符串（列表）:")
    list_json_str = json.dumps([{"Title": "Item 1"}, {"Title": "Item 2"}])
    print(f"输入: {list_json_str}")
    result = await test_update_table_record(test_table_id, test_record_id, list_json_str)
    print(f"结果: {result}")
    
    # 测试案例5: 非字典的JSON字符串（字符串）
    print("\n5. 测试非字典的JSON字符串（字符串）:")
    string_json = json.dumps("just a string")
    print(f"输入: {string_json}")
    result = await test_update_table_record(test_table_id, test_record_id, string_json)
    print(f"结果: {result}")
    
    # 测试案例6: 数字类型
    print("\n6. 测试数字类型:")
    number_input = 123
    print(f"输入: {number_input}")
    result = await test_update_table_record(test_table_id, test_record_id, number_input)
    print(f"结果: {result}")
    
    # 测试案例7: 空字典
    print("\n7. 测试空字典:")
    empty_dict = {}
    print(f"输入: {empty_dict}")
    result = await test_update_table_record(test_table_id, test_record_id, empty_dict)
    print(f"结果: {result}")
    
    # 测试案例8: 空JSON字符串
    print("\n8. 测试空JSON字符串:")
    empty_json_str = json.dumps({})
    print(f"输入: {empty_json_str}")
    result = await test_update_table_record(test_table_id, test_record_id, empty_json_str)
    print(f"结果: {result}")
    
    print("\n测试完成！")

if __name__ == "__main__":
    asyncio.run(test_data_protection())