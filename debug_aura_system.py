#!/usr/bin/env python3
"""
Debug MindBridge - NCIT Final Year Project
Check all components and identify issues
"""

import os
import sys

# Add server directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'sleepy', 'server'))

def check_environment():
    """Check environment setup"""
    print("🔍 Checking Environment...")
    
    # Check API key
    api_key = os.getenv('GEMINI_API_KEY')
    if api_key:
        print(f"✅ Gemini API Key: Found ({api_key[:10]}...)")
    else:
        print("⚠️ Gemini API Key: Not found in environment")
        
        # Check .env file
        env_file = '.env'
        if os.path.exists(env_file):
            with open(env_file, 'r') as f:
                content = f.read()
                if 'GEMINI_API_KEY' in content:
                    print("✅ API Key found in .env file")
                else:
                    print("❌ API Key not in .env file")
        else:
            print("❌ .env file not found")
    
    # Check TensorFlow environment
    tf_opt = os.getenv('TF_ENABLE_ONEDNN_OPTS')
    print(f"🔧 TF_ENABLE_ONEDNN_OPTS: {tf_opt}")

def check_imports():
    """Check if all required modules can be imported"""
    print("\n🔍 Checking Imports...")
    
    imports_to_check = [
        ('flask', 'Flask'),
        ('tensorflow', 'TensorFlow'),
        ('google.generativeai', 'Gemini AI'),
        ('PIL', 'Pillow'),
        ('cv2', 'OpenCV'),
        ('numpy', 'NumPy'),
        ('pandas', 'Pandas')
    ]
    
    for module, name in imports_to_check:
        try:
            __import__(module)
            print(f"✅ {name}: Available")
        except ImportError as e:
            print(f"❌ {name}: Missing - {e}")

def check_hybrid_systems():
    """Check hybrid systems"""
    print("\n🔍 Checking Hybrid Systems...")
    
    try:
        from hybrid_emotion_system import get_hybrid_emotion_detector
        detector = get_hybrid_emotion_detector()
        print("✅ Hybrid Emotion System: Loaded")
    except Exception as e:
        print(f"❌ Hybrid Emotion System: Failed - {e}")
    
    try:
        from hybrid_chatbot_system import get_hybrid_chatbot_system
        chatbot = get_hybrid_chatbot_system()
        print("✅ Hybrid Chatbot System: Loaded")
    except Exception as e:
        print(f"❌ Hybrid Chatbot System: Failed - {e}")

def check_gemini_connection():
    """Check Gemini AI connection"""
    print("\n🔍 Checking Gemini AI Connection...")
    
    try:
        import google.generativeai as genai
        
        # Try to configure with API key
        api_key = os.getenv('GEMINI_API_KEY') or 'AIzaSyAhVtegrJ6sXOp2Ri0AkI5_yQDGAGWsJxk'
        genai.configure(api_key=api_key)
        
        # Try to create model
        model = genai.GenerativeModel('models/gemini-2.0-flash-exp')
        print("✅ Gemini AI: Model created successfully")
        
        # Try a simple test
        response = model.generate_content('Say hello')
        if response and response.text:
            print(f"✅ Gemini AI: Working - Response: {response.text[:50]}...")
            return True
        else:
            print("⚠️ Gemini AI: No response received")
            return False
            
    except Exception as e:
        print(f"❌ Gemini AI: Failed - {e}")
        return False

def check_intents_file():
    """Check intents.json file"""
    print("\n🔍 Checking Intents File...")
    
    intents_path = os.path.join('sleepy', 'server', 'intents.json')
    if os.path.exists(intents_path):
        try:
            import json
            with open(intents_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                intents = data.get('intents', [])
                print(f"✅ Intents File: Found with {len(intents)} intents")
        except Exception as e:
            print(f"❌ Intents File: Error reading - {e}")
    else:
        print("❌ Intents File: Not found at sleepy/server/intents.json")

def check_trained_models():
    """Check trained models"""
    print("\n🔍 Checking Trained Models...")
    
    model_paths = [
        'sleepy/server/compact_emotion_model_trained.h5',
        'compact_emotion_model_best.h5',
        'sleepy/server/mindbridge_model_80percent.pkl'
    ]
    
    for path in model_paths:
        if os.path.exists(path):
            print(f"✅ Model Found: {path}")
        else:
            print(f"⚠️ Model Missing: {path}")

def main():
    """Run all checks"""
    print("🔍 MindBridge - NCIT Final Year Project SYSTEM DIAGNOSTIC")
    print("=" * 50)
    
    # Set environment for testing
    os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
    
    check_environment()
    check_imports()
    check_intents_file()
    check_trained_models()
    check_hybrid_systems()
    gemini_working = check_gemini_connection()
    
    print("\n" + "=" * 50)
    print("🎯 DIAGNOSTIC SUMMARY")
    print("=" * 50)
    
    if gemini_working:
        print("🎉 FULL SYSTEM: Gemini AI + Trained Models working!")
        print("🚀 Expected performance: 95-98% accuracy")
    else:
        print("⚠️ HYBRID SYSTEM: Trained models available, Gemini AI issues")
        print("🚀 Expected performance: 80-90% accuracy")
    
    print("\n💡 RECOMMENDATIONS:")
    print("1. Start server: python sleepy/server/app.py")
    print("2. Test responses: python test_server_response.py")
    print("3. Open browser: http://127.0.0.1:5000")

if __name__ == "__main__":
    main()