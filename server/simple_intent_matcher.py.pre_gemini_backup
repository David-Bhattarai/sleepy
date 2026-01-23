#!/usr/bin/env python3
"""
Simple Direct Intent Matcher - No ML, Just Pure intents.json
Directly matches user input to intents.json patterns without any ML complexity
"""

import json
import random
import re
from difflib import SequenceMatcher

class SimpleIntentMatcher:
    """Simple intent matcher that directly uses intents.json without ML"""
    
    def __init__(self, intents_file='intents.json'):
        self.intents_file = intents_file
        self.intents = []
        self.load_intents()
    
    def load_intents(self):
        """Load intents from JSON file"""
        try:
            with open(self.intents_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.intents = data.get('intents', [])
                print(f"✅ Loaded {len(self.intents)} intents directly from {self.intents_file}")
                return True
        except Exception as e:
            print(f"❌ Error loading intents: {e}")
            return False
    
    def clean_text(self, text):
        """Simple text cleaning"""
        if not text:
            return ""
        
        # Convert to lowercase and strip
        text = text.lower().strip()
        
        # Remove extra spaces
        text = ' '.join(text.split())
        
        return text
    
    def calculate_similarity(self, text1, text2):
        """Calculate similarity between two texts"""
        return SequenceMatcher(None, text1, text2).ratio()
    
    def find_exact_match(self, user_message):
        """Find exact pattern match"""
        user_clean = self.clean_text(user_message)
        
        for intent in self.intents:
            tag = intent.get('tag', '')
            patterns = intent.get('patterns', [])
            
            for pattern in patterns:
                pattern_clean = self.clean_text(pattern)
                
                # Exact match
                if user_clean == pattern_clean:
                    return tag, 1.0, "exact_match"
                
                # Check if user message contains the pattern
                if pattern_clean in user_clean or user_clean in pattern_clean:
                    return tag, 0.9, "contains_match"
        
        return None, 0.0, "no_match"
    
    def find_keyword_match(self, user_message):
        """Find match based on keywords"""
        user_clean = self.clean_text(user_message)
        user_words = set(user_clean.split())
        
        best_match = None
        best_score = 0.0
        best_method = "keyword_match"
        
        for intent in self.intents:
            tag = intent.get('tag', '')
            patterns = intent.get('patterns', [])
            
            total_score = 0
            pattern_count = 0
            
            for pattern in patterns:
                pattern_clean = self.clean_text(pattern)
                pattern_words = set(pattern_clean.split())
                
                if not pattern_words:
                    continue
                
                # Calculate word overlap
                common_words = user_words & pattern_words
                if common_words:
                    overlap_score = len(common_words) / len(pattern_words)
                    total_score += overlap_score
                    pattern_count += 1
            
            if pattern_count > 0:
                avg_score = total_score / pattern_count
                if avg_score > best_score:
                    best_score = avg_score
                    best_match = tag
        
        return best_match, best_score, best_method
    
    def find_similarity_match(self, user_message):
        """Find match based on text similarity"""
        user_clean = self.clean_text(user_message)
        
        best_match = None
        best_score = 0.0
        best_method = "similarity_match"
        
        for intent in self.intents:
            tag = intent.get('tag', '')
            patterns = intent.get('patterns', [])
            
            for pattern in patterns:
                pattern_clean = self.clean_text(pattern)
                
                if not pattern_clean:
                    continue
                
                similarity = self.calculate_similarity(user_clean, pattern_clean)
                
                if similarity > best_score:
                    best_score = similarity
                    best_match = tag
        
        return best_match, best_score, best_method
    
    def get_response(self, tag):
        """Get random response for the given tag"""
        for intent in self.intents:
            if intent.get('tag') == tag:
                responses = intent.get('responses', [])
                if responses:
                    return random.choice(responses)
        return None
    
    def match_intent(self, user_message, min_confidence=0.3):
        """Match user message to intent using multiple methods"""
        if not user_message or not user_message.strip():
            return self.get_fallback_response()
        
        print(f"🔍 Matching: '{user_message}'")
        
        # Method 1: Exact match (highest priority)
        tag, score, method = self.find_exact_match(user_message)
        if tag and score >= 0.8:
            response = self.get_response(tag)
            if response:
                print(f"✅ {method}: {tag} (score: {score:.2f})")
                return response
        
        # Method 2: Keyword match
        tag, score, method = self.find_keyword_match(user_message)
        if tag and score >= min_confidence:
            response = self.get_response(tag)
            if response:
                print(f"✅ {method}: {tag} (score: {score:.2f})")
                return response
        
        # Method 3: Similarity match
        tag, score, method = self.find_similarity_match(user_message)
        if tag and score >= min_confidence:
            response = self.get_response(tag)
            if response:
                print(f"✅ {method}: {tag} (score: {score:.2f})")
                return response
        
        # Fallback
        print(f"⚠️ No good match found, using fallback")
        return self.get_fallback_response()
    
    def get_fallback_response(self):
        """Get fallback response when no intent matches"""
        fallback_responses = [
            "I'm here to listen. Can you tell me more?",
            "That's interesting. What else would you like to talk about?",
            "I understand. How does that make you feel?",
            "Thank you for sharing. Can you elaborate on that?",
            "I'm not sure I understand completely. Could you tell me more?"
        ]
        return random.choice(fallback_responses)

# Global instance
simple_matcher = None

def get_simple_intent_matcher():
    """Get the simple intent matcher instance"""
    global simple_matcher
    if simple_matcher is None:
        simple_matcher = SimpleIntentMatcher()
    return simple_matcher

def generate_simple_response(user_message):
    """Generate response using simple intent matching"""
    matcher = get_simple_intent_matcher()
    return matcher.match_intent(user_message)

# Test function
def test_simple_matcher():
    """Test the simple matcher"""
    print("🧪 Testing Simple Intent Matcher")
    print("=" * 50)
    
    matcher = SimpleIntentMatcher()
    
    test_messages = [
        "Hello",
        "Hi there",
        "Good morning",
        "Thank you",
        "Thanks",
        "Goodbye",
        "Bye",
        "Who are you?",
        "What is your name?",
        "I feel sad",
        "I am anxious",
        "I feel happy",
        "Can you help me?",
        "I need help"
    ]
    
    for message in test_messages:
        response = matcher.match_intent(message)
        print(f"User: '{message}'")
        print(f"AURA: '{response}'")
        print("-" * 30)

if __name__ == "__main__":
    test_simple_matcher()