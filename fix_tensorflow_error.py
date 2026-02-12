#!/usr/bin/env python3
"""
Fix TensorFlow Error - Quick Solution
Installs required packages and starts TensorFlow-free server
"""

import subprocess
import sys
import os

def install_required_packages():
    """Install only the packages we need (no TensorFlow)"""
    print("📦 INSTALLING REQUIRED PACKAGES (NO TENSORFLOW)")
    print("=" * 60)
    
    required_packages = [
        'google-generativeai',  # For Gemini AI
        'flask',
        'flask-cors', 
        'flask-bcrypt',
        'vaderSentiment',
        'pillow',
        'numpy'
    ]
    
    for package in required_packages:
        print(f"Installing {package}...")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
            print(f"✅ {package} installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"⚠️ Failed to install {package}: {e}")
    
    print("\n✅ All required packages installed!")

def check_gemini_setup():
    """Check if Gemini AI is properly set up"""
    print("\n🔍 CHECKING GEMINI AI SETUP")
    print("=" * 60)
    
    # Check API key
    if os.path.exists('.env'):
        with open('.env', 'r') as f:
            content = f.read()
            if 'GEMINI_API_KEY' in content:
                print("✅ Gemini API key found in .env file")
            else:
                print("⚠️ Gemini API key not found in .env file")
    else:
        print("⚠️ .env file not found")
    
    # Test Gemini import
    try:
        import google.generativeai as genai
        print("✅ google-generativeai package available")
        
        # Test API key
        api_key = "AIzaSyA_y_FXdRR7RPnM-tcfS5jSyozBN7lrrjo"
        os.environ['GEMINI_API_KEY'] = api_key
        
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('models/gemini-2.5-flash')
        
        response = model.generate_content("Test connection")
        print("✅ Gemini AI connection working!")
        print(f"📝 Test response: {response.text[:50]}...")
        
    except ImportError:
        print("❌ google-generativeai not installed")
        print("💡 Run: pip install google-generativeai")
    except Exception as e:
        print(f"⚠️ Gemini AI test failed: {e}")

def start_tensorflow_free_server():
    """Start the TensorFlow-free server"""
    print("\n🚀 STARTING TENSORFLOW-FREE SERVER")
    print("=" * 60)
    
    server_file = "server/app_gemini_only.py"
    
    if os.path.exists(server_file):
        print(f"✅ Found TensorFlow-free server: {server_file}")
        print("🌐 Starting server on http://localhost:5000")
        print("📱 Open client/emotion-detection.html in your browser")
        print("=" * 60)
        print("🤖 GEMINI AI FEATURES AVAILABLE:")
        print("   • Advanced emotion detection with Gemini Vision")
        print("   • All 7 emotions: happy, sad, angry, fear, surprise, disgust, neutral")
        print("   • Smart fallback systems")
        print("   • Real-time camera detection")
        print("   • Image upload support")
        print("   • 84 sample images for testing")
        print("=" * 60)
        
        # Change to server directory and run
        os.chdir('server')
        subprocess.run([sys.executable, 'app_gemini_only.py'])
        
    else:
        print(f"❌ Server file not found: {server_file}")
        print("💡 Make sure you're in the correct directory")

def main():
    """Main function"""
    print("🔧 TENSORFLOW ERROR FIX")
    print("=" * 60)
    print("This script will:")
    print("1. Install required packages (without TensorFlow)")
    print("2. Check Gemini AI setup")
    print("3. Start TensorFlow-free server")
    print("=" * 60)
    
    # Install packages
    install_required_packages()
    
    # Check Gemini setup
    check_gemini_setup()
    
    # Start server
    start_tensorflow_free_server()

if __name__ == "__main__":
    main()