#!/usr/bin/env python3

import requests
import base64
import json
from PIL import Image
import numpy as np
from io import BytesIO
import uuid

def create_test_user():
    """Create a test user for API testing"""
    print("🔄 Creating test user...")
    
    user_data = {
        'name': 'Test User',
        'email': 'test3@example.com',
        'password': 'testpass123'
    }
    
    try:
        response = requests.post(
            'http://127.0.0.1:5000/api/signup',
            headers={'Content-Type': 'application/json'},
            json=user_data,
            timeout=10
        )
        
        if response.status_code == 201:
            result = response.json()
            print(f"✅ Test user created: {result['userId']}")
            return result['userId']
        elif response.status_code == 409:
            # User already exists, try to sign in
            print("User already exists, signing in...")
            signin_response = requests.post(
                'http://127.0.0.1:5000/api/signin',
                headers={'Content-Type': 'application/json'},
                json={'email': user_data['email'], 'password': user_data['password']},
                timeout=10
            )
            if signin_response.status_code == 200:
                result = signin_response.json()
                print(f"✅ Signed in as existing user: {result['token']}")
                return result['token']
            else:
                print(f"❌ Signin failed: {signin_response.status_code} - {signin_response.text}")
                return None
        
        print(f"❌ Failed to create/signin user: {response.status_code} - {response.text}")
        return None
        
    except Exception as e:
        print(f"❌ Error creating user: {e}")
        return None

def create_test_image():
    """Create a simple test image with face-like features"""
    # Create a more realistic face pattern
    img = np.ones((400, 400, 3), dtype=np.uint8) * 200  # Light background
    
    # Face outline (oval)
    center_x, center_y = 200, 200
    for y in range(400):
        for x in range(400):
            # Create oval face shape
            dx = (x - center_x) / 120
            dy = (y - center_y) / 150
            if dx*dx + dy*dy < 1:
                img[y, x] = [220, 200, 180]  # Skin color
    
    # Eyes
    img[150:170, 160:180] = [0, 0, 0]  # Left eye
    img[150:170, 220:240] = [0, 0, 0]  # Right eye
    
    # Nose
    img[190:210, 195:205] = [180, 160, 140]  # Nose
    
    # Mouth (smile)
    for x in range(170, 230):
        y_offset = int(10 * np.sin((x - 170) * np.pi / 60))
        y = 250 + y_offset
        if 0 <= y < 400:
            img[y:y+5, x:x+2] = [100, 50, 50]  # Mouth
    
    # Convert to PIL Image
    pil_img = Image.fromarray(img)
    
    # Convert to base64
    buffer = BytesIO()
    pil_img.save(buffer, format='JPEG')
    img_str = base64.b64encode(buffer.getvalue()).decode()
    
    return f"data:image/jpeg;base64,{img_str}"

def test_emotion_detection_api(user_token):
    """Test the emotion detection API with a real user token"""
    print("🔄 Testing emotion detection API...")
    
    # Create test image
    test_image = create_test_image()
    
    # Test data
    test_data = {
        'image': test_image,
        'timestamp': '2024-01-22T21:15:00.000Z'
    }
    
    # Test headers with real user token
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {user_token}'
    }
    
    try:
        # Make request to local server
        response = requests.post(
            'http://127.0.0.1:5000/api/emotion_detection_advanced',
            headers=headers,
            json=test_data,
            timeout=30
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Emotion detection successful!")
            print(f"Dominant emotion: {result.get('dominant_emotion')}")
            print(f"Confidence: {result.get('confidence'):.2f}%")
            print(f"Face detected: {result.get('face_detected')}")
            print(f"Model type: {result.get('model_type')}")
            print(f"Saved to database: {result.get('saved')}")
            
            if result.get('emotions'):
                print(f"\n🎭 Emotion breakdown:")
                for emotion, score in result['emotions'].items():
                    print(f"  {emotion}: {score:.1f}%")
            
            return True
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 Starting Full Emotion Detection API Test")
    print("=" * 50)
    
    # Create test user
    user_token = create_test_user()
    if not user_token:
        print("❌ Cannot proceed without user token")
        return
    
    print(f"Using token: {user_token[:20]}...")
    print()
    
    # Test emotion detection
    success = test_emotion_detection_api(user_token)
    
    print()
    print("=" * 50)
    if success:
        print("✅ All tests passed! Emotion detection is working.")
    else:
        print("❌ Tests failed. Check the server logs for details.")

if __name__ == "__main__":
    main()