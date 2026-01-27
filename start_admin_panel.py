#!/usr/bin/env python3
"""
Start Admin Panel - Quick way to access admin panel
"""

import os
import sys
import subprocess
import webbrowser
import time
import requests

def check_server_running():
    """Check if server is already running"""
    try:
        response = requests.get("http://localhost:5000", timeout=3)
        return True
    except:
        return False

def start_server():
    """Start the Flask server"""
    print("🚀 Starting MindBridge - NCIT Final Year Project server...")
    
    # Change to server directory
    server_dir = "sleepy/server"
    if not os.path.exists(server_dir):
        print("❌ Server directory not found!")
        return False
    
    # Start server
    try:
        os.chdir(server_dir)
        subprocess.Popen([sys.executable, "app.py"], 
                        stdout=subprocess.DEVNULL, 
                        stderr=subprocess.DEVNULL)
        
        # Wait for server to start
        print("⏳ Waiting for server to start...")
        for i in range(10):
            time.sleep(1)
            if check_server_running():
                print("✅ Server started successfully!")
                return True
            print(f"   Waiting... ({i+1}/10)")
        
        print("⚠️ Server may have started but not responding")
        return True
        
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        return False

def open_admin_panel():
    """Open admin panel in browser"""
    admin_url = "http://localhost:5000/admin.html"
    
    print(f"🌐 Opening admin panel: {admin_url}")
    webbrowser.open(admin_url)
    
    print("\n🔑 ADMIN LOGIN CREDENTIALS:")
    print("=" * 30)
    print("Email:    admin@mindbridge.co")
    print("Password: admin123")
    print("=" * 30)

def main():
    """Main function"""
    print("🛠️ MindBridge - NCIT Final Year Project ADMIN PANEL STARTER")
    print("=" * 40)
    
    # Check if server is already running
    if check_server_running():
        print("✅ Server is already running!")
        open_admin_panel()
        return
    
    # Start server
    if start_server():
        time.sleep(2)  # Give server time to fully start
        open_admin_panel()
        
        print("\n💡 Admin Panel Features:")
        print("   • View all database tables")
        print("   • Manage users and doctors")
        print("   • View appointments and payments")
        print("   • Monitor chat history")
        print("   • Export data to CSV")
        
        print("\n🔄 Server is running in background")
        print("   To stop: Press Ctrl+C in the server terminal")
        
    else:
        print("❌ Failed to start server")
        print("\n💡 Manual start:")
        print("   1. cd sleepy/server")
        print("   2. python app.py")
        print("   3. Open: http://localhost:5000/admin.html")

if __name__ == "__main__":
    main()