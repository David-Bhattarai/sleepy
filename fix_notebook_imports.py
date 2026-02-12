#!/usr/bin/env python3
"""
Quick Fix for Notebook Import Errors
Yo script le notebook ko import errors fix garcha
"""

import subprocess
import sys
import os

def run_command(command):
    """Run a command and return success status"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def main():
    print("🔧 FIXING NOTEBOOK IMPORT ERRORS")
    print("=" * 50)
    print()
    
    # Common fixes
    fixes = [
        ("Upgrading pip", "python -m pip install --upgrade pip"),
        ("Installing NumPy", "pip install numpy"),
        ("Installing Pandas", "pip install pandas"),
        ("Installing Matplotlib", "pip install matplotlib"),
        ("Installing OpenCV", "pip install opencv-python"),
        ("Installing TensorFlow", "pip install tensorflow"),
        ("Installing Seaborn", "pip install seaborn"),
        ("Installing Pillow", "pip install Pillow"),
        ("Installing Scikit-learn", "pip install scikit-learn")
    ]
    
    for description, command in fixes:
        print(f"🔧 {description}...")
        success, stdout, stderr = run_command(command)
        
        if success:
            print(f"✅ {description} completed")
        else:
            print(f"⚠️ {description} had issues")
            if stderr:
                print(f"   Error: {stderr.strip()}")
    
    print("\n" + "=" * 50)
    print("🧪 Testing imports...")
    print("-" * 50)
    
    # Test imports
    test_code = '''
import sys
print(f"Python: {sys.version.split()[0]}")

try:
    import numpy as np
    print(f"✅ NumPy: {np.__version__}")
except ImportError as e:
    print(f"❌ NumPy: {e}")

try:
    import pandas as pd
    print(f"✅ Pandas: {pd.__version__}")
except ImportError as e:
    print(f"❌ Pandas: {e}")

try:
    import matplotlib
    print(f"✅ Matplotlib: {matplotlib.__version__}")
except ImportError as e:
    print(f"❌ Matplotlib: {e}")

try:
    import cv2
    print(f"✅ OpenCV: {cv2.__version__}")
except ImportError as e:
    print(f"❌ OpenCV: {e}")

try:
    import tensorflow as tf
    print(f"✅ TensorFlow: {tf.__version__}")
except ImportError as e:
    print(f"❌ TensorFlow: {e}")

try:
    import seaborn as sns
    print(f"✅ Seaborn: {sns.__version__}")
except ImportError as e:
    print(f"❌ Seaborn: {e}")
'''
    
    success, stdout, stderr = run_command(f'python -c "{test_code}"')
    if stdout:
        print(stdout)
    if stderr:
        print(f"Errors: {stderr}")
    
    print("\n" + "=" * 50)
    print("✅ Import fix attempt completed!")
    print("\n💡 If errors persist:")
    print("1. Try: pip install --upgrade --force-reinstall tensorflow")
    print("2. Try: pip install --upgrade --force-reinstall opencv-python")
    print("3. Restart your Jupyter kernel")
    print("4. Check your Python environment (virtual env)")
    print("=" * 50)

if __name__ == "__main__":
    main()