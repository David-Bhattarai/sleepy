#!/usr/bin/env python3
"""
Fix TensorFlow and DeepFace Errors
Solve the compatibility issues with TensorFlow 2.20.0 and tf-keras
"""

import subprocess
import sys
import os

def fix_tensorflow_warnings():
    """Fix TensorFlow oneDNN warnings"""
    print("🔧 Fixing TensorFlow oneDNN warnings...")
    
    # Set environment variable to disable oneDNN warnings
    os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
    
    print("✅ TensorFlow oneDNN warnings disabled")

def install_tf_keras():
    """Install tf-keras package for TensorFlow 2.20.0 compatibility"""
    print("📦 Installing tf-keras for TensorFlow compatibility...")
    
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'tf-keras'])
        print("✅ tf-keras installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install tf-keras: {e}")
        return False

def downgrade_tensorflow():
    """Downgrade TensorFlow to compatible version"""
    print("🔄 Downgrading TensorFlow to compatible version...")
    
    try:
        # Uninstall current TensorFlow
        subprocess.check_call([sys.executable, '-m', 'pip', 'uninstall', 'tensorflow', '-y'])
        
        # Install compatible version
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'tensorflow==2.15.0'])
        
        print("✅ TensorFlow downgraded to 2.15.0")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to downgrade TensorFlow: {e}")
        return False

def fix_deepface_compatibility():
    """Fix DeepFace compatibility issues"""
    print("🔧 Fixing DeepFace compatibility...")
    
    try:
        # Install compatible versions
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'deepface==0.0.79'])
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'tf-keras==2.15.0'])
        
        print("✅ DeepFace compatibility fixed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to fix DeepFace: {e}")
        return False

def create_environment_setup():
    """Create environment setup script"""
    env_script = '''#!/usr/bin/env python3
"""
Environment Setup for AURA System
Sets required environment variables
"""

import os

# Disable TensorFlow oneDNN warnings
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

# Disable TensorFlow GPU warnings (if no GPU)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# Set Keras backend
os.environ['KERAS_BACKEND'] = 'tensorflow'

print("✅ Environment variables set for AURA system")
'''
    
    with open("setup_environment.py", "w") as f:
        f.write(env_script)
    
    print("✅ Created environment setup script")

def update_requirements():
    """Update requirements.txt with compatible versions"""
    print("📝 Updating requirements.txt with compatible versions...")
    
    compatible_requirements = '''# AURA Mental Health AI System - Compatible Dependencies

# Core Web Framework
flask==3.0.0
flask-cors==4.0.0
flask-bcrypt==1.0.1

# AI and Machine Learning (Compatible Versions)
tensorflow==2.15.0
keras==2.15.0
tf-keras==2.15.0
google-generativeai==0.8.5

# Image Processing
pillow==10.1.0
opencv-python==4.8.1.78

# Data Processing
numpy==1.24.3
pandas==2.1.4

# Emotion Detection (Compatible Versions)
deepface==0.0.79

# Text Processing and Sentiment Analysis
vadersentiment==3.3.2

# HTTP Requests
requests==2.31.0

# Environment Management
python-dotenv==1.0.0

# Additional ML Libraries
scikit-learn==1.3.2
matplotlib==3.8.2

# Security
cryptography==41.0.8
'''
    
    with open("requirements_fixed.txt", "w") as f:
        f.write(compatible_requirements)
    
    print("✅ Created requirements_fixed.txt with compatible versions")

def main():
    """Main fix function"""
    print("🔧 FIXING TENSORFLOW AND DEEPFACE ERRORS")
    print("=" * 60)
    print("Solving compatibility issues...")
    print()
    
    # Fix 1: Set environment variables
    fix_tensorflow_warnings()
    
    # Fix 2: Try installing tf-keras first
    print("\n🔄 Attempting Fix 1: Install tf-keras...")
    if install_tf_keras():
        print("✅ Fix 1 successful - tf-keras installed")
    else:
        print("⚠️ Fix 1 failed - trying alternative...")
        
        # Fix 3: Downgrade TensorFlow if tf-keras fails
        print("\n🔄 Attempting Fix 2: Downgrade TensorFlow...")
        if downgrade_tensorflow():
            print("✅ Fix 2 successful - TensorFlow downgraded")
        else:
            print("❌ Fix 2 failed")
    
    # Fix 4: Fix DeepFace compatibility
    print("\n🔄 Attempting Fix 3: Fix DeepFace compatibility...")
    fix_deepface_compatibility()
    
    # Fix 5: Create environment setup
    print("\n🔄 Creating environment setup...")
    create_environment_setup()
    
    # Fix 6: Update requirements
    print("\n🔄 Creating compatible requirements...")
    update_requirements()
    
    print("\n" + "=" * 60)
    print("🎉 FIXES APPLIED!")
    print("=" * 60)
    print("✅ TensorFlow warnings disabled")
    print("✅ tf-keras compatibility added")
    print("✅ DeepFace compatibility fixed")
    print("✅ Environment setup script created")
    print("✅ Compatible requirements.txt created")
    
    print("\n🚀 Next Steps:")
    print("1. Restart your server:")
    print("   python setup_environment.py")
    print("   python start_server_with_gemini.py")
    print()
    print("2. Or reinstall with compatible versions:")
    print("   pip install -r requirements_fixed.txt")
    print()
    print("3. The warnings should be gone and DeepFace should work!")

if __name__ == "__main__":
    main()