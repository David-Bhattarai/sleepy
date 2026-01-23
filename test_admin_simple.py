#!/usr/bin/env python3
"""
Simple Admin Panel Test
Tests basic admin panel functionality
"""

import requests
import json

SERVER_URL = "http://localhost:5000"

def test_admin_login():
    """Test admin login"""
    print("Testing admin login...")
    
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
            print(f"Login successful - Admin: {is_admin}")
            return token
        else:
            print(f"Login failed: {response.status_code}")
            return None
    except Exception as e:
        print(f"Login error: {e}")
        return None

def test_admin_endpoints(token):
    """Test admin endpoints"""
    headers = {"Authorization": f"Bearer {token}"}
    
    endpoints = [
        ("/api/admin/stats", "Statistics"),
        ("/api/admin/users", "Users"),
        ("/api/admin/doctors", "Doctors"),
        ("/api/admin/appointments", "Appointments"),
        ("/api/admin/chat_history", "Chat History"),
        ("/api/admin/mood_entries", "Mood Entries"),
        ("/api/admin/payments", "Payments"),
        ("/api/admin/emotions", "Emotions")
    ]
    
    results = []
    
    for endpoint, name in endpoints:
        try:
            response = requests.get(f"{SERVER_URL}{endpoint}", headers=headers)
            if response.status_code == 200:
                data = response.json()
                print(f"{name}: OK")
                results.append(True)
            else:
                print(f"{name}: Failed ({response.status_code})")
                results.append(False)
        except Exception as e:
            print(f"{name}: Error - {e}")
            results.append(False)
    
    return results

def main():
    print("AURA Admin Panel Simple Test")
    print("=" * 40)
    
    # Test login
    token = test_admin_login()
    if not token:
        print("Cannot proceed without token")
        return
    
    # Test endpoints
    results = test_admin_endpoints(token)
    
    # Summary
    passed = sum(results)
    total = len(results)
    
    print(f"\nResults: {passed}/{total} endpoints working")
    
    if passed == total:
        print("All admin endpoints are working!")
        print("\nAdmin panel is ready:")
        print("- Email: admin@aura.com")
        print("- Password: admin123")
        print("- URL: http://localhost:5000/admin.html")
    else:
        print("Some endpoints need attention")

if __name__ == "__main__":
    main()