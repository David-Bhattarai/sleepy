import sqlite3
import uuid
from typing import Dict, List, Optional

DB_FILE = 'database.db'

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_all_tables():
    """Initialize all database tables"""
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
        
        # Doctors table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS doctors (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                phone TEXT,
                specialty TEXT NOT NULL,
                qualification TEXT,
                experience_years INTEGER DEFAULT 0,
                price_per_session REAL DEFAULT 0.0,
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
                notes TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (doctor_id) REFERENCES doctors (id)
            )
        ''')
        
        # Chat history table
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
                mood_rating INTEGER NOT NULL CHECK (mood_rating >= 1 AND mood_rating <= 5),
                mood_notes TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        conn.commit()
        print("✅ Database tables initialized")

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

def get_all_doctors() -> List[Dict]:
    """Get all doctors from database"""
    try:
        with get_db_connection() as conn:
            doctors = conn.execute('''
                SELECT * FROM doctors WHERE is_available = 1 ORDER BY name
            ''').fetchall()
            return [dict(doctor) for doctor in doctors]
    except Exception as e:
        print(f"Error getting doctors: {e}")
        # Return default doctors as fallback
        return [
            {
                'id': 'dr-smith-001',
                'name': 'Dr. Smith',
                'specialty': 'Mental Health Specialist',
                'qualification': 'MD, Psychiatry',
                'experience_years': 15,
                'price_per_session': 80.0,
                'avatar_emoji': '�‍⚕️',
                'bio': 'Specializes in anxiety and depression treatment with over 15 years of experience.',
                'is_available': 1
            },
            {
                'id': 'dr-johnson-002',
                'name': 'Dr. Johnson',
                'specialty': 'Licensed Counselor',
                'qualification': 'PhD, Clinical Psychology',
                'experience_years': 12,
                'price_per_session': 75.0,
                'avatar_emoji': '�‍⚕️',
                'bio': 'Expert in stress management and cognitive behavioral therapy.',
                'is_available': 1
            },
            {
                'id': 'dr-williams-003',
                'name': 'Dr. Williams',
                'specialty': 'Psychiatrist',
                'qualification': 'MD, Psychiatry, Board Certified',
                'experience_years': 20,
                'price_per_session': 90.0,
                'avatar_emoji': '👨‍⚕️',
                'bio': 'Specializes in mood disorders and psychiatric medication management.',
                'is_available': 1
            },
            {
                'id': 'dr-brown-004',
                'name': 'Dr. Brown',
                'specialty': 'Trauma Specialist',
                'qualification': 'PhD, Clinical Psychology, PTSD Certified',
                'experience_years': 18,
                'price_per_session': 85.0,
                'avatar_emoji': '👩‍⚕️',
                'bio': 'Specializes in trauma therapy and PTSD treatment.',
                'is_available': 1
            },
            {
                'id': 'dr-davis-005',
                'name': 'Dr. Davis',
                'specialty': 'Relationship Counselor',
                'qualification': 'MA, Marriage and Family Therapy',
                'experience_years': 10,
                'price_per_session': 70.0,
                'avatar_emoji': '👨‍⚕️',
                'bio': 'Expert in couples and family therapy.',
                'is_available': 1
            },
            {
                'id': 'dr-wilson-006',
                'name': 'Dr. Wilson',
                'specialty': 'Addiction Specialist',
                'qualification': 'MD, Addiction Medicine',
                'experience_years': 22,
                'price_per_session': 95.0,
                'avatar_emoji': '👩‍⚕️',
                'bio': 'Specializes in substance abuse recovery and addiction treatment.',
                'is_available': 1
            }
        ]

def init_dummy_doctors():
    """Initialize dummy doctors in database"""
    try:
        with get_db_connection() as conn:
            # Check if doctors already exist
            count = conn.execute("SELECT COUNT(*) FROM doctors").fetchone()[0]
            
            if count == 0:
                print("🔄 Initializing dummy doctors...")
                
                doctors_data = [
                    {
                        'id': 'dr-smith-001',
                        'name': 'Dr. Smith',
                        'email': 'dr.smith@mindbridge.com',
                        'phone': '+1-555-0101',
                        'specialty': 'Mental Health Specialist',
                        'qualification': 'MD, Psychiatry',
                        'experience_years': 15,
                        'price_per_session': 80.0,
                        'avatar_emoji': '👨‍⚕️',
                        'bio': 'Specializes in anxiety and depression treatment with over 15 years of experience. Uses evidence-based approaches including CBT and mindfulness techniques.',
                        'is_available': 1
                    },
                    {
                        'id': 'dr-johnson-002',
                        'name': 'Dr. Johnson',
                        'email': 'dr.johnson@mindbridge.com',
                        'phone': '+1-555-0102',
                        'specialty': 'Licensed Counselor',
                        'qualification': 'PhD, Clinical Psychology',
                        'experience_years': 12,
                        'price_per_session': 75.0,
                        'avatar_emoji': '👩‍⚕️',
                        'bio': 'Expert in stress management and cognitive behavioral therapy. Helps clients develop practical coping strategies for daily challenges.',
                        'is_available': 1
                    },
                    {
                        'id': 'dr-williams-003',
                        'name': 'Dr. Williams',
                        'email': 'dr.williams@mindbridge.com',
                        'phone': '+1-555-0103',
                        'specialty': 'Psychiatrist',
                        'qualification': 'MD, Psychiatry, Board Certified',
                        'experience_years': 20,
                        'price_per_session': 90.0,
                        'avatar_emoji': '👨‍⚕️',
                        'bio': 'Specializes in mood disorders and psychiatric medication management. Provides comprehensive mental health care with a focus on personalized treatment plans.',
                        'is_available': 0  # Busy
                    },
                    {
                        'id': 'dr-brown-004',
                        'name': 'Dr. Brown',
                        'email': 'dr.brown@mindbridge.com',
                        'phone': '+1-555-0104',
                        'specialty': 'Trauma Specialist',
                        'qualification': 'PhD, Clinical Psychology, PTSD Certified',
                        'experience_years': 18,
                        'price_per_session': 85.0,
                        'avatar_emoji': '👩‍⚕️',
                        'bio': 'Specializes in trauma therapy and PTSD treatment. Uses EMDR and other trauma-informed approaches to help clients heal from difficult experiences.',
                        'is_available': 1
                    },
                    {
                        'id': 'dr-davis-005',
                        'name': 'Dr. Davis',
                        'email': 'dr.davis@mindbridge.com',
                        'phone': '+1-555-0105',
                        'specialty': 'Relationship Counselor',
                        'qualification': 'MA, Marriage and Family Therapy',
                        'experience_years': 10,
                        'price_per_session': 70.0,
                        'avatar_emoji': '👨‍⚕️',
                        'bio': 'Expert in couples and family therapy. Helps individuals and families improve communication and strengthen relationships.',
                        'is_available': 1
                    },
                    {
                        'id': 'dr-wilson-006',
                        'name': 'Dr. Wilson',
                        'email': 'dr.wilson@mindbridge.com',
                        'phone': '+1-555-0106',
                        'specialty': 'Addiction Specialist',
                        'qualification': 'MD, Addiction Medicine',
                        'experience_years': 22,
                        'price_per_session': 95.0,
                        'avatar_emoji': '👩‍⚕️',
                        'bio': 'Specializes in substance abuse recovery and addiction treatment. Provides compassionate care and evidence-based treatment for addiction recovery.',
                        'is_available': 1
                    }
                ]
                
                for doctor in doctors_data:
                    conn.execute('''
                        INSERT INTO doctors (id, name, email, phone, specialty, qualification, 
                                           experience_years, price_per_session, avatar_emoji, bio, is_available)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (doctor['id'], doctor['name'], doctor['email'], doctor['phone'],
                          doctor['specialty'], doctor['qualification'], doctor['experience_years'],
                          doctor['price_per_session'], doctor['avatar_emoji'], doctor['bio'], doctor['is_available']))
                
                conn.commit()
                print("✅ Dummy doctors initialized successfully")
                return True
            else:
                print("✅ Doctors already exist in database")
                return True
                
    except Exception as e:
        print(f"❌ Error initializing dummy doctors: {e}")
        return False

