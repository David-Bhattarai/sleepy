#!/usr/bin/env python3
"""
Integrate Gemini API Key Now
Yo script le immediately Gemini API key integrate garcha
"""

import os
import subprocess
import sys

def install_gemini_package():
    """Install Google GenerativeAI package"""
    print("📦 Installing Google GenerativeAI package...")
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "google-generativeai"])
        print("✅ google-generativeai installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Installation failed: {e}")
        return False

def set_environment_variable():
    """Set environment variable for current session"""
    api_key = "AIzaSyA_y_FXdRR7RPnM-tcfS5jSyozBN7lrrjo"
    os.environ['GEMINI_API_KEY'] = api_key
    print("✅ Environment variable set for current session")
    return True

def test_quick_integration():
    """Quick test of Gemini integration"""
    print("🧪 Quick integration test...")
    
    try:
        import google.generativeai as genai
        
        api_key = os.getenv('GEMINI_API_KEY')
        genai.configure(api_key=api_key)
        
        model = genai.GenerativeModel('models/gemini-2.5-flash')
        response = model.generate_content("Say 'Gemini AI is now integrated!'")
        
        print(f"✅ Test successful: {response.text}")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def update_server_status():
    """Update server to recognize Gemini is available"""
    print("🔧 Updating server integration status...")
    
    try:
        # Check if server files exist
        server_files = [
            'server/gemini_ai_integration.py',
            'server/gemini_emotion_detector.py'