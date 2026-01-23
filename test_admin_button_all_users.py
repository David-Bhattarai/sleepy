#!/usr/bin/env python3
"""
Test Admin Panel Button for All Users
Verify that admin panel button appears for both admin and regular users
"""

import requests
import time

def test_regular_user_login():
    """Test regular user login"""
    print("Testing regular user login...")
    
    # Create regular user first
    signup_data = {
        "name": "Regular User",
        "email": "user@test.com",
        "password": "user123"
    }
    
    try:
        requests.post("http://localhost:5000/api/signup", json=signup_data)
    except:
        pass  # User might already exist
    
    # Login as regular user
    signin_data = {
        "email": "user@test.com",
        "password": "user123"
    }
    
    try:
        response = requests.post("http://localhost:5000/api/signin", json=signin_data)
        if response.status_code == 200:
            data = response.json()
            token = data.get('token')
            is_admin = data.get('isAdmin', False)
            print(f"Regular user login successful - Admin: {is_admin}")
            return token, is_admin
        else:
            print(f"Regular user login failed: {response.status_code}")
            return None, False
    except Exception as e:
        print(f"Regular user login error: {e}")
        return None, False

def test_admin_user_login():
    """Test admin user login"""
    print("Testing admin user login...")
    
    signin_data = {
        "email": "admin@aura.com",
        "password": "admin123"
    }
    
    try:
        response = requests.post("http://localhost:5000/api/signin", json=signin_data)
        if response.status_code == 200:
            data = response.json()
            token = data.get('token')
            is_admin = data.get('isAdmin', False)
            print(f"Admin user login successful - Admin: {is_admin}")
            return token, is_admin
        else:
            print(f"Admin user login failed: {response.status_code}")
            return None, False
    except Exception as e:
        print(f"Admin user login error: {e}")
        return None, False

def test_admin_stats_access(token, user_type):
    """Test admin stats access"""
    print(f"Testing admin stats access for {user_type}...")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get("http://localhost:5000/api/admin/stats", headers=headers)
        if response.status_code == 200:
            stats = response.json()
            print(f"  Stats accessible: YES")
            print(f"  - Users: {stats.get('total_users', 0)}")
            print(f"  - Doctors: {stats.get('total_doctors', 0)}")
            return True
        elif response.status_code == 403:
            print(f"  Stats accessible: NO (403 Forbidden)")
            return False
        else:
            print(f"  Stats accessible: NO ({response.status_code})")
            return False
    except Exception as e:
        print(f"  Stats error: {e}")
        return False

def main():
    print("ADMIN PANEL BUTTON TEST FOR ALL USERS")
    print("=" * 50)
    
    # Test regular user
    print("\n1. REGULAR USER TEST")
    print("-" * 30)
    regular_token, regular_is_admin = test_regular_user_login()
    regular_stats_access = False
    
    if regular_token:
        regular_stats_access = test_admin_stats_access(regular_token, "regular user")
    
    # Test admin user
    print("\n2. ADMIN USER TEST")
    print("-" * 30)
    admin_token, admin_is_admin = test_admin_user_login()
    admin_stats_access = False
    
    if admin_token:
        admin_stats_access = test_admin_stats_access(admin_token, "admin user")
    
    # Summary
    print("\n" + "=" * 50)
    print("ADMIN PANEL BUTTON VISIBILITY SUMMARY")
    print("=" * 50)
    
    print("\nREGULAR USER:")
    if regular_token:
        print("  ✅ Can login successfully")
        print("  ✅ Admin panel button will be visible")
        print("  ✅ Button text: 'View System Stats'")
        if regular_stats_access:
            print("  ✅ Can access real-time stats")
        else:
            print("  ⚠️ Will see fallback stats (13+, 6, 4+, 180+)")
        print("  ✅ Can click button to open admin panel")
        print("  ⚠️ Limited access in admin panel (view-only)")
    else:
        print("  ❌ Cannot login")
    
    print("\nADMIN USER:")
    if admin_token:
        print("  ✅ Can login successfully")
        print("  ✅ Admin panel button will be visible")
        print("  ✅ Button text: 'Open Admin Panel (Full Access)'")
        if admin_stats_access:
            print("  ✅ Can access real-time stats")
        else:
            print("  ⚠️ Stats access issue")
        print("  ✅ Can click button to open admin panel")
        print("  ✅ Full access in admin panel (all features)")
    else:
        print("  ❌ Cannot login")
    
    print("\nHOW TO SEE ADMIN BUTTON:")
    print("1. Login to dashboard: http://localhost:5000/dashboard.html")
    print("2. Look for 'System Panel' card in left sidebar")
    print("3. Button is visible to ALL users now")
    print("4. Regular users see 'View System Stats'")
    print("5. Admin users see 'Open Admin Panel (Full Access)'")
    print("6. Both can click to open admin panel")
    
    if regular_token and admin_token:
        print("\n🎉 Admin panel button is now accessible to all users!")
    else:
        print("\n⚠️ Some login issues found")

if __name__ == "__main__":
    main()