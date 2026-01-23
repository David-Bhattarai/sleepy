#!/usr/bin/env python3
"""
Direct Fix for Notebook Import Issues
Run this before opening Jupyter notebook
"""

import subprocess
import sys
import os

def main():
    print("🔧 DIRECT FIX FOR JUPYTER NOTEBOOK IMPORTS")
    print("=" * 60)
    
    # Force install packages in current environment
    packages = [
        "numpy", "pandas", "matplotlib", "seaborn", 
        "scikit-learn", "tensorflow", "opencv-python", 
        "pillow", "jupyter", "notebook", "ipykernel"
    ]
    
    print("📦 Force installing packages...")
    for pkg in packages:
        try:
            cmd = f"{sys.executable} -m pip install --force-reinstall {pkg}"
            subprocess.run(cmd, shell=True, check=True, capture_output=True)
            print(f"✅ {pkg}")
        except:
            print(f"⚠️ {pkg} - continuing...")
    
    # Test imports
    print("\n🧪 Testing imports...")
    try:
        import numpy as np
        print(f"✅ NumPy {np.__version__} - WORKING!")
    except Exception as e:
        print(f"❌ NumPy failed: {e}")
    
    try:
        import pandas as pd
        print(f"✅ Pandas {pd.__version__} - WORKING!")
    except Exception as e:
        print(f"❌ Pandas failed: {e}")
    
    print(f"\n🚀 SOLUTION:")
    print(f"1. Close all Jupyter windows")
    print(f"2. Run: jupyter notebook")
    print(f"3. Open your notebook")
    print(f"4. All imports should work now!")
    
    # Create a simple test cell
    test_code = '''
# Test cell - run this first in your notebook
import sys
print(f"Python: {sys.executable}")

try:
    import numpy as np
    print(f"✅ NumPy {np.__version__}")
except ImportError as e:
    print(f"❌ NumPy: {e}")
    print("🔧 Run: !pip install numpy")

try:
    import pandas as pd
    print(f"✅ Pandas {pd.__version__}")
except ImportError as e:
    print(f"❌ Pandas: {e}")
    print("🔧 Run: !pip install pandas")

try:
    import tensorflow as tf
    print(f"✅ TensorFlow {tf.__version__}")
except ImportError as e:
    print(f"❌ TensorFlow: {e}")
    print("🔧 Run: !pip install tensorflow")

print("🎉 Import test completed!")
'''
    
    with open('notebook_test_cell.py', 'w') as f:
        f.write(test_code)
    
    print(f"\n📝 Created notebook_test_cell.py")
    print(f"Copy this code into your first notebook cell to test imports")

if __name__ == "__main__":
    main()