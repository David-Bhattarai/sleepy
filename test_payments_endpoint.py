#!/usr/bin/env python3
"""
Test Payments Endpoint Specifically
"""

import requests
import json

SERVER_URL = "http://localhost:5000"

def test_payments_endpoint():
    """Test payments endpoint specifically"""
    print("🔐 Getting admin token...")
    
    signin_data = {
        "email": "admin@aura.com",
        "password": "admin123"
    }
    
    try:
        response = requests.post(f"{SERVER_URL}/api/signin", json=signin_data)
        if response.status_code == 200:
            data = response.json()
            token = data.get('token')
            print(f"✅ Got token: {token[:20]}...")
        else:
            print(f"❌ Login failed: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Login error: {e}")
        return
    
    print("\n💳 Testing payments endpoint...")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(f"{SERVER_URL}/api/admin/payments", headers=headers)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success: {len(data.get('payments', []))} payments found")
            print(f"Response: {json.dumps(data, indent=2)}")
        else:
            print(f"❌ Failed: {response.status_code}")
            try:
                error_data = response.json()
                print(f"Error: {json.dumps(error_data, indent=2)}")
            except:
                print(f"Raw response: {response.text}")
                
    except Exception as e:
        print(f"❌ Request error: {e}")

if __name__ == "__main__":
    test_payments_endpoint()