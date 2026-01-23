#!/usr/bin/env python3
"""
Quick Install Script
Fast installation of all essential packages
"""

import subprocess
import sys

def install_package(package):
    """Install a single package"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ {package}")
        return True
    except:
        print(f"❌ {package}")
        return False

def main():
    print("🚀 Quick Install - Essential Packages")
    print("=" * 40)
    
    packages = [
        "numpy", "pandas", "matplotlib", "seaborn", 
        "scikit-learn", "tensorflow", "opencv-python", 
        "pillow", "flask", "requests", "jupyter"
    ]
    
    success = 0
    for pkg in packages:
        if install_package(pkg):
            success += 1
    
    print(f"\n📊 Installed: {success}/{len(packages)}")
    
    if success == len(packages):
        print("🎉 All packages installed!")
    else:
        print("⚠️ Some packages failed. Run install_all_requirements.py for details")

if __name__ == "__main__":
    main()