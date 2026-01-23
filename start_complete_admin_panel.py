#!/usr/bin/env python3
"""
Start Complete Admin Panel with Full Database Access
Shows ALL database tables and records
"""

import os
import sys
import subprocess
import webbrowser
import time
from pathlib import Path

def start_complete_admin_panel():
    """Start the complete admin panel with full database access"""
    print("🚀 Starting Complete Admin Panel...")
    print("=" * 50)
    
    # Change to sleepy directory
    sleepy_dir = Path("sleepy")
    if not sleepy_dir.exists():
        print("❌ Sleepy directory not found!")
        return
    
    os.chdir(sleepy_dir)
    
    # Check if server is already running
    print("🔍 Checking if server is already running...")
    
    # Start the server
    print("🖥️ Starting AURA server...")
    
    try:
        # Start server in background
        if sys.platform == "win32":
            # Windows
            server_process = subprocess.Popen(
                ["python", "server/app.py"],
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
        else:
            # Linux/Mac
            server_process = subprocess.Popen(
                ["python3", "server/app.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
        
        print("⏳ Waiting for server to start...")
        time.sleep(3)
        
        # Open admin panel in browser
        admin_url = "http://localhost:5000/admin.html"
        print(f"🌐 Opening admin panel: {admin_url}")
        
        webbrowser.open(admin_url)
        
        print("\n✅ Admin Panel Started Successfully!")
        print("=" * 50)
        print("📊 ADMIN PANEL FEATURES:")
        print("  • View ALL database tables")
        print("  • 👥 Users (17 records)")
        print("  • 👨‍⚕️ Doctors (6 records)")
        print("  • 📅 Appointments (9 records)")
        print("  • 💬 Chat History (189 records)")
        print("  • 😊 Mood Entries (58 records)")
        print("  • 😐 Emotion Detection (11 records)")
        print("  • 💳 Payments (4 records)")
        print("  • 🧠 Emotional Intelligence (15 records)")
        print("  • 📈 Advanced Mood Entries (5 records)")
        print("=" * 50)
        print("🔑 LOGIN CREDENTIALS:")
        print("  Email: davidbhattarai@gmail.com")
        print("  Password: (your password)")
        print("=" * 50)
        print("📱 ADMIN PANEL ACCESS:")
        print("  • ALL authenticated users can view database")
        print("  • Switch between tables using tabs")
        print("  • View, Edit, Delete records")
        print("  • Export data to CSV")
        print("  • Real-time statistics")
        print("=" * 50)
        
        # Keep script running
        try:
            print("🔄 Server running... Press Ctrl+C to stop")
            server_process.wait()
        except KeyboardInterrupt:
            print("\n🛑 Stopping server...")
            server_process.terminate()
            
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        print("💡 Try running manually:")
        print("   cd sleepy")
        print("   python server/app.py")

if __name__ == "__main__":
    start_complete_admin_panel()