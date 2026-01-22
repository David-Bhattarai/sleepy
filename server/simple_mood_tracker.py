"""
Simple Mood Tracker - Basic Python Backend with Database
No ML logic, just simple mood tracking and database operations
"""

import sqlite3
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional

class SimpleMoodTracker:
    """Simple mood tracker with basic database operations"""
    
    def __init__(self, db_path='database.db'):
        self.db_path = db_path
        self.init_simple_tables()
    
    def init_simple_tables(self):
        """Initialize simple mood tracking table"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
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
            
            conn.commit()
            print("✅ Simple mood tracking table initialized")
    
    def add_mood_entry(self, user_id: str, mood_rating: int, mood_notes: str = "") -> Dict:
        """Add a simple mood entry to database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Insert mood entry
                cursor.execute('''
                    INSERT INTO simple_mood_entries (user_id, mood_rating, mood_notes)
                    VALUES (?, ?, ?)
                ''', (user_id, mood_rating, mood_notes))
                
                entry_id = cursor.lastrowid
                conn.commit()
                
                # Get mood label
                mood_labels = {
                    1: {"label": "Very Bad", "emoji": "😭", "color": "#dc2626"},
                    2: {"label": "Bad", "emoji": "😟", "color": "#ea580c"},
                    3: {"label": "Okay", "emoji": "😐", "color": "#ca8a04"},
                    4: {"label": "Good", "emoji": "🙂", "color": "#16a34a"},
                    5: {"label": "Great", "emoji": "😊", "color": "#059669"}
                }
                
                return {
                    'success': True,
                    'entry_id': entry_id,
                    'mood_info': mood_labels[mood_rating],
                    'message': f'Mood logged successfully: {mood_labels[mood_rating]["label"]}'
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': 'Failed to log mood entry'
            }
    
    def get_user_moods(self, user_id: str, days: int = 30) -> List[Dict]:
        """Get user's mood entries from last N days"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT id, mood_rating, mood_notes, timestamp
                    FROM simple_mood_entries 
                    WHERE user_id = ? AND timestamp >= datetime('now', '-{} days')
                    ORDER BY timestamp DESC
                '''.format(days), (user_id,))
                
                moods = []
                for row in cursor.fetchall():
                    moods.append({
                        'id': row[0],
                        'mood_rating': row[1],
                        'mood_notes': row[2],
                        'timestamp': row[3]
                    })
                
                return moods
                
        except Exception as e:
            print(f"Error getting user moods: {e}")
            return []
    
    def get_mood_stats(self, user_id: str, days: int = 30) -> Dict:
        """Get simple mood statistics"""
        try:
            moods = self.get_user_moods(user_id, days)
            
            if not moods:
                return {
                    'total_entries': 0,
                    'message': 'No mood entries found'
                }
            
            # Calculate basic stats
            ratings = [mood['mood_rating'] for mood in moods]
            
            stats = {
                'total_entries': len(moods),
                'average_mood': round(sum(ratings) / len(ratings), 1),
                'highest_mood': max(ratings),
                'lowest_mood': min(ratings),
                'recent_moods': moods[:7],  # Last 7 entries
                'mood_counts': {
                    'great': ratings.count(5),
                    'good': ratings.count(4),
                    'okay': ratings.count(3),
                    'bad': ratings.count(2),
                    'very_bad': ratings.count(1)
                }
            }
            
            return stats
            
        except Exception as e:
            return {
                'error': str(e),
                'message': 'Failed to calculate mood stats'
            }
    
    def delete_mood_entry(self, user_id: str, entry_id: int) -> Dict:
        """Delete a mood entry"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Check if entry belongs to user
                cursor.execute('''
                    SELECT id FROM simple_mood_entries 
                    WHERE id = ? AND user_id = ?
                ''', (entry_id, user_id))
                
                if not cursor.fetchone():
                    return {
                        'success': False,
                        'message': 'Mood entry not found or access denied'
                    }
                
                # Delete entry
                cursor.execute('''
                    DELETE FROM simple_mood_entries 
                    WHERE id = ? AND user_id = ?
                ''', (entry_id, user_id))
                
                conn.commit()
                
                return {
                    'success': True,
                    'message': 'Mood entry deleted successfully'
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': 'Failed to delete mood entry'
            }
    
    def get_mood_chart_data(self, user_id: str, days: int = 30) -> Dict:
        """Get data for mood chart"""
        try:
            moods = self.get_user_moods(user_id, days)
            
            if not moods:
                return {'labels': [], 'data': []}
            
            # Prepare chart data (reverse to show oldest first)
            moods.reverse()
            
            labels = []
            data = []
            
            for mood in moods:
                # Format date for chart
                date_obj = datetime.fromisoformat(mood['timestamp'].replace('Z', '+00:00'))
                labels.append(date_obj.strftime('%m/%d'))
                data.append(mood['mood_rating'])
            
            return {
                'labels': labels,
                'data': data
            }
            
        except Exception as e:
            print(f"Error getting chart data: {e}")
            return {'labels': [], 'data': []}

# Global instance
simple_mood_tracker = SimpleMoodTracker()

def get_simple_mood_tracker():
    """Get the simple mood tracker instance"""
    return simple_mood_tracker