def create_appointment(user_id: str, doctor_id: str, appointment_date: str, appointment_time: str, **kwargs) -> str:
    """Create new appointment"""
    try:
        appointment_id = str(uuid.uuid4())
        with get_db_connection() as conn:
            conn.execute('''
                INSERT INTO appointments (id, user_id, doctor_id, appointment_date, appointment_time,
                                        duration_minutes, status, payment_status, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (appointment_id, user_id, doctor_id, appointment_date, appointment_time,
                  kwargs.get('duration_minutes', 50), kwargs.get('status', 'scheduled'),
                  kwargs.get('payment_status', 'pending'), kwargs.get('notes', '')))
            conn.commit()
            print(f"✅ Appointment created: {appointment_id}")
            return appointment_id
    except Exception as e:
        print(f"❌ Error creating appointment: {e}")
        return None

def get_user_appointments(user_id: str, status: str = None) -> List[Dict]:
    """Get user appointments"""
    try:
        with get_db_connection() as conn:
            if status:
                appointments = conn.execute('''
                    SELECT a.*, d.name as doctor_name, d.specialty, d.avatar_emoji
                    FROM appointments a
                    JOIN doctors d ON a.doctor_id = d.id
                    WHERE a.user_id = ? AND a.status = ?
                    ORDER BY a.appointment_date DESC, a.appointment_time DESC
                ''', (user_id, status)).fetchall()
            else:
                appointments = conn.execute('''
                    SELECT a.*, d.name as doctor_name, d.specialty, d.avatar_emoji
                    FROM appointments a
                    JOIN doctors d ON a.doctor_id = d.id
                    WHERE a.user_id = ?
                    ORDER BY a.appointment_date DESC, a.appointment_time DESC
                ''', (user_id,)).fetchall()
            
            return [dict(appointment) for appointment in appointments]
    except Exception as e:
        print(f"❌ Error getting user appointments: {e}")
        return []

def create_payment(user_id: str, appointment_id: str, amount: float, payment_method: str, **kwargs) -> str:
    """Create payment record"""
    try:
        payment_id = str(uuid.uuid4())
        with get_db_connection() as conn:
            # Create payments table if it doesn't exist
            conn.execute('''
                CREATE TABLE IF NOT EXISTS payments (
                    id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    appointment_id TEXT NOT NULL,
                    amount REAL NOT NULL,
                    payment_method TEXT NOT NULL,
                    currency TEXT DEFAULT 'USD',
                    status TEXT DEFAULT 'pending',
                    transaction_id TEXT,
                    esewa_ref_id TEXT,
                    card_last_four TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id),
                    FOREIGN KEY (appointment_id) REFERENCES appointments (id)
                )
            ''')
            
            conn.execute('''
                INSERT INTO payments (id, user_id, appointment_id, amount, payment_method,
                                    currency, transaction_id, esewa_ref_id, card_last_four)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (payment_id, user_id, appointment_id, amount, payment_method,
                  kwargs.get('currency', 'USD'), kwargs.get('transaction_id'),
                  kwargs.get('esewa_ref_id'), kwargs.get('card_last_four')))
            conn.commit()
            print(f"✅ Payment record created: {payment_id}")
            return payment_id
    except Exception as e:
        print(f"❌ Error creating payment: {e}")
        return None

