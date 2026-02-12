#!/usr/bin/env python3
"""
Install all required packages for Emotion Detection Notebook
Run this before using the notebook
"""

import subprocess
import sys

def install_package(package):
    """Install a package using pip"""
    print(f"📦 Installing {package}...")
    try:
        subprocess.check_call([
            sys.executable, 
            '-m', 
            'pip', 
            'install', 
            package,
            '--upgrade'
        ])
        print(f"✅ {package} installed successfully!\n")
        return True
    except subprocess.CalledProcessError:
        print(f"❌ Failed to install {package}\n")
        return False

def main():
    print("=" * 70)
    print("🚀 EMOTION DETECTION NOTEBOOK - PACKAGE INSTALLER")
    print("=" * 70)
    print()
    
    # List of required packages
    packages = [
        'numpy',
        'pandas',
        'matplotlib',
        'seaborn',
        'opencv-python',
        'pillow',
        'tensorflow'
    ]
    
    print(f"📋 Will install {len(packages)} packages:\n")
    for pkg in packages:
        print(f"   - {pkg}")
    print()
    
    # Install each package
    success_count = 0
    failed_packages = []
    
    for package in packages:
        if install_package(package):
            success_count += 1
        else:
            failed_packages.append(package)
    
    # Summary
    print("=" * 70)
    print("📊 INSTALLATION SUMMARY")
    print("=" * 70)
    print(f"✅ Successfully installed: {success_count}/{len(packages)}")
    
    if failed_packages:
        print(f"❌ Failed to install: {', '.join(failed_packages)}")
        print("\n💡 Try installing failed packages manually:")
        for pkg in failed_packages:
            print(f"   pip install {pkg}")
    else:
        print("🎉 All packages installed successfully!")
    
    print("\n💡 Next Steps:")
    print("1. Restart Jupyter kernel if running")
    print("2. Open emotion_detection_NO_ERRORS.ipynb")
    print("3. Run Cell 1 to verify installation")
    print("=" * 70)

if __name__ == "__main__":
    main()
