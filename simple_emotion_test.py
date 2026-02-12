#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple Emotion Detection Test
Test if detector can detect all 7 emotions
"""

import os
import sys

print("=" * 70)
print("TESTING ALL EMOTIONS DETECTION")
print("=" * 70)

# Check if model exists
model_paths = [
    'server/fer2013_emotion_model.h5',
    'server/simple_fer2013_model_20260123_225231_final.h5',
    'server/compact_emotion_model_trained.h5'
]

model_found = False
for path in model_paths:
    if os.path.exists(path):
        print(f"\nOK Model found: {path}")
        model_found = True
        break

if not model_found:
    print("\nERROR: No model found!")
    print("Please train a model first:")
    print("  python train_high_accuracy_fer2013.py")
    sys.exit(1)

# Try to load detector
print("\nLoading detector...")
sys.path.insert(0, 'server')

try:
    from fer2013_emotion_detector import get_fer2013_emotion_detector
    print("OK Detector module imported")
except Exception as e:
    print(f"ERROR importing detector: {e}")
    sys.exit(1)

# Initialize detector
try:
    detector = get_fer2013_emotion_detector()
    print("OK Detector initialized")
except Exception as e:
    print(f"ERROR initializing detector: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Check model
if detector.model is None:
    print("\nERROR: Model not loaded in detector!")
    print("Detector initialized but model is None")
    sys.exit(1)

print(f"OK Model loaded in detector")
print(f"   Emotions: {detector.emotion_names}")

# Test with random data
print("\n" + "=" * 70)
print("TESTING WITH RANDOM DATA")
print("=" * 70)

import numpy as np

emotion_counts = {e: 0 for e in detector.emotion_names}

print("\nRunning 20 predictions with random data...")

for i in range(20):
    # Create random input
    random_input = np.random.random((1, 48, 48, 1)).astype('float32')
    
    try:
        # Predict
        predictions = detector.model.predict(random_input, verbose=0)
        probs = predictions[0]
        
        # Get dominant emotion
        idx = np.argmax(probs)
        emotion = detector.emotion_labels[idx]
        confidence = probs[idx] * 100
        
        emotion_counts[emotion] += 1
        print(f"  Test {i+1:2d}: {emotion:10s} ({confidence:5.2f}%)")
        
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

# Check variety
unique_emotions = sum(1 for c in emotion_counts.values() if c > 0)
print(f"\nUnique emotions detected: {unique_emotions} out of 7")

if unique_emotions == 1:
    detected = [e for e, c in emotion_counts.items() if c > 0][0]
    print(f"\nPROBLEM: Only detecting '{detected}'!")
    print("Model may not be properly trained")
    print("\nSolution:")
    print("  1. Train new model: python train_high_accuracy_fer2013.py")
    print("  2. Wait 30-60 minutes")
    print("  3. Test again")
elif unique_emotions < 4:
    print(f"\nWARNING: Limited variety ({unique_emotions} emotions)")
    print("Model may need retraining")
else:
    print(f"\nGOOD: Model detects {unique_emotions} different emotions")
    print("Variety is acceptable")

print("\n" + "=" * 70)
print("TEST COMPLETE")
print("=" * 70)
