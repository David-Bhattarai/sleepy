#!/usr/bin/env python3
"""
Start AURA Server with TensorFlow Fixes Applied
This script sets environment variables and starts the server
"""

import os
import sys
import subprocess

def set_environment_variables():
    """Set environment variables to fix TensorFlow warnings"""
    print("🔧 Setting environment variables...")
    
    # Disable TensorFlow oneDNN warnings
    os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
    
    # Disable TensorFlow GPU warnings (if no GPU)
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
    
    # Set Keras backend
    os.environ['KERAS_BACKEND'] = 'tensorflow'
    
    print("✅ Environment variables set:")
    print("   - TF_ENABLE_ONEDNN_OPTS=0 (disables oneDNN warnings)")
    print("   - TF_CPP_MIN_LOG_LEVEL=2 (reduces TensorFlow logging)")
    print("   - KERAS_BACKEND=tensorflow (sets Keras backend)")

def start_server():
    """Start the AURA server"""
    print("\n🚀 Starting AURA Mental Health AI System...")
    print("=" * 60)
    
    try:
        # Change to server directory
        server_dir = os.path.join(os.path.dirname(__file__), 'sleepy', 'server')
        if os.path.exists(server_dir):
            os.chdir(server_dir)
            print(f"📁 Changed to server directory: {server_dir}")
        
        # Start the server
        print("🌟 Starting Flask server...")
        print("🔗 Server will be available at: http://127.0.0.1:5000")
        print("🎯 Press Ctrl+C to stop the server")
        print("=" * 60)
        
        # Run the server
        subprocess.run([sys.executable, 'app.py'], check=True)
        
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user")
    except FileNotFoundError:
        print("❌ Server directory not found. Make sure you're in the project root.")
        print("💡 Try running from the main project directory")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        print("💡 Make sure all dependencies are installed:")
        print("   pip install -r requirements.txt")

def main():
    """Main function"""
    print("🎯 AURA Mental Health AI System - Fixed Startup")
    print("=" * 60)
    
    # Set environment variables first
    set_environment_variables()
    
    # Start the server
    start_server()

if __name__ == "__main__":
    main()