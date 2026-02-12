#!/usr/bin/env python3
"""
Install Required Packages for Emotion Detection Notebook
Yo script le notebook ko lagi chahiney sabai packages install garcha
"""

import subprocess
import sys
import os

def install_package(package_name, pip_name=None):
    """Install a package using pip"""
    if pip_name is None:
        pip_name = package_name
    
    try:
        print(f"🔧 Installing {package_name}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", pip_name])
        print(f"✅ {package_name} installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install {package_name}: {e}")
        return False

def check_package(package_name, import_name=None):
    """Check if a package is already installed"""
    if import_name is None:
        import_name = package_name
    
    try:
        __import__(import_name)
        print(f"✅ {package_name} already installed")
        return True
    except ImportError:
        print(f"⚠️ {package_name} not found")
        return False

def main():
    """Main installation function"""
    print("=" * 60)
    print("🎯 EMOTION DETECTION NOTEBOOK - PACKAGE INSTALLER")
    print("=" * 60)
    print()
    
    # Required packages
    packages = [
        ("NumPy", "numpy"),
        ("Pandas", "pandas"),
        ("Matplotlib", "matplotlib"),
        ("Seaborn", "seaborn"),
        ("OpenCV", "opencv-python", "cv2"),
        ("TensorFlow", "tensorflow"),
        ("Pillow", "Pillow", "PIL"),
        ("Scikit-learn", "scikit-learn", "sklearn")
    ]
    
    print("📊 Checking installed packages...")
    print("-" * 60)
    
    to_install = []
    
    for package_info in packages:
        if len(package_info) == 2:
            name, pip_name = package_info
            import_name = pip_name
        else:
            name, pip_name, import_name = package_info
        
        if not check_package(name, import_name):
            to_install.append((name, pip_name))
    
    if not to_install:
        print("\n🎉 All packages are already installed!")
        print("You can run the notebook now.")
        return
    
    print(f"\n🔧 Installing {len(to_install)} missing packages...")
    print("-" * 60)
    
    success_count = 0
    for name, pip_name in to_install:
        if install_package(name, pip_name):
            success_count += 1
    
    print("\n" + "=" * 60)
    if success_count == len(to_install):
        print("🎉 ALL PACKAGES INSTALLED SUCCESSFULLY!")
        print("✅ You can now run the emotion detection notebook!")
    else:
        print(f"⚠️ {success_count}/{len(to_install)} packages installed successfully")
        print("❌ Some packages failed to install")
        print("\n💡 Manual installation commands:")
        for name, pip_name in to_install:
            print(f"   pip install {pip_name}")
    
    print("=" * 60)
    
    # Test imports
    print("\n🧪 Testing imports...")
    print("-" * 60)
    
    test_imports = [
        ("import numpy as np", "NumPy"),
        ("import pandas as pd", "Pandas"),
        ("import matplotlib.pyplot as plt", "Matplotlib"),
        ("import seaborn as sns", "Seaborn"),
        ("import cv2", "OpenCV"),
        ("import tensorflow as tf", "TensorFlow"),
        ("from PIL import Image", "Pillow"),
        ("from sklearn.metrics import accuracy_score", "Scikit-learn")
    ]
    
    for import_cmd, name in test_imports:
        try:
            exec(import_cmd)
            print(f"✅ {name} import successful")
        except ImportError as e:
            print(f"❌ {name} import failed: {e}")
    
    print("\n✅ Package installation complete!")

if __name__ == "__main__":
    main()