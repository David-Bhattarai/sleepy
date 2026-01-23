#!/usr/bin/env python3
"""
AURA Admin Panel Access Guide
Simple guide to access and use admin panel
"""

import webbrowser
import requests
import time

def check_server():
    """Check if server is running"""
    try:
        response = requests.get("http://localhost:5000", timeout=3)
        return True
    except:
        return False

def open_admin_panel():
    """Open admin panel in browser"""
    if check_server():
        print("Server is running - Opening admin panel...")
        webbrowser.open("http://localhost:5000/admin.html")
        return True
    else:
        print("Server is not running!")
        print("Please start server first:")
        print("  cd sleepy/server")
        print("  python app.py")
        return False

def main():
    print("AURA ADMIN PANEL ACCESS GUIDE")
    print("=" * 40)
    print()
    print("ADMIN LOGIN CREDENTIALS:")
    print("Email:    admin@aura.com")
    print("Password: admin123")
    print("URL:      http://localhost:5000/admin.html")
    print()
    print("ADMIN PANEL FEATURES:")
    print("- Users Management (13 users)")
    print("- Doctors Management (6 doctors)")
    print("- Appointments Tracking (4 appointments)")
    print("- Chat History (181 messages)")
    print("- Mood Entries (48 entries)")
    print("- Payment Records")
    print("- Emotion Detection Data")
    print("- Real-time Statistics")
    print("- Data Export (CSV)")
    print()
    
    choice = input("Open admin panel now? (y/n): ").lower()
    if choice in ['y', 'yes', 'ha']:
        if open_admin_panel():
            print("Admin panel opened in browser!")
            print("Login with credentials shown above.")
        else:
            print("Could not open admin panel.")
    else:
        print("To access manually:")
        print("1. Start server: cd sleepy/server && python app.py")
        print("2. Open: http://localhost:5000/admin.html")
        print("3. Login with admin@aura.com / admin123")

if __name__ == "__main__":
    main()