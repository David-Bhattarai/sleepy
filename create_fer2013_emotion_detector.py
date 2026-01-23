#!/usr/bin/env python3
"""
FER2013-Enhanced Emotion Detector
Creates exact emotion detection based on FER2013-enhanced dataset
"""

import os
import numpy as np
import pandas as pd
import cv2
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Dense, Dropout, Flatten, BatchNormalization
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split
import pickle
import json
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FER2013EmotionDetector:
    """Exact emotion detector based on FER2013-enhanced dataset"""
    
    def __init__(self):
        # FER2013 emotion mapping (exact from dataset)
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
        
        # Dataset info
        self.dataset_path = 'emotion_datasets/fer2013/fer2013_enhanced.csv'
        self.model_path = 'sleepy/server/fer2013_emotion_model.h5'
        self.metadata_path = 'sleepy/server/fer2013_emotion_metadata.json'
        
        logger.info("FER2013 Emotion Detector initialized")
    
    def load_fer2013_dataset(self):
        """Load and preprocess FER2013-enhanced dataset"""
        try:
            logger.info("Loading FER2013-enhanced dataset...")
            
            if not os.path.exists(self.dataset_path):
                raise FileNotFoundError(f"Dataset not found: {self.dataset_path}")
            
            # Load dataset
            df = pd.read_csv(self.dataset_path)
            logger.info(f"Dataset loaded: {len(df)} samples")
            
            # Extract features and labels
            X = []
            y = []
            
            for idx, row in df.iterrows():
                # Parse pixel data
                pixels = np.array([int(pixel) for pixel in row['pixels'].split()])
                # Reshape to 48x48
                image = pixels.reshape(48, 48)
                X.append(image)
                y.append(row['emotion'])
                
                if idx % 1000 == 0:
                    logger.info(f"Processed {idx} samples...")
            
            X = np.array(X)
            y = np.array(y)
            
            # Normalize pixel values
            X = X.astype('float32') / 255.0
            
            # Reshape for CNN (add channel dimension)
            X = X.reshape(X.shape[0], 48, 48, 1)
            
            # Convert labels to categorical
            y = to_categorical(y, num_classes=7)
            
            logger.info(f"Dataset preprocessed: X shape {X.shape}, y shape {y.shape}")
            
            # Split dataset
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42, stratify=y
            )
            
            logger.info(f"Train: {X_train.shape[0]}, Test: {X_test.shape[0]}")
            
            return X_train, X_test, y_train, y_test
            
        except Exception as e:
            logger.error(f"Error loading dataset: {e}")
            return None, None, None, None
    
    def create_fer2013_model(self):
        """Create CNN model optimized for FER2013 dataset"""
        logger.info("Creating FER2013-optimized CNN model...")
        
        model = Sequential([
            # First Convolutional Block
            Conv2D(32, (3, 3), activation='relu', input_shape=(48, 48, 1)),
            BatchNormalization(),
            Conv2D(32, (3, 3), activation='relu'),
            MaxPooling2D(pool_size=(2, 2)),
            Dropout(0.25),
            
            # Second Convolutional Block
            Conv2D(64, (3, 3), activation='relu'),
            BatchNormalization(),
            Conv2D(64, (3, 3), activation='relu'),
            MaxPooling2D(pool_size=(2, 2)),
            Dropout(0.25),
            
            # Third Convolutional Block
            Conv2D(128, (3, 3), activation='relu'),
            BatchNormalization(),
            Conv2D(128, (3, 3), activation='relu'),
            MaxPooling2D(pool_size=(2, 2)),
            Dropout(0.25),
            
            # Dense Layers
            Flatten(),
            Dense(512, activation='relu'),
            BatchNormalization(),
            Dropout(0.5),
            Dense(256, activation='relu'),
            Dropout(0.5),
            Dense(7, activation='softmax')  # 7 emotions
        ])
        
        # Compile model
        model.compile(
            optimizer=Adam(learning_rate=0.0001),
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        logger.info("Model created successfully")
        logger.info(f"Model parameters: {model.count_params():,}")
        
        return model
    
    def train_fer2013_model(self):
        """Train the FER2013 emotion detection model"""
        logger.info("Starting FER2013 model training...")
        
        # Load dataset
        X_train, X_test, y_train, y_test = self.load_fer2013_dataset()
        
        if X_train is None:
            logger.error("Failed to load dataset")
            return False
        
        # Create model
        self.model = self.create_fer2013_model()
        
        # Training callbacks
        from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau, ModelCheckpoint
        
        callbacks = [
            EarlyStopping(
                monitor='val_accuracy',
                patience=10,
                restore_best_weights=True
            ),
            ReduceLROnPlateau(
                monitor='val_loss',
                factor=0.5,
                patience=5,
                min_lr=0.00001
            ),
            ModelCheckpoint(
                self.model_path,
                monitor='val_accuracy',
                save_best_only=True,
                verbose=1
            )
        ]
        
        # Train model
        logger.info("Training model...")
        history = self.model.fit(
            X_train, y_train,
            batch_size=32,
            epochs=50,
            validation_data=(X_test, y_test),
            callbacks=callbacks,
            verbose=1
        )
        
        # Evaluate model
        test_loss, test_accuracy = self.model.evaluate(X_test, y_test, verbose=0)
        logger.info(f"Test Accuracy: {test_accuracy:.4f}")
        
        # Save metadata
        metadata = {
            'model_type': 'FER2013_CNN',
            'dataset': 'FER2013-enhanced',
            'emotions': self.emotion_names,
            'emotion_mapping': self.emotion_labels,
            'input_shape': [48, 48, 1],
            'num_classes': 7,
            'test_accuracy': float(test_accuracy),
            'test_loss': float(test_loss),
            'training_samples': len(X_train),
            'test_samples': len(X_test),
            'created_date': datetime.now().isoformat(),
            'training_history': {
                'final_accuracy': float(history.history['accuracy'][-1]),
                'final_val_accuracy': float(history.history['val_accuracy'][-1]),
                'epochs_trained': len(history.history['accuracy'])
            }
        }
        
        with open(self.metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        logger.info(f"Model saved: {self.model_path}")
        logger.info(f"Metadata saved: {self.metadata_path}")
        
        return True
    
    def load_trained_model(self):
        """Load the trained FER2013 model"""
        try:
            if os.path.exists(self.model_path):
                logger.info(f"Loading trained model: {self.model_path}")
                self.model = tf.keras.models.load_model(self.model_path)
                logger.info("Model loaded successfully")
                return True
            else:
                logger.warning("No trained model found")
                return False
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            return False
    
    def initialize_face_detection(self):
        """Initialize OpenCV face detection"""
        try:
            cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            self.face_cascade = cv2.CascadeClassifier(cascade_path)
            
            if self.face_cascade.empty():
                logger.warning("Could not load face cascade classifier")
                return False
            else:
                logger.info("Face detection initialized")
                return True
        except Exception as e:
            logger.error(f"Error initializing face detection: {e}")
            return False
    
    def preprocess_face_for_prediction(self, face_image):
        """Preprocess face image for FER2013 model prediction"""
        try:
            # Convert to grayscale if needed
            if len(face_image.shape) == 3:
                gray_face = cv2.cvtColor(face_image, cv2.COLOR_BGR2GRAY)
            else:
                gray_face = face_image
            
            # Resize to 48x48 (FER2013 standard)
            face_resized = cv2.resize(gray_face, (48, 48))
            
            # Normalize pixel values
            face_normalized = face_resized.astype('float32') / 255.0
            
            # Apply histogram equalization for better contrast
            face_equalized = cv2.equalizeHist((face_normalized * 255).astype(np.uint8))
            face_final = face_equalized.astype('float32') / 255.0
            
            # Reshape for model input
            face_array = face_final.reshape(1, 48, 48, 1)
            
            return face_array
            
        except Exception as e:
            logger.error(f"Error preprocessing face: {e}")
            return None
    
    def predict_emotion(self, face_array):
        """Predict emotion using FER2013 model"""
        try:
            if self.model is None:
                raise Exception("Model not loaded")
            
            # Get prediction
            predictions = self.model.predict(face_array, verbose=0)
            emotion_probs = predictions[0]
            
            # Get dominant emotion
            dominant_idx = np.argmax(emotion_probs)
            dominant_emotion = self.emotion_labels[dominant_idx]
            confidence = float(emotion_probs[dominant_idx] * 100)
            
            # Create emotion dictionary
            emotions = {}
            for idx, prob in enumerate(emotion_probs):
                emotion_name = self.emotion_labels[idx]
                emotions[emotion_name] = float(prob * 100)
            
            return {
                'dominant_emotion': dominant_emotion,
                'confidence': confidence,
                'emotions': emotions,
                'model_type': 'FER2013_CNN',
                'dataset': 'FER2013-enhanced'
            }
            
        except Exception as e:
            logger.error(f"Error predicting emotion: {e}")
            return None
    
    def detect_emotion_from_image(self, image_data):
        """Main method to detect emotion from image using FER2013 model"""
        try:
            logger.info("Processing FER2013 emotion detection...")
            
            # Decode base64 image
            import base64
            from PIL import Image
            import io
            
            if ',' in image_data:
                image_data = image_data.split(',')[1]
            
            image_bytes = base64.b64decode(image_data)
            image = Image.open(io.BytesIO(image_bytes))
            
            # Convert to OpenCV format
            opencv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            
            # Detect faces
            if self.face_cascade is None:
                self.initialize_face_detection()
            
            gray = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30)
            )
            
            if len(faces) == 0:
                return {
                    'success': False,
                    'error': 'No face detected',
                    'timestamp': datetime.now().isoformat()
                }
            
            # Use the largest face
            largest_face = max(faces, key=lambda x: x[2] * x[3])
            x, y, w, h = largest_face
            
            # Extract face region
            face_roi = opencv_image[y:y+h, x:x+w]
            
            # Preprocess face
            face_array = self.preprocess_face_for_prediction(face_roi)
            if face_array is None:
                raise Exception("Failed to preprocess face")
            
            # Predict emotion
            prediction = self.predict_emotion(face_array)
            if prediction is None:
                raise Exception("Failed to predict emotion")
            
            # Prepare result
            result = {
                'success': True,
                'face_detected': True,
                'face_count': len(faces),
                'timestamp': datetime.now().isoformat(),
                'model_info': {
                    'model_type': 'FER2013_CNN',
                    'dataset': 'FER2013-enhanced',
                    'emotions_supported': self.emotion_names,
                    'input_size': '48x48'
                }
            }
            result.update(prediction)
            
            logger.info(f"FER2013 Emotion detected: {prediction['dominant_emotion']} ({prediction['confidence']:.1f}%)")
            
            return result
            
        except Exception as e:
            logger.error(f"Error in FER2013 emotion detection: {e}")
            return {
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def get_model_info(self):
        """Get FER2013 model information"""
        try:
            info = {
                'model_type': 'FER2013_CNN',
                'dataset': 'FER2013-enhanced',
                'emotions': self.emotion_names,
                'emotion_mapping': self.emotion_labels,
                'input_shape': '48x48x1',
                'num_classes': 7,
                'model_loaded': self.model is not None,
                'face_detection': self.face_cascade is not None
            }
            
            # Load metadata if available
            if os.path.exists(self.metadata_path):
                with open(self.metadata_path, 'r') as f:
                    metadata = json.load(f)
                info.update(metadata)
            
            return info
            
        except Exception as e:
            return {'error': str(e)}

def main():
    """Main function to train and test FER2013 emotion detector"""
    detector = FER2013EmotionDetector()
    
    print("🧪 FER2013 Emotion Detector Training")
    print("=" * 50)
    
    # Check if model already exists
    if os.path.exists(detector.model_path):
        print("✅ Trained model found, loading...")
        detector.load_trained_model()
    else:
        print("🔄 Training new FER2013 model...")
        success = detector.train_fer2013_model()
        
        if not success:
            print("❌ Training failed")
            return
    
    # Initialize face detection
    detector.initialize_face_detection()
    
    # Get model info
    info = detector.get_model_info()
    print(f"📊 Model Type: {info.get('model_type', 'Unknown')}")
    print(f"📊 Dataset: {info.get('dataset', 'Unknown')}")
    print(f"📊 Emotions: {info.get('emotions', [])}")
    print(f"📊 Test Accuracy: {info.get('test_accuracy', 'Unknown')}")
    
    print("\n✅ FER2013 Emotion Detector Ready!")
    print("🎯 Exact emotion detection based on FER2013-enhanced dataset")
    print("💻 Ready for integration with emotion-detection.html")

if __name__ == "__main__":
    main()