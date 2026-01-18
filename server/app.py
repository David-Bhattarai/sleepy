
import base64
import json
import os
import random
import re
import uuid
from datetime import datetime
from io import BytesIO
import sqlite3
from functools import wraps
import numpy as np

from deepface import DeepFace
from flask import Flask, jsonify, request, send_from_directory
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# --- Database Initialization ---
DB_FILE = "database.db"

def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                is_admin INTEGER DEFAULT 0
            )
        ''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS chat_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                user_message TEXT,
                ai_response TEXT,
                sentiment TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS mood_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                rating INTEGER NOT NULL,
                notes TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS emotional_intelligence_scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                awareness_score REAL,
                regulation_score REAL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        conn.commit()

# --- DB Helper Functions ---
def get_user_by_id(user_id):
    with sqlite3.connect(DB_FILE) as conn:
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        return c.fetchone()

def get_user_by_email(email):
    with sqlite3.connect(DB_FILE) as conn:
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE email = ?", (email,))
        return c.fetchone()

def get_all_users():
    with sqlite3.connect(DB_FILE) as conn:
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("SELECT id, name, email, is_admin FROM users")
        return [dict(row) for row in c.fetchall()]

def create_user(user_id, name, email, password, is_admin):
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        is_admin_flag = is_admin or (get_user_count() == 0)
        c.execute("INSERT INTO users (id, name, email, password, is_admin) VALUES (?, ?, ?, ?, ?)",
                  (user_id, name, email, password, 1 if is_admin_flag else 0))
        conn.commit()

def get_user_count():
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM users")
        count = c.fetchone()[0]
    return count if count is not None else 0

def get_full_chat_history(user_id):
    with sqlite3.connect(DB_FILE) as conn:
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("SELECT user_message, ai_response, sentiment, timestamp FROM chat_history WHERE user_id = ? ORDER BY timestamp ASC", (user_id,))
        return [dict(row) for row in c.fetchall()]

def create_chat_history(user_id, user_message, ai_response, sentiment):
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute("INSERT INTO chat_history (user_id, user_message, ai_response, sentiment) VALUES (?, ?, ?, ?)",
                  (user_id, user_message, ai_response, sentiment))
        conn.commit()

def create_mood_entry(user_id, rating, notes):
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute("INSERT INTO mood_entries (user_id, rating, notes) VALUES (?, ?, ?)",
                  (user_id, rating, notes))
        conn.commit()

def get_mood_entries(user_id):
    with sqlite3.connect(DB_FILE) as conn:
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("SELECT rating, notes, timestamp FROM mood_entries WHERE user_id = ? ORDER BY timestamp ASC", (user_id,))
        return [dict(row) for row in c.fetchall()]

def save_ei_scores(user_id, awareness, regulation):
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute("INSERT INTO emotional_intelligence_scores (user_id, awareness_score, regulation_score) VALUES (?, ?, ?)",
                  (user_id, awareness, regulation))
        conn.commit()

def get_ei_history(user_id):
    with sqlite3.connect(DB_FILE) as conn:
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("SELECT awareness_score, regulation_score, timestamp FROM emotional_intelligence_scores WHERE user_id = ? ORDER BY timestamp ASC", (user_id,))
        return [dict(row) for row in c.fetchall()]

# --- App and Authentication ---
app = Flask(__name__, static_folder='../client', static_url_path='/')
app.config['SECRET_KEY'] = 'your_secret_key'
CORS(app)
bcrypt = Bcrypt(app)
sentiment_analyzer = SentimentIntensityAnalyzer()
user_emotions = {}

# --- Emotional Intelligence Calculation Model ---
EMOTION_LEXICON = {
    'happy', 'joyful', 'pleased', 'cheerful', 'delighted', 'glad', 'excited',
    'sad', 'unhappy', 'miserable', 'depressed', 'sorrowful', 'down', 'grieving',
    'angry', 'furious', 'irritated', 'enraged', 'annoyed', 'mad',
    'fearful', 'scared', 'anxious', 'terrified', 'nervous', 'worried',
    'surprised', 'shocked', 'astonished', 'amazed',
    'disgusted', 'repulsed', 'sickened',
    'love', 'caring', 'compassion', 'affection'
}

INTENTS = []
try:
    intents_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'intents.json')
    with open(intents_path, 'r', encoding='utf-8') as f:
        intents_raw = json.load(f)
        INTENTS = intents_raw.get('intents', [])
