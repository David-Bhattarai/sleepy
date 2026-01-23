#!/usr/bin/env python3
"""
Cell 1: Import Libraries (Error-Free Version)
"""

print("📦 Cell 1: Importing libraries with error handling...")

import warnings
warnings.filterwarnings('ignore')

# Initialize status tracking
import_status = {}

# Core libraries
try:
    import os
    import sys
    import_status['core'] = True
    print("✅ Core libraries (os, sys)")
except ImportError as e:
    import_status['core'] = False
    print(f"❌ Core libraries failed: {e}")

# NumPy
try:
    import numpy as np
    import_status['numpy'] = True
    print(f"✅ NumPy {np.__version__}")
except ImportError as e:
    import_status['numpy'] = False
    print(f"❌ NumPy failed: {e}")
    print("🔧 Fix: pip install numpy")

# Pandas
try:
    import pandas as pd
    import_status['pandas'] = True
    print(f"✅ Pandas {pd.__version__}")
except ImportError as e:
    import_status['pandas'] = False
    print(f"❌ Pandas failed: {e}")
    print("🔧 Fix: pip install pandas")

# Computer Vision (with fallback)
try:
    import cv2
    import_status['cv2'] = True
    print(f"✅ OpenCV {cv2.__version__}")
except ImportError:
    import_status['cv2'] = False
    print("⚠️ OpenCV not available, will use PIL fallback")
    cv2 = None

# Deep Learning
try:
    import tensorflow as tf
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import Conv2D, MaxPooling2D, Dense, Dropout, Flatten, BatchNormalization
    from tensorflow.keras.optimizers import Adam
    from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
    from tensorflow.keras.utils import to_categorical
    import_status['tensorflow'] = True
    print(f"✅ TensorFlow {tf.__version__}")
except ImportError as e:
    import_status['tensorflow'] = False
    print(f"❌ TensorFlow failed: {e}")
    print("🔧 Fix: pip install tensorflow")

# Machine Learning
try:
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import classification_report, confusion_matrix
    import_status['sklearn'] = True
    print("✅ Scikit-learn")
except ImportError as e:
    import_status['sklearn'] = False
    print(f"❌ Scikit-learn failed: {e}")
    print("🔧 Fix: pip install scikit-learn")

# Visualization
try:
    import matplotlib.pyplot as plt
    import seaborn as sns
    plt.style.use('default')
    import_status['matplotlib'] = True
    print("✅ Matplotlib & Seaborn")
except ImportError as e:
    import_status['matplotlib'] = False
    print(f"❌ Matplotlib/Seaborn failed: {e}")
    print("🔧 Fix: pip install matplotlib seaborn")

# Utilities
try:
    import pickle
    import json
    from datetime import datetime
    import logging
    import_status['utilities'] = True
    print("✅ Utilities")
except ImportError as e:
    import_status['utilities'] = False
    print(f"❌ Utilities failed: {e}")

# PIL
try:
    from PIL import Image
    import_status['pil'] = True
    print("✅ PIL/Pillow")
except ImportError as e:
    import_status['pil'] = False
    print(f"❌ PIL failed: {e}")
    print("🔧 Fix: pip install pillow")

# Summary
successful_imports = sum(import_status.values())
total_imports = len(import_status)

print(f"\n📊 Import Summary: {successful_imports}/{total_imports} successful")

if successful_imports == total_imports:
    print("🎉 All imports successful!")
else:
    print("⚠️ Some imports failed. Install missing packages.")

# Configure environment if TensorFlow available
if import_status.get('tensorflow', False):
    try:
        # Suppress TensorFlow warnings
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
        tf.get_logger().setLevel('ERROR')
        
        # Check GPU
        gpus = tf.config.list_physical_devices('GPU')
        if gpus:
            print(f"✅ GPU Available: {len(gpus)} device(s)")
            try:
                for gpu in gpus:
                    tf.config.experimental.set_memory_growth(gpu, True)
                print("✅ GPU memory growth configured")
            except RuntimeError as e:
                print(f"⚠️ GPU config warning: {e}")
        else:
            print("⚠️ No GPU detected, using CPU")
    except Exception as e:
        print(f"⚠️ TensorFlow configuration warning: {e}")

print("✅ Cell 1 completed!")
