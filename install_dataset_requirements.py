#!/usr/bin/env python3
"""
Install requirements for dataset downloading and training
"""

import subprocess
import sys

def install_package(package):
    """Install a package using pip"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ {package} installed successfully")
        return True
    except subprocess.CalledProcessError:
        print(f"❌ Failed to install {package}")
        return False

def main():
    """Install all required packages"""
    print("🔄 Installing packages for dataset downloading and training...")
    print("=" * 60)
    
    packages = [
        "pandas",
        "scikit-learn", 
        "matplotlib",
        "seaborn",
        "tqdm",
        "gdown",
        "kaggle"
    ]
    
    success_count = 0
    for package in packages:
        print(f"Installing {package}...")
        if install_package(package):
            success_count += 1
    
    print("=" * 60)
    print(f"📊 Installation Summary:")
    print(f"   Successful: {success_count}/{len(packages)}")
    
    if success_count == len(packages):
        print("🎉 All packages installed successfully!")
        print("\n🔄 Next steps:")
        print("1. Run: python download_real_dataset.py")
        print("2. Run: python train_real_emotion_model.py")
    else:
        print("⚠️ Some packages failed to install")
        print("You may need to install them manually")

if __name__ == "__main__":
    main()