#!/usr/bin/env python3
"""
Fix NumPy and All Dependencies for Jupyter Notebook
Install all required packages for the FER2013 emotion detection training
"""

import subprocess
import sys
import os

def install_package(package):
    """Install a package using pip"""
    try:
        print(f"📦 Installing {package}...")
        result = subprocess.run([sys.executable, "-m", "pip", "install", package], 
                              capture_output=True, text=True, check=True)
        print(f"✅ {package} installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install {package}: {e}")
        print(f"Error output: {e.stderr}")
        return False

def upgrade_pip():
    """Upgrade pip to latest version"""
    try:
        print("🔄 Upgrading pip...")
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], 
                      capture_output=True, text=True, check=True)
        print("✅ pip upgraded successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Failed to upgrade pip: {e}")
        return False

def check_package(package_name):
    """Check if a package is installed"""
    try:
        __import__(package_name)
        print(f"✅ {package_name} is already installed")
        return True
    except ImportError:
        print(f"❌ {package_name} is not installed")
        return False

def fix_numpy_dependencies():
    """Fix NumPy and all ML dependencies"""
    
    print("🔧 Fixing NumPy and ML Dependencies...")
    print("=" * 50)
    
    # Upgrade pip first
    upgrade_pip()
    
    # Core packages in order of dependency
    packages = [
        "numpy",
        "pandas", 
        "matplotlib",
        "seaborn",
        "scikit-learn",
        "opencv-python",
        "pillow",
        "tensorflow",
        "keras",
        "jupyter",
        "ipykernel",
        "notebook"
    ]
    
    print(f"\n📋 Checking current package status...")
    
    # Check current status
    missing_packages = []
    for package in packages:
        package_import_name = package.replace("-", "_").split("_")[0]
        if package_import_name == "opencv":
            package_import_name = "cv2"
        elif package_import_name == "pillow":
            package_import_name = "PIL"
        elif package_import_name == "scikit":
            package_import_name = "sklearn"
        
        if not check_package(package_import_name):
            missing_packages.append(package)
    
    if not missing_packages:
        print("\n🎉 All packages are already installed!")
        return True
    
    print(f"\n📦 Installing {len(missing_packages)} missing packages...")
    
    # Install missing packages
    failed_packages = []
    for package in missing_packages:
        if not install_package(package):
            failed_packages.append(package)
    
    # Try alternative installation methods for failed packages
    if failed_packages:
        print(f"\n🔄 Trying alternative installation methods...")
        
        for package in failed_packages[:]:  # Copy list to modify during iteration
            print(f"\n🔄 Trying alternative installation for {package}...")
            
            # Try with --user flag
            try:
                subprocess.run([sys.executable, "-m", "pip", "install", "--user", package], 
                              capture_output=True, text=True, check=True)
                print(f"✅ {package} installed with --user flag")
                failed_packages.remove(package)
                continue
            except subprocess.CalledProcessError:
                pass
            
            # Try with --no-cache-dir
            try:
                subprocess.run([sys.executable, "-m", "pip", "install", "--no-cache-dir", package], 
                              capture_output=True, text=True, check=True)
                print(f"✅ {package} installed with --no-cache-dir")
                failed_packages.remove(package)
                continue
            except subprocess.CalledProcessError:
                pass
            
            # Try specific versions for problematic packages
            if package == "tensorflow":
                try:
                    subprocess.run([sys.executable, "-m", "pip", "install", "tensorflow-cpu"], 
                                  capture_output=True, text=True, check=True)
                    print(f"✅ tensorflow-cpu installed as alternative")
                    failed_packages.remove(package)
                    continue
                except subprocess.CalledProcessError:
                    pass
            
            if package == "opencv-python":
                try:
                    subprocess.run([sys.executable, "-m", "pip", "install", "opencv-python-headless"], 
                                  capture_output=True, text=True, check=True)
                    print(f"✅ opencv-python-headless installed as alternative")
                    failed_packages.remove(package)
                    continue
                except subprocess.CalledProcessError:
                    pass
    
    # Final status check
    print(f"\n📊 Installation Summary:")
    print("=" * 30)
    
    success_count = 0
    for package in packages:
        package_import_name = package.replace("-", "_").split("_")[0]
        if package_import_name == "opencv":
            package_import_name = "cv2"
        elif package_import_name == "pillow":
            package_import_name = "PIL"
        elif package_import_name == "scikit":
            package_import_name = "sklearn"
        
        if check_package(package_import_name):
            success_count += 1
    
    print(f"\n✅ Successfully installed: {success_count}/{len(packages)} packages")
    
    if failed_packages:
        print(f"\n❌ Failed to install: {failed_packages}")
        print(f"\n💡 Manual installation suggestions:")
        for package in failed_packages:
            print(f"   pip install {package}")
        return False
    else:
        print(f"\n🎉 All packages installed successfully!")
        return True

