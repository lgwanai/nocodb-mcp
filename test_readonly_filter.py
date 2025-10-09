#!/usr/bin/env python3
"""
测试只读字段过滤功能
"""

import json
import copy
from typing import Any, Dict, List, Optional, Union

# 复制过滤函数用于测试
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

def test_readonly_field_filtering():
    """
    测试只读字段过滤功能
    """
    print("测试只读字段过滤功能")
    print("=" * 60)
    
    # 测试案例1: 用户的实际数据（包含CreatedAt和UpdatedAt）
    print("\n1. 测试用户实际数据（包含只读字段）:")
    user_data = {
        "Id": 2, 
        "CreatedAt": "2025-10-07 04:17:57+00:00", 
        "UpdatedAt": "2025-10-08 15:22:27+00:00", 
        "Title": "任务2: 沉睡用户分层模型设计",
        "project": None, 
        "status": "done",
        "result": "### 任务分解：任务2 沉睡用户分层模型设计"
    }
    
    print(f"原始数据字段: {list(user_data.keys())}")
    print(f"包含只读字段: CreatedAt={user_data.get('CreatedAt')}, UpdatedAt={user_data.get('UpdatedAt')}")
    
    filtered_data = filter_readonly_fields(user_data)
    print(f"过滤后字段: {list(filtered_data.keys())}")
    print(f"CreatedAt已删除: {'CreatedAt' not in filtered_data}")
    print(f"UpdatedAt已删除: {'UpdatedAt' not in filtered_data}")
    print(f"Id保留: {'Id' in filtered_data}")
    print(f"Title保留: {'Title' in filtered_data}")
    
    # 测试案例2: 不同大小写的只读字段
    print("\n2. 测试不同大小写的只读字段:")
    mixed_case_data = {
        "id": 1,
        "createdAt": "2025-01-01 00:00:00",
        "updatedAt": "2025-01-02 00:00:00", 
        "Created By": "user1",
        "Updated By": "user2",
        "nc_created_at": "2025-01-01 00:00:00",
        "name": "test record",
        "value": 123
    }
    
    print(f"原始数据字段: {list(mixed_case_data.keys())}")
    filtered_mixed = filter_readonly_fields(mixed_case_data)
    print(f"过滤后字段: {list(filtered_mixed.keys())}")
    
    readonly_removed = [field for field in mixed_case_data.keys() if field not in filtered_mixed]
    print(f"已删除的只读字段: {readonly_removed}")
    
    # 测试案例3: 批量记录
    print("\n3. 测试批量记录:")
    batch_data = [
        {
            "Id": 1,
            "CreatedAt": "2025-01-01 00:00:00",
            "UpdatedAt": "2025-01-02 00:00:00",
            "name": "record1"
        },
        {
            "Id": 2,
            "createdAt": "2025-01-01 00:00:00",
            "updatedAt": "2025-01-02 00:00:00",
            "name": "record2"
        }
    ]
    
    print(f"批量数据记录数: {len(batch_data)}")
    print(f"第一条记录原始字段: {list(batch_data[0].keys())}")
    print(f"第二条记录原始字段: {list(batch_data[1].keys())}")
    
    filtered_batch = filter_readonly_fields(batch_data)
    print(f"过滤后记录数: {len(filtered_batch)}")
    print(f"第一条记录过滤后字段: {list(filtered_batch[0].keys())}")
    print(f"第二条记录过滤后字段: {list(filtered_batch[1].keys())}")
    
    # 测试案例4: 没有只读字段的记录
    print("\n4. 测试没有只读字段的记录:")
    clean_data = {
        "id": 1,
        "name": "clean record",
        "value": 456,
        "description": "no readonly fields"
    }
    
    print(f"原始数据字段: {list(clean_data.keys())}")
    filtered_clean = filter_readonly_fields(clean_data)
    print(f"过滤后字段: {list(filtered_clean.keys())}")
    print(f"字段数量不变: {len(clean_data) == len(filtered_clean)}")
    
    # 测试案例5: 验证原始数据未被修改
    print("\n5. 验证原始数据未被修改:")
    original_data = {
        "Id": 1,
        "CreatedAt": "2025-01-01 00:00:00",
        "name": "test"
    }
    original_keys = list(original_data.keys())
    
    filtered_data = filter_readonly_fields(original_data)
    
    print(f"原始数据字段（过滤前）: {original_keys}")
    print(f"原始数据字段（过滤后）: {list(original_data.keys())}")
    print(f"原始数据未被修改: {original_keys == list(original_data.keys())}")
    print(f"过滤后数据字段: {list(filtered_data.keys())}")

if __name__ == "__main__":
    test_readonly_field_filtering()