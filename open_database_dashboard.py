#!/usr/bin/env python3
"""
Open Database Dashboard - ALL Users Can Access
Opens the database dashboard that shows ALL database records to ALL authenticated users
"""

import webbrowser
import time
import subprocess
import sys
import os
from pathlib import Path

def check_server_running():
    """Check if the server is running"""
    try:
        import requests
        response = requests.get("http://localhost:5000/", timeout=3)
        return response.status_code == 200
    except:
        return False

def start_server():
    """Start the Flask server"""
    print("🚀 Starting AURA server...")
    
    # Find the server file
    server_paths = [
        "sleepy/server/app.py",
        "server/app.py", 
        "app.py"
    ]
    
    server_file = None
    for path in server_paths:
        if os.path.exists(path):
            server_file = path
            break
    
    if not server_file:
        print("❌ Could not find server file (app.py)")
        return None
    
    try:
        # Start server in background
        process = subprocess.Popen([
            sys.executable, server_file
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        print(f"⏳ Server starting... (PID: {process.pid})")
        
        # Wait for server to start
        for i in range(30):  # Wait up to 30 seconds
            if check_server_running():
                print("✅ Server is running!")
                return process
            time.sleep(1)
            print(f"⏳ Waiting for server... ({i+1}/30)")
        
        print("❌ Server failed to start within 30 seconds")
        process.terminate()
        return None
        
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        return None

def main():
    """Main function"""
    print("📊 AURA DATABASE DASHBOARD")
    print("=" * 40)
    print("🔓 ALL authenticated users can view ALL database records")
    print("📋 View 292+ records across 7 database tables")
    print("🛠️  Complete CRUD operations available")
    
    # Check if server is running
    if not check_server_running():
        print("\n⚠️  Server not running. Starting server...")
        server_process = start_server()
        if not server_process:
            print("\n❌ Failed to start server. Please start manually:")
            print("   python sleepy/server/app.py")
            return False
    else:
        print("\n✅ Server is already running!")
        server_process = None
    
    # Open database dashboard
    dashboard_url = "http://localhost:5000/admin.html"
    print(f"\n🌐 Opening Database Dashboard: {dashboard_url}")
    
    try:
        webbrowser.open(dashboard_url)
        print("✅ Database dashboard opened in browser!")
    except Exception as e:
        print(f"❌ Could not open browser: {e}")
        print(f"📋 Please manually open: {dashboard_url}")
    
    print("\n📝 USAGE INSTRUCTIONS:")
    print("1. 🔐 Login with any user account:")
    print("   - Admin: admin@aura.com / admin123")
    print("   - Regular: regular@test.com / testpass123")
    print("   - Any other registered user")
    print("\n2. 📊 View Database Tables:")
    print("   - Users (15+ records)")
    print("   - Doctors (6+ records)")
    print("   - Appointments (9+ records)")
    print("   - Chat History (189+ records)")
    print("   - Mood Entries (58+ records)")
    print("   - Payments (4+ records)")
    print("   - Emotion Detection (11+ records)")
    print("\n3. 🛠️  Available Actions:")
    print("   - View all records in each table")
    print("   - Create new records")
    print("   - Edit existing records")
    print("   - Delete records")
    print("   - Export data to CSV")
    print("   - Real-time statistics")
    
    print("\n🎯 KEY FEATURES:")
    print("✅ ALL users can access (not admin-only)")
    print("✅ View ALL database records")
    print("✅ Complete CRUD operations")
    print("✅ Real-time data updates")
    print("✅ Export functionality")
    print("✅ Responsive design")
    
    if server_process:
        print(f"\n⚠️  Server running in background (PID: {server_process.pid})")
        print("   Press Ctrl+C to stop the server when done")
        
        try:
            # Keep script running
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n\n🛑 Stopping server...")
            server_process.terminate()
            server_process.wait()
            print("✅ Server stopped")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)