except Exception:
    INTENTS = []

def calculate_emotional_intelligence(chat_history):
    if not chat_history or len(chat_history) < 5:
        return 0, 0
    word_count = 0
    found_emotion_words = set()
    for entry in chat_history:
        message = entry['user_message'].lower()
        words = re.findall(r'\b\w+\b', message)
        word_count += len(words)
        for word in words:
            if word in EMOTION_LEXICON:
                found_emotion_words.add(word)
    awareness_score = (len(found_emotion_words) / 20) * 100
    sentiments = [entry['sentiment'] for entry in chat_history if entry['sentiment']]
    sentiment_map = {'Negative': -1, 'Crisis': -1, 'Neutral': 0, 'Positive': 1}
    numeric_sentiments = [sentiment_map.get(s, 0) for s in sentiments]
    regulation_score = 50
    for i in range(1, len(numeric_sentiments)):
        prev_s, curr_s = numeric_sentiments[i-1], numeric_sentiments[i]
        if prev_s == -1 and curr_s > -1: regulation_score += 10
        elif prev_s == -1 and curr_s == -1: regulation_score -= 5
        elif prev_s >= 0 and curr_s == -1: regulation_score -= 5
    awareness_score = max(0, min(100, awareness_score))
    regulation_score = max(0, min(100, regulation_score))
    return round(awareness_score, 2), round(regulation_score, 2)

def generate_intent_based_response(user_message):
    if not INTENTS:
        return None
    message = user_message.lower()
    best_tag = None
    best_score = 0
    for intent in INTENTS:
        patterns = intent.get('patterns', [])
        for pattern in patterns:
            p = pattern.lower().strip()
            if not p:
                continue
            score = 0
            if p in message:
                score = len(p)
            else:
                message_words = set(message.split())
                pattern_words = set(p.split())
                overlap = len(message_words & pattern_words)
                if overlap == 0:
                    continue
                score = overlap
            if score > best_score:
                best_score = score
                best_tag = intent.get('tag')
    if not best_tag:
        fallback_tags = {'no-response', 'default'}
        candidates = [i for i in INTENTS if i.get('tag') in fallback_tags]
        for intent in candidates:
            responses = intent.get('responses') or []
            if responses:
                return random.choice(responses)
        return None
    for intent in INTENTS:
        if intent.get('tag') == best_tag:
            responses = intent.get('responses') or []
            if not responses:
                return None
            return random.choice(responses)
    return None

# --- User Authentication API Endpoints ---
@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.get_json()
    name, email, password = data.get('name'), data.get('email'), data.get('password')
    if not all([name, email, password]):
        return jsonify({'error': 'Missing required fields'}), 400
    if get_user_by_email(email):
        return jsonify({'error': 'Email already registered'}), 409
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    user_id = str(uuid.uuid4())
    create_user(user_id, name, email, hashed_password, is_admin=False)
    return jsonify({'message': 'User created successfully', 'userId': user_id}), 201

@app.route('/api/signin', methods=['POST'])
def signin():
    data = request.get_json()
    email, password = data.get('email'), data.get('password')
    if not all([email, password]):
        return jsonify({'error': 'Email and password are required'}), 400
    user = get_user_by_email(email)
    if not user or not bcrypt.check_password_hash(user['password'], password):
        return jsonify({'error': 'Invalid credentials'}), 401
    return jsonify({
        'message': 'Login successful', 
        'token': user['id'],
        'name': user['name'],
        'isAdmin': user['is_admin']
    }), 200

# --- Main API Endpoints ---
@app.route('/api/emotional_intelligence')
def get_ei_scores():
    auth_header = request.headers.get('Authorization')
    if not auth_header or len(auth_header.split()) < 2:
        return jsonify({'error': 'Authentication required'}), 401
    token = auth_header.split()[1]
    user = get_user_by_id(token)
    if not user:
        return jsonify({'error': 'Invalid user'}), 401
    full_history = get_full_chat_history(user['id'])
    awareness, regulation = calculate_emotional_intelligence(full_history)
    save_ei_scores(user['id'], awareness, regulation)
    ei_history = get_ei_history(user['id'])
    return jsonify({
        'latest': {'awareness': awareness, 'regulation': regulation},
        'history': ei_history
    })

