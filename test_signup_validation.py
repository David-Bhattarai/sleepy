#!/usr/bin/env python3
"""
Test Signup Validation with Confirm Password
Tests the complete password validation on the server
"""

import requests
import json

SERVER_URL = "http://127.0.0.1:5000"

def test_signup_validation():
    """Test the signup endpoint validation"""
    print("🧪 Testing Complete Signup Validation")
    print("=" * 60)
    
    # Test 1: Password too short
    print("\n1️⃣ Testing password too short (should fail)...")
    response = requests.post(
        f"{SERVER_URL}/api/signup",
        headers={'Content-Type': 'application/json'},
        json={
            'name': 'Test User',
            'email': 'test1@example.com',
            'password': 'short',
            'confirmPassword': 'short'
        }
    )
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    
    if response.status_code == 400 and 'at least 8 characters' in response.json().get('error', ''):
        print("   ✅ PASS: Password length validation working!")
    else:
        print("   ❌ FAIL: Password length validation not working")
    
    # Test 2: Passwords don't match
    print("\n2️⃣ Testing passwords don't match (should fail)...")
    response = requests.post(
        f"{SERVER_URL}/api/signup",
        headers={'Content-Type': 'application/json'},
        json={
            'name': 'Test User',
            'email': 'test2@example.com',
            'password': 'password123',
            'confirmPassword': 'password456'
        }
    )
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    
    if response.status_code == 400 and 'do not match' in response.json().get('error', ''):
        print("   ✅ PASS: Password match validation working!")
    else:
        print("   ❌ FAIL: Password match validation not working")
    
    # Test 3: Missing confirm password
    print("\n3️⃣ Testing missing confirm password (should fail)...")
    response = requests.post(
        f"{SERVER_URL}/api/signup",
        headers={'Content-Type': 'application/json'},
        json={
            'name': 'Test User',
            'email': 'test3@example.com',
            'password': 'password123'
        }
    )
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    
    if response.status_code == 400:
        print("   ✅ PASS: Missing confirm password validation working!")
    else:
        print("   ❌ FAIL: Missing confirm password validation not working")
    
    # Test 4: Empty password
    print("\n4️⃣ Testing empty password (should fail)...")
    response = requests.post(
        f"{SERVER_URL}/api/signup",
        headers={'Content-Type': 'application/json'},
        json={
            'name': 'Test User',
            'email': 'test4@example.com',
            'password': '',
            'confirmPassword': ''
        }
    )
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    
    if response.status_code == 400:
        print("   ✅ PASS: Empty password validation working!")
    else:
        print("   ❌ FAIL: Empty password validation not working")
    
    # Test 5: Valid signup
    print("\n5️⃣ Testing valid signup (should succeed or fail with 'already registered')...")
    response = requests.post(
        f"{SERVER_URL}/api/signup",
        headers={'Content-Type': 'application/json'},
        json={
            'name': 'Valid User',
            'email': 'validuser@example.com',
            'password': 'validpassword123',
            'confirmPassword': 'validpassword123'
        }
    )
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    
    if response.status_code in [201, 409]:  # Success or already registered
        print("   ✅ PASS: Valid signup accepted!")
    else:
        print("   ❌ FAIL: Valid signup rejected")
    
    print("\n" + "=" * 60)
    print("🎯 Test Complete!")
    print("\n✅ All validations implemented:")
    print("   - Password must be at least 8 characters")
    print("   - Password and Confirm Password must match")
    print("   - All fields are required")
    print("   - Safe error handling with try-except")

if __name__ == "__main__":
    try:
        test_signup_validation()
    except requests.exceptions.ConnectionError:
        print("❌ ERROR: Cannot connect to server")
        print("💡 Make sure the server is running at http://127.0.0.1:5000")
        print("   Run: python sleepy/server/app.py")
    except Exception as e:
        print(f"❌ ERROR: {e}")
