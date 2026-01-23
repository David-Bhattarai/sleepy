#!/usr/bin/env python3

import base64
import json
from PIL import Image
import numpy as np
from io import BytesIO
from genuine_emotion_detector import get_genuine_emotion_detector

def create_test_image():
    """Create a simple test image with face-like features"""
    # Create a simple face-like pattern
    img = np.ones((200, 200, 3), dtype=np.uint8) * 128  # Gray background
    
    # Add simple face features
    # Eyes
    img[60:80, 60:80] = [0, 0, 0]  # Left eye
    img[60:80, 120:140] = [0, 0, 0]  # Right eye
    
    # Mouth (smile for happy emotion)
    img[140:150, 80:120] = [0, 0, 0]  # Mouth
    
    # Convert to PIL Image
    pil_img = Image.fromarray(img)
    
    # Convert to base64
    buffer = BytesIO()
    pil_img.save(buffer, format='JPEG')
    img_str = base64.b64encode(buffer.getvalue()).decode()
    
    return f"data:image/jpeg;base64,{img_str}"

def test_genuine_emotion_detector():
    """Test the genuine emotion detector directly"""
    print("🔄 Testing Genuine Emotion Detector...")
    
    try:
        # Get detector instance
        detector = get_genuine_emotion_detector()
        print(f"✅ Detector loaded: {detector.model is not None}")
        print(f"✅ Face detection available: {detector.face_cascade is not None}")
        print(f"✅ Supported emotions: {detector.emotions}")
        
        # Create test image
        test_image = create_test_image()
        
        # Test emotion detection
        print("\n🔄 Testing emotion detection...")
        result = detector.detect_emotion_from_image(test_image)
        
        print(f"\n📊 Detection Results:")
        print(f"Success: {result.get('success')}")
        print(f"Dominant emotion: {result.get('dominant_emotion')}")
        print(f"Confidence: {result.get('confidence'):.2f}%")
        print(f"Face detected: {result.get('face_detected')}")
        print(f"Model type: {result.get('model_type')}")
        
        if result.get('emotions'):
            print(f"\n🎭 Emotion breakdown:")
            for emotion, score in result['emotions'].items():
                print(f"  {emotion}: {score:.1f}%")
        
        if result.get('success'):
            print("\n✅ Genuine emotion detection is working!")
        else:
            print(f"\n❌ Detection failed: {result.get('error')}")
            
    except Exception as e:
        print(f"❌ Error testing detector: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_genuine_emotion_detector()