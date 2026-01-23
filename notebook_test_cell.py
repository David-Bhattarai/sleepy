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