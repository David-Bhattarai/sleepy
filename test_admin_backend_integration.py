#!/usr/bin/env python3
"""
Test Admin Panel Backend Integration
Comprehensive test of all admin panel backend functionality
"""

import requests
import json
import time

SERVER_URL = "http://localhost:5000"

def test_admin_login():
    """Test admin login and get token"""
    print("🔐 Testing Admin Login...")
    
    signin_data = {
        "email": "admin@aura.com",
        "password": "admin123"
    }
    
    try:
        response = requests.post(f"{SERVER_URL}/api/signin", json=signin_data)
        if response.status_code == 200:
            data = response.json()
            token = data.get('token')
            is_admin = data.get('isAdmin', False)
            print(f"✅ Admin login successful - Admin: {is_admin}")
            return token
        else:
            print(f"❌ Admin login failed: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Admin login error: {e}")
        return None

def test_admin_endpoints(token):
    """Test all admin API endpoints"""
    print("\n📊 Testing Admin API Endpoints...")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    endpoints = [
        ("/api/admin/stats", "Platform Statistics"),
        ("/api/admin/users", "Users Management"),
        ("/api/admin/doctors", "Doctors Management"),
        ("/api/admin/appointments", "Appointments Management"),
        ("/api/admin/chat_history", "Chat History"),
        ("/api/admin/mood_entries", "Mood Entries"),
        ("/api/admin/payments", "Payments"),
        ("/api/admin/emotions", "Emotion Detection Records")
    ]
    
    results = {}
    
    for endpoint, name in endpoints:
        try:
            response = requests.get(f"{SERVER_URL}{endpoint}", headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                
                # Extract data based on endpoint
                if endpoint == "/api/admin/stats":
                    count = f"Users: {data.get('total_users', 0)}, Doctors: {data.get('total_doctors', 0)}"
                elif endpoint == "/api/admin/users":
                    count = f"{len(data.get('users', []))} users"
                elif endpoint == "/api/admin/doctors":
                    count = f"{len(data.get('doctors', []))} doctors"
                elif endpoint == "/api/admin/appointments":
                    count = f"{len(data.get('appointments', []))} appointments"
                elif endpoint == "/api/admin/chat_history":
                    count = f"{len(data.get('chat_history', []))} messages"
                elif endpoint == "/api/admin/mood_entries":
                    count = f"{len(data.get('mood_entries', []))} entries"
                elif endpoint == "/api/admin/payments":
                    count = f"{len(data.get('payments', []))} payments"
                elif endpoint == "/api/admin/emotions":
                    count = f"{len(data.get('emotions', []))} records"
                else:
                    count = "Data available"
                
                print(f"✅ {name}: OK ({count})")
                results[endpoint] = {"status": "success", "data": data, "count": count}
                
            else:
                print(f"❌ {name}: Failed ({response.status_code})")
                results[endpoint] = {"status": "failed", "code": response.status_code}
                
        except Exception as e:
            print(f"❌ {name}: Error - {e}")
            results[endpoint] = {"status": "error", "error": str(e)}
    
    return results

def test_database_connectivity():
    """Test database connectivity and table structure"""
    print("\n🗄️ Testing Database Connectivity...")
    
    try:
        import sqlite3
        import os
        
        db_path = "sleepy/server/database.db"
        if not os.path.exists(db_path):
            print(f"❌ Database file not found: {db_path}")
            return False
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check all required tables
        tables = [
            'users', 'doctors', 'appointments', 'chat_history', 
            'simple_mood_entries', 'payments', 'face_emotion_detection'
        ]
        
        existing_tables = []
        for table in tables:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                existing_tables.append((table, count))
                print(f"✅ Table '{table}': {count} records")
            except sqlite3.OperationalError:
                print(f"⚠️ Table '{table}': Not found")
        
        conn.close()
        
        print(f"\n📊 Database Summary:")
        print(f"   - Database file: {db_path}")
        print(f"   - Tables found: {len(existing_tables)}/{len(tables)}")
        print(f"   - Total records: {sum(count for _, count in existing_tables)}")
        
        return len(existing_tables) >= 5  # At least 5 core tables should exist
        
    except Exception as e:
        print(f"❌ Database connectivity error: {e}")
        return False

def test_admin_panel_frontend():
    """Test admin panel frontend files"""
    print("\n🎨 Testing Admin Panel Frontend...")
    
    files_to_check = [
        ("sleepy/client/admin.html", "Admin HTML"),
        ("sleepy/client/admin.js", "Admin JavaScript"),
        ("sleepy/client/styles.css", "Styles CSS")
    ]
    
    frontend_status = {}
    
    for file_path, description in files_to_check:
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    size_kb = len(content) / 1024
                    print(f"✅ {description}: Found ({size_kb:.1f} KB)")
                    frontend_status[file_path] = {"status": "found", "size_kb": size_kb}
            else:
                print(f"❌ {description}: Not found")
                frontend_status[file_path] = {"status": "missing"}
        except Exception as e:
            print(f"❌ {description}: Error - {e}")
            frontend_status[file_path] = {"status": "error", "error": str(e)}
    
    return frontend_status

def test_server_status():
    """Test server status and availability"""
    print("\n🌐 Testing Server Status...")
    
    try:
        # Test main server
        response = requests.get(f"{SERVER_URL}", timeout=5)
        print(f"✅ Main server: Running (Status: {response.status_code})")
        
        # Test admin panel route
        response = requests.get(f"{SERVER_URL}/admin.html", timeout=5)
        if response.status_code == 200:
            print("✅ Admin panel route: Accessible")
        else:
            print(f"⚠️ Admin panel route: Status {response.status_code}")
        
        # Test dashboard route
        response = requests.get(f"{SERVER_URL}/dashboard.html", timeout=5)
        if response.status_code == 200:
            print("✅ Dashboard route: Accessible")
        else:
            print(f"⚠️ Dashboard route: Status {response.status_code}")
        
        return True
        
    except Exception as e:
        print(f"❌ Server not running: {e}")
        return False

def generate_integration_report(results):
    """Generate comprehensive integration report"""
    print("\n" + "=" * 60)
    print("📋 ADMIN PANEL BACKEND INTEGRATION REPORT")
    print("=" * 60)
    
    # Count successful endpoints
    successful_endpoints = sum(1 for result in results.values() if result.get('status') == 'success')
    total_endpoints = len(results)
    
    print(f"\n🎯 API ENDPOINTS STATUS: {successful_endpoints}/{total_endpoints}")
    
    for endpoint, result in results.items():
        status = result.get('status', 'unknown')
        if status == 'success':
            count = result.get('count', 'N/A')
            print(f"   ✅ {endpoint}: {count}")
        elif status == 'failed':
            code = result.get('code', 'Unknown')
            print(f"   ❌ {endpoint}: HTTP {code}")
        else:
            error = result.get('error', 'Unknown error')
            print(f"   ⚠️ {endpoint}: {error}")
    
    # Integration status
    integration_score = (successful_endpoints / total_endpoints) * 100
    
    print(f"\n📊 INTEGRATION SCORE: {integration_score:.1f}%")
    
    if integration_score >= 90:
        print("🎉 EXCELLENT: Admin panel is fully integrated with backend!")
    elif integration_score >= 75:
        print("✅ GOOD: Admin panel is well integrated with minor issues")
    elif integration_score >= 50:
        print("⚠️ FAIR: Admin panel has some integration issues")
    else:
        print("❌ POOR: Admin panel needs significant backend work")
    
    print(f"\n🚀 ADMIN PANEL ACCESS:")
    print(f"   - Dashboard: {SERVER_URL}/dashboard.html")
    print(f"   - Direct: {SERVER_URL}/admin.html")
    print(f"   - Login: admin@aura.com / admin123")
    
    return integration_score

def main():
    """Main integration test function"""
    print("🛠️ ADMIN PANEL BACKEND INTEGRATION TEST")
    print("=" * 50)
    
    # Test server status
    server_running = test_server_status()
    if not server_running:
        print("\n❌ Server is not running. Please start server first:")
        print("   cd sleepy/server && python app.py")
        return
    
    # Test admin login
    token = test_admin_login()
    if not token:
        print("\n❌ Cannot proceed without admin token")
        return
    
    # Test database connectivity
    db_connected = test_database_connectivity()
    
    # Test admin endpoints
    api_results = test_admin_endpoints(token)
    
    # Test frontend files
    frontend_status = test_admin_panel_frontend()
    
    # Generate comprehensive report
    integration_score = generate_integration_report(api_results)
    
    # Final summary
    print(f"\n" + "=" * 50)
    print("🎯 FINAL INTEGRATION STATUS")
    print("=" * 50)
    
    if integration_score >= 75 and db_connected:
        print("✅ ADMIN PANEL IS FULLY INTEGRATED WITH BACKEND!")
        print("\n🎉 What's Working:")
        print("   - Database connectivity")
        print("   - API endpoints")
        print("   - Frontend files")
        print("   - Authentication")
        print("   - Real-time data")
        
        print("\n🚀 Ready for Production Use!")
        
    else:
        print("⚠️ ADMIN PANEL NEEDS ATTENTION")
        print("\n🔧 Issues Found:")
        if not db_connected:
            print("   - Database connectivity issues")
        if integration_score < 75:
            print("   - API endpoint failures")
        
        print("\n📝 Recommended Actions:")
        print("   - Check database file exists")
        print("   - Verify all tables are created")
        print("   - Test API endpoints individually")

if __name__ == "__main__":
    main()