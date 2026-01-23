#!/usr/bin/env python3
"""
Simple NumPy Installation Fix
Ensures NumPy is properly installed and working
"""

import subprocess
import sys

def install_numpy():
    """Install NumPy with multiple methods"""
    
    print("🔧 Installing NumPy...")
    
    methods = [
        [sys.executable, "-m", "pip", "install", "numpy"],
        [sys.executable, "-m", "pip", "install", "--upgrade", "numpy"],
        [sys.executable, "-m", "pip", "install", "--user", "numpy"],
        [sys.executable, "-m", "pip", "install", "--no-cache-dir", "numpy"]
    ]
    
    for i, method in enumerate(methods, 1):
        try:
            print(f"📦 Method {i}: {' '.join(method)}")
            result = subprocess.run(method, capture_output=True, text=True, check=True)
            print(f"✅ NumPy installed successfully with method {i}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Method {i} failed: {e}")
            continue
    
    print("❌ All installation methods failed")
    return False

def test_numpy():
    """Test if NumPy works"""
    
    try:
        import numpy as np
        print(f"✅ NumPy test successful! Version: {np.__version__}")
        
        # Test basic operations
        arr = np.array([1, 2, 3])
        print(f"✅ Basic operations work: {arr.sum()}")
        
        return True
        
    except ImportError as e:
        print(f"❌ NumPy import failed: {e}")
        return False
    except Exception as e:
        print(f"❌ NumPy test failed: {e}")
        return False

def main():
    """Main function"""
    
    print("🚀 NumPy Installation Fix")
    print("=" * 30)
    
    # First test if NumPy already works
    if test_numpy():
        print("\n🎉 NumPy is already working!")
        print("✅ Your Jupyter notebook should work fine")
        return
    
    # Try to install NumPy
    print("\n📦 NumPy not working, attempting installation...")
    
    if install_numpy():
        print("\n🧪 Testing NumPy after installation...")
        if test_numpy():
            print("\n🎉 SUCCESS! NumPy is now working!")
            print("✅ You can now run your Jupyter notebook")
        else:
            print("\n❌ NumPy installed but still not working")
            print("🔧 Try restarting your Python environment")
    else:
        print("\n❌ Failed to install NumPy")
        print("🔧 Manual installation required:")
        print("   1. Open terminal/command prompt")
        print("   2. Run: pip install numpy")
        print("   3. Or try: python -m pip install numpy")
        print("   4. Restart your IDE/Jupyter")

if __name__ == "__main__":
    main()