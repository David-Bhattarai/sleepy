#!/usr/bin/env python3
"""
Install All Requirements Files
Comprehensive installation script for all requirements files
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n🔧 {description}")
    print(f"Running: {command}")
    print("-" * 50)
    
    try:
        result = subprocess.run(command, shell=True, check=True, 
                              capture_output=True, text=True)
        print("✅ Success!")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        if e.stderr:
            print(f"Error details: {e.stderr}")
        return False

def check_file_exists(filepath):
    """Check if requirements file exists"""
    if os.path.exists(filepath):
        print(f"✅ Found: {filepath}")
        return True
    else:
        print(f"❌ Not found: {filepath}")
        return False

def install_requirements_file(filepath, description):
    """Install a specific requirements file"""
    print(f"\n{'='*60}")
    print(f"📦 Installing {description}")
    print(f"{'='*60}")
    
    if not check_file_exists(filepath):
        print(f"⚠️ Skipping {filepath} - file not found")
        return False
    
    # Show file contents
    try:
        with open(filepath, 'r') as f:
            content = f.read().strip()
            if content:
                print(f"\n📋 Contents of {filepath}:")
                print(content)
            else:
                print(f"⚠️ {filepath} is empty")
                return False
    except Exception as e:
        print(f"❌ Error reading {filepath}: {e}")
        return False
    
    # Install packages
    command = f"pip install -r {filepath}"
    return run_command(command, f"Installing packages from {filepath}")

def install_individual_packages():
    """Install essential packages individually"""
    print(f"\n{'='*60}")
    print("📦 Installing Essential Packages Individually")
    print(f"{'='*60}")
    
    essential_packages = [
        "numpy",
        "pandas", 
        "matplotlib",
        "seaborn",
        "scikit-learn",
        "tensorflow",
        "opencv-python",
        "pillow",
        "flask",
        "requests",
        "jupyter",
        "notebook",
        "ipykernel"
    ]
    
    success_count = 0
    for package in essential_packages:
        print(f"\n📦 Installing {package}...")
        if run_command(f"pip install {package}", f"Installing {package}"):
            success_count += 1
        else:
            print(f"⚠️ Failed to install {package}, continuing...")
    
    print(f"\n📊 Successfully installed {success_count}/{len(essential_packages)} packages")
    return success_count > 0

def main():
    """Main installation function"""
    print("🚀 COMPREHENSIVE REQUIREMENTS INSTALLATION")
    print("=" * 60)
    print("This script will install all requirements files found in the project")
    print("=" * 60)
    
    # List of requirements files to check and install
    requirements_files = [
        ("requirements.txt", "Main Requirements"),
        ("requirements_ml.txt", "Machine Learning Requirements"), 
        ("requirements_fixed.txt", "Fixed Requirements"),
        ("sleepy/requirements.txt", "Sleepy Server Requirements"),
        ("sleepy/server/requirements.txt", "Server Specific Requirements")
    ]
    
    installed_count = 0
    total_files = len(requirements_files)
    
    # Install each requirements file
    for filepath, description in requirements_files:
        if install_requirements_file(filepath, description):
            installed_count += 1
    
    # Install essential packages individually as backup
    print(f"\n{'='*60}")
    print("🔄 Installing Essential Packages as Backup")
    print(f"{'='*60}")
    install_individual_packages()
    
    # Final summary
    print(f"\n{'='*60}")
    print("📋 INSTALLATION SUMMARY")
    print(f"{'='*60}")
    print(f"✅ Requirements files processed: {installed_count}/{total_files}")
    
    if installed_count > 0:
        print("🎉 Installation completed!")
        print("\n🚀 Next steps:")
        print("1. Test imports: python test_notebook_imports.py")
        print("2. Run notebook: jupyter notebook FER2013_Emotion_Model_Training_FIXED.ipynb")
        print("3. Start server: python sleepy/server/app.py")
    else:
        print("⚠️ No requirements files were successfully installed")
        print("🔧 Try installing packages manually:")
        print("   pip install numpy pandas matplotlib tensorflow scikit-learn")
    
    # Test critical imports
    print(f"\n{'='*60}")
    print("🧪 Testing Critical Imports")
    print(f"{'='*60}")
    
    test_imports = [
        ("numpy", "import numpy as np"),
        ("pandas", "import pandas as pd"),
        ("tensorflow", "import tensorflow as tf"),
        ("matplotlib", "import matplotlib.pyplot as plt"),
        ("sklearn", "from sklearn.model_selection import train_test_split")
    ]
    
    working_imports = 0
    for name, import_statement in test_imports:
        try:
            exec(import_statement)
            print(f"✅ {name} - Working")
            working_imports += 1
        except ImportError:
            print(f"❌ {name} - Failed")
    
    print(f"\n📊 Working imports: {working_imports}/{len(test_imports)}")
    
    if working_imports == len(test_imports):
        print("🎉 All critical packages are working!")
    else:
        print("⚠️ Some packages need attention. Check error messages above.")

if __name__ == "__main__":
    main()