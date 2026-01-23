#!/usr/bin/env python3
"""
Test Real Human Face Emotion Detection
Test the system with realistic human face images
"""

import os
import base64
import requests
import json

def test_real_face_emotion_detection():
    """Test emotion detection with real human face images"""
    
    print("👤 Testing Real Human Face Emotion Detection...")
    
    # Test server URL
    base_url = 'http://localhost:5000'
    
    # Test with created face images
    test_faces_dir = 'test_human_faces'
    
    if not os.path.exists(test_faces_dir):
        print("❌ Test faces directory not found. Run create_real_face_emotion_test.py first.")
        return
    
    # Get auth token (you'll need to login first)
    token = input("Enter your auth token (or press Enter to skip): ").strip()
    if not token:
        token = 'test-token'  # Default for testing
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    emotions = ['happy', 'sad', 'angry', 'fear', 'surprise', 'disgust', 'neutral']
    
    print("\n🧪 Testing each emotion...")
    
    for emotion in emotions:
        emotion_dir = os.path.join(test_faces_dir, emotion)
        
        if not os.path.exists(emotion_dir):
            continue
        
        print(f"\n📸 Testing {emotion.upper()} faces...")
        
        # Test each face image in the emotion directory
        for filename in os.listdir(emotion_dir):
            if filename.endswith('.png'):
                filepath = os.path.join(emotion_dir, filename)
                
                try:
                    # Read and encode image
                    with open(filepath, 'rb') as f:
                        image_bytes = f.read()
                    
                    image_data = base64.b64encode(image_bytes).decode('utf-8')
                    image_data = f"data:image/png;base64,{image_data}"
                    
                    # Send to emotion detection API
                    response = requests.post(f'{base_url}/api/emotion_detection_fer2013', 
                                           json={'image': image_data}, 
                                           headers=headers)
                    
                    if response.status_code == 200:
                        result = response.json()
                        detected_emotion = result.get('dominant_emotion', 'unknown')
                        confidence = result.get('confidence', 0)
                        
                        # Check if detection matches expected emotion
                        is_correct = detected_emotion.lower() == emotion.lower()
                        status = "✅ CORRECT" if is_correct else "❌ INCORRECT"
                        
                        print(f"  {filename}: {status}")
                        print(f"    Expected: {emotion}")
                        print(f"    Detected: {detected_emotion} ({confidence:.1f}%)")
                        
                        if not is_correct:
                            print(f"    ⚠️  Detection mismatch!")
                    
                    else:
                        error = response.json() if response.headers.get('content-type') == 'application/json' else response.text
                        print(f"  {filename}: ❌ API Error - {error}")
                
                except Exception as e:
                    print(f"  {filename}: ❌ Error - {e}")
    
    print("\n✅ Real face emotion detection test completed!")
    print("\n💡 Tips for better results:")
    print("- Use clear, well-lit face images")
    print("- Ensure face is centered and visible")
    print("- Try different angles and expressions")
    print("- Check that the server is running")

def test_face_detection_only():
    """Test just the face detection part"""
    
    print("\n👤 Testing Face Detection Only...")
    
    test_faces_dir = 'test_human_faces'
    
    if not os.path.exists(test_faces_dir):
        print("❌ Test faces directory not found")
        return
    
    try:
        # Import face detection
        import cv2
        import numpy as np
        
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        for emotion in ['happy', 'sad', 'angry']:
            emotion_dir = os.path.join(test_faces_dir, emotion)
            
            if os.path.exists(emotion_dir):
                for filename in os.listdir(emotion_dir):
                    if filename.endswith('.png'):
                        filepath = os.path.join(emotion_dir, filename)
                        
                        # Load image
                        img = cv2.imread(filepath)
                        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                        
                        # Detect faces
                        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
                        
                        if len(faces) > 0:
                            print(f"✅ {filename}: Found {len(faces)} face(s)")
                        else:
                            print(f"❌ {filename}: No face detected")
    
    except ImportError:
        print("⚠️ OpenCV not available for face detection test")
    except Exception as e:
        print(f"❌ Face detection test error: {e}")

if __name__ == '__main__':
    print("Choose test option:")
    print("1. Test emotion detection with face images")
    print("2. Test face detection only")
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == '1':
        test_real_face_emotion_detection()
    elif choice == '2':
        test_face_detection_only()
    else:
        print("Invalid choice. Running both tests...")
        test_face_detection_only()
        test_real_face_emotion_detection()
