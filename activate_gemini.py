#!/usr/bin/env python3
"""
Activate Gemini AI Integration
Immediately activate Gemini with your API key
"""

import os
import sys

def activate_gemini():
    """Activate Gemini AI with your API key"""
    print("🚀 ACTIVATING GEMINI AI INTEGRATION")
    print("=" * 50)
    
    # Set API key
    api_key = "AIzaSyA_y_FXdRR7RPnM-tcfS5jSyozBN7lrrjo"
    os.environ['GEMINI_API_KEY'] = api_key
    
    print(f"✅ API Key set: {api_key[:20]}...")
    
    # Test import
    try:
        import google.generativeai as genai
        print("✅ google-generativeai package available")
        
        # Configure and test
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('models/gemini-2.5-flash')
        
        response = model.generate_content("Say 'Gemini AI activated successfully!'")
        print(f"✅ Gemini response: {response.text}")
        
        print("\n🎉 GEMINI AI IS NOW ACTIVE!")
        print("🤖 Your emotion detection now uses advanced AI")
        
        return True
        
    except ImportError:
        print("❌ google-generativeai not installed")
        print("💡 Run: pip install google-generativeai")
        return False
    except Exception as e:
        print(f"❌ Activation failed: {e}")
        return False

if __name__ == "__main__":
    activate_gemini()