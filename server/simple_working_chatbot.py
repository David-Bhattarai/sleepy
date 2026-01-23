#!/usr/bin/env python3
"""
Simple Working Chatbot
Uses intents.json that actually works
"""

import json
import os
import random
import re

class SimpleWorkingChatbot:
    """Simple chatbot that actually works"""
    
    def __init__(self):
        self.intents = []
        self._load_intents()
    
    def _load_intents(self):
        """Load intents from JSON file"""
        intents_paths = [
            "intents.json",
            os.path.join(os.path.dirname(__file__), "intents.json")
        ]
        
        for path in intents_paths:
            if os.path.exists(path):
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        self.intents = data.get('intents', [])
                    print(f"Loaded {len(self.intents)} intents from {path}")
                    return
                except Exception as e:
                    print(f"Failed to load {path}: {e}")
        
        print("No intents loaded - using fallback responses")
    
    def generate_response(self, user_message):
        """Generate response based on intents"""
        user_message = user_message.lower().strip()
        
        # Crisis detection first
        crisis_keywords = ['kill myself', 'suicide', 'suicidal', 'end my life', 'want to die']
        if any(keyword in user_message for keyword in crisis_keywords):
            return "I'm really concerned about you right now. Please reach out for immediate help: Call or text 988 (US/Canada) or 111 (UK) for crisis support. You don't have to go through this alone."
        
        # Try to match intents
        best_match = None
        best_score = 0
        
        for intent in self.intents:
            patterns = intent.get('patterns', [])
            
            for pattern in patterns:
                pattern_lower = pattern.lower()
                
                # Simple keyword matching
                words_in_pattern = set(pattern_lower.split())
                words_in_message = set(user_message.split())
                
                # Calculate similarity
                common_words = words_in_pattern.intersection(words_in_message)
                if common_words:
                    score = len(common_words) / len(words_in_pattern)
                    
                    if score > best_score and score > 0.3:  # Minimum threshold
                        best_score = score
                        best_match = intent
        
        if best_match:
            responses = best_match.get('responses', [])
            if responses:
                response = random.choice(responses)
                print(f"Matched intent: {best_match.get('tag', 'unknown')} (score: {best_score:.2f})")
                return response
        
        # Fallback responses
        fallback_responses = [
            "I'm here to listen and support you. Can you tell me more about what you're experiencing?",
            "Thank you for sharing that with me. How are you feeling about this situation?",
            "Your feelings are valid, and I'm here to help. What would be most helpful for you right now?",
            "I want to understand better. Can you help me see this from your perspective?",
            "It sounds like there's a lot going on for you. What's the most important thing you'd like to talk about?"
        ]
        
        return random.choice(fallback_responses)

# Global instance
simple_chatbot = None

def get_simple_working_chatbot():
    """Get the simple working chatbot"""
    global simple_chatbot
    if simple_chatbot is None:
        simple_chatbot = SimpleWorkingChatbot()
    return simple_chatbot