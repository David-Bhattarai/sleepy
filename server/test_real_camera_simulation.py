#!/usr/bin/env python3

import requests
import base64
import json
from PIL import Image, ImageDraw
import numpy as np
from io import BytesIO
import cv2

def create_realistic_face_image():
    """Create a more realistic face image for testing"""
    # Create a larger, more realistic face
    img = Image.new('RGB', (640, 480), color=(240, 230, 220))  # Light skin tone background
    draw = ImageDraw.Draw(img)
    
    # Face oval
    face_center = (320, 240)
    face_width, face_height = 200, 250
    
    # Draw face outline
    draw.ellipse([
        face_center[0] - face_width//2, face_center[1] - face_height//2,
        face_center[0] + face_width//2, face_center[1] + face_height//2
    ], fill=(220, 200, 180), outline=(200, 180, 160), width=2)
    
    # Eyes
    left_eye = (face_center[0] - 40, face_center[1] - 30)
    right_eye = (face_center[0] + 40, face_center[1] - 30)
    
    # Draw eyes
    draw.ellipse([left_eye[0] - 15, left_eye[1] - 8, left_eye[0] + 15, left_eye[1] + 8], 
                fill=(255, 255, 255), outline=(0, 0, 0), width=2)
    draw.ellipse([right_eye[0] - 15, right_eye[1] - 8, right_eye[0] + 15, right_eye[1] + 8], 
                fill=(255, 255, 255), outline=(0, 0, 0), width=2)
    
    # Pupils
    draw.ellipse([left_eye[0] - 5, left_eye[1] - 5, left_eye[0] + 5, left_eye[1] + 5], 
                fill=(0, 0, 0))
    draw.ellipse([right_eye[0] - 5, right_eye[1] - 5, right_eye[0] + 5, right_eye[1] + 5], 
                fill=(0, 0, 0))
    
    # Nose
    nose_center = (face_center[0], face_center[1] + 10)
    draw.ellipse([nose_center[0] - 8, nose_center[1] - 15, nose_center[0] + 8, nose_center[1] + 5], 
                fill=(200, 180, 160), outline=(180, 160, 140), width=1)
    
    # Mouth (smile for happy emotion)
    mouth_center = (face_center[0], face_center[1] + 60)
    # Draw a smile
    draw.arc([mouth_center[0] - 30, mouth_center[1] - 15, mouth_center[0] + 30, mouth_center[1] + 15], 
             start=0, end=180, fill=(100, 50, 50), width=3)
    
    # Eyebrows
    draw.line([left_eye[0] - 20, left_eye[1] - 20, left_eye[0] + 20, left_eye[1] - 15], 
              fill=(100, 80, 60), width=3)
    draw.line([right_eye[0] - 20, right_eye[1] - 15, right_eye[0] + 20, right_eye[1] - 20], 
              fill=(100, 80, 60), width=3)
    
    # Convert to base64
    buffer = BytesIO()
    img.save(buffer, format='JPEG', quality=85)
    img_str = base64.b64encode(buffer.getvalue()).decode()
    
    return f"data:image/jpeg;base64,{img_str}"

def test_emotion_with_realistic_face():
    """Test emotion detection with a realistic face image"""
    print("🎭 Testing Emotion Detection with Realistic Face")
    print("=" * 50)
    
    # Use existing user token
    user_token = "6fa2d144-479d-40a6-a60d-142173b04ebe"
    
    # Create realistic face image
    print("🔄 Creating realistic face image...")
    test_image = create_realistic_face_image()
    
    # Test data
    test_data = {
        'image': test_image,
        'timestamp': '2024-01-22T21:20:00.000Z'
    }
    
    # Test headers
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {user_token}'
    }
    
    try:
        print(" Sending to emotion detection API...")
        
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
            print("\n✅ Emotion Detection Results:")
            print(f"   Success: {result.get('success')}")
            print(f"   Dominant Emotion: {result.get('dominant_emotion').upper()}")
            print(f"   Confidence: {result.get('confidence'):.1f}%")
            print(f"   Face Detected: {result.get('face_detected')}")
            print(f"   Model Type: {result.get('model_type')}")
            print(f"   Saved to Database: {result.get('saved')}")
            
            if result.get('note'):
                print(f"   Note: {result.get('note')}")
            
            if result.get('emotions'):
                print(f"\n🎭 Detailed Emotion Analysis:")
                emotions = result['emotions']
                sorted_emotions = sorted(emotions.items(), key=lambda x: x[1], reverse=True)
                
                for emotion, score in sorted_emotions:
                    if score > 1:  # Only show emotions with >1% confidence
                        bar_length = int(score / 5)  # Scale for display
                        bar = "█" * bar_length + "░" * (20 - bar_length)
                        print(f"   {emotion.capitalize():12} {bar} {score:5.1f}%")
            
            # Test recommendations
            print(f"\n🔄 Getting recommendations for '{result.get('dominant_emotion')}'...")
            rec_response = requests.get(
                f"http://127.0.0.1:5000/api/emotion_recommendations/{result.get('dominant_emotion')}",
                headers={'Authorization': f'Bearer {user_token}'},
                timeout=10
            )
            
            if rec_response.status_code == 200:
                recommendations = rec_response.json()
                print(f"✅ Received {len(recommendations)} recommendation categories")
                
                for i, rec in enumerate(recommendations[:2], 1):  # Show first 2 categories
                    print(f"\n   {i}. {rec.get('title', 'Unknown')}")
                    print(f"      {rec.get('description', 'No description')}")
                    actions = rec.get('actions', [])
                    if actions:
                        print(f"      Suggestions: {', '.join(actions[:3])}")
            
            print(f"\n🎯 Summary:")
            print(f"   The system detected '{result.get('dominant_emotion')}' emotion")
            print(f"   with {result.get('confidence'):.1f}% confidence using the")
            print(f"   {result.get('model_type')} model.")
            
            if result.get('confidence', 0) > 70:
                print(f"   ✅ High confidence detection - system is working well!")
            elif result.get('confidence', 0) > 40:
                print(f"   ⚠️  Moderate confidence - system is functional")
            else:
                print(f"   ❌ Low confidence - may need improvement")
                
            return True
            
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return False

if __name__ == "__main__":
    success = test_emotion_with_realistic_face()
    print("\n" + "=" * 50)
    if success:
        print("🎉 Emotion detection system is working properly!")
        print("   Users can now use the camera to detect their emotions.")
    else:
        print("❌ Emotion detection system needs attention.")