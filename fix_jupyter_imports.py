#!/usr/bin/env python3
"""
Quick Fix for Jupyter Import Issues
Simple script to fix numpy and other import issues in Jupyter
"""

import subprocess
import sys

def main():
    print("🔧 Quick Fix for Jupyter Import Issues")
    print("=" * 50)
    
    # Get current Python path
    print(f"Python executable: {sys.executable}")
    print(f"Python version: {sys.version}")
    
    # Install packages using current Python
    packages = ["numpy", "pandas", "matplotlib", "tensorflow", "scikit-learn", "opencv-python", "pillow"]
    
    print(f"\n📦 Installing packages...")
    for package in packages:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✅ {package}")
        except:
            print(f"❌ {package}")
    
    # Test imports
    print(f"\n🧪 Testing imports...")
    try:
        import numpy as np
        print(f"✅ NumPy {np.__version__}")
    except:
        print("❌ NumPy still not working")
    
    try:
        import pandas as pd
        print(f"✅ Pandas {pd.__version__}")
    except:
        print("❌ Pandas still not working")
    
    print(f"\n💡 If issues persist:")
    print(f"1. Restart Jupyter completely")
    print(f"2. Run: jupyter notebook --generate-config")
    print(f"3. Use: python -m jupyter notebook")

if __name__ == "__main__":
    main()