#!/usr/bin/env python3
"""
Start Gemini Server - No TensorFlow Required
Quick start script for emotion detection with Gemini AI
"""

import os
import sys
import subprocess

def main():
    print("🚀 STARTING GEMINI AI EMOTION DETECTION SERVER")
    print("=" * 70)
    print("✅ TensorFlow-free version")
    print("🤖 Full Gemini AI integration")
    print("😊 All 7 emotions supported")
    print("=" * 70)
    
    # Set API key
    api_key = "AIzaSyA_y_FXdRR7RPnM-tcfS5jSyozBN7lrrjo"
    os.environ['GEMINI_API_KEY'] = api_key
    print(f"🔑 API Key set: {api_key[:20]}...")
    
    # Check if we're in the right directory
    if not os.path.exists('server'):
        print("❌ 'server' directory not found")
        print("💡 Make sure you're in the project root directory")
        return
    
    # Check if the TensorFlow-free server exists
    server_file = "server/app_gemini_only.py"
    if not os.path.exists(server_file):
        print(f"❌ Server file not found: {server_file}")
        print("💡 Run fix_tensorflow_error.py first")
        return
    
    print("✅ Server file found")
    print("🌐 Starting server on http://localhost:5000")
    print("📱 Open client/emotion-detection.html after server starts")
    print("=" * 70)
    print("🎯 WHAT YOU CAN DO:")
    print("   📸 Camera Detection - Real-time emotion detection")
    print("   📁 Image Upload - Upload any face image")
    print("   🖼️ Sample Testing - 84 pre-loaded emotion samples")
    print("   🤖 Gemini AI - Advanced facial expression analysis")
    print("=" * 70)
    print("🚀 Server starting...")
    print()
    
    # Change to server directory and start
    try:
        os.chdir('server')
        subprocess.run([sys.executable, 'app_gemini_only.py'])
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Server error: {e}")
        print("💡 Try running: python fix_tensorflow_error.py")

if __name__ == "__main__":
    main()