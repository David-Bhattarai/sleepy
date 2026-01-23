#!/usr/bin/env python3
"""
Real Emotion Model Training Script
Trains the emotion detection model on genuine FER-2013 dataset
"""

import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Dense, Dropout, Flatten, BatchNormalization
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau, ModelCheckpoint
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.utils import to_categorical
import matplotlib.pyplot as plt
import pickle
from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns
from datetime import datetime

class RealEmotionModelTrainer:
    """Train emotion detection model on real datasets"""
    
    def __init__(self):
        self.processed_dir = "emotion_datasets/processed"
        self.models_dir = "trained_models"
        self.img_size = 48
        
        # Create models directory
        os.makedirs(self.models_dir, exist_ok=True)
        
        # Load emotion mapping
        mapping_path = os.path.join(self.processed_dir, "emotion_mapping.pkl")
        if os.path.exists(mapping_path):
            with open(mapping_path, 'rb') as f:
                self.emotion_mapping = pickle.load(f)
        else:
            # Default mapping
            self.emotion_mapping = {
                0: 'angry', 1: 'disgust', 2: 'fear', 3: 'happy',
                4: 'sad', 5: 'surprise', 6: 'neutral'
            }
        
        self.emotions = list(self.emotion_mapping.values())
        self.num_classes = len(self.emotions)
        
        print("🔄 Real Emotion Model Trainer initialized")
        print(f"📁 Models directory: {self.models_dir}")
        print(f"🎭 Emotions: {self.emotions}")
    
    def load_processed_data(self):
        """Load processed training data"""
        print("🔄 Loading processed training data...")
        
        train_path = os.path.join(self.processed_dir, "fer2013_train.npz")
        val_path = os.path.join(self.processed_dir, "fer2013_val.npz")
        test_path = os.path.join(self.processed_dir, "fer2013_test.npz")
        
        if not all(os.path.exists(p) for p in [train_path, val_path, test_path]):
            print("❌ Processed data not found. Please run download_real_dataset.py first")
            return None
        
        # Load data
        train_data = np.load(train_path)
        val_data = np.load(val_path)
        test_data = np.load(test_path)
        
        X_train, y_train = train_data['X'], train_data['y']
        X_val, y_val = val_data['X'], val_data['y']
        X_test, y_test = test_data['X'], test_data['y']
        
        print(f"Data loaded:")
        print(f"   Training: {X_train.shape}")
        print(f"   Validation: {X_val.shape}")
        print(f"   Test: {X_test.shape}")
        
        return (X_train, y_train), (X_val, y_val), (X_test, y_test)
    
    def preprocess_data(self, train_data, val_data, test_data):
        """Preprocess data for training"""
        print(" Preprocessing data...")
        
        X_train, y_train = train_data
        X_val, y_val = val_data
        X_test, y_test = test_data
        
        # Reshape images for CNN (add channel dimension)
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
        
        print(f" Data preprocessed:")
        print(f"   Image shape: {X_train.shape[1:]}")
        print(f"   Number of classes: {self.num_classes}")
        
        return (X_train, y_train), (X_val, y_val), (X_test, y_test)
    
    def create_advanced_model(self):
        """Create advanced CNN model for emotion recognition"""
        print(" Creating advanced CNN model...")
        
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
        
        print(" Advanced CNN model created")
        print(f"📊Total parameters: {model.count_params():,}")
        
        return model
    
    def setup_data_augmentation(self):
        """Setup data augmentation for better training"""
        print(" Setting up data augmentation...")
        
        datagen = ImageDataGenerator(
            rotation_range=10,
            width_shift_range=0.1,
            height_shift_range=0.1,
            shear_range=0.1,
            zoom_range=0.1,
            horizontal_flip=True,
            fill_mode='nearest'
        )
        
        print(" Data augmentation configured")
        return datagen
    
    def setup_callbacks(self, model_name):
        """Setup training callbacks"""
        print(" Setting up training callbacks...")
        
        # Model checkpoint
        checkpoint_path = os.path.join(self.models_dir, f"{model_name}_best.h5")
        checkpoint = ModelCheckpoint(
            checkpoint_path,
            monitor='val_accuracy',
            save_best_only=True,
            save_weights_only=False,
            mode='max',
            verbose=1
        )
        
        # Early stopping
        early_stopping = EarlyStopping(
            monitor='val_accuracy',
            patience=10,
            restore_best_weights=True,
            verbose=1
        )
        
        # Learning rate reduction
        lr_reduction = ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=5,
            min_lr=1e-7,
            verbose=1
        )
        
        callbacks = [checkpoint, early_stopping, lr_reduction]
        
        print(" Callbacks configured")
        return callbacks
    
    def train_model(self, model, train_data, val_data, epochs=50, batch_size=32):
        """Train the emotion recognition model"""
        print(" Starting model training...")
        print("=" * 60)
        
        X_train, y_train = train_data
        X_val, y_val = val_data
        
        # Setup data augmentation
        datagen = self.setup_data_augmentation()
        datagen.fit(X_train)
        
        # Setup callbacks
        model_name = f"real_emotion_model_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        callbacks = self.setup_callbacks(model_name)
        
        print(f" Training Configuration:")
        print(f"   Model: Advanced CNN")
        print(f"   Training samples: {len(X_train):,}")
        print(f"   Validation samples: {len(X_val):,}")
        print(f"   Batch size: {batch_size}")
        print(f"   Max epochs: {epochs}")
        print(f"   Data augmentation: Enabled")
        print()
        
        # Train model
        history = model.fit(
            datagen.flow(X_train, y_train, batch_size=batch_size),
            steps_per_epoch=len(X_train) // batch_size,
            epochs=epochs,
            validation_data=(X_val, y_val),
            callbacks=callbacks,
            verbose=1
        )
        
        print(" Training completed!")
        return history, model_name
    
    def evaluate_model(self, model, test_data):
        """Evaluate model performance"""
        print(" Evaluating model performance...")
        
        X_test, y_test = test_data
        
        # Evaluate on test set
        test_loss, test_accuracy = model.evaluate(X_test, y_test, verbose=0)
        
        # Get predictions
        y_pred = model.predict(X_test, verbose=0)
        y_pred_classes = np.argmax(y_pred, axis=1)
        y_true_classes = np.argmax(y_test, axis=1)
        
        print(f" Test Results:")
        print(f"   Test Loss: {test_loss:.4f}")
        print(f"   Test Accuracy: {test_accuracy:.4f} ({test_accuracy*100:.2f}%)")
        
        # Classification report
        print(f"\n Classification Report:")
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
    
    def plot_training_history(self, history, model_name):
        """Plot training history"""
        print("🔄 Creating training plots...")
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
        
        # Plot accuracy
        ax1.plot(history.history['accuracy'], label='Training Accuracy')
        ax1.plot(history.history['val_accuracy'], label='Validation Accuracy')
        ax1.set_title('Model Accuracy')
        ax1.set_xlabel('Epoch')
        ax1.set_ylabel('Accuracy')
        ax1.legend()
        ax1.grid(True)
        
        # Plot loss
        ax2.plot(history.history['loss'], label='Training Loss')
        ax2.plot(history.history['val_loss'], label='Validation Loss')
        ax2.set_title('Model Loss')
        ax2.set_xlabel('Epoch')
        ax2.set_ylabel('Loss')
        ax2.legend()
        ax2.grid(True)
        
        plt.tight_layout()
        
        # Save plot
        plot_path = os.path.join(self.models_dir, f"{model_name}_training_history.png")
        plt.savefig(plot_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f" Training plots saved: {plot_path}")
    
    def plot_confusion_matrix(self, cm, model_name):
        """Plot confusion matrix"""
        print(" Creating confusion matrix plot...")
        
        plt.figure(figsize=(10, 8))
        sns.heatmap(
            cm, 
            annot=True, 
            fmt='d', 
            cmap='Blues',
            xticklabels=self.emotions,
            yticklabels=self.emotions
        )
        plt.title('Confusion Matrix')
        plt.xlabel('Predicted')
        plt.ylabel('Actual')
        
        # Save plot
        plot_path = os.path.join(self.models_dir, f"{model_name}_confusion_matrix.png")
        plt.savefig(plot_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f" Confusion matrix saved: {plot_path}")
    
    def save_final_model(self, model, model_name, evaluation_results):
        """Save the final trained model"""
        print(" Saving final model...")
        
        # Save model
        model_path = os.path.join(self.models_dir, f"{model_name}_final.h5")
        model.save(model_path)
        
        # Save to server directory for immediate use
        server_model_path = "server/genuine_emotion_model_real.h5"
        model.save(server_model_path)
        
        # Save evaluation results
        results_path = os.path.join(self.models_dir, f"{model_name}_results.pkl")
        with open(results_path, 'wb') as f:
            pickle.dump(evaluation_results, f)
        
        # Save emotion mapping for server
        mapping_path = "server/emotion_mapping_real.pkl"
        with open(mapping_path, 'wb') as f:
            pickle.dump(self.emotion_mapping, f)
        
        print(f" Model saved:")
        print(f"   Full model: {model_path}")
        print(f"   Server model: {server_model_path}")
        print(f"   Results: {results_path}")
        print(f"   Emotion mapping: {mapping_path}")
        
        return model_path
    
    def train_complete_pipeline(self):
        """Complete training pipeline"""
        print(" Starting Complete Real Emotion Model Training")
        print("=" * 70)
        
        # Load data
        data = self.load_processed_data()
        if data is None:
            return False
        
        train_data, val_data, test_data = data
        
        # Preprocess data
        train_data, val_data, test_data = self.preprocess_data(train_data, val_data, test_data)
        
        # Create model
        model = self.create_advanced_model()
        
        # Train model
        history, model_name = self.train_model(model, train_data, val_data, epochs=30)
        
        # Evaluate model
        evaluation_results = self.evaluate_model(model, test_data)
        
        # Create plots
        self.plot_training_history(history, model_name)
        self.plot_confusion_matrix(evaluation_results['confusion_matrix'], model_name)
        
        # Save final model
        model_path = self.save_final_model(model, model_name, evaluation_results)
        
        print("=" * 70)
        print(" TRAINING COMPLETED SUCCESSFULLY!")
        print("=" * 70)
        print(f" Final Results:")
        print(f"   Test Accuracy: {evaluation_results['test_accuracy']*100:.2f}%")
        print(f"   Model saved: {model_path}")
        print(f"   Ready for deployment!")
        print()
        print(" Next Steps:")
        print("1. The new model is automatically saved to server/")
        print("2. Restart the server to use the new trained model")
        print("3. Test emotion detection with real facial expressions")
        
        return True

def main():
    """Main training function"""
    trainer = RealEmotionModelTrainer()
    
    print(" Real Emotion Model Training")
    print("=" * 70)
    print("This will train a new emotion detection model on real FER-2013 data.")
    print("Make sure you have run download_real_dataset.py first.")
    print()
    
    # Check if processed data exists
    if not os.path.exists("emotion_datasets/processed"):
        print(" Processed data not found!")
        print("Please run: python download_real_dataset.py")
        return
    
    success = trainer.train_complete_pipeline()
    
    if success:
        print("\n SUCCESS! Your emotion detection model is now trained on real data!")
        print("The model will now recognize genuine facial expressions much better.")
    else:
        print("\n Training failed. Please check the error messages above.")

if __name__ == "__main__":
    main()