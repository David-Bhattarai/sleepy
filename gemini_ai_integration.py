#!/usr/bin/env python3
"""
Google Gemini AI Integration
Connect both emotion detection and chatbot to Google Gemini AI for better accuracy
"""

import google.generativeai as genai
import base64
import json
import os
from PIL import Image
import io
import requests

class GeminiAIIntegration:
    """Google Gemini AI integration for emotion detection and chatbot"""
    
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            print("⚠️ GEMINI_API_KEY not found. Please set your API key.")
            print("Get your API key from: https://makersuite.google.com/app/apikey")
            return
        
        # Configure Gemini
        genai.configure(api_key=self.api_key)
        
        # Initialize models
        self.vision_model = genai.GenerativeModel('models/gemini-2.5-flash')
        self.text_model = genai.GenerativeModel('models/gemini-2.5-flash')
        
        print("✅ Google Gemini AI initialized successfully!")
    
    def detect_emotion_from_face(self, image_data):
        """
        Use Gemini Vision to detect exact emotions from face
        Much more accurate than local models
        """
        try:
            # Prepare the image
            if image_data.startswith('data:image'):
                # Remove data URL prefix
                image_data = image_data.split(',')[1]
            
            # Decode base64 image
            image_bytes = base64.b64decode(image_data)
            image = Image.open(io.BytesIO(image_bytes))
            
            # Prepare prompt for emotion detection
            emotion_prompt = """
            Analyze this image and detect the person's facial emotion with high accuracy.
            
            Please provide:
            1. The dominant emotion (angry, disgust, fear, happy, neutral, sad, surprise)
            2. Confidence percentage (0-100)
            3. All detected emotions with their percentages
            4. Brief description of facial features that indicate this emotion
            
            Respond in JSON format:
            {
                "dominant_emotion": "emotion_name",
                "confidence": 95.5,
                "all_emotions": {
                    "happy": 85.2,
                    "neutral": 10.1,
                    "sad": 4.7
                },
                "description": "The person shows clear signs of happiness with raised cheeks and slight smile",
                "face_detected": true
            }
            
            If no clear face is detected, set face_detected to false.
            """
            
            # Generate response using Gemini Vision
            response = self.vision_model.generate_content([emotion_prompt, image])
            
            # Parse JSON response
            response_text = response.text.strip()
            
            # Clean up response if it has markdown formatting
            if response_text.startswith('```json'):
                response_text = response_text.replace('```json', '').replace('```', '').strip()
            
            result = json.loads(response_text)
            
            print(f"🤖 Gemini Emotion Detection:")
            print(f"   - Dominant: {result['dominant_emotion']}")
            print(f"   - Confidence: {result['confidence']}%")
            print(f"   - Face Detected: {result['face_detected']}")
            
            return {
                'success': True,
                'dominant_emotion': result['dominant_emotion'],
                'confidence': result['confidence'],
                'emotions': result['all_emotions'],
                'description': result['description'],
                'face_detected': result['face_detected'],
                'method': 'gemini_vision_ai'
            }
            
        except Exception as e:
            print(f"❌ Gemini emotion detection error: {e}")
            return {
                'success': False,
                'error': str(e),
                'dominant_emotion': 'neutral',
                'confidence': 0,
                'emotions': {},
                'face_detected': False,
                'method': 'gemini_vision_ai'
            }
    
    def generate_intelligent_response(self, user_message, emotion_context=None):
        """
        Use Gemini to generate intelligent, contextual responses
        Much better than simple pattern matching
        """
        try:
            # Prepare context-aware prompt
            context_prompt = f"""
            You are AURA, a compassionate AI therapeutic assistant. A user has sent you this message: "{user_message}"
            
            """
            
            if emotion_context:
                context_prompt += f"""
                Additional context: The user's current detected emotion is "{emotion_context['emotion']}" with {emotion_context['confidence']}% confidence.
                Emotion description: {emotion_context.get('description', 'No description')}
                
                """
            
            context_prompt += """
            Please respond as a caring, professional therapeutic assistant. Your response should:
            1. Be empathetic and understanding
            2. Acknowledge their feelings
            3. Ask thoughtful follow-up questions when appropriate
            4. Provide gentle guidance or support
            5. Be conversational and warm, not clinical
            6. Keep responses concise but meaningful (2-3 sentences max)
            
            If the user expresses crisis thoughts (suicide, self-harm), immediately provide crisis resources.
            
            Respond naturally as AURA would, without explaining your process.
            """
            
            # Generate response using Gemini
            response = self.text_model.generate_content(context_prompt)
            ai_response = response.text.strip()
            
            print(f"🤖 Gemini Response Generated:")
            print(f"   - Input: '{user_message[:50]}...'")
            print(f"   - Response: '{ai_response[:50]}...'")
            
            return {
                'success': True,
                'response': ai_response,
                'method': 'gemini_text_ai',
                'emotion_context_used': emotion_context is not None
            }
            
        except Exception as e:
            print(f"❌ Gemini response generation error: {e}")
            
            # Fallback responses
            fallback_responses = [
                "I'm here to listen and support you. Can you tell me more about what you're experiencing?",
                "Thank you for sharing that with me. How are you feeling about this situation?",
                "I understand this might be difficult to talk about. What would be most helpful for you right now?",
                "Your feelings are valid, and I'm here to help. What's been on your mind lately?",
                "I appreciate you opening up to me. How can I best support you today?"
            ]
            
            import random
            fallback = random.choice(fallback_responses)
            
            return {
                'success': False,
                'response': fallback,
                'method': 'fallback',
                'error': str(e)
            }
    
    def analyze_conversation_context(self, conversation_history):
        """
        Use Gemini to analyze conversation patterns and provide insights
        """
        try:
            if not conversation_history or len(conversation_history) < 3:
                return None
            
            # Prepare conversation for analysis
            conversation_text = "\n".join([
                f"User: {entry['user_message']}\nAURA: {entry['ai_response']}"
                for entry in conversation_history[-5:]  # Last 5 exchanges
            ])
            
            analysis_prompt = f"""
            Analyze this conversation between a user and AURA (therapeutic AI assistant):
            
            {conversation_text}
            
            Provide insights in JSON format:
            {{
                "overall_mood": "positive/neutral/negative/crisis",
                "mood_trend": "improving/stable/declining",
                "key_themes": ["theme1", "theme2"],
                "suggested_approach": "brief suggestion for next response",
                "crisis_indicators": false
            }}
            """
            
            response = self.text_model.generate_content(analysis_prompt)
            response_text = response.text.strip()
            
            if response_text.startswith('```json'):
                response_text = response_text.replace('```json', '').replace('```', '').strip()
            
            analysis = json.loads(response_text)
            return analysis
            
        except Exception as e:
            print(f"❌ Conversation analysis error: {e}")
            return None

