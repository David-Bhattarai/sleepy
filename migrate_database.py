#!/usr/bin/env python3
"""
Database Migration Script for AURA Mental Health Platform
Fixes schema issues in existing database
"""

import sqlite3
import os
import sys

def migrate_database():
    """Migrate existing database to new schema"""
    print("🔄 Starting database migration...")
    
    # Change to server directory
    server_dir = os.path.join(os.getcwd(), 'server')
    os.chdir(server_dir)
    
    db_file = 'database.db'
    
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        
        # Check current users table schema
        cursor.execute("PRAGMA table_info(users)")
        users_columns = [row[1] for row in cursor.fetchall()]
        print(f"Current users columns: {users_columns}")
        
        # Migrate users table if needed
        if 'phone' not in users_columns or 'created_at' not in users_columns:
            print("🔄 Migrating users table...")
            
            # Create new users table
            cursor.execute('''
                CREATE TABLE users_new (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    phone TEXT,
                    date_of_birth DATE,
                    gender TEXT,
                    is_admin INTEGER DEFAULT 0,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Copy existing data
            cursor.execute('''
                INSERT INTO users_new (id, name, email, password, is_admin, created_at, updated_at)
                SELECT id, name, email, password, 
                       COALESCE(is_admin, 0), 
                       CURRENT_TIMESTAMP, 
                       CURRENT_TIMESTAMP
                FROM users
            ''')
            
            # Replace old table
            cursor.execute('DROP TABLE users')
            cursor.execute('ALTER TABLE users_new RENAME TO users')
            print("✅ Users table migrated")
        
        # Check chat_history table
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='chat_history'")
        chat_exists = cursor.fetchone()
        
        if chat_exists:
            cursor.execute("PRAGMA table_info(chat_history)")
            chat_columns = [row[1] for row in cursor.fetchall()]
            print(f"Current chat_history columns: {chat_columns}")
            
            if 'doctor_id' not in chat_columns or 'appointment_id' not in chat_columns:
                print("🔄 Migrating chat_history table...")
                
                # Create new chat_history table
                cursor.execute('''
                    CREATE TABLE chat_history_new (
                        id TEXT PRIMARY KEY,
                        user_id TEXT NOT NULL,
                        doctor_id TEXT,
                        appointment_id TEXT,
                        user_message TEXT NOT NULL,
                        ai_response TEXT NOT NULL,
                        sentiment TEXT,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users (id),
                        FOREIGN KEY (doctor_id) REFERENCES doctors (id),
                        FOREIGN KEY (appointment_id) REFERENCES appointments (id)
                    )
                ''')
                
                # Copy existing data with generated IDs if needed
                cursor.execute('''
                    INSERT INTO chat_history_new (id, user_id, user_message, ai_response, sentiment, timestamp)
                    SELECT 
                        CASE WHEN id IS NULL OR id = '' THEN hex(randomblob(16)) ELSE id END,
                        user_id, user_message, ai_response, sentiment, timestamp
                    FROM chat_history
                ''')
                
                # Replace old table
                cursor.execute('DROP TABLE chat_history')
                cursor.execute('ALTER TABLE chat_history_new RENAME TO chat_history')
                print(" Chat history table migrated")
        
        # Ensure all other tables exist
        print("🔄 Creating missing tables...")
        
        # Doctors table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS doctors (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                phone TEXT,
                specialty TEXT NOT NULL,
                qualification TEXT,
                experience_years INTEGER,
                price_per_session REAL NOT NULL,
                avatar_emoji TEXT DEFAULT '👨‍⚕️',
                bio TEXT,
                is_available INTEGER DEFAULT 1,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Appointments table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS appointments (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                doctor_id TEXT NOT NULL,
                appointment_date DATE NOT NULL,
                appointment_time TIME NOT NULL,
                duration_minutes INTEGER DEFAULT 50,
                status TEXT DEFAULT 'scheduled',
                payment_status TEXT DEFAULT 'pending',
                payment_method TEXT,
                payment_amount REAL,
                payment_id TEXT,
                notes TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (doctor_id) REFERENCES doctors (id)
            )
        ''')
        
        # Payments table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS payments (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                appointment_id TEXT NOT NULL,
                amount REAL NOT NULL,
                currency TEXT DEFAULT 'USD',
                payment_method TEXT NOT NULL,
                payment_status TEXT DEFAULT 'pending',
                transaction_id TEXT,
                esewa_ref_id TEXT,
                card_last_four TEXT,
                payment_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (appointment_id) REFERENCES appointments (id)
            )
        ''')
        
        # Face emotion detection table
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='face_emotion_detection'")
        emotion_exists = cursor.fetchone()
        
        if emotion_exists:
            cursor.execute("PRAGMA table_info(face_emotion_detection)")
            emotion_columns = [row for row in cursor.fetchall()]
            id_column = next((col for col in emotion_columns if col[1] == 'id'), None)
            
            if id_column and 'INTEGER' in id_column[2]:
                print("🔄 Migrating face_emotion_detection table...")
                
                # Create new table with TEXT id
                cursor.execute('''
                    CREATE TABLE face_emotion_detection_new (
                        id TEXT PRIMARY KEY,
                        user_id TEXT NOT NULL,
                        detected_emotion TEXT NOT NULL,
                        confidence_score REAL,
                        image_path TEXT,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users (id)
                    )
                ''')
                
                # Copy existing data with new UUID ids
                cursor.execute('''
                    INSERT INTO face_emotion_detection_new (id, user_id, detected_emotion, confidence_score, image_path, timestamp)
                    SELECT hex(randomblob(16)), user_id, detected_emotion, confidence_score, image_path, timestamp
                    FROM face_emotion_detection
                ''')
                
                # Replace old table
                cursor.execute('DROP TABLE face_emotion_detection')
                cursor.execute('ALTER TABLE face_emotion_detection_new RENAME TO face_emotion_detection')
                print("✅ Face emotion detection table migrated")
        else:
            # Face emotion detection table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS face_emotion_detection (
                    id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    detected_emotion TEXT NOT NULL,
                    confidence_score REAL,
                    image_path TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
        
        # Doctor availability table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS doctor_availability (
                id TEXT PRIMARY KEY,
                doctor_id TEXT NOT NULL,
                day_of_week INTEGER NOT NULL,
                start_time TIME NOT NULL,
                end_time TIME NOT NULL,
                is_available INTEGER DEFAULT 1,
                FOREIGN KEY (doctor_id) REFERENCES doctors (id)
            )
        ''')
        
        conn.commit()
        print(" Database migration completed successfully!")

if __name__ == "__main__":
    migrate_database()