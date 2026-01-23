#!/usr/bin/env python3
"""
Retrain AURA Emotion Detection Model with Real FER-2013 Dataset
High accuracy training with real emotion data
"""

import os
import sys
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Dense, Dropout, Flatten, BatchNormalization
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau, ModelCheckpoint
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import json
from datetime import datetime

class FER2013ModelTrainer:
    """Advanced model trainer for FER-2013 dataset"""
    
    def __init__(self):
        self.emotions = ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']
        self.model = None
        self.history = None
        
    def load_fer2013_data(self):
        """Load processed FER-2013 dataset"""
        print(" Loading FER-2013 dataset...")
        
        # Load training data
        train_path = "emotion_datasets/fer2013_real/fer2013_train.npz"
        test_path = "emotion_datasets/fer2013_real/fer2013_test.npz"
        
        if not os.path.exists(train_path) or not os.path.exists(test_path):
            print(" Processed FER-2013 dataset not found!")
            print("Please run: python process_fer2013_dataset.py")
            return None, None, None, None
        
        # Load data
        train_data = np.load(train_path)
        test_data = np.load(test_path)
        
        X_train = train_data['X']
        y_train = train_data['y']
        X_test = test_data['X']
        y_test = test_data['y']
        
        print(f" Dataset loaded successfully!")
        print(f"   Training images: {X_train.shape[0]}")
        print(f"   Test images: {X_test.shape[0]}")
        print(f"   Image shape: {X_train.shape[1:]}")
        
        # Reshape for CNN (add channel dimension)
        X_train = X_train.reshape(-1, 48, 48, 1)
        X_test = X_test.reshape(-1, 48, 48, 1)
        
        # Convert labels to categorical
        y_train_cat = to_categorical(y_train, len(self.emotions))
        y_test_cat = to_categorical(y_test, len(self.emotions))
        
        # Create validation split from training data
        X_train, X_val, y_train_cat, y_val_cat = train_test_split(
            X_train, y_train_cat, test_size=0.2, random_state=42, stratify=y_train
        )
        
        print(f" Data splits:")
        print(f"   Training: {X_train.shape[0]} images")
        print(f"   Validation: {X_val.shape[0]} images")
        print(f"   Test: {X_test.shape[0]} images")
        
        return X_train, X_val, X_test, y_train_cat, y_val_cat, y_test_cat
    
    def create_advanced_model(self):
        """Create advanced CNN model for emotion detection"""
        print(" Creating advanced CNN model...")
        
        model = Sequential([
            # First convolutional block
            Conv2D(64, (3, 3), activation='relu', input_shape=(48, 48, 1), padding='same'),
            BatchNormalization(),
            Conv2D(64, (3, 3), activation='relu', padding='same'),
            MaxPooling2D(pool_size=(2, 2)),
            Dropout(0.25),
            
            # Second convolutional block
            Conv2D(128, (3, 3), activation='relu', padding='same'),
            BatchNormalization(),
            Conv2D(128, (3, 3), activation='relu', padding='same'),
            MaxPooling2D(pool_size=(2, 2)),
            Dropout(0.25),
            
            # Third convolutional block
            Conv2D(256, (3, 3), activation='relu', padding='same'),
            BatchNormalization(),
            Conv2D(256, (3, 3), activation='relu', padding='same'),
            MaxPooling2D(pool_size=(2, 2)),
            Dropout(0.25),
            
            # Fourth convolutional block
            Conv2D(512, (3, 3), activation='relu', padding='same'),
            BatchNormalization(),
            Dropout(0.25),
            
            # Dense layers
            Flatten(),
            Dense(512, activation='relu'),
            BatchNormalization(),
            Dropout(0.5),
            Dense(256, activation='relu'),
            BatchNormalization(),
            Dropout(0.5),
            Dense(len(self.emotions), activation='softmax')
        ])
        
        # Compile with advanced optimizer
        model.compile(
            optimizer=Adam(learning_rate=0.0001, beta_1=0.9, beta_2=0.999),
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        print(" Model created successfully!")
        print(f"   Total parameters: {model.count_params():,}")
        
        return model
    
    def train_model(self, X_train, X_val, X_test, y_train, y_val, y_test):
        """Train the model with advanced techniques"""
        print(" Starting model training...")
        
        # Create model
        self.model = self.create_advanced_model()
        
        # Setup callbacks
        callbacks = [
            EarlyStopping(
                monitor='val_accuracy',
                patience=10,
                restore_best_weights=True,
                verbose=1
            ),
            ReduceLROnPlateau(
                monitor='val_loss',
                factor=0.5,
                patience=5,
                min_lr=1e-7,
                verbose=1
            ),
            ModelCheckpoint(
                'server/advanced_emotion_model_fer2013.h5',
                monitor='val_accuracy',
                save_best_only=True,
                verbose=1
            )
        ]
        
        # Train the model
        print("📚 Training in progress...")
        self.history = self.model.fit(
            X_train, y_train,
            validation_data=(X_val, y_val),
            epochs=50,
            batch_size=32,
            callbacks=callbacks,
            verbose=1
        )
        
        # Evaluate on test set
        print(" Evaluating on test set...")
        test_loss, test_accuracy = self.model.evaluate(X_test, y_test, verbose=0)
        
        print(f"\n Training Results:")
        print(f"   Test Accuracy: {test_accuracy:.4f} ({test_accuracy*100:.2f}%)")
        print(f"   Test Loss: {test_loss:.4f}")
        
        # Save final model
        self.model.save('server/advanced_emotion_model.h5')
        print(" Model saved successfully!")
        
        return test_accuracy, test_loss
    
    def plot_training_history(self):
        """Plot training history"""
        if self.history is None:
            return
        
        print(" Creating training plots...")
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
        
        # Plot accuracy
        ax1.plot(self.history.history['accuracy'], label='Training Accuracy')
        ax1.plot(self.history.history['val_accuracy'], label='Validation Accuracy')
        ax1.set_title('Model Accuracy')
        ax1.set_xlabel('Epoch')
        ax1.set_ylabel('Accuracy')
        ax1.legend()
        ax1.grid(True)
        
        # Plot loss
        ax2.plot(self.history.history['loss'], label='Training Loss')
        ax2.plot(self.history.history['val_loss'], label='Validation Loss')
        ax2.set_title('Model Loss')
        ax2.set_xlabel('Epoch')
        ax2.set_ylabel('Loss')
        ax2.legend()
        ax2.grid(True)
        
        plt.tight_layout()
        plt.savefig('training_history_fer2013.png', dpi=300, bbox_inches='tight')
        print(" Training plots saved as 'training_history_fer2013.png'")
    
    def save_training_report(self, test_accuracy, test_loss):
        """Save detailed training report"""
        report = {
            'model_name': 'Advanced Emotion Detection - FER-2013',
            'dataset': 'FER-2013 Real Dataset',
            'training_date': datetime.now().isoformat(),
            'emotions': self.emotions,
            'test_accuracy': float(test_accuracy),
            'test_loss': float(test_loss),
            'model_architecture': 'Advanced CNN with BatchNormalization',
            'total_parameters': int(self.model.count_params()) if self.model else 0,
            'training_epochs': len(self.history.history['accuracy']) if self.history else 0,
            'best_val_accuracy': float(max(self.history.history['val_accuracy'])) if self.history else 0,
            'dataset_info': {
                'total_images': 35887,
                'training_images': 28709,
                'test_images': 7178,
                'image_size': '48x48',
                'format': 'grayscale'
            }
        }
        
        with open('fer2013_training_report.json', 'w') as f:
            json.dump(report, f, indent=2)
        
        print(" Training report saved as 'fer2013_training_report.json'")

def main():
    """Main training function"""
    print("🎭 AURA Emotion Detection - FER-2013 Training")
    print("=" * 60)
    
    try:
        # Initialize trainer
        trainer = FER2013ModelTrainer()
        
        # Load dataset
        data = trainer.load_fer2013_data()
        if data[0] is None:
            return False
        
        X_train, X_val, X_test, y_train, y_val, y_test = data
        
        # Train model
        test_accuracy, test_loss = trainer.train_model(
            X_train, X_val, X_test, y_train, y_val, y_test
        )
        
        # Create plots and reports
        trainer.plot_training_history()
        trainer.save_training_report(test_accuracy, test_loss)
        
        print(f"\n Training completed successfully!")
        print(f" Final Test Accuracy: {test_accuracy*100:.2f}%")
        print(f"\n Next Steps:")
        print(f"1. Test the model: python test_advanced_emotion.py")
        print(f"2. Start the server: python server/app.py")
        print(f"3. Use emotion detection: Navigate to /emotion-detection.html")
        
        return True
        
    except Exception as e:
        print(f" Training failed: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)