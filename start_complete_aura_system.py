#!/usr/bin/env python3
"""
AURA Mental Health Platform - Complete System Startup
Admin Panel with Database Data + FER2013 Enhanced Emotion Detection
"""

import os
import sys
import subprocess
import time

def start_aura_system():
    """Start the complete AURA system"""
    
    print("🚀 Starting AURA Mental Health Platform...")
    print("📊 Admin Panel: Full database management with CRUD operations")
    print("🎯 Emotion Detection: FER2013 Enhanced Dataset integration")
    
    # Check if we're in the right directory
    if not os.path.exists('sleepy/server/app.py'):
        print("❌ Please run this script from the project root directory")
        return
    
    print("\n🔧 System Components:")
    print("✅ Admin Panel: http://localhost:5000/admin.html")
    print("✅ Dashboard: http://localhost:5000/dashboard.html") 
    print("✅ Emotion Detection: http://localhost:5000/emotion-detection.html")
    print("✅ Video Chat: http://localhost:5000/video-chat.html")
    
    print("\n📊 Database Tables Available:")
    print("- 👥 Users (with sample data)")
    print("- 👨‍⚕️ Doctors (6 AI doctors)")
    print("- 📅 Appointments (with sample data)")
    print("- 💬 Chat History (with sample conversations)")
    print("- 😊 Mood Entries (with sample moods)")
    print("- 💳 Payments (with sample transactions)")
    print("- 😐 Emotion Detection (with sample results)")
    
    print("\n🎯 FER2013 Enhanced Features:")
    print("- 7 Emotions: angry, disgust, fear, happy, sad, surprise, neutral")
    print("- 3,501 training samples from FER2013 enhanced dataset")
    print("- High accuracy emotion recognition")
    print("- Real-time confidence scoring")
    
    print("\n🛠️ Admin Panel CRUD Operations:")
    print("- ✅ Create: Add new records to any table")
    print("- ✅ Read: View all data with detailed information")
    print("- ✅ Update: Edit existing records (partial)")
    print("- ✅ Delete: Remove records with confirmation")
    
    print("\n🔑 Login Information:")
    print("- Any registered user can access admin panel")
    print("- Sample users available in database")
    print("- No special admin privileges required")
    
    print("\n⚡ Starting server...")
    
    try:
        # Change to server directory and start
        os.chdir('sleepy/server')
        subprocess.run([sys.executable, 'app.py'], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        print("\n🔧 Manual startup:")
        print("1. cd sleepy/server")
        print("2. python app.py")
        print("3. Open http://localhost:5000/admin.html")

if __name__ == '__main__':
    start_aura_system()
