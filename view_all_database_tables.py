#!/usr/bin/env python3
"""
Complete Database Viewer - Show ALL tables and data
View all database records for MindBridge - NCIT Final Year Project Platform
"""

import sqlite3
import os
from datetime import datetime

def view_all_database_tables():
    """View all database tables and their data"""
    print("🔍 MindBridge - NCIT Final Year Project Complete Database Viewer")
    print("=" * 60)
    
    # Database paths to check
    db_paths = [
        'sleepy/server/database.db',
        'database.db',
        'sleepy/database.db'
    ]
    
    db_file = None
    for path in db_paths:
        if os.path.exists(path):
            db_file = path
            break
    
    if not db_file:
        print("❌ Database file not found!")
        print("Checked paths:", db_paths)
        return
    
    print(f"📂 Using database: {db_file}")
    print()
    
    with sqlite3.connect(db_file) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Get all table names
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
        tables = cursor.fetchall()
        
        print(f"📊 Found {len(tables)} tables in database:")
        for table in tables:
            print(f"  • {table['name']}")
        print()
        
        # Show data from each table
        for table in tables:
            table_name = table['name']
            print(f"\n{'='*20} {table_name.upper()} TABLE {'='*20}")
            
            try:
                # Get table structure
                cursor.execute(f"PRAGMA table_info({table_name})")
                columns = cursor.fetchall()
                
                print(f"📋 Columns: {', '.join([col['name'] for col in columns])}")
                
                # Get row count
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                count = cursor.fetchone()[0]
                print(f"📈 Total Records: {count}")
                
                if count > 0:
                    # Get all data (limit to 10 for display)
                    cursor.execute(f"SELECT * FROM {table_name} LIMIT 10")
                    rows = cursor.fetchall()
                    
                    print(f"\n📄 Sample Data (showing {len(rows)} records):")
                    print("-" * 80)
                    
                    # Print headers
                    headers = [col['name'] for col in columns]
                    header_line = " | ".join(f"{h:15}" for h in headers)
                    print(header_line)
                    print("-" * len(header_line))
                    
                    # Print data rows
                    for row in rows:
                        row_data = []
                        for col in headers:
                            value = str(row[col]) if row[col] is not None else 'NULL'
                            # Truncate long values
                            if len(value) > 15:
                                value = value[:12] + "..."
                            row_data.append(f"{value:15}")
                        print(" | ".join(row_data))
                    
                    if count > 10:
                        print(f"... and {count - 10} more records")
                else:
                    print("📭 No data in this table")
                    
            except Exception as e:
                print(f"❌ Error reading table {table_name}: {e}")
            
            print()
        
        # Summary statistics
        print("\n" + "="*60)
        print("📊 DATABASE SUMMARY")
        print("="*60)
        
        total_records = 0
        for table in tables:
            table_name = table['name']
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                count = cursor.fetchone()[0]
                total_records += count
                print(f"  {table_name:25} : {count:6} records")
            except:
                print(f"  {table_name:25} : ERROR")
        
        print(f"\n  {'TOTAL RECORDS':25} : {total_records:6}")
        print(f"  {'DATABASE SIZE':25} : {os.path.getsize(db_file):6} bytes")
        
        print("\n✅ Database analysis complete!")

if __name__ == "__main__":
    view_all_database_tables()