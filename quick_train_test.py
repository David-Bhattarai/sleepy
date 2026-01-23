#!/usr/bin/env python3
"""
Quick Training Test - Test if model training works
"""

import os
import sys

print("🧪 QUICK TRAINING TEST")
print("=" * 30)

# Test imports first
print("Testing imports...")

try:
    import numpy as np
    print("✅ NumPy")
except ImportError:
    print("❌ NumPy not available")
    sys.exit(1)

try:
    import pandas as pd
    print("✅ Pandas")
except ImportError:
    print("❌ Pandas not available")
    sys.exit(1)

try:
    import tensorflow as tf
    print(f"✅ TensorFlow {tf.__version__}")
except ImportError:
    print("❌ TensorFlow not available")
    sys.exit(1)

try:
    from sklearn.model_selection import train_test_split
    print("✅ Scikit-learn")
except ImportError:
    print("❌ Scikit-learn not available")
    sys.exit(1)

print("\n🎯 All imports successful!")
print("Ready to train model!")

print("\n💡 To train the model, run:")
print("python simple_model_trainer.py")

# Check if dataset exists
dataset_paths = [
    'emotion_datasets/fer2013/fer2013_enhanced.csv',
    'sleepy/emotion_datasets/fer2013/fer2013_enhanced.csv',
    'fer2013_enhanced.csv'
]

print(f"\n📊 Checking for dataset...")
dataset_found = False
for path in dataset_paths:
    if os.path.exists(path):
        print(f"✅ Dataset found: {path}")
        dataset_found = True
        break

if not dataset_found:
    print("⚠️ FER2013 dataset not found - will use sample data")
    print("This is fine for testing!")

print(f"\n🚀 Ready to train! Run: python simple_model_trainer.py")