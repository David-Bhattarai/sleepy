#!/usr/bin/env python3
"""
Test Gemini AI Integration
Yo script le check garcha ki Gemini AI properly integrated cha ki chaina
"""

import os
import sys
import json

def test_gemini_integration():
    """Test if Gemini AI is properly integrated"""
    print("� TESTING GEMINI AI INTEGRATION")
    print("=" * 50)
    print()
    
    # Check 1: Environment Variable
    print("1️⃣ Checking API Key Configuration:")
    print("-" * 30)
    
    api_key = os.getenv('GEMINI_API_KEY')
    if api_key:
        print(f"✅ GEMINI_API_KEY found in environment")
        print(f"   Key starts with: {api_key[:10]}...")
    else:
        print("❌ GEMINI_API_KEY not found in environment variables")
        
        # Check .env file
        env_file = '.env'
        if os.path.exists(env_file):
            print("📄 Checking .env file...")
            try:
                with open(env_file, 'r') as f:
                    content = f.read()
                    if 'GEMINI_API_KEY=' in content:
                        print("✅ GEMINI_API_KEY found in .env file")
                    else:
                        print("❌ GEMINI_API_KEY not found in .env file")
            except Exception as e:
                print(f"❌ Error reading .env file: {e}")
        else:
            print("❌ .env file not found")
    
    print()
    
    # Check 2: Gemini AI Integration File
    print("2️⃣ Checking Gemini AI Integration Files:")
    print("-" * 30)
    
    integration_files = [
        'server/gemini_ai_integration.py',
        'server/gemini_emotion_detector.py',
        'server/gemini_chatbot.py'
    ]
    
    for file_path in integration_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path} exists")
        else:
            print(f"❌ {file_path} missing")
    
    print()
    
    # Check 3: Try importing Gemini modules
    print("3️⃣ Testing Gemini Module Imports:")
    print("-" * 30)
    
    try:
        sys.path.append('server')
        from gemini_ai_integration import get_gemini_ai
        print("✅ gemini_ai_integration imported successfully")
        
        # Test initialization
        gemini_ai = get_gemini_ai()
        if gemini_ai and gemini_ai.api_key:
            print("✅ Gemini AI initialized with API key")
        else:
            print("❌ Gemini AI not initialized (missing API key)")
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
    except Exception as e:
        print(f"❌ Initialization error: {e}")
    
    print()
    
    # Check 4: Test Google GenerativeAI package
    print("4️⃣ Testing Google GenerativeAI Package:")
    print("-" * 30)
    
    try:
        import google.generativeai as genai
        print("✅ google.generativeai package available")
        
        # Test with API key if available
        if api_key:
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('models/gemini-2.5-flash')
                print("✅ Gemini model initialized successfully")
            except Exception as e:
                print(f"❌ Gemini model initialization failed: {e}")
        else:
            print("⚠️ Cannot test model without API key")
            
    except ImportError as e:
        print(f"❌ google.generativeai not installed: {e}")
        print("💡 Install with: pip install google-generativeai")
    
    print()
    
    # Check 5: Server Integration
    print("5️⃣ Checking Server Integration:")
    print("-" * 30)
    
    try:
        sys.path.append('server')
        from app import GEMINI_AVAILABLE
        if GEMINI_AVAILABLE:
            print("✅ Gemini AI marked as available in server")
        else:
            print("❌ Gemini AI marked as unavailable in server")
    except ImportError as e:
        print(f"❌ Cannot check server integration: {e}")
    
    print()
    
    # Summary and Recommendations
    print("� INTEGRATION STATUS SUMMARY:")
    print("=" * 50)
    
    issues = []
    
    if not api_key:
        issues.append("Missing GEMINI_API_KEY")
    
    if not os.path.exists('server/gemini_ai_integration.py'):
        issues.append("Missing gemini_ai_integration.py")
    
    try:
        import google.generativeai
    except ImportError:
        issues.append("google-generativeai package not installed")
    
    if not issues:
        print("🎉 GEMINI AI FULLY INTEGRATED!")
        print("✅ All components are properly configured")
        print("� Ready for emotion detection and chatbot")
    else:
        print("⚠️ INTEGRATION ISSUES FOUND:")
        for i, issue in enumerate(issues, 1):
            print(f"   {i}. {issue}")
        
        print("\n💡 SOLUTIONS:")
        if "Missing GEMINI_API_KEY" in issues:
            print("🔑 Set up API Key:")
            print("   1. Go to: https://makersuite.google.com/app/apikey")
            print("   2. Create new API key")
            print("   3. Copy .env.example to .env")
            print("   4. Add your API key to .env file")
            print("   5. Or set environment variable:")
            print("      Windows: set GEMINI_API_KEY=your_key_here")
            print("      Linux/Mac: export GEMINI_API_KEY=your_key_here")
        
        if "google-generativeai package not installed" in issues:
            print("📦 Install Package:")
            print("   pip install google-generativeai")
    
    print("=" * 50)

def create_env_file():
    """Create .env file with API key"""
    print("🔧 CREATING .ENV FILE")
    print("=" * 30)
    
    if os.path.exists('.env'):
        print("⚠️ .env file already exists")
        overwrite = input("Do you want to overwrite it? (y/n): ").lower()
        if overwrite != 'y':
            print("❌ Cancelled")
            return
    
    print("📝 Please provide your Gemini API key:")
    print("   Get it from: https://makersuite.google.com/app/apikey")
    
    api_key = input("Enter your Gemini API key: ").strip()
    
    if not api_key:
        print("❌ No API key provided")
        return
    
    try:
        with open('.env', 'w') as f:
            f.write(f"# Gemini AI API Key\n")
            f.write(f"GEMINI_API_KEY={api_key}\n")
        
        print("✅ .env file created successfully!")
        print("🔒 Make sure .env is in .gitignore (it should be)")
        
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")

def main():
    """Main function"""
    print("🎯\ GEMINI AI INTEGRATION TESTER")
    print("=" * 60)
    print()
    
    # Test integration
    test_gemini_integration()
    
    # Offer to create .env file if needed
    if not os.getenv('GEMINI_API_KEY') and not os.path.exists('.env'):
        print()
        create_env = input("Do you want to create .env file with API key? (y/n): ").lower()
        if create_env == 'y':
            create_env_file()

if __name__ == "__main__":
    main()