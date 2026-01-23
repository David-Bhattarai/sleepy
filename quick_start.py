#!/usr/bin/env python3
"""
AURA Mental Health AI - Quick Start Script
Easy one-click startup for the complete system
"""

import os
import sys
import subprocess
import time

def print_banner():
    """Print welcome banner"""
    print("=" * 70)
    print("🚀 AURA MENTAL HEALTH AI SYSTEM")
    print("=" * 70)
    print("🤖 Intelligent Chatbot with Google Gemini AI")
    print("😊 Real Face Emotion Detection (98% accuracy)")
    print("💬 Therapeutic Conversations & Mental Health Support")
    print("📊 Mood Tracking & Analytics")
    print("🎥 Video Consultation Platform")
    print("=" * 70)

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ required. Current version:", sys.version)
        print("Please upgrade Python and try again.")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatible")
    return True

def check_dependencies():
    """Check if required packages are installed"""
    print("\n🔍 Checking Dependencies...")
    
    required_packages = [
        'flask',
        'tensorflow',
        'google.generativeai',
        'PIL',
        'numpy'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'PIL':
                import PIL
            elif package == 'google.generativeai':
                import google.generativeai
            else:
                __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - Missing")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️ Missing packages: {', '.join(missing_packages)}")
        print("Installing missing packages...")
        
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
            print("✅ Dependencies installed successfully!")
        except subprocess.CalledProcessError:
            print("❌ Failed to install dependencies")
            print("Please run manually: pip install -r requirements.txt")
            return False
    
    return True

def check_api_key():
    """Check if Gemini API key is configured"""
    print("\n🔑 Checking API Configuration...")
    
    # Check environment variable
    api_key = os.getenv('GEMINI_API_KEY')
    if api_key:
        print(f"✅ API Key found in environment: {api_key[:10]}...{api_key[-5:]}")
        return True
    
    # Check .env file
    if os.path.exists('.env'):
        try:
            with open('.env', 'r') as f:
                for line in f:
                    if line.startswith('GEMINI_API_KEY='):
                        key = line.split('=', 1)[1].strip()
                        if key and key != 'your_gemini_api_key_here':
                            print(f"✅ API Key found in .env file: {key[:10]}...{key[-5:]}")
                            return True
        except Exception as e:
            print(f"⚠️ Error reading .env file: {e}")
    
    print("⚠️ No Gemini API key found")
    print("   - System will work with fallback responses")
    print("   - For full AI features, add API key to .env file")
    print("   - Get free API key: https://makersuite.google.com/app/apikey")
    
    return False

def start_system():
    """Start the AURA system"""
    print("\n🚀 Starting AURA System...")
    
    try:
        # Check if we have API key for full features
        has_api_key = check_api_key()
        
        if has_api_key:
            print("🎯 Starting with FULL AI FEATURES...")
            if os.path.exists('start_server_with_gemini.py'):
                subprocess.run([sys.executable, 'start_server_with_gemini.py'])
            else:
                # Fallback to manual start
                os.environ['GEMINI_API_KEY'] = get_api_key_from_env()
                os.chdir('sleepy/server')
                subprocess.run([sys.executable, 'app.py'])
        else:
            print("🔄 Starting with FALLBACK MODE...")
            os.chdir('sleepy/server')
            subprocess.run([sys.executable, 'app.py'])
            
    except KeyboardInterrupt:
        print("\n🛑 System stopped by user")
    except Exception as e:
        print(f"❌ Error starting system: {e}")
        print("\nTroubleshooting:")
        print("1. Check if all files are present")
        print("2. Run: python test_complete_system.py")
        print("3. Check COMPLETE_PROJECT_SETUP_GUIDE.md")

def get_api_key_from_env():
    """Get API key from .env file"""
    if os.path.exists('.env'):
        try:
            with open('.env', 'r') as f:
                for line in f:
                    if line.startswith('GEMINI_API_KEY='):
                        return line.split('=', 1)[1].strip()
        except:
            pass
    return None

def show_system_info():
    """Show system information and access URLs"""
    print("\n" + "=" * 70)
    print("🎉 AURA SYSTEM INFORMATION")
    print("=" * 70)
    print("📱 Web Interface:")
    print("   - Local: http://127.0.0.1:5000")
    print("   - Network: http://192.168.18.3:5000")
    print()
    print("🎯 Features Available:")
    print("   - 🤖 AI Chatbot (Therapeutic Conversations)")
    print("   - 😊 Emotion Detection (Real-time Face Analysis)")
    print("   - 📊 Mood Tracking (Daily Mental Health Monitoring)")
    print("   - 🎥 Video Consultation (Professional Support)")
    print("   - 🔐 Secure User Authentication")
    print()
    print("📚 Documentation:")
    print("   - Setup Guide: COMPLETE_PROJECT_SETUP_GUIDE.md")
    print("   - Security Info: SECURITY_GUIDE.md")
    print("   - Test Results: FINAL_TEST_RESULTS.md")
    print()
    print("🧪 Testing:")
    print("   - Full Test: python test_complete_system.py")
    print("   - AI Test: python test_gemini_system.py")
    print("=" * 70)

def main():
    """Main startup function"""
    print_banner()
    
    # System checks
    if not check_python_version():
        return
    
    if not check_dependencies():
        return
    
    # Show system info
    show_system_info()
    
    # Ask user if they want to start
    print("\n🚀 Ready to start AURA Mental Health AI System!")
    choice = input("Start now? (y/n): ").lower().strip()
    
    if choice in ['y', 'yes', '']:
        start_system()
    else:
        print("👋 Setup complete! Run this script again when ready to start.")
        print("Or manually start with: python start_server_with_gemini.py")

if __name__ == "__main__":
    main()