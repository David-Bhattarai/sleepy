#!/usr/bin/env python3
"""
Hybrid Chatbot System
Combines trained ML models with Gemini AI for intelligent responses
Both systems work together for maximum accuracy and empathy
"""

import os
import json
import random
from datetime import datetime

# Import all chatbot methods
try:
    from gemini_chatbot import get_gemini_chatbot
    GEMINI_CHATBOT_AVAILABLE = True
except ImportError:
    GEMINI_CHATBOT_AVAILABLE = False

try:
    from simple_intent_matcher import get_simple_intent_matcher
    INTENT_MATCHER_AVAILABLE = True
except ImportError:
    INTENT_MATCHER_AVAILABLE = False

try:
    from ml_model_realistic import get_realistic_ml_model
    ML_CHATBOT_AVAILABLE = True
except ImportError:
    ML_CHATBOT_AVAILABLE = False

class HybridChatbotSystem:
    """
    Hybrid chatbot system that combines:
    1. Trained ML models (from intents dataset)
    2. Gemini AI conversational AI
    3. Simple intent matching
    """
    
    def __init__(self):
        self.gemini_chatbot = None
        self.intent_matcher = None
        self.ml_model = None
        self.intents_data = None
        
        print("🤖 Initializing Hybrid Chatbot System...")
        self._load_all_chatbots()
    
    def _load_all_chatbots(self):
        """Load all available chatbot methods"""
        
        # Load Gemini AI chatbot
        if GEMINI_CHATBOT_AVAILABLE:
            try:
                self.gemini_chatbot = get_gemini_chatbot()
                print("✅ Gemini AI chatbot loaded")
            except Exception as e:
                print(f"⚠️ Gemini AI chatbot failed: {e}")
        
        # Load intent matcher
        if INTENT_MATCHER_AVAILABLE:
            try:
                self.intent_matcher = get_simple_intent_matcher()
                print("✅ Intent matcher loaded")
            except Exception as e:
                print(f"⚠️ Intent matcher failed: {e}")
        
        # Load trained ML model
        if ML_CHATBOT_AVAILABLE:
            try:
                self.ml_model = get_realistic_ml_model()
                print("✅ ML chatbot model loaded")
            except Exception as e:
                print(f"⚠️ ML chatbot model failed: {e}")
        
        # Load intents data
        self._load_intents_data()
    
    def _load_intents_data(self):
        """Load intents.json data"""
        try:
            # Try multiple possible paths
            possible_paths = [
                "intents.json",
                os.path.join(os.path.dirname(__file__), "intents.json"),
                os.path.join(os.path.dirname(os.path.dirname(__file__)), "sleepy", "server", "intents.json")
            ]
            
            for intents_path in possible_paths:
                if os.path.exists(intents_path):
                    with open(intents_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        self.intents_data = data.get('intents', [])
                    print(f"✅ Intents data loaded from {intents_path} ({len(self.intents_data)} intents)")
                    return
            
            print("⚠️ intents.json not found in any expected location")
            self.intents_data = []
        except Exception as e:
            print(f"⚠️ Failed to load intents: {e}")
            self.intents_data = []
    
    def generate_hybrid_response(self, user_message, user_emotion=None, conversation_history=None):
        """
        Generate response using hybrid approach
        Combines all available methods for best response
        """
        print(f"🤖 Processing message: '{user_message[:50]}...'")
        
        responses = []
        
        # Method 1: Gemini AI (highest priority for complex conversations)
        if self.gemini_chatbot:
            try:
                # Add emotion context to Gemini
                enhanced_message = user_message
                if user_emotion and user_emotion != 'neutral':
                    enhanced_message = f"[User seems {user_emotion}] {user_message}"
                
                gemini_response = self.gemini_chatbot.generate_response(enhanced_message)
                if gemini_response and len(gemini_response) > 20:
                    responses.append({
                        'response': gemini_response,
                        'method': 'gemini_ai',
                        'confidence': 95,
                        'priority': 1,
                        'type': 'conversational'
                    })
                    print(f"🤖 Gemini AI response generated")
            except Exception as e:
                print(f"⚠️ Gemini chatbot failed: {e}")
        
        # Method 2: Trained ML Model
        if self.ml_model:
            try:
                # Try different method names for ML model
                ml_response = None
                if hasattr(self.ml_model, 'predict_intent_and_respond'):
                    ml_response = self.ml_model.predict_intent_and_respond(user_message)
                elif hasattr(self.ml_model, 'predict_response'):
                    ml_response = self.ml_model.predict_response(user_message)
                elif hasattr(self.ml_model, 'get_response'):
                    ml_response = self.ml_model.get_response(user_message)
                
                if ml_response and ml_response != "I'm not sure how to respond to that.":
                    responses.append({
                        'response': ml_response,
                        'method': 'trained_ml_model',
                        'confidence': 85,
                        'priority': 2,
                        'type': 'intent_based'
                    })
                    print(f"🧠 ML model response generated")
            except Exception as e:
                print(f"⚠️ ML model failed: {e}")
        
        # Method 3: Intent Matcher (for specific patterns)
        if self.intent_matcher:
            try:
                intent_response = self.intent_matcher.match_intent(user_message)
                if intent_response:
                    responses.append({
                        'response': intent_response,
                        'method': 'intent_matcher',
                        'confidence': 80,
                        'priority': 3,
                        'type': 'pattern_based'
                    })
                    print(f"🎯 Intent matcher response generated")
            except Exception as e:
                print(f"⚠️ Intent matcher failed: {e}")
        
        # Method 4: Emotion-aware responses
        emotion_response = self._generate_emotion_aware_response(user_message, user_emotion)
        if emotion_response:
            responses.append({
                'response': emotion_response,
                'method': 'emotion_aware',
                'confidence': 75,
                'priority': 4,
                'type': 'emotion_based'
            })
            print(f"😊 Emotion-aware response generated")
        
        # Combine and return best response
        return self._select_best_response(responses, user_message, user_emotion)
    
    def _generate_emotion_aware_response(self, user_message, user_emotion):
        """Generate emotion-aware responses based on detected emotion"""
        if not user_emotion or user_emotion == 'neutral':
            return None
        
        emotion_responses = {
            'happy': [
                "It's wonderful to see you feeling happy! What's bringing you this joy today?",
                "Your happiness is contagious! I'd love to hear more about what's making you feel so positive.",
                "That's fantastic! It's great to connect with you when you're in such a good mood."
            ],
            'sad': [
                "I can sense the sadness in your words, and I want you to know that what you're feeling is completely valid. Can you tell me more about what's weighing on your heart?",
                "It sounds like you're going through a difficult time. I'm here to listen and support you. What's been the hardest part for you?",
                "I can hear the pain in what you're sharing. You're not alone in this. Would you like to talk about what's making you feel this way?"
            ],
            'angry': [
                "I can sense there's a lot of frustration and anger in what you're experiencing. Those feelings are valid. What's been triggering these strong emotions?",
                "It sounds like something has really upset you. Anger often comes from feeling hurt or misunderstood. Can you help me understand what happened?",
                "I hear the intensity in your words. Sometimes anger is our way of protecting ourselves. What's underneath that anger for you?"
            ],
            'fear': [
                "I can sense that you're feeling scared or anxious about something. Fear can be overwhelming, but you're brave for reaching out. What's been causing you to feel this way?",
                "It takes courage to acknowledge when we're afraid. I'm here to support you through this. Can you tell me more about what's making you feel fearful?",
                "Fear is such a human response to uncertainty. You're not alone in feeling this way. What would help you feel safer right now?"
            ],
            'surprise': [
                "It sounds like something unexpected has happened! Sometimes surprises can be overwhelming. How are you processing this?",
                "Life can certainly throw us curveballs! How are you feeling about this surprise?",
                "Unexpected events can stir up a lot of emotions. What's going through your mind right now?"
            ],
            'disgust': [
                "It sounds like something has really bothered or upset you. Those feelings of revulsion are valid. What's been troubling you?",
                "Sometimes we encounter things that just don't sit right with us. Can you tell me more about what's been disturbing you?",
                "I can sense your strong negative reaction to something. What's been causing you to feel this way?"
            ]
        }
        
        if user_emotion in emotion_responses:
            return random.choice(emotion_responses[user_emotion])
        
        return None
    
    def _select_best_response(self, responses, user_message, user_emotion):
        """Select the best response from all available methods"""
        if not responses:
            return self._fallback_response(user_emotion)
        
        # Sort by priority and confidence
        responses.sort(key=lambda x: (x['priority'], -x['confidence']))
        
        # Crisis detection - always prioritize safety
        crisis_keywords = ['kill myself', 'suicide', 'suicidal', 'end my life', 'want to die', 
                          'can\'t go on', 'no reason to live', 'hopeless', 'end it all']
        
        if any(keyword in user_message.lower() for keyword in crisis_keywords):
            crisis_response = {
                'response': "I'm really concerned about you right now. It sounds like you're in tremendous pain. Please reach out for immediate help: Call or text 988 (US/Canada) or 111 (UK) for crisis support. You don't have to go through this alone.",
                'method': 'crisis_intervention',
                'confidence': 100,
                'type': 'safety_priority',
                'hybrid_info': {
                    'crisis_detected': True,
                    'methods_available': len(responses),
                    'safety_override': True
                }
            }
            return crisis_response
        
        # Select best non-crisis response
        best_response = responses[0]
        
        # Add hybrid information
        best_response['hybrid_info'] = {
            'methods_used': len(responses),
            'all_methods': [r['method'] for r in responses],
            'confidence_scores': {r['method']: r['confidence'] for r in responses},
            'user_emotion': user_emotion,
            'response_type': best_response['type']
        }
        
        print(f"🎯 Best response selected: {best_response['method']} ({best_response['confidence']}% confidence)")
        return best_response
    
    def _fallback_response(self, user_emotion=None):
        """Fallback response when all methods fail"""
        fallback_responses = [
            "I'm here to listen and support you. Can you tell me more about what you're experiencing?",
            "Thank you for sharing that with me. How are you feeling about this situation?",
            "Your feelings are valid, and I'm here to help. What would be most helpful for you right now?",
            "I want to understand better. Can you help me see this from your perspective?",
            "It sounds like there's a lot going on for you. What's the most important thing you'd like to talk about?"
        ]
        
        # Emotion-specific fallbacks
        if user_emotion == 'sad':
            fallback_responses.extend([
                "I can sense you're going through a difficult time. I'm here to listen.",
                "It's okay to feel sad. Sometimes we need to sit with these feelings. What's on your mind?"
            ])
        elif user_emotion == 'angry':
            fallback_responses.extend([
                "I can hear the frustration in your words. What's been bothering you?",
                "It sounds like something has really upset you. I'm here to listen."
            ])
        
        return {
            'response': random.choice(fallback_responses),
            'method': 'fallback',
            'confidence': 60,
            'type': 'general_support',
            'hybrid_info': {
                'methods_used': 0,
                'all_methods': [],
                'confidence_scores': {},
                'user_emotion': user_emotion,
                'fallback_reason': 'all_methods_failed'
            }
        }

# Global instance
hybrid_chatbot = None

def get_hybrid_chatbot_system():
    """Get the hybrid chatbot system instance"""
    global hybrid_chatbot
    if hybrid_chatbot is None:
        hybrid_chatbot = HybridChatbotSystem()
    return hybrid_chatbot