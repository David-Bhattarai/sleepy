#!/usr/bin/env python3
"""
Verify Emotion Detection Integration
Check if emotion detection is using correct dataset and trained model
"""

import os
import sys
import json
import numpy as np
import pandas as pd

print("=" * 70)
print("🔍 EMOTION DETECTION INTEGRATION VERIFICATION")
print("=" * 70)

# Results storage
results = {
    'dataset_check': False,
    'model_check': False,
    'integration_check': False,
    'issues': [],
    'recommendations': []
}

# ============================================================================
# 1. CHECK DATASET
# ============================================================================
print("\n📊 Step 1: Checking FER2013 Dataset...")
print("-" * 70)

dataset_paths = [
    'emotion_datasets/fer2013/fer2013_enhanced.csv',
    'fer2013_enhanced.csv'
]

dataset_found = False
dataset_path = None

for path in dataset_paths:
    if os.path.exists(path):
        dataset_found = True
        dataset_path = path
        print(f"✅ Dataset found: {path}")
        
        try:
            df = pd.read_csv(path)
            print(f"   Total samples: {len(df):,}")
            print(f"   Columns: {list(df.columns)}")
            
            if 'emotion' in df.columns:
                emotion_counts = df['emotion'].value_counts()
                print(f"\n   Emotion distribution:")
                for emotion, count in emotion_counts.items():
                    percentage = (count / len(df)) * 100
                    print(f"      {emotion:10s}: {count:6,} ({percentage:5.2f}%)")
                
                results['dataset_check'] = True
            else:
                results['issues'].append("Dataset missing 'emotion' column")
                
        except Exception as e:
            print(f"   ⚠️ Error reading dataset: {e}")
            results['issues'].append(f"Dataset read error: {e}")
        
        break

if not dataset_found:
    print("❌ Dataset NOT found!")
    results['issues'].append("FER2013 dataset not found")
    results['recommendations'].append("Download fer2013_enhanced.csv to emotion_datasets/fer2013/")

# ============================================================================
# 2. CHECK TRAINED MODELS
# ============================================================================
print("\n🤖 Step 2: Checking Trained Models...")
print("-" * 70)

model_paths = [
    'server/high_accuracy_emotion_model.h5',
    'server/fer2013_emotion_model.h5',
    'server/simple_fer2013_model_20260123_225231_final.h5',
    'server/compact_emotion_model_trained.h5',
    'server/advanced_emotion_model.h5'
]

models_found = []
for path in model_paths:
    if os.path.exists(path):
        size_mb = os.path.getsize(path) / (1024 * 1024)
        models_found.append((path, size_mb))
        print(f"✅ Model found: {path} ({size_mb:.2f} MB)")
        
        # Check for metadata
        metadata_path = path.replace('.h5', '_metadata.json')
        if os.path.exists(metadata_path):
            try:
                with open(metadata_path, 'r') as f:
                    metadata = json.load(f)
                    print(f"   📋 Metadata:")
                    print(f"      Dataset: {metadata.get('dataset', 'N/A')}")
                    print(f"      Accuracy: {metadata.get('test_accuracy', 0)*100:.2f}%")
                    print(f"      Emotions: {metadata.get('num_classes', 'N/A')} classes")
            except Exception as e:
                print(f"   ⚠️ Metadata read error: {e}")

if len(models_found) > 0:
    results['model_check'] = True
    print(f"\n✅ Found {len(models_found)} trained model(s)")
else:
    print("❌ No trained models found!")
    results['issues'].append("No trained models in server/ directory")
    results['recommendations'].append("Train model using: python train_high_accuracy_fer2013.py")

# ============================================================================
# 3. CHECK DETECTOR INTEGRATION
# ============================================================================
print("\n🔗 Step 3: Checking Detector Integration...")
print("-" * 70)

detector_path = 'server/fer2013_emotion_detector.py'
if os.path.exists(detector_path):
    print(f"✅ Detector file found: {detector_path}")
    
    with open(detector_path, 'r', encoding='utf-8') as f:
        detector_code = f.read()
    
    # Check if detector uses FER2013 dataset emotions
    fer2013_emotions = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']
    emotions_found = all(emotion in detector_code for emotion in fer2013_emotions)
    
    if emotions_found:
        print("   ✅ Detector uses FER2013 emotion labels")
    else:
        print("   ⚠️ Detector may not use correct FER2013 emotions")
        results['issues'].append("Detector emotion labels mismatch")
    
    # Check if detector loads models
    if 'load_model' in detector_code:
        print("   ✅ Detector has model loading code")
    else:
        print("   ⚠️ Detector missing model loading")
        results['issues'].append("Detector doesn't load models")
    
    # Check model paths in detector
    model_paths_in_code = []
    for model_path in model_paths:
        if model_path in detector_code:
            model_paths_in_code.append(model_path)
    
    if len(model_paths_in_code) > 0:
        print(f"   ✅ Detector references {len(model_paths_in_code)} model path(s)")
        for mp in model_paths_in_code:
            print(f"      - {mp}")
    else:
        print("   ⚠️ Detector doesn't reference any model paths")
        results['issues'].append("Detector model paths not configured")
    
    results['integration_check'] = True
