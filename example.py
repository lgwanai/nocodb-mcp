#!/usr/bin/env python3
"""
NocoDB MCP Server Usage Example

This example demonstrates how to use the NocoDB MCP server tools.
Make sure to configure your .env file with proper NocoDB credentials before running.
"""

import asyncio
import json
from typing import Dict, Any

# Example data structures that match NocoDB field types
EXAMPLE_RECORD = {
    "SingleLineText": "John Doe",
    "LongText": "This is a longer text field that can contain multiple sentences and paragraphs.",
    "Email": "john.doe@example.com",
    "PhoneNumber": "123-456-7890",
    "URL": "https://www.example.com",
    "Number": 42,
    "Decimal": 3.14159,
    "Currency": 1000.50,
    "Percent": 85,
    "Duration": 3600,  # seconds
    "Rating": 4,
    "Checkbox": True,
    "Date": "2024-01-15",
    "DateTime": "2024-01-15 14:30:00+00:00",
    "Time": "14:30:00",
    "Year": 2024,
    "SingleSelect": "Option1",
    "MultiSelect": "Option1,Option2",
    "JSON": {
        "name": "John",
        "age": 30,
        "preferences": ["reading", "coding", "music"]
    },
    "Geometry": "40.7128, -74.0060"  # latitude, longitude
}

EXAMPLE_BATCH_RECORDS = [
    {
        "SingleLineText": "Alice Smith",
        "Email": "alice@example.com",
        "Number": 25,
        "Checkbox": True
    },
    {
        "SingleLineText": "Bob Johnson",
        "Email": "bob@example.com", 
        "Number": 30,
        "Checkbox": False
    },
    {
        "SingleLineText": "Carol Williams",
        "Email": "carol@example.com",
        "Number": 28,
        "Checkbox": True
    }
]

def print_result(operation: str, result: Dict[str, Any]):
    """Helper function to print operation results"""
    print(f"\n=== {operation} ===")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    print("-" * 50)

async def example_usage():
    """
    Example usage of NocoDB MCP server tools.
    
    Note: This is a demonstration of the expected tool interface.
    In actual usage, these tools would be called through the MCP protocol.
    """
    
    # Replace with your actual table ID
    TABLE_ID = "your-table-id-here"
    
    print("NocoDB MCP Server Usage Examples")
    print("=" * 50)
    
    # Example 1: Get server information
    print("\n1. Getting server information...")
    server_info_example = {
        "server_name": "NocoDB MCP Server",
        "nocodb_host": "https://your-nocodb-host.com",
        "mcp_port": 8000,
        "available_tools": [
            "create_table_records",
            "get_table_records",
            "update_table_record", 
            "delete_table_record",
            "get_server_info"
        ]
    }
    print_result("Server Info", server_info_example)
    
    # Example 2: Create a single record
    print("\n2. Creating a single record...")
    create_single_example = {
        "success": True,
        "data": [{"Id": 101}],
        "message": "Successfully created 1 record(s)"
    }
    print(f"Tool call: create_table_records(table_id='{TABLE_ID}', records={json.dumps(EXAMPLE_RECORD, indent=2)})")
    print_result("Create Single Record", create_single_example)
    
    # Example 3: Create multiple records
    print("\n3. Creating multiple records...")
    create_batch_example = {
        "success": True,
        "data": [{"Id": 102}, {"Id": 103}, {"Id": 104}],
        "message": "Successfully created 3 record(s)"
    }
    print(f"Tool call: create_table_records(table_id='{TABLE_ID}', records={json.dumps(EXAMPLE_BATCH_RECORDS, indent=2)})")
    print_result("Create Multiple Records", create_batch_example)
    
    # Example 4: Get records
    print("\n4. Retrieving records...")
    get_records_example = {
        "success": True,
        "data": {
            "list": [
                {"Id": 101, "SingleLineText": "John Doe", "Email": "john.doe@example.com"},
                {"Id": 102, "SingleLineText": "Alice Smith", "Email": "alice@example.com"}
            ],
            "pageInfo": {
                "totalRows": 25,
                "page": 1,
                "pageSize": 25,
                "isFirstPage": True,
                "isLastPage": True
            }
        },
        "message": f"Successfully retrieved records from table {TABLE_ID}"
    }
    print(f"Tool call: get_table_records(table_id='{TABLE_ID}', limit=25, offset=0)")
    print_result("Get Records", get_records_example)
    
    # Example 5: Update a record
    print("\n5. Updating a record...")
    update_data = {
        "SingleLineText": "John Doe Updated",
        "Email": "john.updated@example.com"
    }
    update_example = {
        "success": True,
        "data": {"Id": 101, "SingleLineText": "John Doe Updated", "Email": "john.updated@example.com"},
        "message": "Successfully updated record 101"
    }
    print(f"Tool call: update_table_record(table_id='{TABLE_ID}', record_id='101', data={json.dumps(update_data)})")
    print_result("Update Record", update_example)
    
    # Example 6: Delete a record
    print("\n6. Deleting a record...")
    delete_example = {
        "success": True,
        "message": "Successfully deleted record 101"
    }
    print(f"Tool call: delete_table_record(table_id='{TABLE_ID}', record_id='101')")
    print_result("Delete Record", delete_example)
    
    # Example 7: Error handling
    print("\n7. Error handling example...")
    error_example = {
        "success": False,
        "error": {"msg": "BadRequest [Error]: Table not found"},
        "status_code": 400
    }
    print_result("Error Response", error_example)
    
    print("\n" + "=" * 50)
    print("Examples completed!")
    print("\nTo use this MCP server:")
    print("1. Configure your .env file with NocoDB credentials")
    print("2. Install dependencies: pip install -r requirements.txt")
    print("3. Run in stdio mode: python server.py")
    print("4. Run in SSE mode: python server.py --sse")
    print("\nField Types Supported:")
    print("- SingleLineText, LongText, Email, PhoneNumber, URL")
    print("- Number, Decimal, Currency, Percent, Duration, Rating")
    print("- Checkbox, Date, DateTime, Time, Year")
    print("- SingleSelect, MultiSelect, JSON, Geometry")
    print("- Attachment (file uploads)")
    print("\nRead-only fields (ignored in requests):")
    print("- Look Up, Roll Up, Formula, Auto Number")
    print("- Created By, Updated By, Created At, Updated At")
    print("- Barcode, QR Code")

if __name__ == "__main__":
    asyncio.run(example_usage())