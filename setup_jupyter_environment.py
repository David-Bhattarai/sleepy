#!/usr/bin/env python3
"""
Setup Jupyter Environment for FER2013 Training
Ensures all packages are available in Jupyter notebook
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

def install_packages():
    """Install essential packages for the current Python environment"""
    print("🚀 Installing Essential Packages for Jupyter")
    print("=" * 60)
    
    packages = [
        "numpy>=1.21.0",
        "pandas>=1.3.0", 
        "matplotlib>=3.4.0",
        "seaborn>=0.11.0",
        "scikit-learn>=1.0.0",
        "tensorflow>=2.8.0",
        "opencv-python>=4.5.0",
        "Pillow>=8.3.0",
        "jupyter>=1.0.0",
        "ipykernel>=6.0.0",
        "notebook>=6.4.0"
    ]
    
    success_count = 0
    for package in packages:
        print(f"\n📦 Installing {package}...")
        if run_command(f"python -m pip install {package}", f"Installing {package}"):
            success_count += 1
        else:
            # Try without version constraints
            base_package = package.split(">=")[0]
            print(f"🔄 Retrying without version constraint: {base_package}")
            if run_command(f"python -m pip install {base_package}", f"Installing {base_package}"):
                success_count += 1
    
    print(f"\n📊 Successfully installed {success_count}/{len(packages)} packages")
    return success_count > 0

def setup_jupyter_kernel():
    """Setup Jupyter kernel for current environment"""
    print("\n🔧 Setting up Jupyter kernel...")
    
    # Install ipykernel
    run_command("python -m pip install ipykernel", "Installing ipykernel")
    
    # Install kernel
    kernel_name = "fer2013-env"
    run_command(f"python -m ipykernel install --user --name {kernel_name} --display-name 'FER2013 Environment'", 
                "Installing Jupyter kernel")
    
    print(f"✅ Jupyter kernel '{kernel_name}' installed")
    return kernel_name

def test_imports():
    """Test critical imports"""
    print("\n🧪 Testing Critical Imports")
    print("=" * 40)
    
    test_imports = [
        ("numpy", "import numpy as np; print(f'NumPy {np.__version__}')"),
        ("pandas", "import pandas as pd; print(f'Pandas {pd.__version__}')"),
        ("tensorflow", "import tensorflow as tf; print(f'TensorFlow {tf.__version__}')"),
        ("matplotlib", "import matplotlib.pyplot as plt; print('Matplotlib OK')"),
        ("sklearn", "from sklearn.model_selection import train_test_split; print('Scikit-learn OK')"),
        ("cv2", "import cv2; print(f'OpenCV {cv2.__version__}')"),
        ("PIL", "from PIL import Image; print('PIL OK')")
    ]
    
    working_imports = 0
    for name, import_statement in test_imports:
        try:
            exec(import_statement)
            print(f"✅ {name} - Working")
            working_imports += 1
        except ImportError as e:
            print(f"❌ {name} - Failed: {e}")
        except Exception as e:
            print(f"⚠️ {name} - Warning: {e}")
    
    print(f"\n📊 Working imports: {working_imports}/{len(test_imports)}")
    return working_imports

def create_notebook_test():
    """Create a test notebook to verify environment"""
    notebook_content = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": ["# Environment Test Notebook\n", "Test all required imports for FER2013 training"]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# Test all imports\n",
                    "import sys\n",
                    "print(f'Python version: {sys.version}')\n",
                    "print(f'Python executable: {sys.executable}')\n",
                    "\n",
                    "try:\n",
                    "    import numpy as np\n",
                    "    print(f'✅ NumPy {np.__version__}')\n",
                    "except ImportError as e:\n",
                    "    print(f'❌ NumPy failed: {e}')\n",
                    "\n",
                    "try:\n",
                    "    import pandas as pd\n",
                    "    print(f'✅ Pandas {pd.__version__}')\n",
                    "except ImportError as e:\n",
                    "    print(f'❌ Pandas failed: {e}')\n",
                    "\n",
                    "try:\n",
                    "    import tensorflow as tf\n",
                    "    print(f'✅ TensorFlow {tf.__version__}')\n",
                    "except ImportError as e:\n",
                    "    print(f'❌ TensorFlow failed: {e}')\n",
                    "\n",
                    "try:\n",
                    "    import matplotlib.pyplot as plt\n",
                    "    print('✅ Matplotlib OK')\n",
                    "except ImportError as e:\n",
                    "    print(f'❌ Matplotlib failed: {e}')\n",
                    "\n",
                    "try:\n",
                    "    from sklearn.model_selection import train_test_split\n",
                    "    print('✅ Scikit-learn OK')\n",
                    "except ImportError as e:\n",
                    "    print(f'❌ Scikit-learn failed: {e}')\n",
                    "\n",
                    "print('\\n🎉 Environment test completed!')"
                ]
            }
        ],
        "metadata": {
            "kernelspec": {
                "display_name": "FER2013 Environment",
                "language": "python",
                "name": "fer2013-env"
            },
            "language_info": {
                "name": "python",
                "version": "3.8.5"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }
    
    import json
    with open('Environment_Test.ipynb', 'w') as f:
        json.dump(notebook_content, f, indent=2)
    
    print("✅ Created Environment_Test.ipynb")

def main():
    """Main setup function"""
    print("🚀 JUPYTER ENVIRONMENT SETUP FOR FER2013")
    print("=" * 60)
    print("This script will set up your Jupyter environment for FER2013 training")
    print("=" * 60)
    
    # Step 1: Install packages
    print("\n📦 STEP 1: Installing Packages")
    install_packages()
    
    # Step 2: Setup Jupyter kernel
    print("\n🔧 STEP 2: Setting up Jupyter Kernel")
    kernel_name = setup_jupyter_kernel()
    
    # Step 3: Test imports
    print("\n🧪 STEP 3: Testing Imports")
    working_imports = test_imports()
    
    # Step 4: Create test notebook
    print("\n📝 STEP 4: Creating Test Notebook")
    create_notebook_test()
    
    # Final summary
    print("\n" + "=" * 60)
    print("📋 SETUP SUMMARY")
    print("=" * 60)
    
    if working_imports >= 5:
        print("🎉 Environment setup successful!")
        print(f"\n🚀 Next steps:")
        print(f"1. Start Jupyter: jupyter notebook")
        print(f"2. Open Environment_Test.ipynb to verify setup")
        print(f"3. Select kernel: FER2013 Environment")
        print(f"4. Run FER2013_Emotion_Model_Training_FIXED.ipynb")
        
        print(f"\n💡 Important:")
        print(f"• Always select 'FER2013 Environment' as your kernel")
        print(f"• If imports still fail, restart Jupyter and try again")
        
    else:
        print("⚠️ Some packages are missing")
        print(f"\n🔧 Manual installation:")
        print(f"pip install numpy pandas matplotlib tensorflow scikit-learn")
        print(f"pip install opencv-python pillow jupyter notebook")
    
    print(f"\n📁 Files created:")
    print(f"• Environment_Test.ipynb - Test notebook")
    print(f"• Jupyter kernel: {kernel_name}")

if __name__ == "__main__":
    main()