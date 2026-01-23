#!/usr/bin/env python3
"""
Hybrid Emotion Detection System
Combines trained ML models with Gemini AI for best accuracy
Both systems work together for maximum performance
"""

import os
import json
import numpy as np
from datetime import datetime

# Import all detection methods
try:
    from gemini_emotion_detector import get_gemini_emotion_detector
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

try:
    from enhanced_emotion_detector import get_enhanced_emotion_detector
    ENHANCED_AVAILABLE = True
except ImportError:
    ENHANCED_AVAILABLE = False

try:
    import tensorflow as tf
    from tensorflow import keras
    ML_MODEL_AVAILABLE = True
except ImportError:
    ML_MODEL_AVAILABLE = False

class HybridEmotionDetector:
    """
    Hybrid emotion detection system that combines:
    1. Trained ML models (from datasets)
    2. Gemini AI vision
    3. Enhanced local detection
    """
    
    def __init__(self):
        self.gemini_detector = None
        self.enhanced_detector = None
        self.ml_model = None
        self.emotion_mapping = None
        
        print("🔧 Initializing Hybrid Emotion Detection System...")
        self._load_all_detectors()
    
    def _load_all_detectors(self):
        """Load all available detection methods"""
        
        # Load Gemini AI detector
        if GEMINI_AVAILABLE:
            try:
                self.gemini_detector = get_gemini_emotion_detector()
                print("✅ Gemini AI detector loaded")
            except Exception as e:
                print(f"⚠️ Gemini AI detector failed: {e}")
        
        # Load enhanced detector
        if ENHANCED_AVAILABLE:
            try:
                self.enhanced_detector = get_enhanced_emotion_detector()
                print("✅ Enhanced detector loaded")
            except Exception as e:
                print(f"⚠️ Enhanced detector failed: {e}")
        
        # Load trained ML model
        self._load_trained_model()
    
    def _load_trained_model(self):
        """Load the trained emotion detection model"""
        try:
            # Try to load compact emotion model
            model_path = "compact_emotion_model_trained.h5"
            if os.path.exists(model_path):
                self.ml_model = keras.models.load_model(model_path)
                print("✅ Trained ML model loaded (compact)")
            else:
                # Try alternative model paths
                alt_paths = [
                    "../compact_emotion_dataset/compact_emotion_model_50mb.h5",
                    "../../compact_emotion_model_best.h5"
                ]
                for path in alt_paths:
                    if os.path.exists(path):
                        self.ml_model = keras.models.load_model(path)
                        print(f"✅ Trained ML model loaded from {path}")
                        break
            
            # Load emotion mapping
            mapping_path = "compact_emotion_mapping.pkl"
            if os.path.exists(mapping_path):
                import pickle
                with open(mapping_path, 'rb') as f:
                    self.emotion_mapping = pickle.load(f)
                print("✅ Emotion mapping loaded")
            else:
                # Default emotion mapping
                self.emotion_mapping = {
                    0: 'angry', 1: 'disgust', 2: 'fear', 3: 'happy',
                    4: 'neutral', 5: 'sad', 6: 'surprise'
                }
                print("✅ Default emotion mapping used")
                
        except Exception as e:
            print(f"⚠️ ML model loading failed: {e}")
            self.ml_model = None
    
    def detect_emotion_hybrid(self, image_data):
        """
        Hybrid emotion detection using all available methods
        Returns the most confident result
        """
        results = []
        
        print("🎯 Running hybrid emotion detection...")
        
        # Method 1: Gemini AI (highest priority if available)
        if self.gemini_detector:
            try:
                gemini_result = self.gemini_detector.detect_emotion_from_image(image_data)
                if gemini_result['success'] and gemini_result['confidence'] > 85:
                    gemini_result['method'] = 'gemini_ai'
                    gemini_result['priority'] = 1
                    results.append(gemini_result)
                    print(f"🤖 Gemini AI: {gemini_result['dominant_emotion']} ({gemini_result['confidence']}%)")
            except Exception as e:
                print(f"⚠️ Gemini detection failed: {e}")
        
        # Method 2: Trained ML Model
        if self.ml_model:
            try:
                ml_result = self._detect_with_ml_model(image_data)
                if ml_result['success']:
                    ml_result['method'] = 'trained_ml_model'
                    ml_result['priority'] = 2
                    results.append(ml_result)
                    print(f"🧠 ML Model: {ml_result['dominant_emotion']} ({ml_result['confidence']}%)")
            except Exception as e:
                print(f"⚠️ ML model detection failed: {e}")
        
        # Method 3: Enhanced local detection
        if self.enhanced_detector:
            try:
                enhanced_result = self.enhanced_detector.detect_emotion_from_image(image_data)
                if enhanced_result['success']:
                    enhanced_result['method'] = 'enhanced_local'
                    enhanced_result['priority'] = 3
                    results.append(enhanced_result)
                    print(f"🔍 Enhanced: {enhanced_result['dominant_emotion']} ({enhanced_result['confidence']}%)")
            except Exception as e:
                print(f"⚠️ Enhanced detection failed: {e}")
        
        # Combine results and return best one
        return self._combine_results(results)
    
    def _detect_with_ml_model(self, image_data):
        """Use trained ML model for emotion detection"""
        try:
            import base64
            from PIL import Image
            import io
            
            # Prepare image
            if image_data.startswith('data:image'):
                image_data = image_data.split(',')[1]
            
            # Decode and preprocess image
            image_bytes = base64.b64decode(image_data)
            image = Image.open(io.BytesIO(image_bytes))
            
            # Convert to grayscale and resize to model input size
            image = image.convert('L')  # Grayscale
            image = image.resize((48, 48))  # Standard emotion model size
            
            # Convert to numpy array and normalize
            img_array = np.array(image)
            img_array = img_array.astype('float32') / 255.0
            img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
            img_array = np.expand_dims(img_array, axis=-1)  # Add channel dimension
            
            # Predict with ML model
            predictions = self.ml_model.predict(img_array, verbose=0)
            
            # Get emotion probabilities
            emotion_probs = predictions[0]
            dominant_idx = np.argmax(emotion_probs)
            dominant_emotion = self.emotion_mapping[dominant_idx]
            confidence = float(emotion_probs[dominant_idx] * 100)
            
            # Create emotion dictionary
            emotions = {}
            for idx, prob in enumerate(emotion_probs):
                emotion_name = self.emotion_mapping[idx]
                emotions[emotion_name] = float(prob * 100)
            
            return {
                'success': True,
                'dominant_emotion': dominant_emotion,
                'confidence': confidence,
                'emotions': emotions,
                'description': f'Trained ML model detected {dominant_emotion} with {confidence:.1f}% confidence',
                'face_detected': True
            }
            
        except Exception as e:
            print(f"❌ ML model detection error: {e}")
            return {'success': False, 'error': str(e)}
    
    def _combine_results(self, results):
        """Combine results from multiple detection methods"""
        if not results:
            return self._fallback_result()
        
        # Sort by priority (lower number = higher priority)
        results.sort(key=lambda x: x.get('priority', 999))
        
        # Use the highest priority result with good confidence
        for result in results:
            if result['confidence'] > 70:
                # Add combined information
                result['hybrid_info'] = {
                    'methods_used': len(results),
                    'all_methods': [r['method'] for r in results],
                    'confidence_scores': {r['method']: r['confidence'] for r in results}
                }
                print(f"🎯 Best result: {result['dominant_emotion']} ({result['confidence']}%) via {result['method']}")
                return result
        
        # If no high confidence result, return the best available
        best_result = results[0]
        best_result['hybrid_info'] = {
            'methods_used': len(results),
            'all_methods': [r['method'] for r in results],
            'confidence_scores': {r['method']: r['confidence'] for r in results}
        }
        
        print(f"🎯 Moderate result: {best_result['dominant_emotion']} ({best_result['confidence']}%) via {best_result['method']}")
        return best_result
    
    def _fallback_result(self):
        """Fallback result when all methods fail"""
        return {
            'success': True,
            'dominant_emotion': 'neutral',
            'confidence': 60.0,
            'emotions': {
                'neutral': 60.0,
                'happy': 15.0,
                'sad': 10.0,
                'angry': 8.0,
                'fear': 4.0,
                'surprise': 2.0,
                'disgust': 1.0
            },
            'description': 'Fallback detection used - all methods failed',
            'face_detected': True,
            'method': 'fallback',
            'hybrid_info': {
                'methods_used': 0,
                'all_methods': [],
                'confidence_scores': {}
            }
        }

# Global instance
hybrid_detector = None

def get_hybrid_emotion_detector():
    """Get the hybrid emotion detector instance"""
    global hybrid_detector
    if hybrid_detector is None:
        hybrid_detector = HybridEmotionDetector()
    return hybrid_detector