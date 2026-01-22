"""
Comprehensive Database Helper for AURA Mental Health Platform
Handles all database operations for users, doctors, appointments, payments, mood tracking, etc.
"""

import sqlite3
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import json

# Database file path
DB_FILE = 'database.db'

def get_db_connection():
    """Get database connection with row factory"""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_all_tables():
    """Initialize all database tables with proper migration"""
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        
        # Check and migrate users table
        cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='users'")
        existing_users = cursor.fetchone()
        
        if existing_users and ('phone' not in existing_users[0] or 'created_at' not in existing_users[0]):
            print(" Migrating users table...")
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
            cursor.execute('''
                INSERT INTO users_new (id, name, email, password, is_admin, created_at, updated_at)
                SELECT id, name, email, password, COALESCE(is_admin, 0), CURRENT_TIMESTAMP, CURRENT_TIMESTAMP
                FROM users
            ''')
            cursor.execute('DROP TABLE users')
            cursor.execute('ALTER TABLE users_new RENAME TO users')
            print(" Users table migrated")
        else:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
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
        
        # Check and migrate chat_history table
        cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='chat_history'")
        existing_chat = cursor.fetchone()
        
        if existing_chat and ('doctor_id' not in existing_chat[0] or 'appointment_id' not in existing_chat[0]):
            print(" Migrating chat_history table...")
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
            cursor.execute('''
                INSERT INTO chat_history_new (id, user_id, user_message, ai_response, sentiment, timestamp)
                SELECT 
                    CASE WHEN id IS NULL OR id = '' THEN hex(randomblob(16)) ELSE id END,
                    user_id, user_message, ai_response, sentiment, timestamp
                FROM chat_history
            ''')
            cursor.execute('DROP TABLE chat_history')
            cursor.execute('ALTER TABLE chat_history_new RENAME TO chat_history')
            print(" Chat history table migrated")
        else:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS chat_history (
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
        
        # Simple mood entries table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS simple_mood_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                mood_rating INTEGER NOT NULL CHECK(mood_rating >= 1 AND mood_rating <= 5),
                mood_notes TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Check and migrate face_emotion_detection table
        cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='face_emotion_detection'")
        existing_emotion = cursor.fetchone()
        
        if existing_emotion and 'INTEGER PRIMARY KEY AUTOINCREMENT' in existing_emotion[0]:
            print(" Migrating face_emotion_detection table...")
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
            cursor.execute('''
                INSERT INTO face_emotion_detection_new (id, user_id, detected_emotion, confidence_score, image_path, timestamp)
                SELECT hex(randomblob(16)), user_id, detected_emotion, confidence_score, image_path, timestamp
                FROM face_emotion_detection
            ''')
            cursor.execute('DROP TABLE face_emotion_detection')
            cursor.execute('ALTER TABLE face_emotion_detection_new RENAME TO face_emotion_detection')
            print(" Face emotion detection table migrated")
        else:
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
        
        # Emotional intelligence scores table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS emotional_intelligence_scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                awareness_score REAL,
                regulation_score REAL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
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
        print("✅ All database tables initialized successfully")

# ==================== USER FUNCTIONS ====================
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
        print(" All database tables initialized successfully")

# ==================== USER FUNCTIONS ====================

def get_user_by_email(email: str) -> Optional[sqlite3.Row]:
    """Get user by email"""
    with get_db_connection() as conn:
        return conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()

def get_user_by_id(user_id: str) -> Optional[sqlite3.Row]:
    """Get user by ID"""
    with get_db_connection() as conn:
        return conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()

def create_user(user_id: str, name: str, email: str, password: str, is_admin: bool = False, **kwargs) -> bool:
    """Create new user"""
    try:
        with get_db_connection() as conn:
            conn.execute('''
                INSERT INTO users (id, name, email, password, phone, date_of_birth, gender, is_admin)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (user_id, name, email, password, kwargs.get('phone'), 
                  kwargs.get('date_of_birth'), kwargs.get('gender'), int(is_admin)))
            conn.commit()
            return True
    except Exception as e:
        print(f"Error creating user: {e}")
        return False

def get_user_count() -> int:
    """Get total user count"""
    with get_db_connection() as conn:
        result = conn.execute("SELECT COUNT(id) FROM users").fetchone()
        return result[0] if result else 0

def get_all_users() -> List[Dict]:
    """Get all users (admin function)"""
    with get_db_connection() as conn:
        users = conn.execute('''
            SELECT id, name, email, phone, gender, is_admin, created_at 
            FROM users ORDER BY created_at DESC
        ''').fetchall()
        return [dict(user) for user in users]

# ==================== DOCTOR FUNCTIONS ====================

def init_default_doctors():
    """Initialize default doctors if none exist"""
    with get_db_connection() as conn:
        count = conn.execute("SELECT COUNT(*) FROM doctors").fetchone()[0]
        
        if count == 0:
            doctors_data = [
                {
                    'id': 'dr-smith-001',
                    'name': 'Dr. Smith',
                    'email': 'dr.smith@aura.com',
                    'phone': '+1-555-0101',
                    'specialty': 'Mental Health Specialist',
                    'qualification': 'MD, Psychiatry',
                    'experience_years': 15,
                    'price_per_session': 80.0,
                    'avatar_emoji': '👨‍⚕️',
                    'bio': 'Specializes in anxiety and depression treatment with over 15 years of experience.'
                },
                {
                    'id': 'dr-johnson-002',
                    'name': 'Dr. Johnson',
                    'email': 'dr.johnson@aura.com',
                    'phone': '+1-555-0102',
                    'specialty': 'Licensed Counselor',
                    'qualification': 'PhD, Clinical Psychology',
                    'experience_years': 12,
                    'price_per_session': 75.0,
                    'avatar_emoji': '',
                    'bio': 'Expert in stress management and cognitive behavioral therapy.'
                },
                {
                    'id': 'dr-williams-003',
                    'name': 'Dr. Williams',
                    'email': 'dr.williams@aura.com',
                    'phone': '+1-555-0103',
                    'specialty': 'Psychiatrist',
                    'qualification': 'MD, Psychiatry, Board Certified',
                    'experience_years': 20,
                    'price_per_session': 90.0,
                    'avatar_emoji': '👨‍⚕️',
                    'bio': 'Specializes in mood disorders and psychiatric medication management.'
                },
                {
                    'id': 'dr-brown-004',
                    'name': 'Dr. Brown',
                    'email': 'dr.brown@aura.com',
                    'phone': '+1-555-0104',
                    'specialty': 'Trauma Specialist',
                    'qualification': 'PhD, Trauma Psychology',
                    'experience_years': 18,
                    'price_per_session': 85.0,
                    'avatar_emoji': '👩',
                    'bio': 'Expert in PTSD and trauma therapy using EMDR and other evidence-based approaches.'
                },
                {
                    'id': 'dr-davis-005',
                    'name': 'Dr. Davis',
                    'email': 'dr.davis@aura.com',
                    'phone': '+1-555-0105',
                    'specialty': 'Relationship Counselor',
                    'qualification': 'MA, Marriage and Family Therapy',
                    'experience_years': 10,
                    'price_per_session': 70.0,
                    'avatar_emoji': '👨‍⚕️',
                    'bio': 'Specializes in couples therapy and family counseling.'
                },
                {
                    'id': 'dr-wilson-006',
                    'name': 'Dr. Wilson',
                    'email': 'dr.wilson@aura.com',
                    'phone': '+1-555-0106',
                    'specialty': 'Addiction Specialist',
                    'qualification': 'MD, Addiction Medicine',
                    'experience_years': 16,
                    'price_per_session': 95.0,
                    'avatar_emoji': '👩‍⚕️',
                    'bio': 'Expert in substance abuse treatment and addiction recovery programs.'
                }
            ]
            
            for doctor in doctors_data:
                conn.execute('''
                    INSERT INTO doctors (id, name, email, phone, specialty, qualification, 
                                       experience_years, price_per_session, avatar_emoji, bio)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (doctor['id'], doctor['name'], doctor['email'], doctor['phone'],
                      doctor['specialty'], doctor['qualification'], doctor['experience_years'],
                      doctor['price_per_session'], doctor['avatar_emoji'], doctor['bio']))
            
            conn.commit()
            print(" Default doctors initialized")

def get_all_doctors() -> List[Dict]:
    """Get all doctors"""
    with get_db_connection() as conn:
        doctors = conn.execute('''
            SELECT * FROM doctors WHERE is_available = 1 ORDER BY name
        ''').fetchall()
        return [dict(doctor) for doctor in doctors]

def get_doctor_by_id(doctor_id: str) -> Optional[Dict]:
    """Get doctor by ID"""
    with get_db_connection() as conn:
        doctor = conn.execute("SELECT * FROM doctors WHERE id = ?", (doctor_id,)).fetchone()
        return dict(doctor) if doctor else None



def create_appointment(user_id: str, doctor_id: str, appointment_date: str, 
                      appointment_time: str, **kwargs) -> str:
    """Create new appointment"""
    appointment_id = str(uuid.uuid4())
    
    try:
        with get_db_connection() as conn:
            conn.execute('''
                INSERT INTO appointments (id, user_id, doctor_id, appointment_date, 
                                        appointment_time, duration_minutes, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (appointment_id, user_id, doctor_id, appointment_date, appointment_time,
                  kwargs.get('duration_minutes', 50), kwargs.get('notes', '')))
            conn.commit()
            return appointment_id
    except Exception as e:
        print(f"Error creating appointment: {e}")
        return None

def get_user_appointments(user_id: str, status: str = None) -> List[Dict]:
    """Get user's appointments"""
    with get_db_connection() as conn:
        query = '''
            SELECT a.*, d.name as doctor_name, d.specialty, d.avatar_emoji
            FROM appointments a
            JOIN doctors d ON a.doctor_id = d.id
            WHERE a.user_id = ?
        '''
        params = [user_id]
        
        if status:
            query += " AND a.status = ?"
            params.append(status)
            
        query += " ORDER BY a.appointment_date DESC, a.appointment_time DESC"
        
        appointments = conn.execute(query, params).fetchall()
        return [dict(apt) for apt in appointments]

def get_doctor_appointments(doctor_id: str, date: str = None) -> List[Dict]:
    """Get doctor's appointments"""
    with get_db_connection() as conn:
        query = '''
            SELECT a.*, u.name as user_name, u.email as user_email
            FROM appointments a
            JOIN users u ON a.user_id = u.id
            WHERE a.doctor_id = ?
        '''
        params = [doctor_id]
        
        if date:
            query += " AND a.appointment_date = ?"
            params.append(date)
            
        query += " ORDER BY a.appointment_date, a.appointment_time"
        
        appointments = conn.execute(query, params).fetchall()
        return [dict(apt) for apt in appointments]

def update_appointment_status(appointment_id: str, status: str) -> bool:
    """Update appointment status"""
    try:
        with get_db_connection() as conn:
            conn.execute('''
                UPDATE appointments SET status = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (status, appointment_id))
            conn.commit()
            return True
    except Exception as e:
        print(f"Error updating appointment status: {e}")
        return False

# ==================== PAYMENT FUNCTIONS ====================

def create_payment(user_id: str, appointment_id: str, amount: float, 
                  payment_method: str, **kwargs) -> str:
    """Create payment record"""
    payment_id = str(uuid.uuid4())
    
    try:
        with get_db_connection() as conn:
            conn.execute('''
                INSERT INTO payments (id, user_id, appointment_id, amount, currency,
                                    payment_method, transaction_id, esewa_ref_id, card_last_four)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (payment_id, user_id, appointment_id, amount, kwargs.get('currency', 'USD'),
                  payment_method, kwargs.get('transaction_id'), kwargs.get('esewa_ref_id'),
                  kwargs.get('card_last_four')))
            conn.commit()
            return payment_id
    except Exception as e:
        print(f"Error creating payment: {e}")
        return None

def update_payment_status(payment_id: str, status: str, transaction_id: str = None) -> bool:
    """Update payment status"""
    try:
        with get_db_connection() as conn:
            if transaction_id:
                conn.execute('''
                    UPDATE payments SET payment_status = ?, transaction_id = ?
                    WHERE id = ?
                ''', (status, transaction_id, payment_id))
            else:
                conn.execute('''
                    UPDATE payments SET payment_status = ? WHERE id = ?
                ''', (status, payment_id))
            conn.commit()
            return True
    except Exception as e:
        print(f"Error updating payment status: {e}")
        return False

def get_payment_by_appointment(appointment_id: str) -> Optional[Dict]:
    """Get payment by appointment ID"""
    with get_db_connection() as conn:
        payment = conn.execute('''
            SELECT * FROM payments WHERE appointment_id = ?
        ''', (appointment_id,)).fetchone()
        return dict(payment) if payment else None

# CHAT HISTORY FUNCTIONS

def create_chat_history(user_id: str, user_message: str, ai_response: str, 
                       sentiment: str = None, **kwargs) -> str:
    """Create chat history entry"""
    chat_id = str(uuid.uuid4())
    
    try:
        with get_db_connection() as conn:
            conn.execute('''
                INSERT INTO chat_history (id, user_id, doctor_id, appointment_id,
                                        user_message, ai_response, sentiment)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (chat_id, user_id, kwargs.get('doctor_id'), kwargs.get('appointment_id'),
                  user_message, ai_response, sentiment))
            conn.commit()
            return chat_id
    except Exception as e:
        print(f"Error creating chat history: {e}")
        return None

def get_recent_chat_history(user_id: str, limit: int = 5) -> List[Dict]:
    """Get recent chat history"""
    with get_db_connection() as conn:
        history = conn.execute('''
            SELECT user_message, ai_response, sentiment, timestamp
            FROM chat_history 
            WHERE user_id = ? 
            ORDER BY timestamp DESC 
            LIMIT ?
        ''', (user_id, limit)).fetchall()
        return [dict(chat) for chat in reversed(history)]

def get_full_chat_history(user_id: str) -> List[Dict]:
    """Get full chat history for user"""
    with get_db_connection() as conn:
        history = conn.execute('''
            SELECT user_message, ai_response, sentiment, timestamp
            FROM chat_history 
            WHERE user_id = ? 
            ORDER BY timestamp ASC
        ''', (user_id,)).fetchall()
        return [dict(chat) for chat in history]

# ==================== MOOD TRACKING FUNCTIONS ====================

def create_mood_entry(user_id: str, rating: int, notes: str = '') -> int:
    """Create mood entry"""
    try:
        with get_db_connection() as conn:
            cursor = conn.execute('''
                INSERT INTO simple_mood_entries (user_id, mood_rating, mood_notes)
                VALUES (?, ?, ?)
            ''', (user_id, rating, notes))
            conn.commit()
            return cursor.lastrowid
    except Exception as e:
        print(f"Error creating mood entry: {e}")
        return None

def get_mood_entries(user_id: str, days: int = 30) -> List[Dict]:
    """Get mood entries for user"""
    with get_db_connection() as conn:
        entries = conn.execute('''
            SELECT id, mood_rating, mood_notes, timestamp
            FROM simple_mood_entries 
            WHERE user_id = ? AND timestamp >= datetime('now', '-{} days')
            ORDER BY timestamp DESC
        '''.format(days), (user_id,)).fetchall()
        return [dict(entry) for entry in entries]

def get_mood_stats(user_id: str, days: int = 30) -> Dict:
    """Get mood statistics"""
    entries = get_mood_entries(user_id, days)
    
    if not entries:
        return {'total_entries': 0, 'message': 'No mood entries found'}
    
    ratings = [entry['mood_rating'] for entry in entries]
    
    return {
        'total_entries': len(entries),
        'average_mood': round(sum(ratings) / len(ratings), 1),
        'highest_mood': max(ratings),
        'lowest_mood': min(ratings),
        'recent_moods': entries[:7],
        'mood_counts': {
            'great': ratings.count(5),
            'good': ratings.count(4),
            'okay': ratings.count(3),
            'bad': ratings.count(2),
            'very_bad': ratings.count(1)
        }
    }

# EMOTION DETECTION FUNCTIONS

def create_face_emotion_record(user_id: str, detected_emotion: str, 
                              confidence_score: float, image_path: str = None) -> str:
    """Create face emotion detection record"""
    record_id = str(uuid.uuid4())
    
    try:
        with get_db_connection() as conn:
            conn.execute('''
                INSERT INTO face_emotion_detection (id, user_id, detected_emotion, 
                                                   confidence_score, image_path)
                VALUES (?, ?, ?, ?, ?)
            ''', (record_id, user_id, detected_emotion, confidence_score, image_path))
            conn.commit()
            return record_id
    except Exception as e:
        print(f"Error creating emotion record: {e}")
        return None

def get_face_emotion_history(user_id: str, limit: int = 10) -> List[Dict]:
    """Get face emotion history"""
    with get_db_connection() as conn:
        history = conn.execute('''
            SELECT detected_emotion, confidence_score, timestamp
            FROM face_emotion_detection 
            WHERE user_id = ? 
            ORDER BY timestamp DESC 
            LIMIT ?
        ''', (user_id, limit)).fetchall()
        return [dict(record) for record in history]

# EMOTIONAL INTELLIGENCE FUNCTIONS 

def save_ei_scores(user_id: str, awareness: float, regulation: float) -> int:
    """Save emotional intelligence scores"""
    try:
        with get_db_connection() as conn:
            cursor = conn.execute('''
                INSERT INTO emotional_intelligence_scores (user_id, awareness_score, regulation_score)
                VALUES (?, ?, ?)
            ''', (user_id, awareness, regulation))
            conn.commit()
            return cursor.lastrowid
    except Exception as e:
        print(f"Error saving EI scores: {e}")
        return None

def get_ei_history(user_id: str) -> List[Dict]:
    """Get emotional intelligence history"""
    with get_db_connection() as conn:
        history = conn.execute('''
            SELECT awareness_score, regulation_score, timestamp
            FROM emotional_intelligence_scores 
            WHERE user_id = ? 
            ORDER BY timestamp ASC
        ''', (user_id,)).fetchall()
        return [dict(record) for record in history]

# ANALYTICS FUNCTIONS

def get_platform_analytics() -> Dict:
    """Get platform-wide analytics (admin function)"""
    with get_db_connection() as conn:
        # User stats
        total_users = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
        new_users_today = conn.execute('''
            SELECT COUNT(*) FROM users 
            WHERE date(created_at) = date('now')
        ''').fetchone()[0]
        
        # Appointment stats
        total_appointments = conn.execute("SELECT COUNT(*) FROM appointments").fetchone()[0]
        completed_appointments = conn.execute('''
            SELECT COUNT(*) FROM appointments WHERE status = 'completed'
        ''').fetchone()[0]
        
        # Payment stats
        total_revenue = conn.execute('''
            SELECT COALESCE(SUM(amount), 0) FROM payments WHERE payment_status = 'completed'
        ''').fetchone()[0]
        
        # Mood tracking stats
        total_mood_entries = conn.execute("SELECT COUNT(*) FROM simple_mood_entries").fetchone()[0]
        
        return {
            'users': {
                'total': total_users,
                'new_today': new_users_today
            },
            'appointments': {
                'total': total_appointments,
                'completed': completed_appointments,
                'completion_rate': round((completed_appointments / total_appointments * 100), 2) if total_appointments > 0 else 0
            },
            'revenue': {
                'total': total_revenue,
                'currency': 'USD'
            },
            'mood_tracking': {
                'total_entries': total_mood_entries
            }
        }
# INITIALIZATION

def initialize_database():
    """Initialize the complete database"""
    print("🔄 Initializing AURA database...")
    init_all_tables()
    init_default_doctors()
    print("✅ Database initialization complete!")

# Initialize database when module is imported
if __name__ == "__main__":
    initialize_database()
    initialize_database()