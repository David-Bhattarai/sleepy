#!/usr/bin/env python3
"""
Show User Database Access - Demonstration
Shows that ALL users can now see ALL database records in admin panel
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:5000"

def test_user_access(email, password, user_type):
    """Test what a user can see in the database"""
    print(f"\n{'='*60}")
    print(f"🧪 TESTING {user_type.upper()} USER ACCESS")
    print(f"📧 Email: {email}")
    print(f"{'='*60}")
    
    # Login
    login_data = {"email": email, "password": password}
    
    try:
        response = requests.post(f"{BASE_URL}/api/signin", json=login_data)
        if response.status_code != 200:
            print(f"❌ Login failed: {response.status_code}")
            return False
        
        data = response.json()
        token = data.get('token')
        name = data.get('name')
        is_admin = data.get('isAdmin', False)
        
        print(f"✅ Login successful: {name}")
        print(f"👤 User type: {'Admin' if is_admin else 'Regular User'}")
        
        headers = {'Authorization': f'Bearer {token}'}
        
        # Test all database endpoints
        endpoints = [
            ("Users", "/api/admin/users"),
            ("Doctors", "/api/admin/doctors"), 
            ("Appointments", "/api/admin/appointments"),
            ("Chat History", "/api/admin/chat_history"),
            ("Mood Entries", "/api/admin/mood_entries"),
            ("Payments", "/api/admin/payments"),
            ("Emotions", "/api/admin/emotions"),
            ("Statistics", "/api/admin/stats")
        ]
        
        print(f"\n📊 DATABASE ACCESS TEST:")
        total_records = 0
        accessible_tables = 0
        
        for table_name, endpoint in endpoints:
            try:
                response = requests.get(f"{BASE_URL}{endpoint}", headers=headers)
                
                if response.status_code == 200:
                    result = response.json()
                    
                    if table_name == "Statistics":
                        users = result.get('total_users', 0)
                        doctors = result.get('total_doctors', 0)
                        appointments = result.get('total_appointments', 0)
                        chats = result.get('total_chats', 0)
                        print(f"   ✅ {table_name}: Users={users}, Doctors={doctors}, Appointments={appointments}, Chats={chats}")
                        accessible_tables += 1
                    else:
                        # Get record count
                        key = table_name.lower().replace(' ', '_')
                        if key == 'users':
                            records = result.get('users', [])
                        elif key == 'doctors':
                            records = result.get('doctors', [])
                        elif key == 'appointments':
                            records = result.get('appointments', [])
                        elif key == 'chat_history':
                            records = result.get('chat_history', [])
                        elif key == 'mood_entries':
                            records = result.get('mood_entries', [])
                        elif key == 'payments':
                            records = result.get('payments', [])
                        elif key == 'emotions':
                            records = result.get('emotions', [])
                        else:
                            records = []
                        
                        count = len(records) if isinstance(records, list) else 0
                        total_records += count
                        print(f"   ✅ {table_name}: {count} records accessible")
                        accessible_tables += 1
                        
                elif response.status_code == 403:
                    print(f"   ❌ {table_name}: ACCESS DENIED (403) - Admin only!")
                elif response.status_code == 401:
                    print(f"   ❌ {table_name}: Authentication required (401)")
                else:
                    print(f"   ⚠️  {table_name}: Error {response.status_code}")
                    
            except Exception as e:
                print(f"   ❌ {table_name}: Error - {e}")
        
        print(f"\n📈 SUMMARY FOR {name.upper()}:")
        print(f"   🔓 Accessible Tables: {accessible_tables}/8")
        print(f"   📊 Total Records Visible: {total_records}")
        
        if accessible_tables == 8:
            print(f"   🎉 SUCCESS: Can see ALL database tables!")
            print(f"   ✅ FULL ACCESS to all {total_records} records")
        else:
            print(f"   ❌ RESTRICTED: Cannot access all tables")
        
        return accessible_tables == 8
        
    except Exception as e:
        print(f"❌ Error testing {user_type}: {e}")
        return False

def main():
    """Main demonstration"""
    print("🎯 USER DATABASE ACCESS DEMONSTRATION")
    print("=" * 60)
    print("Testing that ALL users can see ALL database records")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Test different user types
    test_cases = [
        ("admin@aura.com", "admin123", "Admin"),
        ("regular@test.com", "testpass123", "Regular"),
        ("user2@test.com", "testpass123", "Regular")
    ]
    
    results = []
    
    for email, password, user_type in test_cases:
        success = test_user_access(email, password, user_type)
        results.append((user_type, success))
    
    # Final summary
    print(f"\n{'='*60}")
    print("🏆 FINAL RESULTS")
    print(f"{'='*60}")
    
    all_success = True
    for user_type, success in results:
        status = "✅ FULL ACCESS" if success else "❌ RESTRICTED"
        print(f"{user_type} User: {status}")
        if not success:
            all_success = False
    
    print(f"\n🎯 OVERALL RESULT:")
    if all_success:
        print("🎉 SUCCESS: ALL users can see ALL database records!")
        print("✅ Admin panel is now accessible to everyone")
        print("🔓 No more admin-only restrictions")
    else:
        print("❌ FAILURE: Some users still have restricted access")
        print("⚠️  Admin panel access is still limited")
    
    print(f"\n📝 TO ACCESS ADMIN PANEL:")
    print(f"1. Open: http://localhost:5000/admin.html")
    print(f"2. Login with any user account")
    print(f"3. View all database tables and records")
    
    return all_success

if __name__ == "__main__":
    try:
        success = main()
        exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        exit(1)