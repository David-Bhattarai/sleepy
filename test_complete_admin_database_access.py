#!/usr/bin/env python3
"""
Test Complete Admin Database Access
Test all database tables and API endpoints
"""

import requests
import json
import time

def test_complete_admin_database_access():
    """Test all admin database endpoints"""
    print("🧪 Testing Complete Admin Database Access...")
    print("=" * 60)
    
    base_url = "http://localhost:5000"
    
    # Test endpoints
    endpoints = {
        'users': '/api/admin/users',
        'doctors': '/api/admin/doctors', 
        'appointments': '/api/admin/appointments',
        'chat_history': '/api/admin/chat_history',
        'mood_entries': '/api/admin/mood_entries',
        'payments': '/api/admin/payments',
        'emotions': '/api/admin/emotions',
        'emotional_intelligence': '/api/admin/emotional_intelligence',
        'mood_entries_advanced': '/api/admin/mood_entries_advanced',
        'mood_insights': '/api/admin/mood_insights',
        'mood_patterns': '/api/admin/mood_patterns',
        'doctor_availability': '/api/admin/doctor_availability'
    }
    
    # Test token (you'll need to get this from login)
    test_token = "your_auth_token_here"
    
    headers = {
        'Authorization': f'Bearer {test_token}',
        'Content-Type': 'application/json'
    }
    
    print("📊 TESTING ALL DATABASE ENDPOINTS:")
    print()
    
    results = {}
    
    for table_name, endpoint in endpoints.items():
        print(f"🔍 Testing {table_name}...")
        
        try:
            response = requests.get(f"{base_url}{endpoint}", headers=headers, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                
                # Count records
                record_count = 0
                if table_name == 'users' and 'users' in data:
                    record_count = len(data['users'])
                elif table_name == 'doctors' and 'doctors' in data:
                    record_count = len(data['doctors'])
                elif table_name == 'appointments' and 'appointments' in data:
                    record_count = len(data['appointments'])
                elif table_name == 'chat_history' and 'chat_history' in data:
                    record_count = len(data['chat_history'])
                elif table_name == 'mood_entries' and 'mood_entries' in data:
                    record_count = len(data['mood_entries'])
                elif table_name == 'payments' and 'payments' in data:
                    record_count = len(data['payments'])
                elif table_name == 'emotions' and 'emotions' in data:
                    record_count = len(data['emotions'])
                elif table_name == 'emotional_intelligence' and 'emotional_intelligence' in data:
                    record_count = len(data['emotional_intelligence'])
                elif table_name == 'mood_entries_advanced' and 'mood_entries_advanced' in data:
                    record_count = len(data['mood_entries_advanced'])
                elif table_name == 'mood_insights' and 'mood_insights' in data:
                    record_count = len(data['mood_insights'])
                elif table_name == 'mood_patterns' and 'mood_patterns' in data:
                    record_count = len(data['mood_patterns'])
                elif table_name == 'doctor_availability' and 'doctor_availability' in data:
                    record_count = len(data['doctor_availability'])
                
                results[table_name] = {
                    'status': 'SUCCESS',
                    'records': record_count,
                    'response_time': response.elapsed.total_seconds()
                }
                
                print(f"  ✅ {table_name}: {record_count} records")
                
            else:
                results[table_name] = {
                    'status': 'ERROR',
                    'error': f"HTTP {response.status_code}",
                    'response_time': response.elapsed.total_seconds()
                }
                print(f"  ❌ {table_name}: HTTP {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            results[table_name] = {
                'status': 'CONNECTION_ERROR',
                'error': 'Server not running'
            }
            print(f"  🔌 {table_name}: Server not running")
            
        except Exception as e:
            results[table_name] = {
                'status': 'ERROR',
                'error': str(e)
            }
            print(f"  ❌ {table_name}: {e}")
    
    print()
    print("=" * 60)
    print("📊 TEST SUMMARY:")
    print("=" * 60)
    
    total_records = 0
    successful_endpoints = 0
    
    for table_name, result in results.items():
        if result['status'] == 'SUCCESS':
            successful_endpoints += 1
            total_records += result['records']
            print(f"  ✅ {table_name:25} : {result['records']:6} records")
        else:
            print(f"  ❌ {table_name:25} : {result['status']}")
    
    print()
    print(f"  📈 Successful Endpoints: {successful_endpoints}/{len(endpoints)}")
    print(f"  📊 Total Records Found: {total_records}")
    
    if successful_endpoints == len(endpoints):
        print("\n🎉 ALL DATABASE ENDPOINTS WORKING!")
        print("✅ Admin panel ready for full database access")
    else:
        print(f"\n⚠️  {len(endpoints) - successful_endpoints} endpoints need attention")
        print("💡 Make sure server is running: python sleepy/server/app.py")
    
    print("\n🌐 Open admin panel: http://localhost:5000/admin.html")

if __name__ == "__main__":
    test_complete_admin_database_access()