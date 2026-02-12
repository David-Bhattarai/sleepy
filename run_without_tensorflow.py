#!/usr/bin/env python3
"""
TensorFlow बिना Server चलाउने Script
Python 3.11 मा TensorFlow काम गर्दैन, तर Gemini AI पूरै काम गर्छ!
"""

import os
import sys
import subprocess

def main():
    print("🚀 TENSORFLOW बिना EMOTION DETECTION SERVER")
    print("=" * 70)
    print("✅ Python 3.11 compatible")
    print("🤖 पूरै Gemini AI integration")
    print("😊 सबै 7 emotions: happy, sad, angry, fear, surprise, disgust, neutral")
    print("=" * 70)
    
    # API key set गर्नुहोस्
    api_key = "AIzaSyA_y_FXdRR7RPnM-tcfS5jSyozBN7lrrjo"
    os.environ['GEMINI_API_KEY'] = api_key
    print(f"🔑 API Key set: {api_key[:20]}...")
    
    # Required packages install गर्नुहोस्
    print("\n📦 Required packages install गर्दै...")
    packages = [
        'google-generativeai',
        'flask',
        'flask-cors', 
        'flask-bcrypt',
        'vaderSentiment',
        'pillow',
        'numpy'
    ]
    
    for package in packages:
        try:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package], 
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"✅ {package} installed")
        except:
            print(f"⚠️ {package} already installed or failed")
    
    print("\n✅ सबै packages ready!")
    
    # Server file check गर्नुहोस्
    server_file = "server/app_gemini_only.py"
    if not os.path.exists(server_file):
        print(f"❌ Server file not found: {server_file}")
        return
    
    print(f"✅ Server file found: {server_file}")
    print("\n🌐 Server starting on http://localhost:5000")
    print("📱 Browser मा खोल्नुहोस्: client/emotion-detection.html")
    print("=" * 70)
    print("🎯 के के गर्न सक्नुहुन्छ:")
    print("   📸 Camera Detection - Real-time emotion detection")
    print("   📁 Image Upload - कुनै पनि face image upload गर्नुहोस्")
    print("   🖼️ Sample Testing - 84 sample images test गर्नुहोस्")
    print("   🤖 Gemini AI - Advanced facial expression analysis")
    print("=" * 70)
    print("🚀 Server starting...")
    print()
    
    # Server start गर्नुहोस्
    try:
        os.chdir('server')
        subprocess.run([sys.executable, 'app_gemini_only.py'])
    except KeyboardInterrupt:
        print("\n👋 Server stopped")
    except Exception as e:
        print(f"\n❌ Server error: {e}")

if __name__ == "__main__":
    main()