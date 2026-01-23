#!/usr/bin/env python3
"""
Setup Admin User for AURA Admin Panel
Creates an admin user in the database for testing admin panel functionality
"""

import sqlite3
import uuid
import bcrypt
from datetime import datetime

DB_FILE = 'sleepy/server/database.db'

def setup_admin_user():
    """Create admin user in database"""
    print("Setting up admin user...")
    
    try:
        # Connect to database
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        # Check if admin user already exists
        admin_email = "admin@aura.com"
        existing_admin = cursor.execute(
            "SELECT * FROM users WHERE email = ?", 
            (admin_email,)
        ).fetchone()
        
        if existing_admin:
            # Update existing user to be admin
            cursor.execute(
                "UPDATE users SET is_admin = 1 WHERE email = ?",
                (admin_email,)
            )
            print(f"Updated existing user {admin_email} to admin")
        else:
            # Create new admin user
            admin_id = str(uuid.uuid4())
            admin_name = "Admin User"
            admin_password = "admin123"
            
            # Hash password
            hashed_password = bcrypt.hashpw(admin_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            # Insert admin user
            cursor.execute('''
                INSERT INTO users (id, name, email, password, is_admin, created_at)
                VALUES (?, ?, ?, ?, 1, ?)
            ''', (admin_id, admin_name, admin_email, hashed_password, datetime.now().isoformat()))
            
            print(f"Created new admin user:")
            print(f"   - Email: {admin_email}")
            print(f"   - Password: {admin_password}")
            print(f"   - ID: {admin_id}")
        
        # Commit changes
        conn.commit()
        conn.close()
        
        print("Admin user setup completed successfully")
        return True
        
    except Exception as e:
        print(f"Error setting up admin user: {e}")
        return False

def verify_admin_setup():
    """Verify admin user was created correctly"""
    print("\nVerifying admin setup...")
    
    try:
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Get admin user
        admin = cursor.execute(
            "SELECT * FROM users WHERE email = ? AND is_admin = 1",
            ("admin@aura.com",)
        ).fetchone()
        
        if admin:
            print("Admin user verified:")
            print(f"   - Name: {admin['name']}")
            print(f"   - Email: {admin['email']}")
            print(f"   - Admin: {bool(admin['is_admin'])}")
            print(f"   - Created: {admin['created_at']}")
            
            conn.close()
            return True
        else:
            print("Admin user not found")
            conn.close()
            return False
            
    except Exception as e:
        print(f"Error verifying admin setup: {e}")
        return False

def show_database_stats():
    """Show current database statistics"""
    print("\nDatabase Statistics:")
    
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        # Get table counts
        tables = [
            ('users', 'Users'),
            ('doctors', 'Doctors'),
            ('appointments', 'Appointments'),
            ('chat_history', 'Chat Messages'),
            ('simple_mood_entries', 'Mood Entries')
        ]
        
        for table_name, display_name in tables:
            try:
                count = cursor.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]
                print(f"   - {display_name}: {count}")
            except sqlite3.OperationalError:
                print(f"   - {display_name}: Table not found")
        
        conn.close()
        
    except Exception as e:
        print(f"Error getting database stats: {e}")

def main():
    """Main setup function"""
    print("AURA Admin User Setup")
    print("=" * 40)
    
    # Setup admin user
    if setup_admin_user():
        # Verify setup
        if verify_admin_setup():
            # Show stats
            show_database_stats()
            
            print("\nAdmin setup completed successfully!")
            print("\nAdmin Login Credentials:")
            print("   - Email: admin@aura.com")
            print("   - Password: admin123")
            print("\nAccess admin panel at:")
            print("   - http://localhost:5000/admin.html")
            print("\nRemember to change the admin password in production!")
        else:
            print("Admin setup verification failed")
    else:
        print("Admin setup failed")

if __name__ == "__main__":
    main()