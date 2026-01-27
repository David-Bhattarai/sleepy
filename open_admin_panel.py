#!/usr/bin/env python3
"""
Admin Panel Access Guide
Step-by-step guide to open and use admin panel
"""

import webbrowser
import time
import requests

def check_server_status():
    """Check if server is running"""
    print("🔍 Checking server status...")
    try:
        response = requests.get("http://localhost:5000", timeout=5)
        print("✅ Server is running")
        return True
    except:
        print("❌ Server is not running")
        return False

def open_admin_panel():
    """Open admin panel in browser"""
    print("🌐 Opening admin panel...")
    
    # Check server first
    if not check_server_status():
        print("\n⚠️ Server is not running. Please start server first:")
        print("   1. Open terminal/command prompt")
        print("   2. Navigate to: cd sleepy/server")
        print("   3. Run: python app.py")
        print("   4. Then run this script again")
        return False
    
    # Open admin panel
    admin_url = "http://localhost:5000/admin.html"
    print(f"🚀 Opening: {admin_url}")
    
    try:
        webbrowser.open(admin_url)
        print("✅ Admin panel opened in browser")
        return True
    except Exception as e:
        print(f"❌ Error opening browser: {e}")
        print(f"   Please manually open: {admin_url}")
        return False

def show_admin_credentials():
    """Show admin login credentials"""
    print("\n🔐 ADMIN LOGIN CREDENTIALS:")
    print("=" * 40)
    print("Email:    admin@mindbridge.com")
    print("Password: admin123")
    print("URL:      http://localhost:5000/admin.html")
    print("=" * 40)

def show_admin_features():
    """Show admin panel features"""
    print("\n📊 ADMIN PANEL FEATURES:")
    print("=" * 40)
    print("1. 👥 Users Management - View all users")
    print("2. 👨‍⚕️ Doctors Management - Manage doctors")
    print("3. 📅 Appointments - Track appointments")
    print("4. 💬 Chat History - Monitor conversations")
    print("5. 😊 Mood Entries - View mood tracking")
    print("6. 💳 Payments - Payment records")
    print("7. 😐 Emotion Detection - Emotion data")
    print("8. 📈 Statistics - Real-time stats")
    print("9. 📤 Export Data - Download CSV files")
    print("=" * 40)

def main():
    """Main function"""
    print("🛠️ MindBridge - NCIT Final Year Project ADMIN PANEL ACCESS GUIDE")
    print("=" * 50)
    
    # Show credentials
    show_admin_credentials()
    
    # Show features
    show_admin_features()
    
    # Ask user if they want to open admin panel
    print("\n❓ Do you want to open admin panel now? (y/n): ", end="")
    choice = input().lower().strip()
    
    if choice in ['y', 'yes', 'ha', 'हो']:
        if open_admin_panel():
            print("\n🎉 Admin panel opened successfully!")
            print("\n📝 Next steps:")
            print("1. Login with the credentials shown above")
            print("2. Navigate through different database tables")
            print("3. Use export functionality as needed")
            print("4. Monitor real-time statistics")
        else:
            print("\n⚠️ Could not open admin panel automatically")
            print("Please manually open: http://localhost:5000/admin.html")
    else:
        print("\n📝 To access admin panel manually:")
        print("1. Make sure server is running (python sleepy/server/app.py)")
        print("2. Open browser and go to: http://localhost:5000/admin.html")
        print("3. Login with credentials shown above")

if __name__ == "__main__":
    main()