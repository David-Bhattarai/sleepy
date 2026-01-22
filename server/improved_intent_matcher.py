import json
import re
import random
from difflib import SequenceMatcher
from collections import Counter

class ImprovedIntentMatcher:
    def __init__(self, intents_file='intents.json'):
        with open(intents_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.intents = data.get('intents', [])
        
        # Create intent priority weights (lower = higher priority)
        self.intent_priorities = {
            'suicide': 1,      # Highest priority for safety
            'greeting': 2,
            'anxious': 3,
            'depressed': 3,
            'stressed': 3,
            'sad': 4,          # Lower priority due to too many patterns
            'thanks': 2,
            'goodbye': 2,
            'help': 3,
            'default': 10,     # Lowest priority
            'no-response': 10
        }
    
    def preprocess_text(self, text):
        """Clean and normalize text"""
        text = text.lower().strip()
        # Remove punctuation but keep question marks and exclamation points
        text = re.sub(r'[^\w\s\?\!]', ' ', text)
        text = ' '.join(text.split())  # Remove extra whitespace
        return text
    
    def calculate_similarity(self, text1, text2):
        """Calculate similarity between two texts"""
        return SequenceMatcher(None, text1, text2).ratio()
    
    def get_word_overlap_score(self, message_words, pattern_words):
        """Calculate weighted word overlap score"""
        overlap = len(message_words & pattern_words)
        if overlap == 0:
            return 0
        
        # Weight by pattern length (shorter patterns get higher weight)
        pattern_length = len(pattern_words)
        message_length = len(message_words)
        
        # Exact match bonus
        if message_words == pattern_words:
            return 100
        
        # Calculate overlap ratio
        overlap_ratio = overlap / max(pattern_length, message_length)
        return overlap_ratio * 50  # Scale to 0-50 range
    
    def match_intent(self, user_message):
        """Improved intent matching with multiple scoring methods"""
        message = self.preprocess_text(user_message)
        message_words = set(message.split())
        
        best_matches = []
        
        for intent in self.intents:
            tag = intent.get('tag', '')
            patterns = intent.get('patterns', [])
            
            max_score = 0
            best_pattern = ""
            
            for pattern in patterns:
                if not pattern.strip():
                    continue
                    
                processed_pattern = self.preprocess_text(pattern)
                pattern_words = set(processed_pattern.split())
                
                # Method 1: Exact substring match (highest score)
                if processed_pattern in message or message in processed_pattern:
                    score = 80 + len(processed_pattern)
                    if score > max_score:
                        max_score = score
                        best_pattern = pattern
                
                # Method 2: High similarity match
                elif self.calculate_similarity(message, processed_pattern) > 0.8:
                    score = 70 + self.calculate_similarity(message, processed_pattern) * 10
                    if score > max_score:
                        max_score = score
                        best_pattern = pattern
                
                # Method 3: Word overlap with context
                else:
                    overlap_score = self.get_word_overlap_score(message_words, pattern_words)
                    if overlap_score > 0:
                        # Bonus for key emotional words
                        emotional_words = {'anxious', 'anxiety', 'worried', 'stress', 'depressed', 'sad', 'happy', 'angry'}
                        if any(word in message_words and word in pattern_words for word in emotional_words):
                            overlap_score += 20
                        
                        if overlap_score > max_score:
                            max_score = overlap_score
                            best_pattern = pattern
            
            if max_score > 0:
                # Apply priority weighting
                priority_weight = self.intent_priorities.get(tag, 5)
                adjusted_score = max_score / priority_weight
                
                best_matches.append({
                    'tag': tag,
                    'score': adjusted_score,
                    'raw_score': max_score,
                    'pattern': best_pattern,
                    'priority': priority_weight
                })
        
        # Sort by adjusted score (highest first)
        best_matches.sort(key=lambda x: x['score'], reverse=True)
        
        return best_matches
    
    def get_response(self, user_message):
        """Get the best response for user message"""
        matches = self.match_intent(user_message)
        
        if not matches or matches[0]['score'] < 5:

            fallback_intents = [intent for intent in self.intents if intent.get('tag') in ['no-response', 'default']]
            if fallback_intents:
                responses = fallback_intents[0].get('responses', [])
                if responses:
                    return random.choice(responses)
            return "I'm not sure I understand. Could you tell me more?"
        
        best_match = matches[0]
        tag = best_match['tag']
        
    
        for intent in self.intents:
            if intent.get('tag') == tag:
                responses = intent.get('responses', [])
                if responses:
                    return random.choice(responses)
        
        return "I'm here to help. Please tell me more
improved_matcher = None

def get_improved_intent_response(user_message):
    """Get improved intent-based response"""
    global improved_matcher
    if improved_matcher is None:
        improved_matcher = ImprovedIntentMatcher()
    
    return improved_matcher.get_response(user_message)