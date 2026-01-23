#!/usr/bin/env python3
"""
Test Admin Panel Access for ALL Users
Tests that ALL authenticated users (not just admins) can access and view ALL database records
"""

import requests
import json
import sys
import time
from datetime import datetime

# Server configuration
BASE_URL = "http://localhost:5000"
ADMIN_PANEL_URL = f"{BASE_URL}/admin.html"

def test_user_login(email, password, expected_admin=False):
    """Test user login and return token"""
    print(f"\n🔐 Testing login for: {email}")
    
    login_data = {
        "email": email,
        "password": password
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/signin", json=login_data)
        
        if response.status_code == 200:
            data = response.json()
            token = data.get('token')
            name = data.get('name')
            is_admin = data.get('isAdmin', False)
            
            print(f"✅ Login successful: {name} (Admin: {is_admin})")
            
            if expected_admin and not is_admin:
                print(f"⚠️  Expected admin user but got regular user")
            elif not expected_admin and is_admin:
                print(f"⚠️  Expected regular user but got admin user")
            
            return {
                'token': token,
                'name': name,
                'is_admin': is_admin,
                'success': True
            }
        else:
            print(f"❌ Login failed: {response.status_code} - {response.text}")
            return {'success': False}
            
    except Exception as e:
        print(f"❌ Login error: {e}")
        return {'success': False}

def test_admin_endpoint_access(token, endpoint_name, endpoint_url, user_name, is_admin):
    """Test access to admin endpoint"""
    print(f"\n📊 Testing {endpoint_name} access for {user_name} (Admin: {is_admin})")
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.get(f"{BASE_URL}{endpoint_url}", headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            
            if endpoint_name == "Statistics":
                print(f"✅ {endpoint_name} accessible - Users: {data.get('total_users', 0)}, Doctors: {data.get('total_doctors', 0)}")
            elif 'success' in data and data['success']:
                records = data.get(endpoint_name.lower().replace(' ', '_'), [])
                if isinstance(records, list):
                    print(f"✅ {endpoint_name} accessible - {len(records)} records found")
                else:
                    print(f"✅ {endpoint_name} accessible - Data retrieved")
            else:
                print(f"⚠️  {endpoint_name} accessible but unexpected format: {data}")
            
            return True
            
        elif response.status_code == 401:
            print(f"❌ {endpoint_name} - Authentication required (401)")
            return False
        elif response.status_code == 403:
            print(f"❌ {endpoint_name} - Access forbidden (403) - This should NOT happen for any authenticated user!")
            return False
        else:
            print(f"❌ {endpoint_name} - Error {response.status_code}: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ {endpoint_name} error: {e}")
        return False

def test_all_admin_endpoints(user_info):
    """Test all admin endpoints for a user"""
    token = user_info['token']
    name = user_info['name']
    is_admin = user_info['is_admin']
    
    print(f"\n🧪 Testing ALL admin endpoints for {name} (Admin: {is_admin})")
    print("=" * 60)
    
    # Define all admin endpoints
    endpoints = [
        ("Statistics", "/api/admin/stats"),
        ("Users", "/api/admin/users"),
        ("Doctors", "/api/admin/doctors"),
        ("Appointments", "/api/admin/appointments"),
        ("Chat History", "/api/admin/chat_history"),
        ("Mood Entries", "/api/admin/mood_entries"),
        ("Payments", "/api/admin/payments"),
        ("Emotions", "/api/admin/emotions"),
        ("Analytics", "/api/admin/analytics")
    ]
    
    results = {}
    
    for endpoint_name, endpoint_url in endpoints:
        success = test_admin_endpoint_access(token, endpoint_name, endpoint_url, name, is_admin)
        results[endpoint_name] = success
        time.sleep(0.5)  # Small delay between requests
    
    return results

def create_test_users():
    """Create test users if they don't exist"""
    print("\n👥 Creating test users...")
    
    test_users = [
        {
            "name": "Regular User Test",
            "email": "regular@test.com",
            "password": "testpass123"
        },
        {
            "name": "Another User Test",
            "email": "user2@test.com", 
            "password": "testpass123"
        }
    ]
    
    for user_data in test_users:
        try:
            response = requests.post(f"{BASE_URL}/api/signup", json=user_data)
            if response.status_code == 201:
                print(f"✅ Created user: {user_data['email']}")
            elif response.status_code == 409:
                print(f"ℹ️  User already exists: {user_data['email']}")
            else:
                print(f"⚠️  Failed to create user {user_data['email']}: {response.status_code}")
        except Exception as e:
            print(f"❌ Error creating user {user_data['email']}: {e}")

def main():
    """Main test function"""
    print("🚀 ADMIN PANEL ALL USERS ACCESS TEST")
    print("=" * 50)
    print("Testing that ALL authenticated users can access ALL database records")
    print(f"Server: {BASE_URL}")
    print(f"Admin Panel: {ADMIN_PANEL_URL}")
    print(f"Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Create test users
    create_test_users()
    
    # Test users to check
    test_cases = [
        {
            "email": "admin@aura.com",
            "password": "admin123",
            "expected_admin": True,
            "description": "Admin User"
        },
        {
            "email": "regular@test.com", 
            "password": "testpass123",
            "expected_admin": False,
            "description": "Regular User 1"
        },
        {
            "email": "user2@test.com",
            "password": "testpass123", 
            "expected_admin": False,
            "description": "Regular User 2"
        }
    ]
    
    all_results = {}
    
    # Test each user
    for test_case in test_cases:
        print(f"\n{'='*60}")
        print(f"🧪 TESTING: {test_case['description']}")
        print(f"{'='*60}")
        
        # Login
        user_info = test_user_login(
            test_case['email'], 
            test_case['password'], 
            test_case['expected_admin']
        )
        
        if user_info['success']:
            # Test all admin endpoints
            results = test_all_admin_endpoints(user_info)
            all_results[test_case['description']] = {
                'user_info': user_info,
                'endpoint_results': results
            }
        else:
            print(f"❌ Skipping endpoint tests for {test_case['description']} due to login failure")
            all_results[test_case['description']] = {
                'user_info': user_info,
                'endpoint_results': {}
            }
    
    # Summary Report
    print(f"\n{'='*60}")
    print("📊 FINAL SUMMARY REPORT")
    print(f"{'='*60}")
    
    total_tests = 0
    total_passed = 0
    
    for user_type, data in all_results.items():
        user_info = data['user_info']
        results = data['endpoint_results']
        
        if user_info['success']:
            passed = sum(1 for success in results.values() if success)
            total = len(results)
            total_tests += total
            total_passed += passed
            
            print(f"\n{user_type}:")
            print(f"  Login: ✅ Success ({user_info['name']})")
            print(f"  Admin Status: {'✅ Admin' if user_info['is_admin'] else '👤 Regular User'}")
            print(f"  Endpoint Access: {passed}/{total} endpoints accessible")
            
            if passed == total:
                print(f"  Result: ✅ ALL DATABASE RECORDS ACCESSIBLE")
            else:
                print(f"  Result: ❌ Some endpoints blocked")
                for endpoint, success in results.items():
                    if not success:
                        print(f"    ❌ {endpoint} - BLOCKED")
        else:
            print(f"\n{user_type}:")
            print(f"  Login: ❌ Failed")
            print(f"  Result: ❌ Cannot test endpoints")
    
    print(f"\n{'='*60}")
    print(f"🎯 OVERALL RESULTS:")
    print(f"Total Endpoint Tests: {total_tests}")
    print(f"Successful Access: {total_passed}")
    print(f"Success Rate: {(total_passed/total_tests*100):.1f}%" if total_tests > 0 else "N/A")
    
    if total_passed == total_tests and total_tests > 0:
        print(f"🎉 SUCCESS: ALL users can access ALL database records!")
        print(f"✅ Admin panel is now accessible to ALL authenticated users")
    else:
        print(f"❌ FAILURE: Some users cannot access all database records")
        print(f"⚠️  Admin panel access is still restricted")
    
    print(f"\n📝 Instructions:")
    print(f"1. Start the server: python sleepy/server/app.py")
    print(f"2. Open browser: {ADMIN_PANEL_URL}")
    print(f"3. Login with any user account")
    print(f"4. Verify you can see all database tables and records")
    
    return total_passed == total_tests and total_tests > 0

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print(f"\n\n⚠️  Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Test failed with error: {e}")
        sys.exit(1)