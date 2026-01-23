#!/usr/bin/env python3
"""
Database Browser - View database tables in web browser
Simple HTML interface to view all database tables
"""

import sqlite3
import os
from flask import Flask, render_template_string
import webbrowser
import threading
import time

# HTML template for database browser
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AURA Database Browser</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #333;
            text-align: center;
            margin-bottom: 30px;
        }
        .table-section {
            margin-bottom: 40px;
        }
        .table-title {
            background: #4CAF50;
            color: white;
            padding: 10px 15px;
            margin: 0;
            border-radius: 5px 5px 0 0;
            font-size: 18px;
        }
        .table-container {
            overflow-x: auto;
            border: 1px solid #ddd;
            border-radius: 0 0 5px 5px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            background: white;
        }
        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        th {
            background-color: #f8f9fa;
            font-weight: 600;
            color: #333;
        }
        tr:hover {
            background-color: #f5f5f5;
        }
        .record-count {
            background: #2196F3;
            color: white;
            padding: 5px 10px;
            border-radius: 15px;
            font-size: 12px;
            margin-left: 10px;
        }
        .no-data {
            text-align: center;
            padding: 20px;
            color: #666;
            font-style: italic;
        }
        .refresh-btn {
            background: #4CAF50;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            margin-bottom: 20px;
        }
        .refresh-btn:hover {
            background: #45a049;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🗄️ AURA Database Browser</h1>
        <button class="refresh-btn" onclick="location.reload()">🔄 Refresh Data</button>
        
        {% for table_name, data in tables.items() %}
        <div class="table-section">
            <h2 class="table-title">
                📊 {{ table_name.upper() }}
                <span class="record-count">{{ data.records|length }} records</span>
            </h2>
            <div class="table-container">
                {% if data.records %}
                <table>
                    <thead>
                        <tr>
                            {% for column in data.columns %}
                            <th>{{ column }}</th>
                            {% endfor %}
                        </tr>
                    </thead>
                    <tbody>
                        {% for record in data.records %}
                        <tr>
                            {% for value in record %}
                            <td>{{ value if value is not none else '' }}</td>
                            {% endfor %}
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
                {% else %}
                <div class="no-data">No data available in this table</div>
                {% endif %}
            </div>
        </div>
        {% endfor %}
    </div>
</body>
</html>
"""

def get_database_data():
    """Get all data from database tables"""
    # Try different database paths
    db_paths = [
        'sleepy/server/database.db',
        'database.db',
        'sleepy/database.db'
    ]
    
    db_path = None
    for path in db_paths:
        if os.path.exists(path):
            db_path = path
            break
    
    if not db_path:
        return {"error": "Database file not found"}
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get all table names
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        database_data = {}
        
        for table in tables:
            table_name = table[0]
            
            # Get table structure
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns_info = cursor.fetchall()
            columns = [col[1] for col in columns_info]
            
            # Get table data
            cursor.execute(f"SELECT * FROM {table_name}")
            records = cursor.fetchall()
            
            database_data[table_name] = {
                'columns': columns,
                'records': records
            }
        
        conn.close()
        return database_data
        
    except Exception as e:
        return {"error": f"Database error: {e}"}

# Flask app for database browser
app = Flask(__name__)

@app.route('/')
def database_browser():
    """Main database browser page"""
    tables = get_database_data()
    
    if "error" in tables:
        error_html = f"""
        <html>
        <body style="font-family: Arial; padding: 50px; text-align: center;">
            <h1 style="color: red;">❌ Database Error</h1>
            <p>{tables['error']}</p>
            <p>Make sure the database file exists and the server is not running.</p>
        </body>
        </html>
        """
        return error_html
    
    return render_template_string(HTML_TEMPLATE, tables=tables)

def open_browser():
    """Open browser after a short delay"""
    time.sleep(1.5)
    webbrowser.open('http://localhost:5001')

def main():
    """Main function to start database browser"""
    print("🗄️ AURA DATABASE BROWSER")
    print("=" * 40)
    
    # Check if database exists
    db_paths = [
        'sleepy/server/database.db',
        'database.db', 
        'sleepy/database.db'
    ]
    
    db_found = False
    for path in db_paths:
        if os.path.exists(path):
            print(f"✅ Database found: {path}")
            db_found = True
            break
    
    if not db_found:
        print("❌ Database not found!")
        print("Make sure you're in the project directory and database exists.")
        return
    
    print("🌐 Starting database browser...")
    print("📊 Opening browser at: http://localhost:5001")
    print("🔄 Press Ctrl+C to stop")
    
    # Start browser in separate thread
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    # Start Flask app
    try:
        app.run(host='localhost', port=5001, debug=False)
    except KeyboardInterrupt:
        print("\n👋 Database browser stopped")

if __name__ == "__main__":
    main()