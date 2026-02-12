#!/usr/bin/env python3
"""
Test All Emotions Detection
Verify that detector can detect ALL 7 emotions, not just happy
"""

import os
import sys
import numpy as np
import cv2
import base64
from io import BytesIO
from PIL import Image

print("=" * 70)
print("TESTING ALL EMOTIONS DETECTION")
print("=" * 70)

# Add server to path
sys.path.insert(0, 'server')

# Import detector
try:
    from fer2013_emotion_detector import get_fer2013_emotion_detector
    print("OK Detector imported successfully")
except Exception as e:
    print(f"❌ Failed to import detector: {e}")
    sys.exit(1)

# Initialize detector
print("\n📊 Initializing detector...")
try:
    detector = get_fer2013_emotion_detector()
    print(f"✅ Detector initialized")
    print(f"   Available emotions: {detector.emotion_names}")
    print(f"   Model loaded: {detector.model is not None}")
except Exception as e:
    print(f"❌ Failed to initialize detector: {e}")
    sys.exit(1)

# Check if model is loaded
if detector.model is None:
    print("\n❌ ERROR: Model not loaded!")
    print("Please train a model first:")
    print("  python train_high_accuracy_fer2013.py")
    sys.exit(1)

print(f"\n✅ Model loaded successfully")
print(f"   Input shape: {detector.model.input_shape}")
print(f"   Output shape: {detector.model.output_shape}")

# Test with synthetic images for each emotion
print("\n" + "=" * 70)
print("🎯 TESTING EMOTION DETECTION")
print("=" * 70)

def create_test_image():
    """Create a simple test image (48x48 grayscale)"""
    # Create random grayscale image
    img = np.random.randint(0, 256, (48, 48), dtype=np.uint8)
    
    # Convert to PIL Image
    pil_img = Image.fromarray(img, mode='L')
    
    # Convert to base64
    buffered = BytesIO()
    pil_img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    
    return f"data:image/png;base64,{img_str}"

# Test multiple times to see variety of emotions
print("\n🔍 Running 20 test predictions...")
print("-" * 70)

emotion_counts = {emotion: 0 for emotion in detector.emotion_names}
all_results = []

for i in range(20):
    # Create test image
    test_image = create_test_image()
    
    # Detect emotion
    try:
        result = detector.detect_emotion_from_image(test_image)
        
        if result['success']:
            emotion = result['dominant_emotion']
            confidence = result['confidence']
            emotion_counts[emotion] += 1
            all_results.append(result)
            
            print(f"Test {i+1:2d}: {emotion:10s} ({confidence:5.2f}%)")
        else:
            print(f"Test {i+1:2d}: ❌ FAILED - {result.get('error', 'Unknown error')}")
            
    except Exception as e:
        print(f"Test {i+1:2d}: ❌ ERROR - {e}")

# Analyze results
print("\n" + "=" * 70)
print("📊 RESULTS ANALYSIS")
print("=" * 70)

print(f"\n✅ Completed {len(all_results)} successful predictions")

print(f"\n📈 Emotion Distribution:")
for emotion, count in sorted(emotion_counts.items(), key=lambda x: x[1], reverse=True):
    percentage = (count / len(all_results)) * 100 if len(all_results) > 0 else 0
    bar = "█" * int(percentage / 5)
    print(f"   {emotion:10s}: {count:2d} times ({percentage:5.1f}%) {bar}")

# Check if only detecting one emotion
unique_emotions = sum(1 for count in emotion_counts.values() if count > 0)
print(f"\n🎯 Unique emotions detected: {unique_emotions} out of 7")

if unique_emotions == 1:
    detected_emotion = [e for e, c in emotion_counts.items() if c > 0][0]
    print(f"\n❌ PROBLEM DETECTED!")
    print(f"   Only detecting: {detected_emotion}")
    print(f"   Expected: All 7 emotions should be possible")
    print(f"\n💡 Possible causes:")
    print(f"   1. Model not properly trained")
    print(f"   2. Model always predicts same emotion")
    print(f"   3. Preprocessing issue")
    print(f"\n🔧 Solutions:")
    print(f"   1. Retrain model: python train_high_accuracy_fer2013.py")
    print(f"   2. Check model file is not corrupted")
    print(f"   3. Verify dataset has all emotions")
elif unique_emotions < 4:
    print(f"\n⚠️ WARNING: Limited emotion variety")
    print(f"   Only {unique_emotions} emotions detected")
    print(f"   Model may need retraining for better diversity")
else:
    print(f"\n✅ GOOD: Model detects multiple emotions")
    print(f"   Variety is acceptable")

# Show sample prediction details
if len(all_results) > 0:
    print(f"\n📋 Sample Prediction Details:")
    sample = all_results[0]
    print(f"   Dominant: {sample['dominant_emotion']} ({sample['confidence']:.2f}%)")
    print(f"   All probabilities:")
    for emotion, prob in sorted(sample['emotions'].items(), key=lambda x: x[1], reverse=True):
        print(f"      {emotion:10s}: {prob:5.2f}%")

# Test with real face image if available
print("\n" + "=" * 70)
print("🖼️ TESTING WITH REAL IMAGES (if available)")
print("=" * 70)

test_image_paths = [
    'test_images/happy.jpg',
    'test_images/sad.jpg',
    'test_images/angry.jpg',
    'test_images/neutral.jpg'
]

real_image_tested = False
for img_path in test_image_paths:
    if os.path.exists(img_path):
        real_image_tested = True
        print(f"\n📸 Testing: {img_path}")
        
        try:
            # Read image
            img = cv2.imread(img_path)
            if img is None:
                print(f"   ❌ Could not read image")
                continue
            
            # Convert to base64
            _, buffer = cv2.imencode('.jpg', img)
            img_str = base64.b64encode(buffer).decode()
            img_data = f"data:image/jpeg;base64,{img_str}"
            
            # Detect emotion
            result = detector.detect_emotion_from_image(img_data)
            
            if result['success']:
                print(f"   ✅ Detected: {result['dominant_emotion']} ({result['confidence']:.2f}%)")
                print(f"   Top 3 emotions:")
                sorted_emotions = sorted(result['emotions'].items(), key=lambda x: x[1], reverse=True)
                for emotion, prob in sorted_emotions[:3]:
                    print(f"      {emotion:10s}: {prob:5.2f}%")
            else:
                print(f"   ❌ Detection failed: {result.get('error', 'Unknown')}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")

if not real_image_tested:
    print("\n💡 No test images found")
    print("   Create test_images/ folder with sample face images to test")

# Final verdict
print("\n" + "=" * 70)
print("🎯 FINAL VERDICT")
print("=" * 70)

if unique_emotions >= 5:
    print("\n✅ PASS: Detector can detect multiple emotions")
    print("   System is working properly")
elif unique_emotions >= 3:
    print("\n⚠️ PARTIAL: Detector detects some emotions")
    print("   May need model retraining for better variety")
elif unique_emotions == 1:
    print("\n❌ FAIL: Detector only detects ONE emotion")
    print("   Model needs retraining!")
    print("\n🔧 Action required:")
    print("   1. Run: python train_high_accuracy_fer2013.py")
    print("   2. Wait for training to complete (30-60 min)")
    print("   3. Run this test again")
else:
    print("\n❌ FAIL: Detector not working properly")
    print("   Please check model and configuration")

print("\n" + "=" * 70)
print("✅ Test complete!")
print("=" * 70)