# Global instance
gemini_ai = None

def get_gemini_ai():
    """Get the Gemini AI instance"""
    global gemini_ai
    if gemini_ai is None:
        gemini_ai = GeminiAIIntegration()
    return gemini_ai

def setup_gemini_api_key():
    """Setup Gemini API key"""
    print("🔑 Setting up Google Gemini API Key")
    print("=" * 50)
    print("1. Go to: https://makersuite.google.com/app/apikey")
    print("2. Create a new API key")
    print("3. Copy the API key")
    print("4. Set it as environment variable: GEMINI_API_KEY")
    print()
    print("For Windows:")
    print("set GEMINI_API_KEY=your_api_key_here")
    print()
    print("For Linux/Mac:")
    print("export GEMINI_API_KEY=your_api_key_here")
    print()
    
    api_key = input("Enter your Gemini API key (or press Enter to skip): ").strip()
    
    if api_key:
        os.environ['GEMINI_API_KEY'] = api_key
        print("✅ API key set for this session!")
        return api_key
    else:
        print("⚠️ No API key provided. You'll need to set GEMINI_API_KEY environment variable.")
        return None

def test_gemini_integration():
    """Test Gemini AI integration"""
    print("🧪 Testing Google Gemini AI Integration")
    print("=" * 60)
    
    # Setup API key if needed
    if not os.getenv('GEMINI_API_KEY'):
        api_key = setup_gemini_api_key()
        if not api_key:
            print("❌ Cannot test without API key")
            return
    
    # Initialize Gemini
    ai = get_gemini_ai()
    if not ai.api_key:
        print("❌ Gemini AI not initialized")
        return
    
    # Test text generation
    print("\n🤖 Testing Intelligent Response Generation:")
    test_messages = [
        "I feel really sad today",
        "I'm so stressed about work",
        "Thank you for helping me",
        "I don't know what to do anymore"
    ]
    
    for message in test_messages:
        print(f"\nUser: '{message}'")
        result = ai.generate_intelligent_response(message)
        if result['success']:
            print(f"AURA: '{result['response']}'")
        else:
            print(f"Error: {result.get('error', 'Unknown error')}")
    
    # Test emotion detection (with dummy image)
    print("\n😊 Testing Emotion Detection:")
    print("Note: This would work with real face images")
    
    print("\n✅ Gemini AI integration test completed!")

if __name__ == "__main__":
    test_gemini_integration()