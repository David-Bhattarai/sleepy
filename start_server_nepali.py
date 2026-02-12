#!/usr/bin/env python3
"""
Server Start गर्ने Script - Nepali Guide
TensorFlow बिना पूरै Gemini AI emotion detection
"""

import os
import sys
import subprocess

def install_packages():
    """आवश्यक packages install गर्नुहोस्"""
    print("📦 आवश्यक packages install गर्दै...")
    
    packages = [
        'google-generativeai',  # Gemini AI को लागि
        'flask',               # Web server को लागि
        'flask-cors',          # Cross-origin requests को लागि
        'flask-bcrypt',        # Password hashing को लागि
        'vaderSentiment',      # Sentiment analysis को लागि
        'pillow',              # Image processing को लागि
        'numpy'                # Array operations को लागि
    ]
    
    for package in packages:
        try:
            print(f"  Installing {package}...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package], 
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"  ✅ {package} installed")
        except:
            print(f"  ⚠️ {package} already installed or failed")
    
    print("✅ सबै packages ready!")

def check_files():
    """आवश्यक files check गर्नुहोस्"""
    print("\n📁 Files checking...")
    
    required_files = [
        'server/app_gemini_only.py',
        'server/simple_emotion_detector.py',
        'server/gemini_ai_integration.py',
        'server/db_helper_simple.py',
        '.env'
    ]
    
    missing_files = []
    for file in required_files:
        if os.path.exists(file):
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file} - Missing!")
            missing_files.append(file)
    
    if missing_files:
        print(f"\n⚠️ {len(missing_files)} files missing!")
        return False
    
    print("✅ सबै files ready!")
    return True

def setup_api_key():
    """Gemini API key setup गर्नुहोस्"""
    print("\n🔑 API Key setup...")
    
    api_key = "AIzaSyA_y_FXdRR7RPnM-tcfS5jSyozBN7lrrjo"
    os.environ['GEMINI_API_KEY'] = api_key
    
    print(f"✅ API Key set: {api_key[:20]}...")
    return api_key

def test_gemini():
    """Gemini AI test गर्नुहोस्"""
    print("\n🤖 Gemini AI testing...")
    
    try:
        import google.generativeai as genai
        
        api_key = os.environ.get('GEMINI_API_KEY')
        genai.configure(api_key=api_key)
        
        model = genai.GenerativeModel('models/gemini-2.5-flash')
        response = model.generate_content("Test connection - respond with 'Working!'")
        
        print(f"✅ Gemini AI working!")
        print(f"📝 Response: {response.text[:50]}...")
        return True
        
    except ImportError:
        print("❌ google-generativeai package missing!")
        print("💡 Run: pip install google-generativeai")
        return False
    except Exception as e:
        print(f"⚠️ Gemini test failed: {e}")
        return False

def start_server():
    """Server start गर्नुहोस्"""
    print("\n🚀 SERVER STARTING...")
    print("=" * 70)
    print("🌐 URL: http://localhost:5000")
    print("📱 Browser मा खोल्नुहोस्: client/emotion-detection.html")
    print("=" * 70)
    print("🎯 के के गर्न सक्नुहुन्छ:")
    print("   📸 Camera - Real-time emotion detection")
    print("   📁 Upload - Image upload गरेर test गर्नुहोस्")
    print("   🖼️ Samples - 84 sample images test गर्नुहोस्")
    print("   🤖 Gemini AI - Advanced emotion analysis")
    print("=" * 70)
    print("😊 Emotions: happy, sad, angry, fear, surprise, disgust, neutral")
    print("=" * 70)
    
    try:
        # Server directory मा जानुहोस्
        original_dir = os.getcwd()
        os.chdir('server')
        
        # Server start गर्नुहोस्
        subprocess.run([sys.executable, 'app_gemini_only.py'])
        
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except FileNotFoundError:
        print("\n❌ Server file not found!")
        print("💡 Make sure app_gemini_only.py exists in server/ directory")
    except Exception as e:
        print(f"\n❌ Server error: {e}")
    finally:
        # Original directory मा फर्कनुहोस्
        try:
            os.chdir(original_dir)
        except:
            pass

def main():
    """Main function"""
    print("🚀 GEMINI AI EMOTION DETECTION SERVER")
    print("=" * 70)
    print("✅ Python 3.11 compatible (TensorFlow बिना)")
    print("🤖 पूरै Gemini AI integration")
    print("😊 सबै 7 emotions detect गर्छ")
    print("=" * 70)
    
    # Step 1: Install packages
    install_packages()
    
    # Step 2: Check files
    if not check_files():
        print("\n❌ कुछ files missing छन्!")
        print("💡 Make sure you have all required files")
        return
    
    # Step 3: Setup API key
    setup_api_key()
    
    # Step 4: Test Gemini
    if not test_gemini():
        print("\n⚠️ Gemini AI test failed, but server will still work with fallback")
    
    # Step 5: Start server
    start_server()

if __name__ == "__main__":
    main()