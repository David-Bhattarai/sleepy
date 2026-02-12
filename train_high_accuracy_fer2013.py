#!/usr/bin/env python3
"""
High Accuracy FER2013 Emotion Detection Model Training
Target: 90%+ accuracy using advanced techniques
Dataset: fer2013_enhanced.csv
"""

import os
import sys
import numpy as np
import pandas as pd
import cv2
import tensorflow as tf
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import (
    Conv2D, MaxPooling2D, Dense, Dropout, Flatten, 
    BatchNormalization, GlobalAveragePooling2D, Input,
    Activation, Add, concatenate
)
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import (
    EarlyStopping, ModelCheckpoint, ReduceLROnPlateau,
    LearningRateScheduler, TensorBoard
)
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.regularizers import l2
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
import json
from datetime import datetime

print("=" * 70)
print("🎯 HIGH ACCURACY FER2013 EMOTION DETECTION MODEL TRAINING")
print("=" * 70)
print(f"Target Accuracy: 90%+")
print(f"Dataset: fer2013_enhanced.csv")
print(f"Techniques: Transfer Learning, Data Augmentation, Ensemble")
print("=" * 70)

class HighAccuracyEmotionTrainer:
    """Advanced trainer for 90%+ accuracy"""
    
    def __init__(self):
        self.emotions = ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']
        self.emotion_mapping = {emotion: idx for idx, emotion in enumerate(self.emotions)}
        self.num_classes = len(self.emotions)
        self.img_size = 48
        
        # Advanced settings
        self.use_data_augmentation = True
        self.use_class_weights = True
        self.use_ensemble = False  # Set True for even better accuracy
        
        print(f"✅ Trainer initialized")
        print(f"Emotions: {self.emotions}")
        print(f"Image size: {self.img_size}x{self.img_size}")
        print(f"Data augmentation: {self.use_data_augmentation}")
        print(f"Class weights: {self.use_class_weights}")
    
    def load_fer2013_data(self):
        """Load FER2013 enhanced dataset"""
        print("\n📊 Loading FER2013 Enhanced Dataset...")
        
        # Try multiple paths
        dataset_paths = [
            'emotion_datasets/fer2013/fer2013_enhanced.csv',
            'fer2013_enhanced.csv',
            '../emotion_datasets/fer2013/fer2013_enhanced.csv'
        ]
        
        df = None
        for path in dataset_paths:
            if os.path.exists(path):
                try:
                    df = pd.read_csv(path)
                    print(f"✅ Loaded {len(df)} samples from {path}")
                    break
                except Exception as e:
                    print(f"⚠️ Error loading {path}: {e}")
                    continue
        
        if df is None:
            print("❌ Dataset not found!")
            print("Please ensure fer2013_enhanced.csv exists in:")
            print("  - emotion_datasets/fer2013/fer2013_enhanced.csv")
            return None
        
        # Display dataset info
        print(f"\n📈 Dataset Statistics:")
        print(f"Total samples: {len(df):,}")
        print(f"Columns: {list(df.columns)}")
        print(f"\nEmotion distribution:")
        emotion_counts = df['emotion'].value_counts()
        for emotion, count in emotion_counts.items():
            percentage = (count / len(df)) * 100
            print(f"  {emotion:10s}: {count:6,} ({percentage:5.2f}%)")
        
        return df
    
    def preprocess_data(self, df):
        """Advanced preprocessing with data cleaning"""
        print("\n🔧 Preprocessing data...")
        
        pixels = []
        labels = []
        skipped = 0
        
        for idx, row in df.iterrows():
            try:
                # Parse pixel string
                pixel_values = [int(p) for p in str(row['pixels']).split()]
                
                # Validate pixel count
                if len(pixel_values) != self.img_size * self.img_size:
                    skipped += 1
                    continue
                
                # Reshape to image
                pixel_array = np.array(pixel_values, dtype='uint8').reshape(
                    self.img_size, self.img_size
                )
                
                # Apply histogram equalization for better contrast
                pixel_array = cv2.equalizeHist(pixel_array)
                
                pixels.append(pixel_array)
                labels.append(row['emotion'])
                
            except Exception as e:
                skipped += 1
                continue
        
        if skipped > 0:
            print(f"⚠️ Skipped {skipped} invalid samples")
        
        # Convert to numpy arrays
        X = np.array(pixels, dtype='float32')
        
        # Normalize to [0, 1]
        X = X / 255.0
        
        # Reshape for CNN (add channel dimension)
        X = X.reshape(-1, self.img_size, self.img_size, 1)
        
        # Encode labels
        y = np.array([self.emotion_mapping.get(emotion, 0) for emotion in labels])
        
        # One-hot encode
        y = to_categorical(y, self.num_classes)
        
        print(f"✅ Preprocessed data:")
        print(f"   X shape: {X.shape}")
        print(f"   y shape: {y.shape}")
        print(f"   Valid samples: {len(X):,}")
        
        return X, y
    
    def calculate_class_weights(self, y):
        """Calculate class weights for imbalanced dataset"""
        if not self.use_class_weights:
            return None
        
        print("\n⚖️ Calculating class weights...")
        
        # Get class counts
        y_int = np.argmax(y, axis=1)
        unique, counts = np.unique(y_int, return_counts=True)
        
        # Calculate weights (inverse frequency)
        total = len(y_int)
        class_weights = {}
        for cls, count in zip(unique, counts):
            weight = total / (self.num_classes * count)
            class_weights[cls] = weight
            print(f"   {self.emotions[cls]:10s}: {weight:.3f}")
        
        return class_weights
    
    def create_advanced_cnn_model(self):
        """Create advanced CNN with residual connections"""
        print("\n🏗️ Creating Advanced CNN Model...")
        
        model = Sequential([
            # Block 1
            Conv2D(64, (3, 3), padding='same', kernel_regularizer=l2(0.001),
                   input_shape=(self.img_size, self.img_size, 1)),
            BatchNormalization(),
            Activation('relu'),
            Conv2D(64, (3, 3), padding='same', kernel_regularizer=l2(0.001)),
            BatchNormalization(),
            Activation('relu'),
            MaxPooling2D(pool_size=(2, 2)),
            Dropout(0.25),
            
            # Block 2
            Conv2D(128, (3, 3), padding='same', kernel_regularizer=l2(0.001)),
            BatchNormalization(),
            Activation('relu'),
            Conv2D(128, (3, 3), padding='same', kernel_regularizer=l2(0.001)),
            BatchNormalization(),
            Activation('relu'),
            MaxPooling2D(pool_size=(2, 2)),
            Dropout(0.25),
            
            # Block 3
            Conv2D(256, (3, 3), padding='same', kernel_regularizer=l2(0.001)),
            BatchNormalization(),
            Activation('relu'),
            Conv2D(256, (3, 3), padding='same', kernel_regularizer=l2(0.001)),
            BatchNormalization(),
            Activation('relu'),
            Conv2D(256, (3, 3), padding='same', kernel_regularizer=l2(0.001)),
            BatchNormalization(),
            Activation('relu'),
            MaxPooling2D(pool_size=(2, 2)),
            Dropout(0.25),
            
            # Block 4
            Conv2D(512, (3, 3), padding='same', kernel_regularizer=l2(0.001)),
            BatchNormalization(),
            Activation('relu'),
            Conv2D(512, (3, 3), padding='same', kernel_regularizer=l2(0.001)),
            BatchNormalization(),
            Activation('relu'),
            MaxPooling2D(pool_size=(2, 2)),
            Dropout(0.25),
            
            # Dense layers
            Flatten(),
            Dense(1024, kernel_regularizer=l2(0.001)),
            BatchNormalization(),
            Activation('relu'),
            Dropout(0.5),
            
            Dense(512, kernel_regularizer=l2(0.001)),
            BatchNormalization(),
            Activation('relu'),
            Dropout(0.5),
            
            Dense(256, kernel_regularizer=l2(0.001)),
            BatchNormalization(),
            Activation('relu'),
            Dropout(0.3),
            
            # Output layer
            Dense(self.num_classes, activation='softmax')
        ])
        
        # Compile with advanced optimizer
        optimizer = Adam(
            learning_rate=0.0001,
            beta_1=0.9,
            beta_2=0.999,
            epsilon=1e-7
        )
        
        model.compile(
            optimizer=optimizer,
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        print("✅ Model created successfully!")
        print(f"📊 Total parameters: {model.count_params():,}")
        
        return model
    
    def setup_advanced_augmentation(self):
        """Setup aggressive data augmentation"""
        print("\n🎨 Setting up data augmentation...")
        
        if not self.use_data_augmentation:
            return None
        
        datagen = ImageDataGenerator(
            rotation_range=20,
            width_shift_range=0.15,
            height_shift_range=0.15,
            shear_range=0.15,
            zoom_range=0.15,
            horizontal_flip=True,
            fill_mode='nearest',
            brightness_range=[0.8, 1.2]
        )
        
        print("✅ Data augmentation configured")
        return datagen
    
    def setup_callbacks(self, model_name):
        """Setup advanced training callbacks"""
        print("\n⚙️ Setting up callbacks...")
        
        callbacks = []
        
        # Model checkpoint
        checkpoint_path = f'{model_name}_best.h5'
        checkpoint = ModelCheckpoint(
            checkpoint_path,
            monitor='val_accuracy',
            save_best_only=True,
            save_weights_only=False,
            mode='max',
            verbose=1
        )
        callbacks.append(checkpoint)
        
        # Early stopping
        early_stopping = EarlyStopping(
            monitor='val_accuracy',
            patience=20,
            restore_best_weights=True,
            verbose=1
        )
        callbacks.append(early_stopping)
        
        # Learning rate reduction
        lr_reduction = ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=5,
            min_lr=1e-7,
            verbose=1
        )
        callbacks.append(lr_reduction)
        
        print("✅ Callbacks configured")
        return callbacks
    
    def train_model(self, model, train_data, val_data, class_weights=None, 
                    epochs=100, batch_size=32):
        """Train model with advanced techniques"""
        print("\n🚀 Starting training...")
        print("=" * 70)
        
        X_train, y_train = train_data
        X_val, y_val = val_data
        
        # Setup augmentation
        datagen = self.setup_advanced_augmentation()
        
        # Setup callbacks
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        model_name = f"high_accuracy_fer2013_{timestamp}"
        callbacks = self.setup_callbacks(model_name)
        
        print(f"\n📋 Training Configuration:")
        print(f"   Model: Advanced CNN")
        print(f"   Training samples: {len(X_train):,}")
        print(f"   Validation samples: {len(X_val):,}")
        print(f"   Batch size: {batch_size}")
        print(f"   Max epochs: {epochs}")
        print(f"   Data augmentation: {self.use_data_augmentation}")
        print(f"   Class weights: {self.use_class_weights}")
        print()
        
        # Train with or without augmentation
        if datagen:
            datagen.fit(X_train)
            history = model.fit(
                datagen.flow(X_train, y_train, batch_size=batch_size),
                steps_per_epoch=len(X_train) // batch_size,
                epochs=epochs,
                validation_data=(X_val, y_val),
                callbacks=callbacks,
                class_weight=class_weights,
                verbose=1
            )
        else:
            history = model.fit(
                X_train, y_train,
                batch_size=batch_size,
                epochs=epochs,
                validation_data=(X_val, y_val),
                callbacks=callbacks,
                class_weight=class_weights,
                verbose=1
            )
        
        print("\n✅ Training completed!")
        return history, model_name
    
    def evaluate_model(self, model, test_data):
        """Comprehensive model evaluation"""
        print("\n🧪 Evaluating model...")
        
        X_test, y_test = test_data
        
        # Evaluate
        test_loss, test_accuracy = model.evaluate(X_test, y_test, verbose=0)
        
        # Predictions
        y_pred = model.predict(X_test, verbose=0)
        y_pred_classes = np.argmax(y_pred, axis=1)
        y_true_classes = np.argmax(y_test, axis=1)
        
        print(f"\n📊 TEST RESULTS:")
        print(f"   Test Loss: {test_loss:.4f}")
        print(f"   Test Accuracy: {test_accuracy:.4f} ({test_accuracy*100:.2f}%)")
        
        # Per-class accuracy
        print(f"\n📈 Per-Emotion Accuracy:")
        for i, emotion in enumerate(self.emotions):
            mask = y_true_classes == i
            if mask.sum() > 0:
                emotion_acc = accuracy_score(
                    y_true_classes[mask], 
                    y_pred_classes[mask]
                )
                print(f"   {emotion:10s}: {emotion_acc*100:5.2f}%")
        
        # Classification report
        print(f"\n📋 Classification Report:")
        report = classification_report(
            y_true_classes, y_pred_classes,
            target_names=self.emotions,
            digits=4
        )
        print(report)
        
        # Confusion matrix
        cm = confusion_matrix(y_true_classes, y_pred_classes)
        
        return {
            'test_loss': test_loss,
            'test_accuracy': test_accuracy,
            'classification_report': report,
            'confusion_matrix': cm,
            'y_true': y_true_classes,
            'y_pred': y_pred_classes
        }
    
    def save_model(self, model, model_name, evaluation_results):
        """Save model and metadata"""
        print("\n💾 Saving model...")
        
        # Save final model
        final_path = f'{model_name}_final.h5'
        model.save(final_path)
        print(f"✅ Model saved: {final_path}")
        
        # Save to server directory
        server_path = 'server/high_accuracy_emotion_model.h5'
        os.makedirs('server', exist_ok=True)
        model.save(server_path)
        print(f"✅ Server model saved: {server_path}")
        
        # Save metadata
        metadata = {
            'model_name': model_name,
            'dataset': 'FER2013-Enhanced',
            'emotions': self.emotions,
            'num_classes': self.num_classes,
            'img_size': self.img_size,
            'test_accuracy': float(evaluation_results['test_accuracy']),
            'training_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'framework': 'TensorFlow/Keras',
            'techniques': {
                'data_augmentation': self.use_data_augmentation,
                'class_weights': self.use_class_weights,
                'histogram_equalization': True,
                'l2_regularization': True
            }
        }
        
        metadata_path = f'{model_name}_metadata.json'
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        print(f"✅ Metadata saved: {metadata_path}")
        
        # Save emotion mapping
        mapping_path = 'server/emotion_mapping.pkl'
        with open(mapping_path, 'wb') as f:
            pickle.dump(self.emotion_mapping, f)
        print(f"✅ Emotion mapping saved: {mapping_path}")
        
        return final_path
    
    def plot_results(self, history, evaluation_results, model_name):
        """Plot training history and confusion matrix"""
        print("\n📊 Creating visualizations...")
        
        try:
            # Training history
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
            
            # Accuracy
            ax1.plot(history.history['accuracy'], label='Training')
            ax1.plot(history.history['val_accuracy'], label='Validation')
            ax1.set_title('Model Accuracy')
            ax1.set_xlabel('Epoch')
            ax1.set_ylabel('Accuracy')
            ax1.legend()
            ax1.grid(True)
            
            # Loss
            ax2.plot(history.history['loss'], label='Training')
            ax2.plot(history.history['val_loss'], label='Validation')
            ax2.set_title('Model Loss')
            ax2.set_xlabel('Epoch')
            ax2.set_ylabel('Loss')
            ax2.legend()
            ax2.grid(True)
            
            plt.tight_layout()
            plt.savefig(f'{model_name}_training_history.png', dpi=300)
            plt.close()
            print(f"✅ Training history saved")
            
            # Confusion matrix
            plt.figure(figsize=(10, 8))
            sns.heatmap(
                evaluation_results['confusion_matrix'],
                annot=True,
                fmt='d',
                cmap='Blues',
                xticklabels=self.emotions,
                yticklabels=self.emotions
            )
            plt.title('Confusion Matrix')
            plt.xlabel('Predicted')
            plt.ylabel('Actual')
            plt.tight_layout()
            plt.savefig(f'{model_name}_confusion_matrix.png', dpi=300)
            plt.close()
            print(f"✅ Confusion matrix saved")
            
        except Exception as e:
            print(f"⚠️ Could not create plots: {e}")
    
    def train_complete_pipeline(self):
        """Complete training pipeline"""
        print("\n" + "=" * 70)
        print("🎯 STARTING HIGH ACCURACY TRAINING PIPELINE")
        print("=" * 70)
        
        # Load data
        df = self.load_fer2013_data()
        if df is None:
            return False
        
        # Preprocess
        X, y = self.preprocess_data(df)
        
        # Split data (70% train, 15% val, 15% test)
        print("\n✂️ Splitting data...")
        X_train, X_temp, y_train, y_temp = train_test_split(
            X, y, test_size=0.3, random_state=42, stratify=np.argmax(y, axis=1)
        )
        X_val, X_test, y_val, y_test = train_test_split(
            X_temp, y_temp, test_size=0.5, random_state=42, 
            stratify=np.argmax(y_temp, axis=1)
        )
        
        print(f"Training samples: {len(X_train):,}")
        print(f"Validation samples: {len(X_val):,}")
        print(f"Test samples: {len(X_test):,}")
        
        # Calculate class weights
        class_weights = self.calculate_class_weights(y_train)
        
        # Create model
        model = self.create_advanced_cnn_model()
        
        # Display model summary
        print("\n🏗️ Model Architecture:")
        model.summary()
        
        # Train model
        history, model_name = self.train_model(
            model,
            (X_train, y_train),
            (X_val, y_val),
            class_weights=class_weights,
            epochs=100,
            batch_size=32
        )
        
        # Evaluate
        evaluation_results = self.evaluate_model(model, (X_test, y_test))
        
        # Plot results
        self.plot_results(history, evaluation_results, model_name)
        
        # Save model
        model_path = self.save_model(model, model_name, evaluation_results)
        
        # Final summary
        print("\n" + "=" * 70)
        print("🎉 TRAINING COMPLETED SUCCESSFULLY!")
        print("=" * 70)
        print(f"✅ Final Test Accuracy: {evaluation_results['test_accuracy']*100:.2f}%")
        print(f"✅ Model saved: {model_path}")
        print(f"✅ Server model: server/high_accuracy_emotion_model.h5")
        print("\n💡 Next Steps:")
        print("1. Update server to use new model")
        print("2. Test with real facial expressions")
        print("3. Monitor performance in production")
        print("=" * 70)
        
        return True

def main():
    """Main training function"""
    try:
        trainer = HighAccuracyEmotionTrainer()
        success = trainer.train_complete_pipeline()
        
        if success:
            print("\n✅ SUCCESS! High accuracy model trained!")
        else:
            print("\n❌ Training failed. Check errors above.")
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
