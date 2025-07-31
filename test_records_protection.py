#!/usr/bin/env python3
"""
测试 create_table_records 函数的 records 参数保护逻辑
"""

import json
import asyncio
from server import create_table_records

async def test_records_protection():
    """
    测试不同类型的 records 参数
    """
    print("测试 create_table_records 的 records 参数保护逻辑")
    print("=" * 50)
    
    # 测试用的 table_id（这里只是测试参数处理，不会真正调用API）
    test_table_id = "test_table_123"
    
    # 测试案例1: 正常的字典
    print("\n1. 测试正常的字典参数:")
    dict_records = {"Title": "Test Record", "Number": 42}
    print(f"输入: {dict_records}")
    try:
        result = await create_table_records(test_table_id, dict_records)
        print(f"结果: {result.get('message', 'Unknown')}")
    except Exception as e:
        print(f"异常: {e}")
    
    # 测试案例2: 正常的列表
    print("\n2. 测试正常的列表参数:")
    list_records = [{"Title": "Record 1"}, {"Title": "Record 2"}]
    print(f"输入: {list_records}")
    try:
        result = await create_table_records(test_table_id, list_records)
        print(f"结果: {result.get('message', 'Unknown')}")
    except Exception as e:
        print(f"异常: {e}")
    
    # 测试案例3: 有效的JSON字符串（字典）
    print("\n3. 测试有效的JSON字符串（字典）:")
    json_dict_str = json.dumps({"Title": "JSON Test", "Number": 100})
    print(f"输入: {json_dict_str}")
    try:
        result = await create_table_records(test_table_id, json_dict_str)
        print(f"结果: {result.get('message', 'Unknown')}")
    except Exception as e:
        print(f"异常: {e}")
    
    # 测试案例4: 有效的JSON字符串（列表）
    print("\n4. 测试有效的JSON字符串（列表）:")
    json_list_str = json.dumps([{"Title": "JSON Record 1"}, {"Title": "JSON Record 2"}])
    print(f"输入: {json_list_str}")
    try:
        result = await create_table_records(test_table_id, json_list_str)
        print(f"结果: {result.get('message', 'Unknown')}")
    except Exception as e:
        print(f"异常: {e}")
    
    # 测试案例5: 无效的JSON字符串
    print("\n5. 测试无效的JSON字符串:")
    invalid_json_str = '{"Title": "Invalid JSON", "Number": }'
    print(f"输入: {invalid_json_str}")
    try:
        result = await create_table_records(test_table_id, invalid_json_str)
        print(f"结果: {result}")
    except Exception as e:
        print(f"异常: {e}")
    
    # 测试案例6: 非字典/列表的JSON字符串
    print("\n6. 测试非字典/列表的JSON字符串:")
    invalid_type_json = json.dumps("just a string")
    print(f"输入: {invalid_type_json}")
    try:
        result = await create_table_records(test_table_id, invalid_type_json)
        print(f"结果: {result}")
    except Exception as e:
        print(f"异常: {e}")
    
    # 测试案例7: 数字类型
    print("\n7. 测试数字类型:")
    number_input = 123
    print(f"输入: {number_input}")
    try:
        result = await create_table_records(test_table_id, number_input)
        print(f"结果: {result}")
    except Exception as e:
        print(f"异常: {e}")
    
    print("\n测试完成！")

if __name__ == "__main__":
    asyncio.run(test_records_protection())