def update_payment_status(payment_id: str, status: str, transaction_id: str = None) -> bool:
    """Update payment status"""
    try:
        with get_db_connection() as conn:
            if transaction_id:
                conn.execute('''
                    UPDATE payments SET status = ?, transaction_id = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                ''', (status, transaction_id, payment_id))
            else:
                conn.execute('''
                    UPDATE payments SET status = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                ''', (status, payment_id))
            conn.commit()
            print(f"✅ Payment status updated: {payment_id} -> {status}")
            return True
    except Exception as e:
        print(f"❌ Error updating payment status: {e}")
        return False

def create_mood_entry(user_id: str, rating: int, notes: str = '') -> int:
    return 1

def get_mood_stats(user_id: str, days: int = 30) -> Dict:
    return {'total_entries': 0}

def create_chat_history(user_id: str, user_message: str, ai_response: str, sentiment: str = None, **kwargs) -> str:
    return str(uuid.uuid4())

def get_recent_chat_history(user_id: str, limit: int = 5) -> List[Dict]:
    return []

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

def get_all_users() -> List[Dict]:
    """Get all users (admin function)"""
    try:
        with get_db_connection() as conn:
            users = conn.execute('''
                SELECT id, name, email, phone, gender, is_admin, created_at 
                FROM users ORDER BY created_at DESC
            ''').fetchall()
            return [dict(user) for user in users]
    except Exception as e:
        print(f"Error getting all users: {e}")
        return []

def get_doctor_by_id(doctor_id: str):
    """Get doctor by ID"""
    try:
        with get_db_connection() as conn:
            doctor = conn.execute("SELECT * FROM doctors WHERE id = ?", (doctor_id,)).fetchone()
            return dict(doctor) if doctor else None
    except Exception as e:
        print(f"Error getting doctor by ID: {e}")
        return None

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

def initialize_database():
    """Initialize the database with all tables and dummy data"""
    print("🔄 Initializing database...")
    try:
        init_all_tables()
        init_dummy_doctors()  # Initialize dummy doctors
        print("✅ Database initialized successfully with dummy doctors")
        return True
    except Exception as e:
        print(f"❌ Database initialization error: {e}")
        return False

