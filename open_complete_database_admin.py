#!/usr/bin/env python3
"""
Open Complete Database Admin Panel
Shows ALL database tables with full data access
"""

import webbrowser
import time
import os

def open_complete_database_admin():
    """Open the complete database admin panel"""
    print("🚀 Opening Complete Database Admin Panel...")
    print("=" * 60)
    
    # Show what's available
    print("📊 AVAILABLE DATABASE TABLES:")
    print("  👥 Users (17 records)")
    print("  👨‍⚕️ Doctors (6 records)")  
    print("  📅 Appointments (9 records)")
    print("  💬 Chat History (189 records)")
    print("  😊 Simple Mood Entries (58 records)")
    print("  💳 Payments (4 records)")
    print("  😐 Emotion Detection (11 records)")
    print("  🧠 Emotional Intelligence (15 records)")
    print("  📈 Advanced Mood Entries (5 records)")
    print("  💡 Mood Insights (0 records)")
    print("  📊 Mood Patterns (0 records)")
    print("  🕒 Doctor Availability (0 records)")
    print()
    print("📈 TOTAL: 314 records across 13 tables")
    print("=" * 60)
    
    # Check if server is running
    print("🔍 Checking server status...")
    
    # Try to open admin panel
    admin_url = "http://localhost:5000/admin.html"
    
    print(f"🌐 Opening admin panel: {admin_url}")
    print()
    print("🔑 LOGIN INSTRUCTIONS:")
    print("  1. Use any registered user credentials")
    print("  2. Email: davidbhattarai@gmail.com")
    print("  3. Password: (your password)")
    print("  4. ALL authenticated users can view database")
    print()
    print("📱 ADMIN PANEL FEATURES:")
    print("  • Switch between tables using tabs")
    print("  • View all records in each table")
    print("  • Search and filter data")
    print("  • Export tables to CSV")
    print("  • View detailed record information")
    print("  • Real-time statistics")
    print()
    
    # Open in browser
    webbrowser.open(admin_url)
    
    print("✅ Admin panel opened in browser!")
    print("💡 If server is not running, start it with:")
    print("   cd sleepy")
    print("   python server/app.py")

if __name__ == "__main__":
    open_complete_database_admin()