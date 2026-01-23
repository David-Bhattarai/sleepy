#!/usr/bin/env python3
"""
Gemini AI Chatbot
Use Google Gemini for intelligent, contextual responses
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from gemini_ai_integration import get_gemini_ai

class GeminiChatbot:
    """Chatbot using Google Gemini AI for intelligent responses"""
    
    def __init__(self):
        self.gemini_ai = get_gemini_ai()
        self.available = self.gemini_ai and self.gemini_ai.api_key
        
        if self.available:
            print("✅ Gemini Chatbot initialized")
        else:
            print("⚠️ Gemini API key not found - using fallback")
    
    def generate_response(self, user_message, emotion_context=None, conversation_history=None):
        """
        Generate intelligent response using Gemini AI
        Much better than simple pattern matching
        """
        if not self.available:
            return self._fallback_response(user_message)
        
        try:
            # Analyze conversation context if available
            context_analysis = None
            if conversation_history and len(conversation_history) >= 3:
                context_analysis = self.gemini_ai.analyze_conversation_context(conversation_history)
            
            # Generate response with context
            result = self.gemini_ai.generate_intelligent_response(
                user_message, 
                emotion_context
            )
            
            if result['success']:
                print(f"🎯 Gemini response generated for: '{user_message[:30]}...'")
                return result['response']
            else:
                print(f"⚠️ Gemini response failed: {result.get('error')}")
                return self._fallback_response(user_message)
                
        except Exception as e:
            print(f"❌ Gemini chatbot error: {e}")
            return self._fallback_response(user_message)
    
    def _fallback_response(self, user_message):
        """Fallback responses when Gemini is not available"""
        import random
        
        # Simple keyword-based responses
        message_lower = user_message.lower()
        
        if any(word in message_lower for word in ['hello', 'hi', 'hey', 'greetings']):
            responses = [
                "Hello! I'm here to listen and support you. How are you feeling today?",
                "Hi there! It's good to connect with you. What's on your mind?",
                "Hey! I'm glad you reached out. How can I help you today?"
            ]
        elif any(word in message_lower for word in ['sad', 'depressed', 'down', 'unhappy']):
            responses = [
                "I'm sorry to hear you're feeling this way. Your feelings are valid, and I'm here to listen. Can you tell me more about what's been troubling you?",
                "It sounds like you're going through a difficult time. I want you to know that you're not alone. What's been weighing on your heart?",
                "I can hear the pain in your words. Thank you for trusting me with these feelings. What would help you feel a little less alone right now?"
            ]
        elif any(word in message_lower for word in ['stressed', 'overwhelmed', 'anxious', 'worried']):
            responses = [
                "Stress can feel overwhelming, but you're not alone in this. What's been the biggest source of pressure for you lately?",
                "It sounds like you're carrying a heavy load. When we're stressed, it's important to take things one step at a time. What's one thing that's within your control right now?",
                "I understand how exhausting stress can be. You've shown strength by reaching out. What usually helps you feel more grounded?"
            ]
        elif any(word in message_lower for word in ['thank', 'thanks', 'grateful']):
            responses = [
                "You're very welcome! I'm here whenever you need support.",
                "I'm glad I could help. Remember, reaching out shows strength.",
                "Thank you for sharing with me. How are you feeling now?"
            ]
        elif any(word in message_lower for word in ['bye', 'goodbye', 'see you']):
            responses = [
                "Take care of yourself. Remember, I'm here whenever you need to talk.",
                "Goodbye for now. You've shown courage by opening up today.",
                "See you later. Remember to be kind to yourself."
            ]
        else:
            responses = [
                "I'm here to listen and support you. Can you tell me more about what you're experiencing?",
                "Thank you for sharing that with me. How are you feeling about this situation?",
                "Your feelings matter, and I'm here to help. What would be most helpful for you right now?",
                "I appreciate you opening up to me. What's been on your mind lately?"
            ]
        
        return random.choice(responses)

# Global instance
gemini_chatbot = None

def get_gemini_chatbot():
    """Get the Gemini chatbot instance"""
    global gemini_chatbot
    if gemini_chatbot is None:
        gemini_chatbot = GeminiChatbot()
    return gemini_chatbot
