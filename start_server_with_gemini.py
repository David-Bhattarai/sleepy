#!/usr/bin/env python3
"""
Start Server with Gemini API Key
Properly set environment variable and start server
"""

import os
import subprocess
import sys

def start_server_with_api():
    """Start server with Gemini API key"""
    print("🚀 Starting Server with Gemini AI")
    print("=" * 50)
    
    # Set the API key as environment variable
    api_key = "AIzaSyAhVtegrJ6sXOp2Ri0AkI5_yQDGAGWsJxk"
    os.environ['GEMINI_API_KEY'] = api_key
    
    print(f"✅ API Key set: {api_key[:10]}...{api_key[-5:]}")
    print("🔄 Starting server with full Gemini AI features...")
    
    # Change to server directory and start
    try:
        os.chdir('sleepy/server')
        
        # Start the server with environment variable
        env = os.environ.copy()
        env['GEMINI_API_KEY'] = api_key
        
        subprocess.run([sys.executable, 'app.py'], env=env)
        
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")

if __name__ == "__main__":
    start_server_with_api()