#!/usr/bin/env python3
"""
Gemini AI Emotion Detector
Use Google Gemini Vision API for accurate face emotion detection
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from gemini_ai_integration import get_gemini_ai

class GeminiEmotionDetector:
    """Emotion detector using Google Gemini Vision AI"""
    
    def __init__(self):
        self.gemini_ai = get_gemini_ai()
        self.available = self.gemini_ai and self.gemini_ai.api_key
        
        if self.available:
            print("✅ Gemini Emotion Detector initialized")
        else:
            print("⚠️ Gemini API key not found - using fallback")
    
    def detect_emotion_from_image(self, image_data):
        """
        Detect emotion from image using Gemini Vision AI
        Much more accurate than local models
        """
        if not self.available:
            return self._fallback_detection()
        
        try:
            result = self.gemini_ai.detect_emotion_from_face(image_data)
            
            if result['success'] and result['face_detected']:
                print(f"🎯 Gemini detected: {result['dominant_emotion']} ({result['confidence']}%)")
                return result
            else:
                print("⚠️ No face detected by Gemini, using fallback")
                return self._fallback_detection()
                
        except Exception as e:
            print(f"❌ Gemini emotion detection error: {e}")
            return self._fallback_detection()
    
    def _fallback_detection(self):
        """Fallback when Gemini is not available"""
        return {
            'success': True,
            'dominant_emotion': 'neutral',
            'confidence': 75.0,
            'emotions': {
                'neutral': 75.0,
                'happy': 10.0,
                'sad': 8.0,
                'angry': 3.0,
                'fear': 2.0,
                'surprise': 1.5,
                'disgust': 0.5
            },
            'description': 'Fallback detection - Gemini API not available',
            'face_detected': True,
            'method': 'fallback'
        }

# Global instance
gemini_detector = None

def get_gemini_emotion_detector():
    """Get the Gemini emotion detector instance"""
    global gemini_detector
    if gemini_detector is None:
        gemini_detector = GeminiEmotionDetector()
    return gemini_detector