def init_dummy_doctors():
    """Initialize dummy doctors in database"""
    try:
        with get_db_connection() as conn:
            # Check if doctors already exist
            count = conn.execute("SELECT COUNT(*) FROM doctors").fetchone()[0]
            
            if count == 0:
                print("🔄 Initializing dummy doctors...")
                
                doctors_data = [
                    {
                        'id': 'dr-smith-001',
                        'name': 'Dr. Smith',
                        'email': 'dr.smith@mindbridge.com',
                        'phone': '+1-555-0101',
                        'specialty': 'Mental Health Specialist',
                        'qualification': 'MD, Psychiatry',
                        'experience_years': 15,
                        'price_per_session': 80.0,
                        'avatar_emoji': '👨‍⚕️',
                        'bio': 'Specializes in anxiety and depression treatment with over 15 years of experience. Uses evidence-based approaches including CBT and mindfulness techniques.',
                        'is_available': 1
                    },
                    {
                        'id': 'dr-johnson-002',
                        'name': 'Dr. Johnson',
                        'email': 'dr.johnson@mindbridge.com',
                        'phone': '+1-555-0102',
                        'specialty': 'Licensed Counselor',
                        'qualification': 'PhD, Clinical Psychology',
                        'experience_years': 12,
                        'price_per_session': 75.0,
                        'avatar_emoji': '👩‍⚕️',
                        'bio': 'Expert in stress management and cognitive behavioral therapy. Helps clients develop practical coping strategies for daily challenges.',
                        'is_available': 1
                    },
                    {
                        'id': 'dr-williams-003',
                        'name': 'Dr. Williams',
                        'email': 'dr.williams@mindbridge.com',
                        'phone': '+1-555-0103',
                        'specialty': 'Psychiatrist',
                        'qualification': 'MD, Psychiatry, Board Certified',
                        'experience_years': 20,
                        'price_per_session': 90.0,
                        'avatar_emoji': '👨‍⚕️',
                        'bio': 'Specializes in mood disorders and psychiatric medication management. Provides comprehensive mental health care with a focus on personalized treatment plans.',
                        'is_available': 0  # Busy
                    },
                    {
                        'id': 'dr-brown-004',
                        'name': 'Dr. Brown',
                        'email': 'dr.brown@mindbridge.com',
                        'phone': '+1-555-0104',
                        'specialty': 'Trauma Specialist',
                        'qualification': 'PhD, Clinical Psychology, PTSD Certified',
                        'experience_years': 18,
                        'price_per_session': 85.0,
                        'avatar_emoji': '👩‍⚕️',
                        'bio': 'Specializes in trauma therapy and PTSD treatment. Uses EMDR and other trauma-informed approaches to help clients heal from difficult experiences.',
                        'is_available': 1
                    },
                    {
                        'id': 'dr-davis-005',
                        'name': 'Dr. Davis',
                        'email': 'dr.davis@mindbridge.com',
                        'phone': '+1-555-0105',
                        'specialty': 'Relationship Counselor',
                        'qualification': 'MA, Marriage and Family Therapy',
                        'experience_years': 10,
                        'price_per_session': 70.0,
                        'avatar_emoji': '👨‍⚕️',
                        'bio': 'Expert in couples and family therapy. Helps individuals and families improve communication and strengthen relationships.',
                        'is_available': 1
                    },
                    {
                        'id': 'dr-wilson-006',
                        'name': 'Dr. Wilson',
                        'email': 'dr.wilson@mindbridge.com',
                        'phone': '+1-555-0106',
                        'specialty': 'Addiction Specialist',
                        'qualification': 'MD, Addiction Medicine',
                        'experience_years': 22,
                        'price_per_session': 95.0,
                        'avatar_emoji': '👩‍⚕️',
                        'bio': 'Specializes in substance abuse recovery and addiction treatment. Provides compassionate care and evidence-based treatment for addiction recovery.',
                        'is_available': 1
                    }
                ]
                
                for doctor in doctors_data:
                    conn.execute('''
                        INSERT INTO doctors (id, name, email, phone, specialty, qualification, 
                                           experience_years, price_per_session, avatar_emoji, bio, is_available)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (doctor['id'], doctor['name'], doctor['email'], doctor['phone'],
                          doctor['specialty'], doctor['qualification'], doctor['experience_years'],
                          doctor['price_per_session'], doctor['avatar_emoji'], doctor['bio'], doctor['is_available']))
                
                conn.commit()
                print("✅ Dummy doctors initialized successfully")
                return True
            else:
                print("✅ Doctors already exist in database")
                return True
                
    except Exception as e:
        print(f"❌ Error initializing dummy doctors: {e}")
        return False