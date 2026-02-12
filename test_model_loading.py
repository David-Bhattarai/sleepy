#!/usr/bin/env python3
"""
Test Model Loading for Notebook
Yo script le notebook ma use hune model files check garcha
"""

import os
import json
import numpy as np

def check_model_files():
    """Check if model files exist and can be loaded"""
    print("🔍 CHECKING MODEL FILES")
    print("=" * 50)
    print()
    
    # Model paths to check
    model_paths = [
        'server/high_accuracy_emotion_model.h5',
        'high_accuracy_emotion_model.h5',
        'server/emotion_model.h5',
        'emotion_model.h5',
        'fer2013_emotion_model.h5',
        'server/fer2013_emotion_model.h5'
    ]
    
    found_models = []
    
    for path in model_paths:
        if os.path.exists(path):
            size = os.path.getsize(path) / (1024 * 1024)  # MB
            print(f"✅ Found: {path} ({size:.1f} MB)")
            found_models.append(path)
        else:
            print(f"❌ Missing: {path}")
    
    if not found_models:
        print("\n⚠️ No model files found!")
        print("💡 Train a model first using:")
        print("   python train_high_accuracy_fer2013.py")
        return None
    
    print(f"\n📊 Found {len(found_models)} model files")
    
    # Try to load TensorFlow and test model loading
    try:
        import tensorflow as tf
        print(f"✅ TensorFlow available: {tf.__version__}")
        
        # Test loading the first model
        test_model_path = found_models[0]
        print(f"\n🧪 Testing model loading: {test_model_path}")
        
        model = tf.keras.models.load_model(test_model_path, compile=False)
        print(f"✅ Model loaded successfully!")
        print(f"   Input shape: {model.input_shape}")
        print(f"   Output shape: {model.output_shape}")
        print(f"   Parameters: {model.count_params():,}")
        
        # Test prediction with dummy data
        dummy_input = np.random.random((1, 48, 48, 1)).astype('float32')
        prediction = model.predict(dummy_input, verbose=0)
        print(f"✅ Test prediction successful: {prediction.shape}")
        
        return test_model_path
        
    except ImportError:
        print("❌ TensorFlow not available")
        print("Install: pip install tensorflow")
        return None
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        return None

def check_metadata_files():
    """Check metadata files"""
    print("\n📄 CHECKING METADATA FILES")
    print("=" * 50)
    
    metadata_paths = [
        'server/emotion_detector_config.json',
        'server/fer2013_emotion_metadata.json',
        'high_accuracy_emotion_model_metadata.json'
    ]
    
    for path in metadata_paths:
        if os.path.exists(path):
            try:
                with open(path, 'r') as f:
                    data = json.load(f)
                print(f"✅ {path}")
                
                if 'accuracy' in data:
                    print(f"   Accuracy: {data['accuracy']}%")
                if 'test_accuracy' in data:
                    print(f"   Test Accuracy: {data['test_accuracy']*100:.2f}%")
                if 'dataset' in data:
                    print(f"   Dataset: {data['dataset']}")
                    
            except Exception as e:
                print(f"⚠️ {path}: Error reading - {e}")
        else:
            print(f"❌ Missing: {path}")

def check_dataset_files():
    """Check if dataset files exist"""
    print("\n📊 CHECKING DATASET FILES")
    print("=" * 50)
    
    dataset_paths = [
        'emotion_datasets/fer2013/fer2013_enhanced.csv',
        'fer2013_enhanced.csv',
        'fer2013.csv',
        '../emotion_datasets/fer2013/fer2013_enhanced.csv'
    ]
    
    found_datasets = []
    
    for path in dataset_paths:
        if os.path.exists(path):
            try:
                import pandas as pd
                df = pd.read_csv(path)
                size = len(df)
                print(f"✅ Found: {path} ({size:,} samples)")
                found_datasets.append(path)
            except Exception as e:
                print(f"⚠️ {path}: Error reading - {e}")
        else:
            print(f"❌ Missing: {path}")
    
    if not found_datasets:
        print("\n⚠️ No dataset files found!")
        print("💡 The notebook will use simulated data for demonstration")
    
    return found_datasets

def main():
    """Main check function"""
    print("🎯 MODEL AND DATA READINESS CHECK")
    print("=" * 60)
    print()
    
    # Check models
    model_path = check_model_files()
    
    # Check metadata
    check_metadata_files()
    
    # Check datasets
    dataset_paths = check_dataset_files()
    
    print("\n" + "=" * 60)
    print("📋 SUMMARY")
    print("=" * 60)
    
    if model_path:
        print("✅ Model: Ready for notebook")
        print(f"   Using: {model_path}")
    else:
        print("❌ Model: Not available")
        print("   Action: Train model first")
    
    if dataset_paths:
        print("✅ Dataset: Available for real testing")
        print(f"   Using: {dataset_paths[0]}")
    else:
        print("⚠️ Dataset: Not available")
        print("   Action: Notebook will use simulated data")
    
    print("\n💡 NEXT STEPS:")
    if model_path and dataset_paths:
        print("🎉 Everything ready! Run the notebook now.")
    elif model_path:
        print("⚠️ Model ready, but no dataset for real testing")
        print("   Notebook will work with simulated confusion matrix")
    else:
        print("🔧 Train model first: python train_high_accuracy_fer2013.py")
    
    print("=" * 60)

if __name__ == "__main__":
    main()