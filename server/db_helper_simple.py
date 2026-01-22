import sqlite3
import uuid
from typing import Dict, List, Optional

DB_FILE = 'database.db'

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def initialize_database():
    """Initialize the database with all tables"""
    print("🔄 Initializing database...")
    try:
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            
            # Users table
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
            
            # Chat history table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS chat_history (
                    id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    user_message TEXT NOT NULL,
                    ai_response TEXT NOT NULL,
                    sentiment TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            
            # Simple mood entries table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS simple_mood_entries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    mood_rating INTEGER NOT NULL CHECK (mood_rating >= 1 AND mood_rating <= 5),
                    mood_notes TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            
            conn.commit()
            print("✅ Database initialized successfully")
            return True
    except Exception as e:
        print(f"❌ Database initialization error: {e}")
        return False

def get_user_by_email(email: str):
    """Get user by email"""
    try:
        with get_db_connection() as conn:
            user = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
            return dict(user) if user else None
    except Exception as e:
        print(f"Error getting user by email: {e}")
        return None

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

def get_user_by_id(user_id: str):
    """Get user by ID"""
    try:
        with get_db_connection() as conn:
            user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
            return dict(user) if user else None
    except Exception as e:
        print(f"Error getting user by ID: {e}")
        return None

def create_chat_history(user_id: str, user_message: str, ai_response: str, sentiment: str = None, **kwargs) -> str:
    """Create chat history entry"""
    try:
        chat_id = str(uuid.uuid4())
        with get_db_connection() as conn:
            conn.execute('''
                INSERT INTO chat_history (id, user_id, user_message, ai_response, sentiment)
                VALUES (?, ?, ?, ?, ?)
            ''', (chat_id, user_id, user_message, ai_response, sentiment))
            conn.commit()
            return chat_id
    except Exception as e:
        print(f"Error creating chat history: {e}")
        return str(uuid.uuid4())

def get_full_chat_history(user_id: str) -> List[Dict]:
    """Get full chat history for user"""
    try:
        with get_db_connection() as conn:
            history = conn.execute('''
                SELECT user_message, ai_response, sentiment, timestamp
                FROM chat_history 
                WHERE user_id = ? 
                ORDER BY timestamp ASC
            ''', (user_id,)).fetchall()
            return [dict(chat) for chat in history]
    except Exception as e:
        print(f"Error getting full chat history: {e}")
        return []

# Stub functions for other features
def get_all_doctors() -> List[Dict]:
    return [
        {
            'id': 'dr-smith-001',
            'name': 'Dr. Smith',
            'specialty': 'Mental Health Specialist',
            'qualification': 'MD, Psychiatry',
            'experience_years': 15,
            'price_per_session': 80.0,
            'avatar_emoji': '👨‍⚕️',
            'bio': 'Specializes in anxiety and depression treatment.'
        }
    ]

def create_appointment(user_id: str, doctor_id: str, appointment_date: str, appointment_time: str, **kwargs) -> str:
    return str(uuid.uuid4())

def get_user_appointments(user_id: str, status: str = None) -> List[Dict]:
    return []

def create_payment(user_id: str, appointment_id: str, amount: float, payment_method: str, **kwargs) -> str:
    return str(uuid.uuid4())

def update_payment_status(payment_id: str, status: str, transaction_id: str = None) -> bool:
    return True

def create_face_emotion_record(user_id: str, detected_emotion: str, confidence_score: float, image_path: str = None) -> str:
    return str(uuid.uuid4())

def get_face_emotion_history(user_id: str, limit: int = 10) -> List[Dict]:
    return []

def save_ei_scores(user_id: str, awareness: float, regulation: float) -> int:
    return 1

def get_ei_history(user_id: str) -> List[Dict]:
    return []

def get_platform_analytics() -> Dict:
    return {'users': {'total': 0}}

def get_all_users() -> List[Dict]:
    return []

def get_doctor_by_id(doctor_id: str):
    return None

def update_appointment_status(appointment_id: str, status: str) -> bool:
    return True