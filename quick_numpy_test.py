#!/usr/bin/env python3
"""
Quick NumPy Test - Verify numpy works
"""

try:
    import numpy as np
    print(f"✅ NumPy imported successfully!")
    print(f"✅ NumPy version: {np.__version__}")
    
    # Test basic operations
    arr = np.array([1, 2, 3, 4, 5])
    print(f"✅ Array created: {arr}")
    print(f"✅ Array shape: {arr.shape}")
    print(f"✅ Array sum: {np.sum(arr)}")
    
    # Test 2D array (like images)
    img_array = np.random.randint(0, 256, (48, 48))
    print(f"✅ 2D array (48x48): {img_array.shape}")
    
    print("\n🎉 NumPy is working perfectly!")
    print("✅ Your Jupyter notebook should work fine now!")
    
except ImportError as e:
    print(f"❌ NumPy import failed: {e}")
    print("\n🔧 Try these fixes:")
    print("1. pip install numpy")
    print("2. pip install --upgrade numpy")
    print("3. python -m pip install numpy")
    print("4. Restart your terminal/IDE")
    
except Exception as e:
    print(f"❌ NumPy test failed: {e}")
    print("NumPy is installed but not working properly")