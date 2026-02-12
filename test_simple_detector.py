#!/usr/bin/env python3
"""
Test Simple Emotion Detector
Works WITHOUT TensorFlow!
"""

import sys
import os

print("=" * 70)
print("TESTING SIMPLE EMOTION DETECTOR (NO TENSORFLOW)")
print("=" * 70)

# Add server to path
sys.path.insert(0, 'server')

# Import simple detector
try:
    from simple_emotion_detector import get_simple_emotion_detector
    print("\nOK Simple detector imported")
except Exception as e:
    print(f"\nERROR importing: {e}")
    sys.exit(1)

# Initialize
try:
    detector = get_simple_emotion_detector()
    print("OK Detector initialized")
    print(f"   Emotions: {detector.emotions}")
except Exception as e:
    print(f"ERROR initializing: {e}")
    sys.exit(1)

# Test with random images
print("\n" + "=" * 70)
print("TESTING WITH RANDOM IMAGES")
print("=" * 70)

import numpy as np
import cv2
import base64
from io import BytesIO

def create_test_image():
    """Create random test image"""
    img = np.random.randint(0, 256, (200, 200, 3), dtype=np.uint8)
    _, buffer = cv2.imencode('.jpg', img)
    img_str = base64.b64encode(buffer).decode()
    return f"data:image/jpeg;base64,{img_str}"

emotion_counts = {e: 0 for e in detector.emotions}

print("\nRunning 20 tests...")
for i in range(20):
    test_img = create_test_image()
    
    try:
        result = detector.detect_emotion_from_image(test_img)
        
        if result['success']:
            emotion = result['dominant_emotion']
            confidence = result['confidence']
            emotion_counts[emotion] += 1
            print(f"  Test {i+1:2d}: {emotion:10s} ({confidence:5.2f}%)")
        else:
            print(f"  Test {i+1:2d}: FAILED - {result.get('error')}")
    except Exception as e:
        print(f"  Test {i+1:2d}: ERROR - {e}")

# Results
print("\n" + "=" * 70)
print("RESULTS")
print("=" * 70)

print("\nEmotion Distribution:")
for emotion, count in sorted(emotion_counts.items(), key=lambda x: x[1], reverse=True):
    percentage = (count / 20) * 100
    bar = "#" * int(percentage / 5)
    print(f"  {emotion:10s}: {count:2d} times ({percentage:5.1f}%) {bar}")

unique = sum(1 for c in emotion_counts.values() if c > 0)
print(f"\nUnique emotions: {unique} out of 7")

if unique >= 5:
    print("\nGOOD: Detector shows variety!")
    print("Multiple emotions detected")
elif unique == 1:
    print("\nPROBLEM: Only one emotion!")
else:
    print(f"\nOK: {unique} emotions detected")

print("\n" + "=" * 70)
print("TEST COMPLETE")
print("=" * 70)
print("\nNOTE: This detector works WITHOUT TensorFlow!")
print("It uses OpenCV face analysis instead of deep learning.")
