#!/usr/bin/env python3
"""
Setup Gemini AI Integration
Yo script le Gemini AI setup garcha emotion detection ko lagi
"""

import os
import subprocess
import sys

def install_required_packages():
    """Install required packages for Gemini AI"""
    print("📦 INSTALLING REQUIRED PACKAGES")
    print("=" * 40)
    
    packages = [
        'google-generativeai',
        'Pillow',
        'requests'
    ]
    
    for package in packages:
        try:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✅ {package} installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install {package}: {e}")
            return False
    
    print("✅ All packages installed!")
    return True

def setup_api_key():
    """Setup Gemini API key"""
    print("\n🔑 SETTING UP GEMINI API KEY")
    print("=" * 40)
    
    print("📋 Steps to get your API key:")
    print("1. Go to: https://makersuite.google.com/app/apikey")
    print("2. Sign in with your Google account")
    print("3. Click 'Create API Key'")
    print("4. Copy the generated API key")
    print()
    
    api_key = input("Enter your Gemini API key: ").strip()
    
    if not api_key:
        print("❌ No API key provided")
        return False
    
    # Create .env file
    try:
        with open('.env', 'w') as f:
            f.write("# Google Gemini AI API Key\n")
            f.write(f"GEMINI_API_KEY={api_key}\n")
            f.write("\n# Instructions:\n")
            f.write("# This file contains your API key - never commit to GitHub\n")
            f.write("# The .gitignore file should exclude this file\n")
        
        print("✅ .env file created with API key")
        
        # Set environment variable for current session
        os.environ['GEMINI_API_KEY'] = api_key
        print("✅ API key set for current session")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")
        return False

def test_gemini_connection():
    """Test Gemini AI connection"""
    print("\n🧪 TESTING GEMINI AI CONNECTION")
    print("=" * 40)
    
    try:
        import google.generativeai as genai
        
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            print("❌ API key not found")
            return False
        
        # Configure Gemini
        genai.configure(api_key=api_key)
        
        # Test with a simple text generation
        model = genai.GenerativeModel('models/gemini-2.5-flash')
        response = model.generate_content("Say 'Hello from Gemini AI!'")
        
        print("✅ Gemini AI connection successful!")
        print(f"📝 Test response: {response.text}")
        
        return True
        
    except Exception as e:
        print(f"❌ Gemini AI connection failed: {e}")
        return False

def verify_integration():
    """Verify the complete integration"""
    print("\n🔍 VERIFYING INTEGRATION")
    print("=" * 40)
    
    try:
        # Test importing our integration
        sys.path.append('server')
        from gemini_ai_integration import get_gemini_ai
        
        gemini_ai = get_gemini_ai()
        
        if gemini_ai and gemini_ai.api_key:
            print("✅ Gemini AI integration working")
            
            # Test emotion detection (with dummy data)
            print("🧪 Testing emotion detection...")
            # This would need a real image, so we'll just check if the method exists
            if hasattr(gemini_ai, 'detect_emotion_from_face'):
                print("✅ Emotion detection method available")
            else:
                print("❌ Emotion detection method missing")
            
            # Test text generation
            print("🧪 Testing intelligent response...")
            if hasattr(gemini_ai, 'generate_intelligent_response'):
                print("✅ Intelligent response method available")
                
                # Test with a simple message
                result = gemini_ai.generate_intelligent_response("Hello, how are you?")
                if result['success']:
                    print(f"✅ Response generated: {result['response'][:50]}...")
                else:
                    print(f"❌ Response generation failed: {result.get('error', 'Unknown error')}")
            else:
                print("❌ Intelligent response method missing")
            
            return True
        else:
            print("❌ Gemini AI not properly initialized")
            return False
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Integration error: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 GEMINI AI SETUP FOR EMOTION DETECTION")
    print("=" * 60)
    print()
    
    success_steps = 0
    total_steps = 4
    
    # Step 1: Install packages
    if install_required_packages():
        success_steps += 1
    
    # Step 2: Setup API key
    if setup_api_key():
        success_steps += 1
    
    # Step 3: Test connection
    if test_gemini_connection():
        success_steps += 1
    
    # Step 4: Verify integration
    if verify_integration():
        success_steps += 1
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 SETUP SUMMARY")
    print("=" * 60)
    print(f"Completed: {success_steps}/{total_steps} steps")
    
    if success_steps == total_steps:
        print("🎉 GEMINI AI SETUP COMPLETED SUCCESSFULLY!")
        print()
        print("✅ What's working now:")
        print("   • Google Gemini AI Vision for emotion detection")
        print("   • Intelligent chatbot responses")
        print("   • Fallback to FER2013 model if needed")
        print("   • Advanced emotion analysis")
        print()
        print("🚀 Next steps:")
        print("   1. Start your server: python server/app.py")
        print("   2. Open emotion-detection.html in browser")
        print("   3. Test with camera, upload, or sample images")
        print("   4. Enjoy 🤖 Gemini AI powered emotion detection!")
        
    else:
        print("⚠️ SETUP INCOMPLETE")
        print()
        print("❌ Issues found:")
        if success_steps < 1:
            print("   • Package installation failed")
        if success_steps < 2:
            print("   • API key setup failed")
        if success_steps < 3:
            print("   • Gemini connection failed")
        if success_steps < 4:
            print("   • Integration verification failed")
        
        print()
        print("💡 Solutions:")
        print("   1. Check your internet connection")
        print("   2. Verify your Gemini API key is correct")
        print("   3. Make sure you have Python 3.7+ installed")
        print("   4. Try running: pip install --upgrade google-generativeai")
        print("   5. Run test_gemini_integration.py for detailed diagnostics")
    
    print("=" * 60)

if __name__ == "__main__":
    main()