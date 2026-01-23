#!/usr/bin/env python3
"""
Train Model with Compact Dataset (34.3 MB)
This will create a better emotion detection model using the compact dataset
"""

import os
import numpy as np
import pickle
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Dense, Dropout, Flatten, BatchNormalization
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

class CompactModelTrainer:
    """Train emotion model with compact dataset"""
    
    def __init__(self):
        self.compact_dir = "compact_emotion_dataset"
        self.processed_dir = os.path.join(self.compact_dir, "processed")
        self.server_dir = "sleepy/server"
        self.img_size = 48
        
        # Load emotion mapping
        mapping_path = os.path.join(self.processed_dir, "emotion_mapping.pkl")
        with open(mapping_path, 'rb') as f:
            self.emotion_mapping = pickle.load(f)
        
        self.emotions = list(self.emotion_mapping.values())
        self.num_classes = len(self.emotions)
        
        print("🔄 Compact Model Trainer initialized")
        print(f"📁 Dataset: {self.compact_dir}")
        print(f"🎭 Emotions: {self.emotions}")
        print(f"📊 Classes: {self.num_classes}")
    
    def load_compact_data(self):
        """Load the compact dataset"""
        print("🔄 Loading compact dataset...")
        
        # Load data files
        train_data = np.load(os.path.join(self.processed_dir, "compact_train.npz"))
        val_data = np.load(os.path.join(self.processed_dir, "compact_val.npz"))
        test_data = np.load(os.path.join(self.processed_dir, "compact_test.npz"))
        
        X_train, y_train = train_data['X'], train_data['y']
        X_val, y_val = val_data['X'], val_data['y']
        X_test, y_test = test_data['X'], test_data['y']
        
        print(f"✅ Data loaded:")
        print(f"   Training: {X_train.shape}")
        print(f"   Validation: {X_val.shape}")
        print(f"   Test: {X_test.shape}")
        
        return (X_train, y_train), (X_val, y_val), (X_test, y_test)
    
    def preprocess_data(self, train_data, val_data, test_data):
        """Preprocess data for training"""
        print("🔄 Preprocessing data...")
        
        X_train, y_train = train_data
        X_val, y_val = val_data
        X_test, y_test = test_data
        
        # Reshape for CNN (add channel dimension)
        X_train = X_train.reshape(-1, self.img_size, self.img_size, 1)
        X_val = X_val.reshape(-1, self.img_size, self.img_size, 1)
        X_test = X_test.reshape(-1, self.img_size, self.img_size, 1)
        
        # Normalize pixel values
        X_train = X_train.astype('float32') / 255.0
        X_val = X_val.astype('float32') / 255.0
        X_test = X_test.astype('float32') / 255.0
        
        # Convert labels to categorical
        y_train = to_categorical(y_train, self.num_classes)
        y_val = to_categorical(y_val, self.num_classes)
        y_test = to_categorical(y_test, self.num_classes)
        
        print(f"✅ Data preprocessed:")
        print(f"   Image shape: {X_train.shape[1:]}")
        print(f"   Label shape: {y_train.shape[1:]}")
        
        return (X_train, y_train), (X_val, y_val), (X_test, y_test)
    
    def create_improved_model(self):
        """Create improved CNN model"""
        print("🔄 Creating improved CNN model...")
        
        model = Sequential([
            # First Convolutional Block
            Conv2D(64, (3, 3), activation='relu', input_shape=(self.img_size, self.img_size, 1)),
            BatchNormalization(),
            Conv2D(64, (3, 3), activation='relu'),
            MaxPooling2D(pool_size=(2, 2)),
            Dropout(0.25),
            
            # Second Convolutional Block
            Conv2D(128, (3, 3), activation='relu'),
            BatchNormalization(),
            Conv2D(128, (3, 3), activation='relu'),
            MaxPooling2D(pool_size=(2, 2)),
            Dropout(0.25),
            
            # Third Convolutional Block
            Conv2D(256, (3, 3), activation='relu'),
            BatchNormalization(),
            Conv2D(256, (3, 3), activation='relu'),
            MaxPooling2D(pool_size=(2, 2)),
            Dropout(0.25),
            
            # Dense Layers
            Flatten(),
            Dense(512, activation='relu'),
            BatchNormalization(),
            Dropout(0.5),
            
            Dense(256, activation='relu'),
            BatchNormalization(),
            Dropout(0.5),
            
            Dense(128, activation='relu'),
            Dropout(0.3),
            
            # Output layer
            Dense(self.num_classes, activation='softmax')
        ])
        
        # Compile model
        model.compile(
            optimizer=Adam(learning_rate=0.0001, beta_1=0.9, beta_2=0.999),
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        print("✅ Improved CNN model created")
        print(f"📊 Total parameters: {model.count_params():,}")
        
        return model
    
    def train_model(self, model, train_data, val_data):
        """Train the model"""
        print("🔄 Training model...")
        
        X_train, y_train = train_data
        X_val, y_val = val_data
        
        # Setup callbacks
        callbacks = [
            EarlyStopping(
                monitor='val_accuracy',
                patience=10,
                restore_best_weights=True,
                verbose=1
            ),
            ModelCheckpoint(
                'compact_emotion_model_best.h5',
                monitor='val_accuracy',
                save_best_only=True,
                save_weights_only=False,
                mode='max',
                verbose=1
            )
        ]
        
        # Train model
        history = model.fit(
            X_train, y_train,
            batch_size=32,
            epochs=50,
            validation_data=(X_val, y_val),
            callbacks=callbacks,
            verbose=1
        )
        
        print("✅ Model training completed")
        return history
    
    def evaluate_model(self, model, test_data):
        """Evaluate model performance"""
        print("🔄 Evaluating model...")
        
        X_test, y_test = test_data
        
        # Evaluate
        test_loss, test_accuracy = model.evaluate(X_test, y_test, verbose=0)
        
        # Predictions
        predictions = model.predict(X_test, verbose=0)
        y_pred = np.argmax(predictions, axis=1)
        y_true = np.argmax(y_test, axis=1)
        
        print(f"✅ Model evaluation:")
        print(f"   Test Accuracy: {test_accuracy*100:.2f}%")
        print(f"   Test Loss: {test_loss:.4f}")
        
        # Classification report
        print("\n📊 Classification Report:")
        print(classification_report(y_true, y_pred, target_names=self.emotions))
        
        return test_accuracy, test_loss, y_true, y_pred
    
    def save_model_for_server(self, model):
        """Save model for server integration"""
        print("🔄 Saving model for server integration...")
        
        # Save to server directory
        server_model_path = os.path.join(self.server_dir, "compact_emotion_model_trained.h5")
        model.save(server_model_path)
        
        # Also save emotion mapping for server
        server_mapping_path = os.path.join(self.server_dir, "compact_emotion_mapping.pkl")
        with open(server_mapping_path, 'wb') as f:
            pickle.dump(self.emotion_mapping, f)
        
        print(f"✅ Model saved for server:")
        print(f"   Model: {server_model_path}")
        print(f"   Mapping: {server_mapping_path}")
        
        return server_model_path
    
    def train_complete_model(self):
        """Complete training pipeline"""
        print("🚀 Starting Complete Model Training")
        print("=" * 60)
        
        # Load data
        train_data, val_data, test_data = self.load_compact_data()
        
        # Preprocess data
        train_data, val_data, test_data = self.preprocess_data(train_data, val_data, test_data)
        
        # Create model
        model = self.create_improved_model()
        
        # Train model
        history = self.train_model(model, train_data, val_data)
        
        # Evaluate model
        accuracy, loss, y_true, y_pred = self.evaluate_model(model, test_data)
        
        # Save for server
        server_model_path = self.save_model_for_server(model)
        
        print("=" * 60)
        print("🎉 MODEL TRAINING COMPLETED!")
        print(f"✅ Final Accuracy: {accuracy*100:.2f}%")
        print(f"✅ Model saved: {server_model_path}")
        print("✅ Ready for server integration!")
        
        return model, accuracy, server_model_path

def main():
    """Main training function"""
    trainer = CompactModelTrainer()
    model, accuracy, model_path = trainer.train_complete_model()
    
    print(f"\n🎯 Next Steps:")
    print(f"1. Model trained with {accuracy*100:.2f}% accuracy")
    print(f"2. Model saved to: {model_path}")
    print(f"3. Restart the server to use the new model")
    print(f"4. The new model should detect emotions much better!")

if __name__ == "__main__":
    main()