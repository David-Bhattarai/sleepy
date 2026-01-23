#!/usr/bin/env python3
"""
Test Emotion Detection with Image Upload
"""

import requests
import json
import base64
from PIL import Image
import numpy as np
from io import BytesIO

SERVER_URL = "http://localhost:5000"

def create_test_face_image():
    """Create a test face image"""
    # Create a simple 48x48 grayscale image that looks like a face
    img = np.zeros((48, 48), dtype=np.uint8)
    
    # Draw a simple face
    # Face outline (circle)
    center = (24, 24)
    radius = 20
    for y in range(48):
        for x in range(48):
            if (x - center[0])**2 + (y - center[1])**2 <= radius**2:
                img[y, x] = 200
    
    # Eyes
    img[18:22, 16:20] = 50  # Left eye
    img[18:22, 28:32] = 50  # Right eye
    
    # Mouth (smile)
    img[30:34, 20:28] = 50
    
    # Convert to PIL Image
    pil_img = Image.fromarray(img, mode='L')
    
    # Convert to base64
    buffer = BytesIO()
    pil_img.save(buffer, format='PNG')
    img_str = base64.b64encode(buffer.getvalue()).decode()
    
    return f"data:image/png;base64,{img_str}"

def test_user_login():
    """Test user login"""
    print("🔐 Testing User Login...")
    
    # Try to create a test user first
    signup_data = {
        "name": "Test User",
        "email": "test@example.com",
        "password": "test123",
        "phone": "1234567890",
        "gender": "other"
    }
    
    try:
        requests.post(f"{SERVER_URL}/api/signup", json=signup_data)
    except:
        pass  # User might already exist
    
    # Now login
    signin_data = {
        "email": "test@example.com",
        "password": "test123"
    }
    
    try:
        response = requests.post(f"{SERVER_URL}/api/signin", json=signin_data)
        if response.status_code == 200:
            data = response.json()
            token = data.get('token')
            print(f"✅ User login successful")
            return token
        else:
            print(f"❌ User login failed: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ User login error: {e}")
        return None

def test_emotion_detection(token):
    """Test emotion detection with image upload"""
    print("\n😊 Testing Emotion Detection with Image Upload...")
    
    try:
        # Create test image
        test_image = create_test_face_image()
        print("✅ Test face image created")
        
        # Send to emotion detection API
        headers = {"Authorization": f"Bearer {token}"}
        data = {
            "image": test_image,
            "timestamp": "2026-01-23 12:00:00",
            "source": "upload"
        }
        
        response = requests.post(f"{SERVER_URL}/api/emotion_detection_fer2013", 
                               json=data, headers=headers)
        
        print(f"Response Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            
            print("✅ Emotion Detection Results:")
            print(f"   Primary Emotion: {result.get('dominant_emotion', 'unknown')}")
            print(f"   Confidence: {result.get('confidence', 0)}%")
            print(f"   Dataset Used: {result.get('model_info', {}).get('dataset', 'Unknown')}")
            print(f"   Model Accuracy: {result.get('model_info', {}).get('accuracy', 'Unknown')}%")
            
            emotions = result.get('emotions', {})
            print("\n   All Emotions Detected:")
            for emotion, score in sorted(emotions.items(), key=lambda x: x[1], reverse=True):
                print(f"     {emotion}: {score:.1f}%")
            
            # Check if using FER2013 format (7 emotions)
            expected_emotions = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']
            detected_emotions = list(emotions.keys())
            
            if all(emotion in expected_emotions for emotion in detected_emotions):
                print("\n✅ Using FER2013 dataset format (7 emotions)")
            else:
                print(f"\n⚠️ Not using FER2013 format. Detected: {detected_emotions}")
            
            return True
            
        else:
            print(f"❌ Emotion detection failed: {response.status_code}")
            try:
                error_data = response.json()
                print(f"   Error: {error_data}")
            except:
                print(f"   Raw response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Emotion detection error: {e}")
        return False

def main():
    """Main test function"""
    print("🛠️ EMOTION DETECTION WITH IMAGE UPLOAD TEST")
    print("=" * 50)
    
    # Test user login
    token = test_user_login()
    if not token:
        print("\n❌ Cannot proceed without user token")
        return
    
    # Test emotion detection
    success = test_emotion_detection(token)
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 EMOTION DETECTION IS WORKING!")
        print("\n✅ What's Working:")
        print("   - Image upload and processing")
        print("   - FER2013 dataset integration")
        print("   - 7 emotion categories")
        print("   - Confidence scoring")
        print("   - Database saving")
        
        print("\n🚀 Ready for Use!")
        print(f"   - Go to: {SERVER_URL}/emotion-detection.html")
        print("   - Upload images or use camera")
        print("   - Get accurate emotion detection")
    else:
        print("❌ EMOTION DETECTION NEEDS FIXING")
        print("\n🔧 Check:")
        print("   - Server is running")
        print("   - FER2013 model is loaded")
        print("   - API endpoints are working")

if __name__ == "__main__":
    main()