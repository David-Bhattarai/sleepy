#!/usr/bin/env python3

import requests
import base64
import json
from PIL import Image
import numpy as np
from io import BytesIO

def create_test_image():
    """Create a simple test image"""
    # Create a simple face-like pattern
    img = np.ones((200, 200, 3), dtype=np.uint8) * 128  # Gray background
    
    # Add simple face features
    # Eyes
    img[60:80, 60:80] = [0, 0, 0]  # Left eye
    img[60:80, 120:140] = [0, 0, 0]  # Right eye
    
    # Mouth (smile)
    img[140:150, 80:120] = [0, 0, 0]  # Mouth
    
    # Convert to PIL Image
    pil_img = Image.fromarray(img)
    
    # Convert to base64
    buffer = BytesIO()
    pil_img.save(buffer, format='JPEG')
    img_str = base64.b64encode(buffer.getvalue()).decode()
    
    return f"data:image/jpeg;base64,{img_str}"

def test_emotion_detection():
    """Test the emotion detection API"""
    print("🔄 Testing emotion detection API...")
    
    # Create test image
    test_image = create_test_image()
    
    # Test data
    test_data = {
        'image': test_image,
        'timestamp': '2024-01-22T21:10:00.000Z'
    }
    
    # Test headers (you'll need a valid token)
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer test-token-123'
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
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Emotion detection successful!")
            print(f"Dominant emotion: {result.get('dominant_emotion')}")
            print(f"Confidence: {result.get('confidence')}")
        else:
            print(f"❌ Error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Request failed: {e}")

if __name__ == "__main__":
    test_emotion_detection()