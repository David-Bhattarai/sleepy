"""
Advanced Mood Intelligence System for MindBridge - NCIT Final Year Project
This module provides comprehensive mood tracking, analysis, and AI-powered insights
for mental health monitoring and personalized recommendations.
"""

import json
import sqlite3
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from collections import defaultdict, Counter
import re
from typing import Dict, List, Tuple, Optional
import statistics

class MoodIntelligenceEngine:
    """
    Advanced AI-powered mood intelligence system that provides:
    - Comprehensive mood analysis and pattern recognition
    - Personalized insights and recommendations
    - Predictive mood forecasting
    - Trigger identification and correlation analysis
    - Mental health risk assessment
    """
    
    def __init__(self, db_path='database.db'):
        self.db_path = db_path
        self.mood_categories = {
            1: {"label": "Severely Low", "emoji": "😭", "color": "#dc2626", "severity": "critical"},
            2: {"label": "Low", "emoji": "😟", "color": "#ea580c", "severity": "concerning"},
            3: {"label": "Below Average", "emoji": "😐", "color": "#ca8a04", "severity": "mild"},
            4: {"label": "Good", "emoji": "🙂", "color": "#16a34a", "severity": "positive"},
            5: {"label": "Excellent", "emoji": "😊", "color": "#059669", "severity": "very_positive"}
        }
        
        # Advanced mood analysis patterns
        self.mood_patterns = {
            'depression_indicators': ['tired', 'exhausted', 'hopeless', 'empty', 'worthless', 'sad', 'down'],
            'anxiety_indicators': ['worried', 'anxious', 'nervous', 'stressed', 'panic', 'overwhelmed'],
            'positive_indicators': ['happy', 'excited', 'grateful', 'accomplished', 'peaceful', 'content'],
            'energy_indicators': ['energetic', 'motivated', 'productive', 'active', 'focused'],
            'social_indicators': ['lonely', 'isolated', 'connected', 'supported', 'loved'],
            'physical_indicators': ['headache', 'tired', 'sick', 'healthy', 'strong', 'weak']
        }
        
        # Initialize database tables
        self.init_advanced_tables()
    
    def init_advanced_tables(self):
        """Initialize advanced mood tracking tables"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Enhanced mood entries table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS mood_entries_advanced (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    mood_rating INTEGER NOT NULL CHECK(mood_rating >= 1 AND mood_rating <= 5),
                    mood_notes TEXT,
                    energy_level INTEGER CHECK(energy_level >= 1 AND energy_level <= 5),
                    sleep_quality INTEGER CHECK(sleep_quality >= 1 AND sleep_quality <= 5),
                    stress_level INTEGER CHECK(stress_level >= 1 AND stress_level <= 5),
                    social_interaction INTEGER CHECK(social_interaction >= 1 AND social_interaction <= 5),
                    physical_activity INTEGER CHECK(physical_activity >= 1 AND physical_activity <= 5),
                    weather_condition TEXT,
                    location TEXT,
                    triggers TEXT,
                    medications TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            
            # Mood insights and analytics table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS mood_insights (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    insight_type TEXT NOT NULL,
                    insight_data TEXT NOT NULL,
                    confidence_score REAL,
                    generated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            
            # Mood patterns and correlations table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS mood_patterns (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    pattern_type TEXT NOT NULL,
                    pattern_data TEXT NOT NULL,
                    strength REAL,
                    last_updated DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            
            conn.commit()
    
    def log_advanced_mood(self, user_id: str, mood_data: Dict) -> Dict:
        """
        Log comprehensive mood entry with advanced tracking
        
        Args:
            user_id: User identifier
            mood_data: Dictionary containing mood information
            
        Returns:
            Dictionary with logging result and immediate insights
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Extract mood data with defaults
                mood_rating = mood_data.get('mood_rating', 3)
                mood_notes = mood_data.get('mood_notes', '')
                energy_level = mood_data.get('energy_level', 3)
                sleep_quality = mood_data.get('sleep_quality', 3)
                stress_level = mood_data.get('stress_level', 3)
                social_interaction = mood_data.get('social_interaction', 3)
                physical_activity = mood_data.get('physical_activity', 3)
                weather_condition = mood_data.get('weather_condition', '')
                location = mood_data.get('location', '')
                triggers = mood_data.get('triggers', '')
                medications = mood_data.get('medications', '')
                
                # Insert advanced mood entry
                cursor.execute('''
                    INSERT INTO mood_entries_advanced 
                    (user_id, mood_rating, mood_notes, energy_level, sleep_quality, 
                     stress_level, social_interaction, physical_activity, weather_condition, 
                     location, triggers, medications)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (user_id, mood_rating, mood_notes, energy_level, sleep_quality,
                      stress_level, social_interaction, physical_activity, weather_condition,
                      location, triggers, medications))
                
                entry_id = cursor.lastrowid
                conn.commit()
                
                # Generate immediate insights
                immediate_insights = self.generate_immediate_insights(user_id, mood_data)
                
                # Update user patterns
                self.update_mood_patterns(user_id)
                
                return {
                    'success': True,
                    'entry_id': entry_id,
                    'mood_category': self.mood_categories[mood_rating],
                    'immediate_insights': immediate_insights,
                    'message': 'Mood logged successfully with advanced analytics'
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': 'Failed to log mood entry'
            }
    
    def generate_immediate_insights(self, user_id: str, mood_data: Dict) -> Dict:
        """Generate immediate insights from current mood entry"""
        insights = {
            'mood_interpretation': self.interpret_mood_combination(mood_data),
            'recommendations': self.get_personalized_recommendations(user_id, mood_data),
            'risk_assessment': self.assess_mental_health_risk(user_id, mood_data),
            'pattern_alerts': self.check_pattern_alerts(user_id, mood_data)
        }
        
        return insights
    
    def interpret_mood_combination(self, mood_data: Dict) -> Dict:
        """Interpret the combination of mood factors"""
        mood_rating = mood_data.get('mood_rating', 3)
        energy_level = mood_data.get('energy_level', 3)
        stress_level = mood_data.get('stress_level', 3)
        sleep_quality = mood_data.get('sleep_quality', 3)
        
        # Calculate overall wellness score
        wellness_score = (mood_rating + energy_level + (6 - stress_level) + sleep_quality) / 4
        
        # Determine mood state
        if wellness_score >= 4.0:
            state = "thriving"
            message = "You're in a great mental space! Your mood, energy, and sleep are all supporting your wellbeing."
        elif wellness_score >= 3.5:
            state = "stable"
            message = "You're doing well overall. There might be small areas to focus on for optimal wellbeing."
        elif wellness_score >= 2.5:
            state = "managing"
            message = "You're managing, but there are some challenges affecting your mood and energy."
        elif wellness_score >= 2.0:
            state = "struggling"
            message = "You seem to be going through a difficult time. Consider reaching out for support."
        else:
            state = "crisis"
            message = "You're experiencing significant challenges. Please consider professional support immediately."
        
        return {
            'wellness_score': round(wellness_score, 2),
            'state': state,
            'message': message,
            'factors': {
                'mood': self.mood_categories[mood_rating]['label'],
                'energy': f"Energy level: {energy_level}/5",
                'stress': f"Stress level: {stress_level}/5",
                'sleep': f"Sleep quality: {sleep_quality}/5"
            }
        }
    
    def get_personalized_recommendations(self, user_id: str, mood_data: Dict) -> List[Dict]:
        """Generate personalized recommendations based on mood data and history"""
        recommendations = []
        
        mood_rating = mood_data.get('mood_rating', 3)
        energy_level = mood_data.get('energy_level', 3)
        stress_level = mood_data.get('stress_level', 3)
        sleep_quality = mood_data.get('sleep_quality', 3)
        
        # Low mood recommendations
        if mood_rating <= 2:
            recommendations.extend([
                {
                    'type': 'immediate',
                    'category': 'self_care',
                    'title': 'Gentle Self-Care',
                    'description': 'Try a warm bath, listen to calming music, or practice deep breathing.',
                    'priority': 'high'
                },
                {
                    'type': 'social',
                    'category': 'connection',
                    'title': 'Reach Out',
                    'description': 'Consider calling a friend, family member, or mental health professional.',
                    'priority': 'high'
                }
            ])
        
        # High stress recommendations
        if stress_level >= 4:
            recommendations.extend([
                {
                    'type': 'immediate',
                    'category': 'stress_relief',
                    'title': 'Stress Reduction',
                    'description': 'Try progressive muscle relaxation, meditation, or a short walk.',
                    'priority': 'medium'
                },
                {
                    'type': 'planning',
                    'category': 'organization',
                    'title': 'Prioritize Tasks',
                    'description': 'Make a list of priorities and tackle one thing at a time.',
                    'priority': 'medium'
                }
            ])
        
        # Low energy recommendations
        if energy_level <= 2:
            recommendations.extend([
                {
                    'type': 'physical',
                    'category': 'energy',
                    'title': 'Gentle Movement',
                    'description': 'Try light stretching, yoga, or a brief walk in fresh air.',
                    'priority': 'medium'
                },
                {
                    'type': 'nutrition',
                    'category': 'wellness',
                    'title': 'Nourish Yourself',
                    'description': 'Have a healthy snack and stay hydrated throughout the day.',
                    'priority': 'low'
                }
            ])
        
        # Poor sleep recommendations
        if sleep_quality <= 2:
            recommendations.extend([
                {
                    'type': 'evening',
                    'category': 'sleep_hygiene',
                    'title': 'Sleep Preparation',
                    'description': 'Create a calming bedtime routine and limit screen time before bed.',
                    'priority': 'medium'
                }
            ])
        
        return recommendations
    
    def assess_mental_health_risk(self, user_id: str, mood_data: Dict) -> Dict:
        """Assess mental health risk based on current and historical data"""
        try:
            # Get recent mood history
            recent_moods = self.get_recent_mood_history(user_id, days=7)
            
            current_mood = mood_data.get('mood_rating', 3)
            current_stress = mood_data.get('stress_level', 3)
            
            risk_factors = []
            risk_score = 0
            
            # Current mood risk
            if current_mood <= 2:
                risk_factors.append("Current low mood")
                risk_score += 3
            
            # High stress risk
            if current_stress >= 4:
                risk_factors.append("High stress levels")
                risk_score += 2
            
            # Historical pattern analysis
            if recent_moods:
                avg_mood = np.mean([entry['mood_rating'] for entry in recent_moods])
                if avg_mood <= 2.5:
                    risk_factors.append("Consistently low mood over past week")
                    risk_score += 4
                
                # Check for declining trend
                if len(recent_moods) >= 3:
                    recent_ratings = [entry['mood_rating'] for entry in recent_moods[-3:]]
                    if all(recent_ratings[i] >= recent_ratings[i+1] for i in range(len(recent_ratings)-1)):
                        risk_factors.append("Declining mood trend")
                        risk_score += 2
            
            # Determine risk level
            if risk_score >= 7:
                risk_level = "high"
                message = "Multiple concerning factors detected. Consider professional support."
            elif risk_score >= 4:
                risk_level = "moderate"
                message = "Some concerning patterns. Monitor closely and consider support."
            elif risk_score >= 2:
                risk_level = "low"
                message = "Minor concerns detected. Practice self-care and monitor."
            else:
                risk_level = "minimal"
                message = "No significant risk factors detected."
            
            return {
                'risk_level': risk_level,
                'risk_score': risk_score,
                'risk_factors': risk_factors,
                'message': message,
                'recommendations': self.get_risk_based_recommendations(risk_level)
            }
            
        except Exception as e:
            return {
                'risk_level': 'unknown',
                'error': str(e),
                'message': 'Unable to assess risk at this time'
            }
    
    def get_risk_based_recommendations(self, risk_level: str) -> List[str]:
        """Get recommendations based on risk level"""
        recommendations = {
            'high': [
                "Contact a mental health professional immediately",
                "Reach out to a trusted friend or family member",
                "Consider calling a crisis helpline if needed",
                "Avoid making major decisions while distressed"
            ],
            'moderate': [
                "Schedule an appointment with a counselor or therapist",
                "Maintain regular contact with supportive people",
                "Practice daily self-care activities",
                "Monitor your mood patterns closely"
            ],
            'low': [
                "Continue regular self-care practices",
                "Stay connected with friends and family",
                "Consider stress management techniques",
                "Keep tracking your mood patterns"
            ],
            'minimal': [
                "Keep up the good work with self-care",
                "Continue healthy lifestyle habits",
                "Stay aware of your mental health needs"
            ]
        }
        
        return recommendations.get(risk_level, [])
    
    def check_pattern_alerts(self, user_id: str, mood_data: Dict) -> List[Dict]:
        """Check for concerning patterns and generate alerts"""
        alerts = []
        
        try:
            # Get recent history for pattern analysis
            recent_entries = self.get_recent_mood_history(user_id, days=14)
            
            if len(recent_entries) >= 3:
                recent_moods = [entry['mood_rating'] for entry in recent_entries[-7:]]
                
                # Check for consistently low moods
                if all(mood <= 2 for mood in recent_moods[-3:]):
                    alerts.append({
                        'type': 'pattern',
                        'severity': 'high',
                        'title': 'Persistent Low Mood',
                        'message': 'Your mood has been consistently low for several days.',
                        'action': 'Consider reaching out for professional support.'
                    })
                
                # Check for rapid mood decline
                if len(recent_moods) >= 5:
                    if recent_moods[-1] <= 2 and recent_moods[-5] >= 4:
                        alerts.append({
                            'type': 'trend',
                            'severity': 'medium',
                            'title': 'Rapid Mood Decline',
                            'message': 'Your mood has declined significantly over the past few days.',
                            'action': 'Take extra care of yourself and consider talking to someone.'
                        })
            
            return alerts
            
        except Exception as e:
            return [{
                'type': 'error',
                'severity': 'low',
                'title': 'Pattern Analysis Unavailable',
                'message': 'Unable to analyze patterns at this time.',
                'action': 'Continue monitoring your mood.'
            }]
    
    def get_recent_mood_history(self, user_id: str, days: int = 30) -> List[Dict]:
        """Get recent mood history for analysis"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT mood_rating, energy_level, stress_level, sleep_quality, 
                           mood_notes, timestamp
                    FROM mood_entries_advanced 
                    WHERE user_id = ? AND timestamp >= datetime('now', '-{} days')
                    ORDER BY timestamp ASC
                '''.format(days), (user_id,))
                
                entries = []
                for row in cursor.fetchall():
                    entries.append({
                        'mood_rating': row[0],
                        'energy_level': row[1],
                        'stress_level': row[2],
                        'sleep_quality': row[3],
                        'mood_notes': row[4],
                        'timestamp': row[5]
                    })
                
                return entries
                
        except Exception as e:
            print(f"Error fetching mood history: {e}")
            return []
    
    def update_mood_patterns(self, user_id: str):
        """Update user's mood patterns based on recent data"""
        try:
            recent_entries = self.get_recent_mood_history(user_id, days=30)
            
            if len(recent_entries) < 5:
                return  # Need more data for pattern analysis
            
            patterns = self.analyze_mood_patterns(recent_entries)
            
            # Store patterns in database
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                for pattern_type, pattern_data in patterns.items():
                    cursor.execute('''
                        INSERT OR REPLACE INTO mood_patterns 
                        (user_id, pattern_type, pattern_data, strength)
                        VALUES (?, ?, ?, ?)
                    ''', (user_id, pattern_type, json.dumps(pattern_data), 
                          pattern_data.get('strength', 0.0)))
                
                conn.commit()
                
        except Exception as e:
            print(f"Error updating mood patterns: {e}")
    
    def analyze_mood_patterns(self, entries: List[Dict]) -> Dict:
        """Analyze mood patterns from historical data"""
        patterns = {}
        
        if not entries:
            return patterns
        
        # Weekly pattern analysis
        weekly_moods = defaultdict(list)
        for entry in entries:
            timestamp = datetime.fromisoformat(entry['timestamp'].replace('Z', '+00:00'))
            day_of_week = timestamp.strftime('%A')
            weekly_moods[day_of_week].append(entry['mood_rating'])
        
        # Calculate average mood by day of week
        weekly_averages = {}
        for day, moods in weekly_moods.items():
            if moods:
                weekly_averages[day] = np.mean(moods)
        
        if weekly_averages:
            patterns['weekly'] = {
                'averages': weekly_averages,
                'best_day': max(weekly_averages, key=weekly_averages.get),
                'worst_day': min(weekly_averages, key=weekly_averages.get),
                'strength': np.std(list(weekly_averages.values()))
            }
        
        # Trend analysis
        recent_moods = [entry['mood_rating'] for entry in entries[-14:]]  # Last 2 weeks
        if len(recent_moods) >= 7:
            # Simple linear trend
            x = np.arange(len(recent_moods))
            trend_slope = np.polyfit(x, recent_moods, 1)[0]
            
            patterns['trend'] = {
                'slope': trend_slope,
                'direction': 'improving' if trend_slope > 0.1 else 'declining' if trend_slope < -0.1 else 'stable',
                'strength': abs(trend_slope)
            }
        
        return patterns
    
    def get_comprehensive_analytics(self, user_id: str, days: int = 30) -> Dict:
        """Get comprehensive mood analytics for dashboard"""
        try:
            entries = self.get_recent_mood_history(user_id, days)
            
            if not entries:
                return {
                    'message': 'No mood data available for analysis',
                    'entries_count': 0
                }
            
            # Basic statistics
            mood_ratings = [entry['mood_rating'] for entry in entries]
            energy_levels = [entry['energy_level'] for entry in entries if entry['energy_level']]
            stress_levels = [entry['stress_level'] for entry in entries if entry['stress_level']]
            
            analytics = {
                'summary': {
                    'total_entries': len(entries),
                    'date_range': {
                        'start': entries[0]['timestamp'],
                        'end': entries[-1]['timestamp']
                    },
                    'average_mood': round(np.mean(mood_ratings), 2),
                    'mood_trend': self.calculate_trend(mood_ratings),
                    'best_mood': max(mood_ratings),
                    'lowest_mood': min(mood_ratings),
                    'mood_stability': round(np.std(mood_ratings), 2)
                },
                'detailed_metrics': {
                    'energy': {
                        'average': round(np.mean(energy_levels), 2) if energy_levels else None,
                        'trend': self.calculate_trend(energy_levels) if energy_levels else None
                    },
                    'stress': {
                        'average': round(np.mean(stress_levels), 2) if stress_levels else None,
                        'trend': self.calculate_trend(stress_levels) if stress_levels else None
                    }
                },
                'patterns': self.analyze_mood_patterns(entries),
                'insights': self.generate_analytics_insights(entries),
                'chart_data': self.prepare_chart_data(entries)
            }
            
            return analytics
            
        except Exception as e:
            return {
                'error': str(e),
                'message': 'Failed to generate analytics'
            }
    
    def calculate_trend(self, values: List[float]) -> str:
        """Calculate trend direction from a list of values"""
        if len(values) < 3:
            return 'insufficient_data'
        
        x = np.arange(len(values))
        slope = np.polyfit(x, values, 1)[0]
        
        if slope > 0.1:
            return 'improving'
        elif slope < -0.1:
            return 'declining'
        else:
            return 'stable'
    
    def generate_analytics_insights(self, entries: List[Dict]) -> List[Dict]:
        """Generate insights from analytics data"""
        insights = []
        
        if not entries:
            return insights
        
        mood_ratings = [entry['mood_rating'] for entry in entries]
        
        # Consistency insight
        mood_std = np.std(mood_ratings)
        if mood_std < 0.5:
            insights.append({
                'type': 'consistency',
                'title': 'Stable Mood Pattern',
                'message': 'Your mood has been quite consistent recently.',
                'positive': True
            })
        elif mood_std > 1.5:
            insights.append({
                'type': 'consistency',
                'title': 'Variable Mood Pattern',
                'message': 'Your mood has been quite variable. Consider tracking triggers.',
                'positive': False
            })
        
        # Recent trend insight
        recent_moods = mood_ratings[-7:] if len(mood_ratings) >= 7 else mood_ratings
        trend = self.calculate_trend(recent_moods)
        
        if trend == 'improving':
            insights.append({
                'type': 'trend',
                'title': 'Positive Trend',
                'message': 'Your mood has been improving recently. Keep up the good work!',
                'positive': True
            })
        elif trend == 'declining':
            insights.append({
                'type': 'trend',
                'title': 'Concerning Trend',
                'message': 'Your mood has been declining. Consider additional self-care.',
                'positive': False
            })
        
        return insights
    
    def prepare_chart_data(self, entries: List[Dict]) -> Dict:
        """Prepare data for frontend charts"""
        chart_data = {
            'mood_over_time': {
                'labels': [],
                'datasets': [
                    {
                        'label': 'Mood Rating',
                        'data': [],
                        'borderColor': '#3b82f6',
                        'backgroundColor': 'rgba(59, 130, 246, 0.1)',
                        'fill': True
                    }
                ]
            },
            'mood_distribution': {
                'labels': ['Severely Low', 'Low', 'Below Average', 'Good', 'Excellent'],
                'data': [0, 0, 0, 0, 0]
            }
        }
        
        for entry in entries:
            # Time series data
            timestamp = datetime.fromisoformat(entry['timestamp'].replace('Z', '+00:00'))
            chart_data['mood_over_time']['labels'].append(timestamp.strftime('%m/%d'))
            chart_data['mood_over_time']['datasets'][0]['data'].append(entry['mood_rating'])
            
            # Distribution data
            mood_index = entry['mood_rating'] - 1  # Convert 1-5 to 0-4
            chart_data['mood_distribution']['data'][mood_index] += 1
        
        return chart_data

# Global instance
mood_intelligence = MoodIntelligenceEngine()

def get_mood_intelligence():
    """Get the global mood intelligence instance"""
    return mood_intelligence