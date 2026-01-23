#!/usr/bin/env python3
"""
Cell 1: Import Libraries - Test all required imports
"""

print("📦 Cell 1: Testing all imports...")

import warnings
warnings.filterwarnings('ignore')

# Test each import individually
imports_status = {}

# Core libraries
try:
    import os
    import sys
    imports_status['os, sys'] = True
    print("✅ os, sys")
except ImportError as e:
    imports_status['os, sys'] = False
    print(f"❌ os, sys: {e}")

# NumPy
try:
    import numpy as np
    imports_status['numpy'] = True
    print(f"✅ NumPy {np.__version__}")
except ImportError as e:
    imports_status['numpy'] = False
    print(f"❌ NumPy: {e}")
    print("🔧 Fix: pip install numpy")

# Pandas
try:
    import pandas as pd
    imports_status['pandas'] = True
    print(f"✅ Pandas {pd.__version__}")
except ImportError as e:
    imports_status['pandas'] = False
    print(f"❌ Pandas: {e}")
    print("🔧 Fix: pip install pandas")

# Computer Vision
try:
    import cv2
    imports_status['opencv'] = True
    print(f"✅ OpenCV {cv2.__version__}")
except ImportError:
    imports_status['opencv'] = False
    print("⚠️ OpenCV not available")
    print("🔧 Fix: pip install opencv-python")

# Deep Learning
try:
    import tensorflow as tf
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import Conv2D, MaxPooling2D, Dense, Dropout, Flatten, BatchNormalization
    from tensorflow.keras.optimizers import Adam
    from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
    from tensorflow.keras.utils import to_categorical
    imports_status['tensorflow'] = True
    print(f"✅ TensorFlow {tf.__version__}")
except ImportError as e:
    imports_status['tensorflow'] = False
    print(f"❌ TensorFlow: {e}")
    print("🔧 Fix: pip install tensorflow")

# Machine Learning
try:
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import classification_report, confusion_matrix
    imports_status['sklearn'] = True
    print("✅ Scikit-learn")
except ImportError as e:
    imports_status['sklearn'] = False
    print(f"❌ Scikit-learn: {e}")
    print("🔧 Fix: pip install scikit-learn")

# Visualization
try:
    import matplotlib.pyplot as plt
    import seaborn as sns
    plt.style.use('default')
    imports_status['matplotlib'] = True
    print("✅ Matplotlib, Seaborn")
except ImportError as e:
    imports_status['matplotlib'] = False
    print(f"❌ Matplotlib/Seaborn: {e}")
    print("🔧 Fix: pip install matplotlib seaborn")

# Utilities
try:
    import pickle
    import json
    from datetime import datetime
    import logging
    imports_status['utilities'] = True
    print("✅ Utilities (pickle, json, datetime, logging)")
except ImportError as e:
    imports_status['utilities'] = False
    print(f"❌ Utilities: {e}")

# PIL
try:
    from PIL import Image
    imports_status['pil'] = True
    print("✅ PIL/Pillow")
except ImportError as e:
    imports_status['pil'] = False
    print(f"❌ PIL: {e}")
    print("🔧 Fix: pip install pillow")

# Summary
print(f"\n📊 Import Summary:")
success_count = sum(imports_status.values())
total_count = len(imports_status)

print(f"✅ Successful: {success_count}/{total_count}")
print(f"❌ Failed: {total_count - success_count}/{total_count}")

if success_count == total_count:
    print("\n🎉 ALL IMPORTS SUCCESSFUL!")
    print("✅ Ready for next cell")
else:
    print(f"\n⚠️ Some imports failed. Install missing packages:")
    failed_packages = []
    if not imports_status.get('numpy', True):
        failed_packages.append('numpy')
    if not imports_status.get('pandas', True):
        failed_packages.append('pandas')
    if not imports_status.get('tensorflow', True):
        failed_packages.append('tensorflow')
    if not imports_status.get('sklearn', True):
        failed_packages.append('scikit-learn')
    if not imports_status.get('opencv', True):
        failed_packages.append('opencv-python')
    if not imports_status.get('matplotlib', True):
        failed_packages.extend(['matplotlib', 'seaborn'])
    if not imports_status.get('pil', True):
        failed_packages.append('pillow')
    
    if failed_packages:
        print(f"🔧 Run: pip install {' '.join(failed_packages)}")

# GPU Check
if imports_status.get('tensorflow', False):
    try:
        gpus = tf.config.list_physical_devices('GPU')
        if gpus:
            print(f"\n🖥️ GPU Available: {len(gpus)} device(s)")
        else:
            print(f"\n⚠️ No GPU detected, using CPU")
    except:
        print(f"\n⚠️ Could not check GPU status")

print(f"\n✅ Cell 1 completed!")