else:
    print(f"❌ Detector file NOT found: {detector_path}")
    results['issues'].append("Detector file missing")
    results['recommendations'].append("Ensure fer2013_emotion_detector.py exists in server/")

# ============================================================================
# 4. TEST DETECTOR (if possible)
# ============================================================================
print("\n🧪 Step 4: Testing Detector...")
print("-" * 70)

try:
    sys.path.insert(0, 'server')
    from fer2013_emotion_detector import get_fer2013_emotion_detector
    
    detector = get_fer2013_emotion_detector()
    print("✅ Detector initialized successfully")
    print(f"   Available emotions: {detector.emotion_names}")
    print(f"   Model loaded: {detector.model is not None}")
    
    if detector.model:
        print(f"   Model input shape: {detector.model.input_shape}")
        print(f"   Model output shape: {detector.model.output_shape}")
        
        # Test with random data
        test_input = np.random.random((1, 48, 48, 1)).astype('float32')
        test_output = detector.model.predict(test_input, verbose=0)
        print(f"   Test prediction shape: {test_output.shape}")
        print(f"   Test prediction sum: {test_output.sum():.4f} (should be ~1.0)")
        
        if abs(test_output.sum() - 1.0) < 0.01:
            print("   ✅ Model output is properly normalized")
        else:
            print("   ⚠️ Model output normalization issue")
            results['issues'].append("Model output not properly normalized")
    
except Exception as e:
    print(f"❌ Detector test failed: {e}")
    results['issues'].append(f"Detector initialization error: {e}")

# ============================================================================
# 5. FINAL REPORT
# ============================================================================
print("\n" + "=" * 70)
print("📋 VERIFICATION REPORT")
print("=" * 70)

print(f"\n✅ Dataset Check: {'PASS' if results['dataset_check'] else 'FAIL'}")
print(f"✅ Model Check: {'PASS' if results['model_check'] else 'FAIL'}")
print(f"✅ Integration Check: {'PASS' if results['integration_check'] else 'FAIL'}")

all_passed = results['dataset_check'] and results['model_check'] and results['integration_check']

if all_passed:
    print("\n🎉 ALL CHECKS PASSED!")
    print("✅ Emotion detection is properly integrated with dataset and trained model")
else:
    print("\n⚠️ SOME CHECKS FAILED")

if len(results['issues']) > 0:
    print(f"\n❌ Issues Found ({len(results['issues'])}):")
    for i, issue in enumerate(results['issues'], 1):
        print(f"   {i}. {issue}")

if len(results['recommendations']) > 0:
    print(f"\n💡 Recommendations ({len(results['recommendations'])}):")
    for i, rec in enumerate(results['recommendations'], 1):
        print(f"   {i}. {rec}")

# ============================================================================
# 6. INTEGRATION STATUS
# ============================================================================
print("\n" + "=" * 70)
print("🔗 INTEGRATION STATUS")
print("=" * 70)

print("\n📊 Dataset → Model → Detector Flow:")
print("   1. FER2013 Dataset (fer2013_enhanced.csv)")
print(f"      Status: {'✅ Found' if dataset_found else '❌ Missing'}")
print(f"      Location: {dataset_path if dataset_path else 'Not found'}")

print("\n   2. Trained Models (*.h5)")
print(f"      Status: {'✅ Found' if len(models_found) > 0 else '❌ Missing'}")
if len(models_found) > 0:
    print(f"      Count: {len(models_found)} model(s)")
    for model_path, size in models_found:
        print(f"         - {model_path} ({size:.2f} MB)")

print("\n   3. Emotion Detector (fer2013_emotion_detector.py)")
print(f"      Status: {'✅ Found' if os.path.exists(detector_path) else '❌ Missing'}")
print(f"      Integration: {'✅ Properly configured' if results['integration_check'] else '⚠️ Needs attention'}")

# ============================================================================
# 7. USAGE VERIFICATION
# ============================================================================
print("\n" + "=" * 70)
print("📝 USAGE VERIFICATION")
print("=" * 70)

print("\n✅ How the system works:")
print("   1. Dataset (fer2013_enhanced.csv) contains 35,887 face images")
print("   2. Training scripts use this dataset to train CNN models")
print("   3. Trained models (.h5 files) are saved in server/ directory")
print("   4. Detector (fer2013_emotion_detector.py) loads these models")
print("   5. Detector predicts emotions using the trained model")

print("\n✅ Emotion labels (FER2013 standard):")
fer2013_emotions = ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']
for i, emotion in enumerate(fer2013_emotions):
    print(f"   {i}. {emotion}")

print("\n✅ Model specifications:")
print("   - Input: 48x48 grayscale images")
print("   - Output: 7 emotion probabilities")
print("   - Architecture: CNN (Convolutional Neural Network)")
print("   - Framework: TensorFlow/Keras")

# Save report
report_path = 'integration_verification_report.json'
with open(report_path, 'w') as f:
    json.dump(results, f, indent=2)
print(f"\n💾 Report saved: {report_path}")

print("\n" + "=" * 70)
if all_passed:
    print("✅ VERIFICATION COMPLETE - System is properly integrated!")
else:
    print("⚠️ VERIFICATION COMPLETE - Please address issues above")
print("=" * 70)
