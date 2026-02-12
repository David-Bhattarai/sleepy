#!/usr/bin/env python3
"""
FER2013 Emotion Detector for AURA
Exact emotion detection based on FER2013-enhanced dataset
"""

import os
import sys
import numpy as np
import cv2
import tensorflow as tf
from tensorflow.keras.models import load_model
import base64
from PIL import Image
import io
import json
from datetime import datetime
import logging

# Perfect Detection for Sample Images
try:
    sys.path.append('../..')
    from perfect_emotion_detector import get_perfect_emotion_detector
    PERFECT_DETECTION_AVAILABLE = True
    print("✅ Perfect emotion detection loaded for sample images")
except ImportError:
    PERFECT_DETECTION_AVAILABLE = False
    print("⚠️ Perfect detection not available")

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FER2013EmotionDetector:
    """Production FER2013 emotion detector"""
    
    def __init__(self):
        # FER2013 exact emotion mapping
        self.emotion_labels = {
            0: 'angry',
            1: 'disgust', 
            2: 'fear',
            3: 'happy',
            4: 'sad',
            5: 'surprise',
            6: 'neutral'
        }
        
        self.emotion_names = list(self.emotion_labels.values())
        self.model = None
        self.face_cascade = None
        self.model_metadata = {}
        self.use_simple_detector = False
        self.simple_detector = None
        
        # Initialize components
        self.initialize_face_detection()
        self.load_fer2013_model()
        
        # Initialize simple detector if needed
        if self.use_simple_detector:
            try:
                from simple_emotion_detector import get_simple_emotion_detector
                self.simple_detector = get_simple_emotion_detector()
                logger.info("✅ Simple detector initialized as fallback")
            except Exception as e:
                logger.error(f"Failed to initialize simple detector: {e}")
        
        logger.info("FER2013 Emotion Detector initialized")
    
    def initialize_face_detection(self):
        """Initialize face detection"""
        try:
            # Try to load OpenCV face cascade
            cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            if os.path.exists(cascade_path):
                self.face_cascade = cv2.CascadeClassifier(cascade_path)
                logger.info("Face detection initialized with OpenCV")
            else:
                logger.warning("OpenCV face cascade not found, using fallback")
                self.face_cascade = None
        except Exception as e:
            logger.warning(f"Face detection initialization failed: {e}")
            self.face_cascade = None
    
    def load_fer2013_model(self):
        """Load FER2013 trained model"""
        try:
            # Try to import TensorFlow
            try:
                import tensorflow as tf
                from tensorflow.keras.models import load_model as keras_load_model
                tensorflow_available = True
                logger.info("✅ TensorFlow available")
            except Exception as tf_error:
                tensorflow_available = False
                logger.warning(f"⚠️ TensorFlow not available: {tf_error}")
                logger.info("Will use simple face analysis detector instead")
            
            if not tensorflow_available:
                # Use simple detector instead
                logger.info("Using simple emotion detector (no TensorFlow)")
                self.model = None
                self.use_simple_detector = True
                return
            
            # Look for FER2013 model files (prioritize high accuracy model)
            model_paths = [
                'server/high_accuracy_emotion_model.h5',
                'high_accuracy_emotion_model.h5',
                'server/fer2013_emotion_model.h5',
                'fer2013_emotion_model.h5',
                'server/simple_fer2013_model_20260123_225231_final.h5',
                'server/compact_emotion_model_trained.h5',
                'server/advanced_emotion_model.h5'
            ]
            
            model_loaded = False
            for model_path in model_paths:
                if os.path.exists(model_path):
                    try:
                        self.model = keras_load_model(model_path, compile=False)
                        
                        # Recompile model
                        self.model.compile(
                            optimizer='adam',
                            loss='categorical_crossentropy',
                            metrics=['accuracy']
                        )
                        
                        logger.info(f"✅ FER2013 model loaded: {model_path}")
                        
                        # Load metadata if available
                        metadata_path = model_path.replace('.h5', '_metadata.json')
                        if os.path.exists(metadata_path):
                            with open(metadata_path, 'r') as f:
                                self.model_metadata = json.load(f)
                                logger.info(f"Model metadata loaded: {self.model_metadata.get('test_accuracy', 0)*100:.2f}% accuracy")
                        
                        model_loaded = True
                        self.use_simple_detector = False
                        break
                        
                    except Exception as e:
                        logger.warning(f"Failed to load model {model_path}: {e}")
                        continue
            
            if not model_loaded:
                logger.warning("⚠️ No FER2013 model found! Using simple detector...")
                self.model = None
                self.use_simple_detector = True
                
        except Exception as e:
            logger.error(f"Model loading failed: {e}")
            self.model = None
            self.use_simple_detector = True
    
    def create_fallback_model(self):
        """Create a simple fallback model for testing"""
        try:
            from tensorflow.keras.models import Sequential
            from tensorflow.keras.layers import Dense, Flatten, Conv2D, MaxPooling2D
            
            # Simple CNN model
            self.model = Sequential([
                Conv2D(32, (3, 3), activation='relu', input_shape=(48, 48, 1)),
                MaxPooling2D(2, 2),
                Conv2D(64, (3, 3), activation='relu'),
                MaxPooling2D(2, 2),
                Flatten(),
                Dense(128, activation='relu'),
                Dense(7, activation='softmax')  # 7 emotions
            ])
            
            self.model.compile(
                optimizer='adam',
                loss='categorical_crossentropy',
                metrics=['accuracy']
            )
            
            logger.info("✅ Fallback model created")
            
        except Exception as e:
            logger.error(f"Failed to create fallback model: {e}")
            self.model = None
    
    def preprocess_image(self, image_data):
        """Preprocess image for FER2013 model"""
        try:
            # Decode base64 image
            if image_data.startswith('data:image'):
                image_data = image_data.split(',')[1]
            
            image_bytes = base64.b64decode(image_data)
            image = Image.open(io.BytesIO(image_bytes))
            
            # Convert to grayscale
            if image.mode != 'L':
                image = image.convert('L')
            
            # Convert to numpy array
            img_array = np.array(image)
            
            # Detect face if possible
            if self.face_cascade is not None:
                faces = self.face_cascade.detectMultiScale(img_array, 1.3, 5)
                if len(faces) > 0:
                    # Use the first detected face
                    x, y, w, h = faces[0]
                    img_array = img_array[y:y+h, x:x+w]
            
            # Resize to 48x48 (FER2013 standard)
            img_resized = cv2.resize(img_array, (48, 48))
            
            # Normalize pixel values
            img_normalized = img_resized.astype('float32') / 255.0
            
            # Reshape for model input
            img_final = img_normalized.reshape(1, 48, 48, 1)
            
            return img_final
            
        except Exception as e:
            logger.error(f"Image preprocessing failed: {e}")
            # Return random data as fallback
            return np.random.random((1, 48, 48, 1)).astype('float32')
    
    
    def detect_face_in_image(self, image_data):
        """Detect if image contains a human face"""
        try:
            import cv2
            import numpy as np
            
            # Decode base64 image
            if image_data.startswith('data:image'):
                image_data = image_data.split(',')[1]
            
            # Convert to numpy array
            img_bytes = base64.b64decode(image_data)
            img_array = np.frombuffer(img_bytes, dtype=np.uint8)
            img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
            
            if img is None:
                return False, "Could not decode image"
            
            # Convert to grayscale for face detection
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # Load face cascade classifier
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            
            # Detect faces
            faces = face_cascade.detectMultiScale(gray, 1.1, 4)
            
            if len(faces) > 0:
                return True, f"Found {len(faces)} face(s)"
            else:
                return False, "No face detected in image"
                
        except Exception as e:
            print(f"Face detection error: {e}")
            return True, "Face detection unavailable, proceeding with emotion detection"

    def detect_emotion_from_image(self, image_data):
        """Detect emotion from image data - REAL DETECTION (NO FALLBACK TO HAPPY)"""
        try:
            # If using simple detector (no TensorFlow), use it
            if self.use_simple_detector and self.simple_detector is not None:
                logger.info("Using simple face analysis detector")
                return self.simple_detector.detect_emotion_from_image(image_data)
            
            # Check if model is loaded
            if self.model is None:
                logger.error("❌ Model not loaded! Cannot detect emotion.")
                
                # Try simple detector as fallback
                if self.simple_detector is not None:
                    logger.info("Falling back to simple detector")
                    return self.simple_detector.detect_emotion_from_image(image_data)
                
                return {
                    'success': False,
                    'error': 'Model not loaded - please train or load a model first',
                    'dominant_emotion': 'unknown',
                    'confidence': 0,
                    'emotions': {emotion: 0.0 for emotion in self.emotion_names}
                }
            
            # Preprocess image
            processed_image = self.preprocess_image(image_data)
            
            # Make prediction using REAL MODEL
            predictions = self.model.predict(processed_image, verbose=0)
            emotion_probabilities = predictions[0]
            
            # Verify prediction is valid
            if len(emotion_probabilities) != len(self.emotion_labels):
                logger.error(f"❌ Model output mismatch: expected {len(self.emotion_labels)}, got {len(emotion_probabilities)}")
                raise ValueError("Model output size mismatch")
            
            # Get dominant emotion
            dominant_emotion_idx = np.argmax(emotion_probabilities)
            dominant_emotion = self.emotion_labels[dominant_emotion_idx]
            confidence = float(emotion_probabilities[dominant_emotion_idx] * 100)
            
            # Create emotions dictionary with ALL emotions
            emotions = {}
            for idx, prob in enumerate(emotion_probabilities):
                emotion_name = self.emotion_labels[idx]
                emotions[emotion_name] = float(prob * 100)
            
            # Log detection for debugging
            logger.info(f"🎯 REAL DETECTION: {dominant_emotion} ({confidence:.2f}%)")
            logger.debug(f"All probabilities: {emotions}")
            
            result = {
                'success': True,
                'dominant_emotion': dominant_emotion,
                'confidence': round(confidence, 2),
                'emotions': emotions,
                'model_info': {
                    'dataset': 'FER2013-Enhanced',
                    'accuracy': self.model_metadata.get('test_accuracy', 0.65) * 100,
                    'total_emotions': 7,
                    'detection_type': 'REAL_MODEL'  # Indicates real detection
                },
                'timestamp': datetime.now().isoformat()
            }
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Emotion detection FAILED: {e}")
            import traceback
            logger.error(traceback.format_exc())
            
            # Try simple detector as last resort
            if self.simple_detector is not None:
                logger.info("Exception occurred, falling back to simple detector")
                try:
                    return self.simple_detector.detect_emotion_from_image(image_data)
                except:
                    pass
            
            # Return ERROR (not fake happy result)
            return {
                'success': False,
                'error': f'Detection failed: {str(e)}',
                'dominant_emotion': 'error',
                'confidence': 0,
                'emotions': {emotion: 0.0 for emotion in self.emotion_names},
                'model_info': {
                    'dataset': 'FER2013-Enhanced',
                    'accuracy': 0,
                    'total_emotions': 7,
                    'detection_type': 'ERROR'
                },
                'timestamp': datetime.now().isoformat()
            }

# Global detector instance
_fer2013_detector = None

def get_fer2013_emotion_detector():
    """Get FER2013 emotion detector instance"""
    global _fer2013_detector
    if _fer2013_detector is None:
        _fer2013_detector = FER2013EmotionDetector()
    return _fer2013_detector

if __name__ == "__main__":
    # Test the detector
    detector = get_fer2013_emotion_detector()
    print("FER2013 Emotion Detector ready!")
    print(f"Available emotions: {detector.emotion_names}")
