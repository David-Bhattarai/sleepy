#!/usr/bin/env python3
"""
Jupyter NumPy Fix - Install packages directly in Jupyter's Python environment
"""

import subprocess
import sys
import os

def main():
    print("🔧 JUPYTER NUMPY FIX")
    print("=" * 50)
    
    # Get Jupyter's Python path
    print(f"Current Python: {sys.executable}")
    print(f"Python version: {sys.version}")
    
    # Install packages using Jupyter's Python
    packages = [
        "numpy", "pandas", "matplotlib", "seaborn", 
        "scikit-learn", "tensorflow", "opencv-python", 
        "pillow", "jupyter", "ipykernel"
    ]
    
    print("\n📦 Installing packages in Jupyter's Python environment...")
    
    for package in packages:
        try:
            # Use the exact Python executable that Jupyter is using
            cmd = [sys.executable, "-m", "pip", "install", "--user", package]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            print(f"✅ {package}")
        except subprocess.CalledProcessError as e:
            print(f"⚠️ {package} - {e}")
            # Try without --user flag
            try:
                cmd = [sys.executable, "-m", "pip", "install", package]
                subprocess.run(cmd, capture_output=True, text=True, check=True)
                print(f"✅ {package} (retry)")
            except:
                print(f"❌ {package} - failed")
    
    # Test imports
    print("\n🧪 Testing imports...")
    
    try:
        import numpy as np
        print(f"✅ NumPy {np.__version__}")
    except ImportError as e:
        print(f"❌ NumPy: {e}")
    
    try:
        import pandas as pd
        print(f"✅ Pandas {pd.__version__}")
    except ImportError as e:
        print(f"❌ Pandas: {e}")
    
    try:
        import tensorflow as tf
        print(f"✅ TensorFlow {tf.__version__}")
    except ImportError as e:
        print(f"❌ TensorFlow: {e}")
    
    print("\n🚀 NEXT STEPS:")
    print("1. Restart Jupyter completely (close all tabs)")
    print("2. Run: jupyter notebook")
    print("3. Open your notebook")
    print("4. Add this as first cell:")
    print("   import sys")
    print("   !{sys.executable} -m pip install numpy pandas tensorflow")
    print("   import numpy as np")

if __name__ == "__main__":
    main()