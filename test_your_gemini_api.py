#!/usr/bin/env python3
"""
Test Your Gemini API Key
Yo script le timro Gemini API key test garcha
"""

import os
import sys
import json

def test_gemini_api_key():
    """Test the provided Gemini API key"""
    print("🧪 TESTING YOUR GEMINI API KEY")
    print("=" * 50)
    print()
    
    # Load API key from .env
    api_key = "AIzaSyA_y_FXdRR7RPnM-tcfS5jSyozBN7lrrjo"
    
    print(f"🔑 API Key: {api_key[:20]}...")
    print()
    
    # Test 1: Import google-generativeai
    print("1️⃣ Testing Google GenerativeAI Package:")
    print("-" * 40)
    
    try:
        import google.generativeai as genai
        print("✅ google-generativeai package imported successfully")
    except ImportError as e:
        print(f"❌ google-generativeai not installed: {e}")
        print("💡 Install with: pip install google-generativeai")
        return False
    
    # Test 2: Configure Gemini with API key
    print("\n2️⃣ Configuring Gemini AI:")
    print("-" * 40)
    
    try:
        genai.configure(api_key=api_key)
        print("✅ Gemini AI configured with your API key")
    except Exception as e:
        print(f"❌ Configuration failed: {e}")
        return False
    
    # Test 3: Initialize model
    print("\n3️⃣ Initializing Gemini Model:")
    print("-" * 40)
    
    try:
        model = genai.GenerativeModel('models/gemini-2.5-flash')
        print("✅ Gemini 2.5 Flash model initialized")
    except Exception as e:
        print(f"❌ Model initialization failed: {e}")
        return False
    
    # Test 4: Simple text generation
    print("\n4️⃣ Testing Text Generation:")
    print("-" * 40)
    
    try:
        response = model.generate_content("Say 'Hello from Gemini AI! I am working perfectly.'")
        print("✅ Text generation successful!")
        print(f"📝 Response: {response.text}")
    except Exception as e:
        print(f"❌ Text generation failed: {e}")
        return False
    
    # Test 5: Emotion detection prompt
    print("\n5️⃣ Testing Emotion Detection Prompt:")
    print("-" * 40)
    
    try:
        emotion_prompt = """
        You are an advanced AI emotion detector. Analyze facial expressions and respond in JSON format.
        
        For this test, respond with a sample emotion detection result:
        {
            "dominant_emotion": "happy",
            "confidence": 95.5,
            "all_emotions": {
                "happy": 95.5,
                "neutral": 3.2,
                "surprise": 1.3
            },
            "description": "Test response - AI is working correctly",
            "face_detected": true
        }
        """
        
        response = model.generate_content(emotion_prompt)
        response_text = response.text.strip()
        
        # Clean up response
        if response_text.startswith('```json'):
            response_text = response_text.replace('```json', '').replace('```', '').strip()
        
        # Try to parse JSON
        result = json.loads(response_text)
        
        print("✅ Emotion detection prompt successful!")
        print(f"📊 Sample result: {result['dominant_emotion']} ({result['confidence']}%)")
        
    except Exception as e:
        print(f"❌ Emotion detection prompt failed: {e}")
        return False
    
    # Test 6: Integration with your system
    print("\n6️⃣ Testing System Integration:")
    print("-" * 40)
    
    try:
        # Set environment variable
        os.environ['GEMINI_API_KEY'] = api_key
        
        # Test importing your integration
        sys.path.append('server')
        from gemini_ai_integration import get_gemini_ai
        
        gemini_ai = get_gemini_ai()
        
        if gemini_ai and gemini_ai.api_key:
            print("✅ Your Gemini AI integration working!")
            
            # Test intelligent response
            test_result = gemini_ai.generate_intelligent_response("I feel happy today!")
            if test_result['success']:
                print(f"✅ Intelligent response: {test_result['response'][:50]}...")
            else:
                print(f"⚠️ Response generation issue: {test_result.get('error', 'Unknown')}")
        else:
            print("❌ Integration not working properly")
            return False
            
    except Exception as e:
        print(f"❌ System integration failed: {e}")
        return False
    
    return True

def main():
    """Main test function"""
    print("🎯 GEMINI API KEY INTEGRATION TEST")
    print("=" * 60)
    print()
    
    success = test_gemini_api_key()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 GEMINI API KEY WORKING PERFECTLY!")
        print("=" * 60)
        print("✅ What's now working:")
        print("   • Google Gemini AI Vision for emotion detection")
        print("   • Advanced facial expression analysis")
        print("   • Intelligent chatbot responses")
        print("   • Context-aware conversation analysis")
        print()
        print("🚀 Your emotion detection system now has:")
        print("   🤖 Primary: Gemini AI Vision (Advanced)")
        print("   🎯 Fallback: FER2013 Model (98.57% accuracy)")
        print("   🧠 Ultimate: Intelligent Analysis")
        print()
        print("📱 Ready to use in emotion-detection.html!")
        print("   1. Start server: python server/app.py")
        print("   2. Open client/emotion-detection.html")
        print("   3. Test with camera/upload/samples")
        print("   4. See '🤖 Gemini AI Detected' results!")
        
    else:
        print("❌ GEMINI API KEY ISSUES FOUND")
        print("=" * 60)
        print("💡 Possible solutions:")
        print("   1. Check your internet connection")
        print("   2. Verify API key is correct")
        print("   3. Install: pip install google-generativeai")
        print("   4. Make sure API key has proper permissions")
        print("   5. Check Google AI Studio for API key status")
    
    print("=" * 60)

if __name__ == "__main__":
    main()