@app.route('/api/detect_emotion', methods=['POST'])
def detect_emotion():
    auth_header = request.headers.get('Authorization')
    if not auth_header or len(auth_header.split()) < 2:
        return jsonify({'error': 'Authentication required'}), 401
    token = auth_header.split()[1]
    user = get_user_by_id(token)
    if not user:
        return jsonify({'error': 'Invalid user'}), 401

    data = request.get_json()
    image_data = data.get('image') if data else None
    if not image_data:
        return jsonify({'error': 'No image data provided'}), 400

    try:
        if ',' in image_data:
            _, encoded = image_data.split(',', 1)
        else:
            encoded = image_data
        img_bytes = base64.b64decode(encoded)
        temp_path = f"temp_emotion_{uuid.uuid4().hex}.jpg"
        with open(temp_path, 'wb') as f:
            f.write(img_bytes)

        emotion = 'Unknown'
        try:
            analysis = DeepFace.analyze(img_path=temp_path, actions=['emotion'])
            if isinstance(analysis, list) and analysis:
                analysis = analysis[0]
            detected = analysis.get('dominant_emotion') if isinstance(analysis, dict) else None
            if isinstance(detected, str) and detected:
                emotion = detected.capitalize()
        finally:
            try:
                os.remove(temp_path)
            except OSError:
                pass
    except Exception:
        emotion = 'Unknown'

    user_emotions[user['id']] = emotion
    return jsonify({'emotion': emotion})

@app.route('/api/doctor_chat', methods=['POST'])
def handle_chat():
    auth_header = request.headers.get('Authorization')
    if not auth_header or len(auth_header.split()) < 2:
        return jsonify({'error': 'Authentication required'}), 401
    token = auth_header.split()[1]
    user_data = get_user_by_id(token)
    if not user_data:
        return jsonify({'error': 'Invalid user token'}), 401

    user_message = request.json['message']
    last_emotion = user_emotions.get(user_data['id'], 'neutral')
    sentiment_scores = sentiment_analyzer.polarity_scores(user_message)
    compound_score = sentiment_scores['compound']
    conversation_history = [dict(row) for row in get_full_chat_history(user_data['id'])][-5:]

    intent_response = generate_intent_based_response(user_message)
    ai_response = intent_response or generate_professional_ai_response(last_emotion, compound_score, conversation_history, user_message)

    sentiment = "Crisis" if "988" in ai_response else "Neutral"
    if compound_score <= -0.2: sentiment = "Negative"
    elif compound_score >= 0.2: sentiment = "Positive"
    
    create_chat_history(user_data['id'], user_message, ai_response, sentiment)

    return jsonify({
        'user_message': user_message,
        'ai_response': ai_response,
        'sentiment': sentiment
    })

def generate_professional_ai_response(last_emotion, text_sentiment, conversation_history, user_message):
    crisis_keywords = ['kill myself', 'suicide', 'suicidal', 'end my life', 'want to die', 'can\'t go on', 'no reason to live', 'hopeless', 'end it all']
    if any(keyword in user_message.lower() for keyword in crisis_keywords):
        return "It sounds like you are in a tremendous amount of pain... Please call or text 988 in the US and Canada, or call 111 in the UK."
    if last_emotion == 'sad': return "I can truly sense the sadness in you right now. Please, tell me what's happening."
    if last_emotion == 'angry': return "I see a lot of anger in your expression. Let's explore it together."
    if last_emotion == 'fear': return "You seem frightened. It's okay to feel that way. Let's take a calming breath together."
    if last_emotion == 'happy' and text_sentiment < -0.3: return "It's interesting... I can see a smile on your face, but your words seem to carry a heavy weight."
    if last_emotion in ['neutral', 'unknown'] and text_sentiment < -0.5: return "Even if your expression is neutral, the words you're using convey a deep sense of pain. I'm listening."
    if last_emotion == 'happy' or text_sentiment > 0.6: return "It's wonderful to see you looking happy! What's bringing you this joy today?"
    if conversation_history:
        full_history_text = " ".join([h['user_message'] for h in conversation_history])
        if full_history_text.count('anxiety') > 1: return "I've noticed the theme of anxiety has come up a few times. Let's focus on that."
    if text_sentiment < -0.2: return "I'm hearing you. What thoughts are swirling around that feeling?"
    return "I see. Let's go a bit deeper. What does that mean to you personally?"

# --- Static File Serving ---
@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    try:
        return send_from_directory(app.static_folder, path)
    except:
        return send_from_directory(app.static_folder, 'index.html')


if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
