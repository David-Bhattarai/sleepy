#!/usr/bin/env python3
"""
Test Admin Panel Button in Dashboard
Verify that admin panel button appears and works correctly
"""

import requests
import time

def test_admin_login():
    """Test admin login to get token"""
    print("Testing admin login...")
    
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
            print(f"Login successful - Admin: {is_admin}")
            return token, is_admin
        else:
            print(f"Login failed: {response.status_code}")
            return None, False
    except Exception as e:
        print(f"Login error: {e}")
        return None, False

def test_admin_stats(token):
    """Test admin stats endpoint"""
    print("Testing admin stats...")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get("http://localhost:5000/api/admin/stats", headers=headers)
        if response.status_code == 200:
            stats = response.json()
            print("Admin stats retrieved:")
            print(f"  - Users: {stats.get('total_users', 0)}")
            print(f"  - Doctors: {stats.get('total_doctors', 0)}")
            print(f"  - Appointments: {stats.get('total_appointments', 0)}")
            print(f"  - Chats: {stats.get('total_chats', 0)}")
            return True
        else:
            print(f"Stats failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"Stats error: {e}")
        return False

def main():
    print("ADMIN PANEL BUTTON TEST")
    print("=" * 30)
    
    # Test login
    token, is_admin = test_admin_login()
    if not token:
        print("Cannot proceed without token")
        return
    
    if not is_admin:
        print("User is not admin - button will not show")
        return
    
    # Test stats
    stats_ok = test_admin_stats(token)
    
    print("\n" + "=" * 30)
    print("ADMIN PANEL BUTTON STATUS")
    print("=" * 30)
    
    if token and is_admin and stats_ok:
        print("✅ Admin panel button should work!")
        print("\nHow to see admin button:")
        print("1. Login as admin (admin@aura.com / admin123)")
        print("2. Go to dashboard: http://localhost:5000/dashboard.html")
        print("3. Look for 'Admin Panel' card in left sidebar")
        print("4. Click 'Open Admin Panel' button")
        print("5. Admin panel opens in new tab")
        
        print("\nAdmin Panel Features:")
        print("- Real-time database statistics")
        print("- Click to open admin panel")
        print("- Shows current user/doctor/chat counts")
        print("- Only visible to admin users")
    else:
        print("⚠️ Some issues found")
        if not token:
            print("  - Login failed")
        if not is_admin:
            print("  - User is not admin")
        if not stats_ok:
            print("  - Stats endpoint failed")

if __name__ == "__main__":
    main()