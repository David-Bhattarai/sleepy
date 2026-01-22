#!/usr/bin/env python3
"""
Database Viewer Script for AURA Mental Health Platform
View all data in a formatted way
"""

import sqlite3
import os
from datetime import datetime

def view_database():
    """View all database data in formatted way"""
    print("🔍 AURA Database Viewer")
    print("=" * 50)
    
    # Change to server directory
    server_dir = os.path.join(os.getcwd(), 'server')
    db_file = os.path.join(server_dir, 'database.db')
    
    if not os.path.exists(db_file):
        print("❌ Database file not found!")
        return
    
    with sqlite3.connect(db_file) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Users
        print("\n👥 USERS:")
        cursor.execute("SELECT name, email, phone, is_admin, created_at FROM users")
        users = cursor.fetchall()
        for user in users:
            admin_status = "👑 Admin" if user['is_admin'] else "👤 User"
            print(f"  • {user['name']} ({user['email']}) - {admin_status}")
            print(f"    Phone: {user['phone'] or 'Not provided'}")
            print(f"    Joined: {user['created_at']}")
            print()
        
        # Doctors
        print("\n👨‍⚕️ DOCTORS:")
        cursor.execute("SELECT name, specialty, price_per_session, experience_years FROM doctors")
        doctors = cursor.fetchall()
        for doctor in doctors:
            print(f"  • {doctor['name']} - {doctor['specialty']}")
            print(f"    Price: ${doctor['price_per_session']}/session")
            print(f"    Experience: {doctor['experience_years']} years")
            print()
        
        # Appointments
        print("\n📅 APPOINTMENTS:")
        cursor.execute("""
            SELECT a.appointment_date, a.appointment_time, a.status, a.payment_status,
                   u.name as user_name, d.name as doctor_name, a.payment_amount
            FROM appointments a
            JOIN users u ON a.user_id = u.id
            JOIN doctors d ON a.doctor_id = d.id
            ORDER BY a.appointment_date DESC, a.appointment_time DESC
        """)
        appointments = cursor.fetchall()
        for apt in appointments:
            print(f"  • {apt['user_name']} → {apt['doctor_name']}")
            print(f"    Date: {apt['appointment_date']} at {apt['appointment_time']}")
            print(f"    Status: {apt['status']} | Payment: {apt['payment_status']}")
            print(f"    Amount: ${apt['payment_amount'] or 'Not set'}")
            print()
        
        # Mood Entries
        print("\n😊 MOOD ENTRIES (Recent 10):")
        cursor.execute("""
            SELECT s.mood_rating, s.mood_notes, s.timestamp, u.name as user_name
            FROM simple_mood_entries s
            JOIN users u ON s.user_id = u.id
            ORDER BY s.timestamp DESC
            LIMIT 10
        """)
        moods = cursor.fetchall()
        mood_emojis = {1: "😢", 2: "😔", 3: "😐", 4: "😊", 5: "😄"}
        for mood in moods:
            emoji = mood_emojis.get(mood['mood_rating'], "😐")
            print(f"  • {mood['user_name']}: {emoji} {mood['mood_rating']}/5")
            print(f"    Note: {mood['mood_notes'] or 'No notes'}")
            print(f"    Time: {mood['timestamp']}")
            print()
        
        # Chat History
        print("\n💬 RECENT CHAT HISTORY:")
        cursor.execute("""
            SELECT c.user_message, c.ai_response, c.sentiment, c.timestamp, u.name as user_name
            FROM chat_history c
            JOIN users u ON c.user_id = u.id
            ORDER BY c.timestamp DESC
            LIMIT 5
        """)
        chats = cursor.fetchall()
        for chat in chats:
            print(f"  • {chat['user_name']} ({chat['sentiment']}):")
            print(f"    User: {chat['user_message'][:100]}...")
            print(f"    AI: {chat['ai_response'][:100]}...")
            print(f"    Time: {chat['timestamp']}")
            print()
        
        # Payments
        print("\n💳 PAYMENTS:")
        cursor.execute("""
            SELECT p.amount, p.payment_method, p.payment_status, p.payment_date, u.name as user_name
            FROM payments p
            JOIN users u ON p.user_id = u.id
            ORDER BY p.payment_date DESC
        """)
        payments = cursor.fetchall()
        for payment in payments:
            print(f"  • {payment['user_name']}: ${payment['amount']}")
            print(f"    Method: {payment['payment_method']} | Status: {payment['payment_status']}")
            print(f"    Date: {payment['payment_date']}")
            print()
        
        # Statistics
        print("\n📊 STATISTICS:")
        cursor.execute("SELECT COUNT(*) FROM users")
        total_users = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM appointments")
        total_appointments = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM simple_mood_entries")
        total_moods = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM chat_history")
        total_chats = cursor.fetchone()[0]
        
        cursor.execute("SELECT SUM(amount) FROM payments WHERE payment_status = 'completed'")
        total_revenue = cursor.fetchone()[0] or 0
        
        print(f"  • Total Users: {total_users}")
        print(f"  • Total Appointments: {total_appointments}")
        print(f"  • Total Mood Entries: {total_moods}")
        print(f"  • Total Chat Messages: {total_chats}")
        print(f"  • Total Revenue: ${total_revenue}")
        
        print("\n✅ Database view complete!")

if __name__ == "__main__":
    view_database()