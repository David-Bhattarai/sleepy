#!/usr/bin/env python3

# Simple test to check database initialization
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from db_helper import initialize_database, init_all_tables
    print("✅ Successfully imported database functions")
    
    # Test init_all_tables function
    print("🔄 Testing init_all_tables...")
    init_all_tables()
    print("✅ init_all_tables works!")
    
    # Test initialize_database function
    print("🔄 Testing initialize_database...")
    result = initialize_database()
    print(f"✅ initialize_database result: {result}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()