
import sqlite3
import uuid

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_user_by_email(email):
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
    conn.close()
    return user

def get_user_by_id(user_id):
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    return user

def create_user(user_id, name, email, password, is_admin):
    conn = get_db_connection()
    conn.execute(
        "INSERT INTO users (id, name, email, password, is_admin) VALUES (?, ?, ?, ?, ?)",
        (user_id, name, email, password, is_admin)
    )
    conn.commit()
    conn.close()

def get_user_count():
    conn = get_db_connection()
    count = conn.execute("SELECT COUNT(id) FROM users").fetchone()[0]
    conn.close()
    return count

def get_subscription(user_id):
    conn = get_db_connection()
    sub = conn.execute("SELECT expiry_date FROM subscriptions WHERE user_id = ?", (user_id,)).fetchone()
    conn.close()
    return sub

def create_chat_history(user_id, user_message, ai_response, sentiment):
    conn = get_db_connection()
    conn.execute(
        "INSERT INTO chat_history (id, user_id, user_message, ai_response, sentiment, timestamp) VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)",
        (str(uuid.uuid4()), user_id, user_message, ai_response, sentiment)
    )
    conn.commit()
    conn.close()

def get_recent_chat_history(user_id, limit=5):
    conn = get_db_connection()
    history = conn.execute(
        "SELECT user_message, ai_response, sentiment FROM chat_history WHERE user_id = ? ORDER BY timestamp DESC LIMIT ?",
        (user_id, limit)
    ).fetchall()
    conn.close()
    # Return in conversational order (oldest first)
    return list(reversed(history))

def get_mood_history(user_id, days=30):
    """Fetches the user's mood history over a specified number of days."""
    conn = get_db_connection()
    mood_data = conn.execute(
        """
        SELECT 
            date(timestamp) as entry_date, 
            sentiment 
        FROM chat_history 
        WHERE user_id = ? AND date(timestamp) >= date('now', ?)
        ORDER BY entry_date;
        """, 
        (user_id, f'-{days} days')
    ).fetchall()
    conn.close()
    return mood_data
