# 🔧 Fix Import Errors - Complete Solution

## ❌ Error:
```
ModuleNotFoundError: No module named 'numpy'
```

## ✅ Solution:

### Method 1: Install in Jupyter Notebook (EASIEST)

**Run this in a NEW cell in your notebook:**

```python
# Cell 1: Install all packages
import sys
!{sys.executable} -m pip install numpy pandas matplotlib seaborn opencv-python pillow tensorflow

print("✅ All packages installed!")
print("Now restart kernel: Kernel → Restart")
```

**Then:**
1. Wait for installation to complete
2. Restart kernel: `Kernel → Restart`
3. Run your cells again

---

### Method 2: Install via Command Line

**Open terminal/command prompt and run:**

```bash
pip install numpy pandas matplotlib seaborn opencv-python pillow tensorflow
```

**Or if using Python 3.11:**
```bash
C:\Users\DELL\AppData\Local\Programs\Python\Python311\python.exe -m pip install numpy pandas matplotlib seaborn opencv-python pillow tensorflow
```

---

### Method 3: Install One by One

```bash
pip install numpy
pip install pandas
pip install matplotlib
pip install seaborn
pip install opencv-python
pip install pillow
pip install tensorflow
```

---

## 📦 Required Packages List

| Package | Purpose | Install Command |
|---------|---------|-----------------|
| numpy | Numerical operations | `pip install numpy` |
| pandas | Data handling | `pip install pandas` |
| matplotlib | Plotting | `pip install matplotlib` |
| seaborn | Visualization | `pip install seaborn` |
| opencv-python | Image processing | `pip install opencv-python` |
| pillow | Image handling | `pip install pillow` |
| tensorflow | Deep learning | `pip install tensorflow` |

---

## 🚀 Complete Installation Script

**Save this as `install_requirements.py`:**

```python
import subprocess
import sys

packages = [
    'numpy',
    'pandas', 
    'matplotlib',
    'seaborn',
    'opencv-python',
    'pillow',
    'tensorflow'
]

print("🔧 Installing required packages...\n")

for package in packages:
    print(f"Installing {package}...")
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
        print(f"✅ {package} installed\n")
    except:
        print(f"❌ Failed to install {package}\n")

print("✅ Installation complete!")
print("Restart Jupyter kernel: Kernel → Restart")
```

**Run:**
```bash
python install_requirements.py
```

---

## 🔍 Verify Installation

**Run this in Jupyter to check:**

```python
# Check if packages are installed
import sys

packages = ['numpy', 'pandas', 'matplotlib', 'seaborn', 'cv2', 'PIL', 'tensorflow']

print("📦 Checking installed packages:\n")

for package in packages:
    try:
        if package == 'cv2':
            import cv2
            print(f"✅ opencv-python: {cv2.__version__}")
        elif package == 'PIL':
            import PIL
            print(f"✅ pillow: {PIL.__version__}")
        else:
            module = __import__(package)
            version = getattr(module, '__version__', 'installed')
            print(f"✅ {package}: {version}")
    except ImportError:
        print(f"❌ {package}: NOT INSTALLED")

print("\n💡 If any package shows NOT INSTALLED, run:")
print("!pip install <package-name>")
```

---

## 🎯 Quick Fix for Jupyter

**Create a new cell at the TOP of your notebook:**

```python
# ============================================================================
# CELL 0: INSTALL PACKAGES (Run this first if you get import errors)
# ============================================================================

import sys
import subprocess

def install_package(package):
    """Install a package using pip"""
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', package, '-q'])
        return True
    except:
        return False

# List of required packages
required_packages = {
    'numpy': 'numpy',
    'pandas': 'pandas',
    'matplotlib': 'matplotlib',
    'seaborn': 'seaborn',
    'cv2': 'opencv-python',
    'PIL': 'pillow',
    'tensorflow': 'tensorflow'
}

print("🔧 Checking and installing packages...\n")

for module_name, package_name in required_packages.items():
    try:
        __import__(module_name)
        print(f"✅ {package_name} already installed")
    except ImportError:
        print(f"⚠️ {package_name} not found, installing...")
        if install_package(package_name):
            print(f"✅ {package_name} installed successfully")
        else:
            print(f"❌ Failed to install {package_name}")

print("\n✅ Package check complete!")
print("💡 If you installed new packages, restart kernel: Kernel → Restart")
```

---

## 🛠️ Troubleshooting

### Problem: pip not found
```bash
# Solution: Use python -m pip
python -m pip install numpy
```

### Problem: Permission denied
```bash
# Solution: Use --user flag
pip install --user numpy pandas matplotlib seaborn opencv-python pillow tensorflow
```

### Problem: Slow installation
```bash
# Solution: Use --no-cache-dir
pip install --no-cache-dir numpy pandas matplotlib seaborn opencv-python pillow tensorflow
```

### Problem: Specific Python version
```bash
# For Python 3.11
C:\Users\DELL\AppData\Local\Programs\Python\Python311\python.exe -m pip install numpy pandas matplotlib seaborn opencv-python pillow tensorflow
```

---

## 📋 After Installation Checklist

- [ ] All packages installed
- [ ] Jupyter kernel restarted
- [ ] Import cell runs without errors
- [ ] Can import numpy, pandas, etc.
- [ ] Ready to use notebook

---

## 🎉 Success Indicators

After successful installation, you should see:

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import cv2
from PIL import Image
import tensorflow as tf

print("✅ All imports successful!")
print(f"NumPy: {np.__version__}")
print(f"Pandas: {pd.__version__}")
print(f"TensorFlow: {tf.__version__}")
print(f"OpenCV: {cv2.__version__}")
```

**Output:**
```
✅ All imports successful!
NumPy: 1.24.3
Pandas: 2.0.3
TensorFlow: 2.13.0
OpenCV: 4.8.0
```

---

## 💡 Pro Tips

1. **Always restart kernel after installing packages**
2. **Use virtual environment for clean installation**
3. **Check Python version compatibility**
4. **Install in Jupyter for notebook-specific packages**

---

**Follow these steps and your import errors will be fixed!** 🚀
