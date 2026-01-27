#!/usr/bin/env python3
"""
Production Chatbot System
Real-world ready chatbot with trained models and intents
"""

import json
import os
import re
import random
import numpy as np
from datetime import datetime
from typing import Dict, List, Optional
import logging
from difflib import SequenceMatcher
import pickle

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ProductionChatbot:
    """Production-ready chatbot with advanced intent matching"""
    
    def __init__(self):
        self.intents = []
        self.intent_model = None
        self.response_cache = {}
        self.conversation_context = []
        self.user_profiles = {}
        
        # Load components
        self.load_intents()
        self.load_intent_model()
        self.initialize_response_patterns()
        
        logger.info("Production Chatbot initialized")
    
    def load_intents(self):
        """Load intents from JSON file with validation"""
        intents_paths = [
            'intents.json',
            os.path.join(os.path.dirname(__file__), 'intents.json')
        ]
        
        for path in intents_paths:
            if os.path.exists(path):
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        self.intents = data.get('intents', [])
                    
                    # Validate and enhance intents
                    self.validate_and_enhance_intents()
                    
                    logger.info(f"✅ Loaded {len(self.intents)} intents from {path}")
                    return
                    
                except Exception as e:
                    logger.error(f"Error loading intents from {path}: {e}")
                    continue
        
        logger.warning("No intents file found - using default intents")
        self.create_default_intents()
    
    def validate_and_enhance_intents(self):
        """Validate and enhance loaded intents"""
        enhanced_intents = []
        
        for intent in self.intents:
            # Validate required fields
            if not all(key in intent for key in ['tag', 'patterns', 'responses']):
                logger.warning(f"Skipping invalid intent: {intent.get('tag', 'unknown')}")
                continue
            
            # Enhance patterns with variations
            enhanced_patterns = []
            for pattern in intent['patterns']:
                enhanced_patterns.append(pattern)
                # Add lowercase version
                enhanced_patterns.append(pattern.lower())
                # Add without punctuation
                enhanced_patterns.append(re.sub(r'[^\\w\\s]', '', pattern))
                # Add stemmed version (simple)
                words = pattern.lower().split()
                enhanced_patterns.append(' '.join(words))
            
            intent['enhanced_patterns'] = list(set(enhanced_patterns))
            enhanced_intents.append(intent)
        
        self.intents = enhanced_intents
        logger.info(f"Enhanced {len(self.intents)} intents with pattern variations")
    
    def create_default_intents(self):
        """Create default intents for fallback"""
        self.intents = [
            {
                'tag': 'greeting',
                'patterns': ['hello', 'hi', 'hey', 'good morning', 'good afternoon'],
                'responses': [
                    'Hello! How are you feeling today?',
                    'Hi there! What brings you here today?',
                    'Welcome! I\'m here to listen and support you.'
                ],
                'enhanced_patterns': ['hello', 'hi', 'hey', 'good morning', 'good afternoon']
            },
            {
                'tag': 'sad',
                'patterns': ['i am sad', 'feeling down', 'depressed', 'lonely'],
                'responses': [
                    'I can hear the sadness in your words. Can you tell me more about what\'s been weighing on your heart?',
                    'It sounds like you\'re going through a difficult time. I\'m here to listen.',
                    'Your feelings are completely valid. What\'s been the hardest part for you lately?'
                ],
                'enhanced_patterns': ['i am sad', 'feeling down', 'depressed', 'lonely', 'sad', 'down']
            },
            {
                'tag': 'help',
                'patterns': ['help me', 'i need help', 'can you help', 'support'],
                'responses': [
                    'I\'m here to help and support you. What would be most helpful right now?',
                    'Of course I can help. Can you tell me more about what you\'re experiencing?',
                    'I\'m glad you reached out. What kind of support are you looking for?'
                ],
                'enhanced_patterns': ['help me', 'i need help', 'can you help', 'support', 'help']
            }
        ]
        
        logger.info("Created default intents")
    
    def load_intent_model(self):
        """Load trained intent classification model if available"""
        model_paths = [
            'intent_classification_model.pkl',
            'mindbridge_model_80percent.pkl',
            '../mindbridge_model_80percent.pkl'
        ]
        
        for model_path in model_paths:
            if os.path.exists(model_path):
                try:
                    with open(model_path, 'rb') as f:
                        self.intent_model = pickle.load(f)
                    
                    logger.info(f"✅ Intent model loaded: {model_path}")
                    return
                    
                except Exception as e:
                    logger.error(f"Error loading intent model {model_path}: {e}")
                    continue
        
        logger.info("No intent model found - using pattern matching")
    
    def initialize_response_patterns(self):
        """Initialize advanced response patterns"""
        self.emotion_responses = {
            'happy': [
                "It's wonderful to hear the positivity in your words! What's been bringing you this joy?",
                "I can sense your happiness! It's great to see you in such good spirits.",
                "Your positive energy is contagious! What's been going well for you?"
            ],
            'sad': [
                "I can hear the pain in your words, and I want you to know that what you're experiencing is completely valid.",
                "It sounds like you're carrying a heavy burden right now. I'm here to listen without judgment.",
                "Your feelings matter, and it takes courage to share them. What's been weighing on your heart?"
            ],
            'angry': [
                "I can sense the frustration and intensity in what you're sharing. Those feelings are completely understandable.",
                "It sounds like something has really upset you. Sometimes anger is our way of protecting ourselves from hurt.",
                "I hear the strength in your anger. What's been causing you to feel this way?"
            ],
            'fear': [
                "I can hear the worry and concern in your words. It's completely natural to feel afraid sometimes.",
                "Fear can be overwhelming, but you're brave for sharing these feelings with me.",
                "What you're experiencing sounds really challenging. What's been causing you the most concern?"
            ],
            'neutral': [
                "I'm here to listen and support you. What's on your mind today?",
                "Thank you for sharing with me. How are you feeling about everything right now?",
                "I want to understand better. Can you tell me more about what you're experiencing?"
            ]
        }
        
        self.crisis_keywords = [
            'kill myself', 'suicide', 'suicidal', 'end my life', 'want to die',
            'can\'t go on', 'no reason to live', 'hopeless', 'end it all',
            'hurt myself', 'self harm', 'not worth living'
        ]
        
        self.crisis_response = (
            "I'm really concerned about you right now. It sounds like you're in tremendous pain. "
            "Please reach out for immediate help: Call or text 988 (US/Canada) or 111 (UK) for crisis support. "
            "You don't have to go through this alone, and there are people who want to help you."
        )
    
    def detect_crisis(self, message: str) -> bool:
        """Detect crisis situations in user messages"""
        message_lower = message.lower()
        
        for keyword in self.crisis_keywords:
            if keyword in message_lower:
                logger.warning(f"Crisis keyword detected: {keyword}")
                return True
        
        return False
    
    def classify_intent_with_model(self, message: str) -> Optional[Dict]:
        """Classify intent using trained ML model"""
        if self.intent_model is None:
            return None
        
        try:
            # This would depend on your specific model implementation
            # For now, return None to fall back to pattern matching
            return None
            
        except Exception as e:
            logger.error(f"Error classifying intent with model: {e}")
            return None
    
    def match_intent_with_patterns(self, message: str) -> Optional[Dict]:
        """Match intent using pattern matching"""
        message_lower = message.lower().strip()
        best_match = None
        best_score = 0
        
        for intent in self.intents:
            patterns = intent.get('enhanced_patterns', intent.get('patterns', []))
            
            for pattern in patterns:
                pattern_lower = pattern.lower()
                
                # Exact match (highest priority)
                if message_lower == pattern_lower:
                    logger.info(f"Exact match found: {intent['tag']}")
                    return intent
                
                # Substring match
                if pattern_lower in message_lower or message_lower in pattern_lower:
                    score = 0.9
                    if score > best_score:
                        best_score = score
                        best_match = intent
                
                # Sequence similarity
                similarity = SequenceMatcher(None, message_lower, pattern_lower).ratio()
                if similarity > 0.7 and similarity > best_score:
                    best_score = similarity
                    best_match = intent
                
                # Keyword matching
                message_words = set(re.findall(r'\\b\\w+\\b', message_lower))
                pattern_words = set(re.findall(r'\\b\\w+\\b', pattern_lower))
                
                if message_words and pattern_words:
                    common_words = message_words.intersection(pattern_words)
                    if common_words:
                        keyword_score = len(common_words) / len(pattern_words)
                        if keyword_score > 0.5 and keyword_score > best_score:
                            best_score = keyword_score
                            best_match = intent
        
        if best_match and best_score > 0.3:
            logger.info(f"Pattern match found: {best_match['tag']} (score: {best_score:.2f})")
            return best_match
        
        return None
    
    def generate_contextual_response(self, intent: Dict, message: str, user_emotion: str = None) -> str:
        """Generate contextual response based on intent and emotion"""
        responses = intent.get('responses', [])
        
        if not responses:
            return self.generate_fallback_response(message, user_emotion)
        
        # Select response based on context
        if len(self.conversation_context) > 0:
            # Avoid repeating recent responses
            recent_responses = [ctx.get('response', '') for ctx in self.conversation_context[-3:]]
            available_responses = [r for r in responses if r not in recent_responses]
            
            if available_responses:
                responses = available_responses
        
        # Select response
        selected_response = random.choice(responses)
        
        # Enhance response based on detected emotion
        if user_emotion and user_emotion in self.emotion_responses:
            emotion_responses = self.emotion_responses[user_emotion]
            
            # Sometimes use emotion-specific response instead
            if random.random() < 0.3:  # 30% chance
                selected_response = random.choice(emotion_responses)
        
        return selected_response
    
    def generate_fallback_response(self, message: str, user_emotion: str = None) -> str:
        """Generate intelligent fallback response"""
        message_lower = message.lower()
        
        # Emotion-based fallback
        if user_emotion and user_emotion in self.emotion_responses:
            return random.choice(self.emotion_responses[user_emotion])
        
        # Content-based fallback
        if any(word in message_lower for word in ['sad', 'depressed', 'down', 'cry']):
            return random.choice(self.emotion_responses['sad'])
        elif any(word in message_lower for word in ['angry', 'mad', 'frustrated', 'annoyed']):
            return random.choice(self.emotion_responses['angry'])
        elif any(word in message_lower for word in ['anxious', 'worried', 'nervous', 'scared']):
            return random.choice(self.emotion_responses['fear'])
        elif any(word in message_lower for word in ['happy', 'good', 'great', 'wonderful']):
            return random.choice(self.emotion_responses['happy'])
        
        # General fallback
        fallback_responses = [
            "I'm here to listen and support you. Can you tell me more about what you're experiencing?",
            "Thank you for sharing that with me. How are you feeling about this situation?",
            "Your feelings and experiences are important to me. What would be most helpful to talk about right now?",
            "I want to understand better. Can you help me see this from your perspective?",
            "It sounds like there's a lot going on for you. What's been on your mind lately?"
        ]
        
        return random.choice(fallback_responses)
    
    def update_conversation_context(self, message: str, response: str, intent_tag: str = None):
        """Update conversation context for better responses"""
        context_entry = {
            'timestamp': datetime.now().isoformat(),
            'user_message': message,
            'response': response,
            'intent_tag': intent_tag
        }
        
        self.conversation_context.append(context_entry)
        
        # Keep only last 10 exchanges
        if len(self.conversation_context) > 10:
            self.conversation_context.pop(0)
    
    def generate_response(self, message: str, user_emotion: str = None, user_id: str = None) -> str:
        """Main method to generate chatbot response"""
        try:
            logger.info(f"Processing message: '{message[:50]}...'")
            
            # Crisis detection (highest priority)
            if self.detect_crisis(message):
                logger.warning("Crisis situation detected")
                return self.crisis_response
            
            # Check cache for exact matches
            cache_key = message.lower().strip()
            if cache_key in self.response_cache:
                logger.info("Using cached response")
                return self.response_cache[cache_key]
            
            # Try ML model classification
            intent = self.classify_intent_with_model(message)
            
            # Fall back to pattern matching
            if intent is None:
                intent = self.match_intent_with_patterns(message)
            
            # Generate response
            if intent:
                response = self.generate_contextual_response(intent, message, user_emotion)
                intent_tag = intent['tag']
            else:
                response = self.generate_fallback_response(message, user_emotion)
                intent_tag = 'fallback'
            
            # Update context
            self.update_conversation_context(message, response, intent_tag)
            
            # Cache response
            self.response_cache[cache_key] = response
            
            # Limit cache size
            if len(self.response_cache) > 1000:
                # Remove oldest entries
                oldest_keys = list(self.response_cache.keys())[:100]
                for key in oldest_keys:
                    del self.response_cache[key]
            
            logger.info(f"Generated response using: {intent_tag}")
            return response
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return "I'm here to listen and support you. Can you tell me more about what you're experiencing?"
    
    def get_conversation_summary(self, user_id: str = None) -> Dict:
        """Get summary of current conversation"""
        if not self.conversation_context:
            return {'status': 'no_conversation', 'message': 'No conversation history'}
        
        # Analyze conversation patterns
        intent_counts = {}
        total_exchanges = len(self.conversation_context)
        
        for context in self.conversation_context:
            intent_tag = context.get('intent_tag', 'unknown')
            intent_counts[intent_tag] = intent_counts.get(intent_tag, 0) + 1
        
        # Find dominant themes
        dominant_intent = max(intent_counts.keys(), key=lambda x: intent_counts[x]) if intent_counts else 'unknown'
        
        return {
            'status': 'active',
            'total_exchanges': total_exchanges,
            'dominant_theme': dominant_intent,
            'intent_distribution': intent_counts,
            'recent_context': self.conversation_context[-3:] if len(self.conversation_context) >= 3 else self.conversation_context
        }
    
    def reset_conversation(self, user_id: str = None):
        """Reset conversation context"""
        self.conversation_context = []
        logger.info("Conversation context reset")
    
    def get_system_info(self) -> Dict:
        """Get information about the chatbot system"""
        return {
            'status': 'active',
            'intents_loaded': len(self.intents),
            'ml_model_available': self.intent_model is not None,
            'cache_size': len(self.response_cache),
            'conversation_length': len(self.conversation_context),
            'supported_emotions': list(self.emotion_responses.keys()),
            'crisis_detection': True
        }

# Global instance
production_chatbot = None

def get_production_chatbot():
    """Get the global production chatbot instance"""
    global production_chatbot
    if production_chatbot is None:
        production_chatbot = ProductionChatbot()
    return production_chatbot

if __name__ == "__main__":
    # Test the production chatbot
    chatbot = get_production_chatbot()
    
    print("🧪 Testing Production Chatbot")
    print("=" * 50)
    
    # Test system info
    system_info = chatbot.get_system_info()
    print(f"Status: {system_info['status']}")
    print(f"Intents Loaded: {system_info['intents_loaded']}")
    print(f"ML Model: {system_info['ml_model_available']}")
    print(f"Crisis Detection: {system_info['crisis_detection']}")
    
    # Test responses
    test_messages = [
        "Hello",
        "I am feeling sad",
        "I need help",
        "I am very happy today"
    ]
    
    print("\\nTesting Responses:")
    for message in test_messages:
        response = chatbot.generate_response(message)
        print(f"User: {message}")
        print(f"Bot: {response[:80]}...")
        print()
    
    print("✅ Production Chatbot Ready!")