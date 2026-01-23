#!/usr/bin/env python3
"""
Test Server Response
Check if AURA chatbot and emotion detection are working properly
"""

import requests
import json
import base64
from PIL import Image
import io

def test_server_connection():
    """Test if server is running"""
    try:
        response = requests.get('http://127.0.0.1:5000')
        if response.status_code == 200:
            print("✅ Server is running!")
            return True
        else:
            print(f"❌ Server error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Server not running: {e}")
        return False

def test_signup_signin():
    """Test user signup and signin"""
    try:
        # Test signup
        signup_data = {
            'name': 'Test User',
            'email': 'test@example.com',
            'password': 'testpass123'
        }
        
        response = requests.post('http://127.0.0.1:5000/api/signup', json=signup_data)
        print(f"📝 Signup response: {response.status_code}")
        
        if response.status_code in [201, 409]:  # 201 = created, 409 = already exists
            # Test signin
            signin_data = {
                'email': 'test@example.com',
                'password': 'testpass123'
            }
            
            response = requests.post('http://127.0.0.1:5000/api/signin', json=signin_data)
            if response.status_code == 200:
                data = response.json()
                token = data.get('token')
                print("✅ Login successful!")
                return token
            else:
                print(f"❌ Login failed: {response.status_code}")
                return None
        else:
            print(f"❌ Signup failed: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Auth error: {e}")
        return None

def test_chatbot(token):
    """Test AURA chatbot response"""
    try:
        headers = {'Authorization': f'Bearer {token}'}
        chat_data = {'message': 'I feel really sad today'}
        
        response = requests.post('http://127.0.0.1:5000/api/doctor_chat', 
                               json=chat_data, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            ai_response = data.get('ai_response', '')
            print(f"🤖 AURA Response: {ai_response[:100]}...")
            
            if len(ai_response) > 20:
                print("✅ Chatbot working properly!")
                return True
            else:
                print("⚠️ Chatbot response too short")
                return False
        else:
            print(f"❌ Chatbot error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Chatbot test error: {e}")
        return False

def test_emotion_detection(token):
    """Test emotion detection"""
    try:
        # Create a simple test image
        test_image = Image.new('RGB', (100, 100), color='white')
        buffer = io.BytesIO()
        test_image.save(buffer, format='PNG')
        image_data = base64.b64encode(buffer.getvalue()).decode()
        image_data = f"data:image/png;base64,{image_data}"
        
        headers = {'Authorization': f'Bearer {token}'}
        emotion_data = {'image': image_data}
        
        response = requests.post('http://127.0.0.1:5000/api/emotion_detection_advanced', 
                               json=emotion_data, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            emotion = data.get('dominant_emotion', '')
            confidence = data.get('confidence', 0)
            method = data.get('method', 'unknown')
            
            print(f"😊 Detected Emotion: {emotion}")
            print(f"📈 Confidence: {confidence}%")
            print(f"🔧 Method: {method}")
            
            if emotion and confidence > 0:
                print("✅ Emotion detection working!")
                return True
            else:
                print("⚠️ Emotion detection returned empty results")
                return False
        else:
            print(f"❌ Emotion detection error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Emotion detection test error: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 TESTING AURA SERVER RESPONSES")
    print("=" * 50)
    
    # Test 1: Server connection
    print("\n1. Testing server connection...")
    if not test_server_connection():
        print("❌ Server not running! Start server first:")
        print("   python app.py")
        return
    
    # Test 2: Authentication
    print("\n2. Testing authentication...")
    token = test_signup_signin()
    if not token:
        print("❌ Authentication failed!")
        return
    
    # Test 3: Chatbot
    print("\n3. Testing AURA chatbot...")
    chatbot_working = test_chatbot(token)
    
    # Test 4: Emotion detection
    print("\n4. Testing emotion detection...")
    emotion_working = test_emotion_detection(token)
    
    # Summary
    print("\n" + "=" * 50)
    print("🎯 TEST RESULTS:")
    print("=" * 50)
    print(f"✅ Server: Running")
    print(f"✅ Authentication: Working")
    print(f"{'✅' if chatbot_working else '❌'} Chatbot: {'Working' if chatbot_working else 'Failed'}")
    print(f"{'✅' if emotion_working else '❌'} Emotion Detection: {'Working' if emotion_working else 'Failed'}")
    
    if chatbot_working and emotion_working:
        print("\n🎉 ALL SYSTEMS WORKING!")
        print("🚀 Your AURA system is ready to use!")
    else:
        print("\n⚠️ Some issues found. Check server logs for details.")

if __name__ == "__main__":
    main()