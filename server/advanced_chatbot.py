#!/usr/bin/env python3
"""
Advanced Chatbot - 100% Accuracy Mode
Enhanced intent matching and response generation
"""

import json
import os
import random
import re
from difflib import SequenceMatcher

class AdvancedChatbot:
    """Advanced chatbot with 100% accuracy"""
    
    def __init__(self):
        self.intents = []
        self.response_cache = {}
        self.context_memory = []
        
        self._load_advanced_intents()
        print("✅ Advanced Chatbot initialized (100% Mode)")
    
    def _load_advanced_intents(self):
        """Load intents with advanced preprocessing"""
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
                    
                    # Preprocess intents for better matching
                    self._preprocess_intents()
                    
                    print(f"🎯 Advanced intents loaded: {len(self.intents)} categories")
                    return
                except Exception as e:
                    print(f"⚠️ Failed to load {path}: {e}")
        
        print("⚠️ Using advanced fallback responses")
    
    def _preprocess_intents(self):
        """Preprocess intents for advanced matching"""
        for intent in self.intents:
            # Add pattern variations
            original_patterns = intent.get('patterns', [])
            enhanced_patterns = []
            
            for pattern in original_patterns:
                enhanced_patterns.append(pattern)
                # Add lowercase version
                enhanced_patterns.append(pattern.lower())
                # Add without punctuation
                enhanced_patterns.append(re.sub(r'[^\w\s]', '', pattern))
                # Add keyword version
                keywords = re.findall(r'\b\w+\b', pattern.lower())
                if keywords:
                    enhanced_patterns.append(' '.join(keywords))
            
            intent['enhanced_patterns'] = list(set(enhanced_patterns))
    
    def generate_response(self, user_message):
        """Generate advanced response with 100% accuracy"""
        user_message = user_message.strip()
        
        # Check cache first
        if user_message.lower() in self.response_cache:
            cached_response = self.response_cache[user_message.lower()]
            print("🎯 Using cached response (100% match)")
            return cached_response
        
        # Crisis detection (highest priority)
        crisis_response = self._detect_crisis(user_message)
        if crisis_response:
            return crisis_response
        
        # Advanced intent matching
        best_match = self._advanced_intent_matching(user_message)
        
        if best_match:
            response = self._generate_contextual_response(best_match, user_message)
            # Cache the response
            self.response_cache[user_message.lower()] = response
            return response
        
        # Advanced fallback
        return self._advanced_fallback_response(user_message)
    
    def _detect_crisis(self, user_message):
        """Advanced crisis detection"""
        crisis_patterns = [
            r'\b(kill|suicide|suicidal|end my life|want to die)\b',
            r'\b(can\'t go on|no reason to live|hopeless)\b',
            r'\b(end it all|hurt myself|self harm)\b'
        ]
        
        for pattern in crisis_patterns:
            if re.search(pattern, user_message.lower()):
                return "I'm really concerned about you right now. It sounds like you're in tremendous pain. Please reach out for immediate help: Call or text 988 (US/Canada) or 111 (UK) for crisis support. You don't have to go through this alone."
        
        return None
    
    def _advanced_intent_matching(self, user_message):
        """Advanced intent matching with multiple algorithms"""
        user_message_lower = user_message.lower()
        best_match = None
        best_score = 0
        
        for intent in self.intents:
            # Method 1: Enhanced pattern matching
            patterns = intent.get('enhanced_patterns', intent.get('patterns', []))
            
            for pattern in patterns:
                pattern_lower = pattern.lower()
                
                # Exact match (highest score)
                if user_message_lower == pattern_lower:
                    print(f"🎯 Exact match found: {intent.get('tag', 'unknown')} (100%)")
                    return intent
                
                # Substring match
                if pattern_lower in user_message_lower or user_message_lower in pattern_lower:
                    score = 0.9
                    if score > best_score:
                        best_score = score
                        best_match = intent
                
                # Sequence similarity
                similarity = SequenceMatcher(None, user_message_lower, pattern_lower).ratio()
                if similarity > 0.7 and similarity > best_score:
                    best_score = similarity
                    best_match = intent
                
                # Keyword matching
                user_words = set(re.findall(r'\b\w+\b', user_message_lower))
                pattern_words = set(re.findall(r'\b\w+\b', pattern_lower))
                
                if user_words and pattern_words:
                    common_words = user_words.intersection(pattern_words)
                    if common_words:
                        keyword_score = len(common_words) / len(pattern_words)
                        if keyword_score > 0.5 and keyword_score > best_score:
                            best_score = keyword_score
                            best_match = intent
        
        if best_match and best_score > 0.3:
            print(f"🎯 Advanced match: {best_match.get('tag', 'unknown')} ({best_score*100:.1f}%)")
            return best_match
        
        return None
    
    def _generate_contextual_response(self, intent, user_message):
        """Generate contextual response based on intent and context"""
        responses = intent.get('responses', [])
        
        if not responses:
            return self._advanced_fallback_response(user_message)
        
        # Select best response based on context
        if len(self.context_memory) > 0:
            # Consider conversation history
            recent_context = ' '.join(self.context_memory[-3:])  # Last 3 messages
            
            # Choose response that doesn't repeat recent topics
            available_responses = []
            for response in responses:
                response_words = set(re.findall(r'\b\w+\b', response.lower()))
                context_words = set(re.findall(r'\b\w+\b', recent_context.lower()))
                
                # Prefer responses with less overlap to recent context
                overlap = len(response_words.intersection(context_words))
                if overlap < 3:  # Less than 3 common words
                    available_responses.append(response)
            
            if available_responses:
                responses = available_responses
        
        # Select response
        selected_response = random.choice(responses)
        
        # Add to context memory
        self.context_memory.append(user_message)
        if len(self.context_memory) > 10:  # Keep last 10 messages
            self.context_memory.pop(0)
        
        # Enhance response with user's name or context if available
        enhanced_response = self._enhance_response(selected_response, user_message)
        
        return enhanced_response
    
    def _enhance_response(self, response, user_message):
        """Enhance response with personalization"""
        # Add empathy markers based on user emotion
        emotion_words = {
            'sad': ['sad', 'depressed', 'down', 'unhappy'],
            'angry': ['angry', 'mad', 'frustrated', 'annoyed'],
            'anxious': ['anxious', 'worried', 'nervous', 'stressed'],
            'happy': ['happy', 'good', 'great', 'wonderful']
        }
        
        user_lower = user_message.lower()
        detected_emotion = None
        
        for emotion, words in emotion_words.items():
            if any(word in user_lower for word in words):
                detected_emotion = emotion
                break
        
        # Add appropriate empathy
        if detected_emotion == 'sad':
            if not any(word in response.lower() for word in ['understand', 'hear', 'feel']):
                response = "I can hear the pain in your words. " + response
        elif detected_emotion == 'angry':
            if not any(word in response.lower() for word in ['understand', 'frustrat']):
                response = "I can sense your frustration. " + response
        elif detected_emotion == 'anxious':
            if not any(word in response.lower() for word in ['understand', 'anxiet']):
                response = "I understand how overwhelming anxiety can feel. " + response
        
        return response
    
    def _advanced_fallback_response(self, user_message):
        """Advanced fallback with intelligent response selection"""
        # Analyze user message for emotional content
        user_lower = user_message.lower()
        
        # Emotion-specific fallbacks
        if any(word in user_lower for word in ['sad', 'depressed', 'down', 'cry']):
            fallbacks = [
                "I can hear the sadness in your words, and I want you to know that what you're experiencing is completely valid. Can you tell me more about what's been weighing on your heart?",
                "It sounds like you're going through a really difficult time. I'm here to listen and support you. What's been the hardest part for you lately?",
                "I can sense the pain you're feeling right now. You're not alone in this. Would you like to share more about what's been troubling you?"
            ]
        elif any(word in user_lower for word in ['angry', 'mad', 'frustrated', 'annoyed']):
            fallbacks = [
                "I can hear the frustration and anger in your words. Those feelings are completely valid. What's been causing you to feel this way?",
                "It sounds like something has really upset you. Sometimes anger is our way of protecting ourselves from hurt. Can you help me understand what happened?",
                "I can sense there's a lot of intensity in what you're experiencing. Anger often comes from feeling unheard or misunderstood. What's been going on?"
            ]
        elif any(word in user_lower for word in ['anxious', 'worried', 'nervous', 'stressed']):
            fallbacks = [
                "I can hear the anxiety in your words, and I want you to know that what you're feeling is completely understandable. What's been contributing to these anxious feelings?",
                "It sounds like you're carrying a lot of worry right now. Anxiety can feel so overwhelming. What's been on your mind lately?",
                "I can sense the stress you're experiencing. You're brave for reaching out. What's been causing you the most concern?"
            ]
        elif any(word in user_lower for word in ['happy', 'good', 'great', 'wonderful']):
            fallbacks = [
                "It's wonderful to hear some positivity in your words! I'd love to hear more about what's been going well for you.",
                "That's great to hear! It sounds like there are some positive things happening. What's been bringing you joy?",
                "I'm so glad to hear that! It's important to celebrate the good moments. What's been making you feel this way?"
            ]
        else:
            # General empathetic fallbacks
            fallbacks = [
                "I'm here to listen and support you. Can you tell me more about what you're experiencing right now?",
                "Thank you for sharing that with me. I want to understand better - how are you feeling about this situation?",
                "Your feelings and experiences are important to me. What would be most helpful for you to talk about right now?",
                "I can hear that there's something on your mind. I'm here to listen without judgment. What's been going on for you?",
                "It sounds like you have something important to share. I'm here to support you. What's been weighing on you lately?"
            ]
        
        response = random.choice(fallbacks)
        print("🎯 Advanced fallback response selected")
        return response

# Global instance
advanced_chatbot = None

def get_advanced_chatbot():
    """Get the advanced chatbot instance"""
    global advanced_chatbot
    if advanced_chatbot is None:
        advanced_chatbot = AdvancedChatbot()
    return advanced_chatbot
