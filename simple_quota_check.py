#!/usr/bin/env python3
"""
Simple Quota Check
Quick check of Gemini API status
"""

import os

def main():
    print("📊 GEMINI QUOTA STATUS CHECK")
    print("=" * 40)
    
    api_key = 'AIzaSyAhVtegrJ6sXOp2Ri0AkI5_yQDGAGWsJxk'
    print(f"🔑 API Key: {api_key[:10]}...")
    
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        
        print("🧪 Testing API...")
        model = genai.GenerativeModel('models/gemini-2.0-flash-exp')
        response = model.generate_content('Hello')
        
        print("✅ API WORKING!")
        print("🎉 Quota available!")
        
    except Exception as e:
        error = str(e)
        print("❌ API ERROR:")
        print(f"📝 {error[:100]}...")
        
        if '429' in error:
            print("\n🚫 QUOTA EXCEEDED!")
            print("📊 You've used all 1,500 daily requests")
            print("⏰ Resets in ~24 hours")
            
            # Extract retry time
            if 'retry in' in error:
                import re
                match = re.search(r'retry in (\d+\.?\d*)s', error)
                if match:
                    seconds = float(match.group(1))
                    hours = seconds / 3600
                    print(f"⏳ Exact reset: {hours:.1f} hours")
        
        print("\n💡 SOLUTIONS:")
        print("1. ⏰ Wait for reset")
        print("2. 🔑 Get new API key")
        print("3. 🤖 Use without Gemini:")
        print("   python start_server_without_gemini.py")

if __name__ == "__main__":
    main()