def create_requirements_file():
    """Create a requirements.txt file with all dependencies"""
    
    requirements_content = """# Core ML and Data Science packages
numpy>=1.21.0
pandas>=1.3.0
matplotlib>=3.4.0
seaborn>=0.11.0
scikit-learn>=1.0.0

# Computer Vision
opencv-python>=4.5.0
Pillow>=8.3.0

# Deep Learning
tensorflow>=2.8.0
keras>=2.8.0

# Jupyter and Notebook
jupyter>=1.0.0
ipykernel>=6.0.0
notebook>=6.4.0

# Additional utilities
pickle-mixin>=1.0.2
datetime
json5>=0.9.0
logging
"""
    
    try:
        with open('requirements_ml.txt', 'w') as f:
            f.write(requirements_content)
        print("✅ Created requirements_ml.txt file")
        return True
    except Exception as e:
        print(f"❌ Failed to create requirements file: {e}")
        return False

def test_imports():
    """Test all critical imports"""
    
    print("\n🧪 Testing critical imports...")
    
    test_imports = [
        ("numpy", "np"),
        ("pandas", "pd"),
        ("matplotlib.pyplot", "plt"),
        ("seaborn", "sns"),
        ("sklearn", None),
        ("tensorflow", "tf"),
        ("PIL", None)
    ]
    
    failed_imports = []
    
    for import_name, alias in test_imports:
        try:
            if alias:
                exec(f"import {import_name} as {alias}")
                print(f"✅ import {import_name} as {alias}")
            else:
                exec(f"import {import_name}")
                print(f"✅ import {import_name}")
        except ImportError as e:
            print(f"❌ import {import_name} failed: {e}")
            failed_imports.append(import_name)
    
    # Test OpenCV separately
    try:
        import cv2
        print(f"✅ import cv2 (OpenCV version: {cv2.__version__})")
    except ImportError as e:
        print(f"❌ import cv2 failed: {e}")
        failed_imports.append("cv2")
    
    if failed_imports:
        print(f"\n❌ Failed imports: {failed_imports}")
        return False
    else:
        print(f"\n🎉 All imports successful!")
        return True

def setup_jupyter_kernel():
    """Setup Jupyter kernel with current environment"""
    
    print("\n🔧 Setting up Jupyter kernel...")
    
    try:
        # Install ipykernel if not already installed
        subprocess.run([sys.executable, "-m", "pip", "install", "ipykernel"], 
                      capture_output=True, text=True, check=True)
        
        # Install kernel
        subprocess.run([sys.executable, "-m", "ipykernel", "install", "--user", "--name", "ml-env"], 
                      capture_output=True, text=True, check=True)
        
        print("✅ Jupyter kernel 'ml-env' installed successfully")
        print("💡 Use 'ml-env' kernel when running the notebook")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Failed to setup Jupyter kernel: {e}")
        return False

def main():
    """Main function to fix all dependencies"""
    
    print("🚀 Starting NumPy and ML Dependencies Fix...")
    print("=" * 60)
    
    # Check Python version
    python_version = sys.version_info
    print(f"🐍 Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 7):
        print("⚠️ Warning: Python 3.7+ recommended for best compatibility")
    
    # Step 1: Fix dependencies
    success = fix_numpy_dependencies()
    
    # Step 2: Create requirements file
    create_requirements_file()
    
    # Step 3: Test imports
    test_success = test_imports()
    
    # Step 4: Setup Jupyter kernel
    setup_jupyter_kernel()
    
    # Final summary
    print("\n" + "=" * 60)
    print("📋 FINAL SUMMARY")
    print("=" * 60)
    
    if success and test_success:
        print("🎉 SUCCESS: All dependencies fixed!")
        print("\n✅ Next steps:")
        print("1. Restart your Jupyter notebook")
        print("2. Select 'ml-env' kernel if available")
        print("3. Run the FER2013_Emotion_Model_Training.ipynb notebook")
        print("\n💡 If you still get import errors:")
        print("- Restart your IDE/terminal")
        print("- Try: pip install -r requirements_ml.txt")
        print("- Use: python -m pip install numpy --upgrade")
    else:
        print("❌ Some issues remain. Check error messages above.")
        print("\n🔧 Manual fix commands:")
        print("pip install --upgrade pip")
        print("pip install numpy pandas matplotlib seaborn scikit-learn")
        print("pip install tensorflow opencv-python pillow")
        print("pip install jupyter notebook ipykernel")
    
    print("\n🔗 Useful commands:")
    print("- Check installed packages: pip list")
    print("- Upgrade package: pip install --upgrade <package>")
    print("- Install from requirements: pip install -r requirements_ml.txt")

if __name__ == "__main__":
    main()