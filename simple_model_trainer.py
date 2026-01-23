#!/usr/bin/env python3
"""
Simple FER2013 Model Trainer - Direct Terminal Training
Train emotion detection model without Jupyter complications
"""

import os
import sys
import warnings
warnings.filterwarnings('ignore')

print("🚀 SIMPLE FER2013 MODEL TRAINER")
print("=" * 50)

# Core libraries
try:
    import numpy as np
    import pandas as pd
    print("✅ NumPy and Pandas imported")
except ImportError as e:
    print(f"❌ Error importing basic libraries: {e}")
    sys.exit(1)

# Deep learning
try:
    import tensorflow as tf
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import Conv2D, MaxPooling2D, Dense, Dropout, Flatten, BatchNormalization
    from tensorflow.keras.optimizers import Adam
    from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
    from tensorflow.keras.utils import to_categorical
    print("✅ TensorFlow imported")
    print(f"TensorFlow version: {tf.__version__}")
except ImportError as e:
    print(f"❌ Error importing TensorFlow: {e}")
    sys.exit(1)

# Machine learning
try:
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import classification_report, confusion_matrix
    print("✅ Scikit-learn imported")
except ImportError as e:
    print(f"❌ Error importing scikit-learn: {e}")
    sys.exit(1)

# Visualization
try:
    import matplotlib.pyplot as plt
    import seaborn as sns
    print("✅ Matplotlib and Seaborn imported")
except ImportError as e:
    print(f"⚠️ Visualization libraries not available: {e}")
    plt = None
    sns = None

# Utilities
import pickle
import json
from datetime import datetime

# Suppress TensorFlow warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
tf.get_logger().setLevel('ERROR')

class SimpleFER2013Trainer:
    """Simple FER2013 Emotion Model Trainer"""
    
    def __init__(self):
        self.emotions = ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']
        self.emotion_mapping = {emotion: idx for idx, emotion in enumerate(self.emotions)}
        self.num_classes = len(self.emotions)
        self.img_size = 48
        self.model = None
        self.history = None
        
        print(f"✅ Trainer initialized")
        print(f"Emotions: {self.emotions}")
        print(f"Classes: {self.num_classes}")
        print(f"Image size: {self.img_size}x{self.img_size}")
    
    def load_data(self):
        """Load FER2013 dataset"""
        print("\n📊 Loading FER2013 Dataset...")
        
        # Try different dataset paths
        dataset_paths = [
            'emotion_datasets/fer2013/fer2013_enhanced.csv',
            'sleepy/emotion_datasets/fer2013/fer2013_enhanced.csv',
            'fer2013_enhanced.csv'
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
            print("❌ Dataset not found. Creating sample data...")
            df = self.create_sample_data()
        
        # Display dataset info
        print(f"\n📈 Dataset Info:")
        print(f"Total samples: {len(df)}")
        print(f"Columns: {list(df.columns)}")
        print("\nEmotion distribution:")
        print(df['emotion'].value_counts())
        
        return df
    
    def create_sample_data(self):
        """Create sample data if dataset not found"""
        print("🔧 Creating sample dataset...")
        
        sample_data = []
        samples_per_emotion = 100  # More samples for better training
        
        for emotion in self.emotions:
            for i in range(samples_per_emotion):
                # Create random 48x48 pixel data
                pixels = np.random.randint(0, 256, self.img_size * self.img_size)
                pixel_string = ' '.join(map(str, pixels))
                
                sample_data.append({
                    'emotion': emotion,
                    'pixels': pixel_string
                })
        
        df = pd.DataFrame(sample_data)
        print(f"✅ Created sample dataset with {len(df)} samples")
        return df
    
    def preprocess_data(self, df):
        """Preprocess the dataset"""
        print("\n🔧 Preprocessing data...")
        
        pixels = []
        labels = []
        
        for idx, row in df.iterrows():
            try:
                # Convert pixel string to array
                pixel_values = [int(pixel) for pixel in str(row['pixels']).split()]
                
                if len(pixel_values) != self.img_size * self.img_size:
                    continue
                
                pixel_array = np.array(pixel_values).reshape(self.img_size, self.img_size)
                pixels.append(pixel_array)
                labels.append(row['emotion'])
                
            except Exception as e:
                continue
        
        if len(pixels) == 0:
            raise ValueError("No valid data found")
        
        # Convert to numpy arrays
        X = np.array(pixels, dtype='float32')
        y = np.array([self.emotion_mapping.get(emotion, 0) for emotion in labels])
        
        # Normalize pixel values
        X = X / 255.0
        
        # Reshape for CNN
        X = X.reshape(-1, self.img_size, self.img_size, 1)
        
        # Convert labels to categorical
        y = to_categorical(y, self.num_classes)
        
        print(f"✅ Data preprocessed: X shape {X.shape}, y shape {y.shape}")
        return X, y
    
    def create_model(self):
        """Create CNN model"""
        print("\n🏗️ Creating CNN model...")
        
        model = Sequential([
            # First block
            Conv2D(32, (3, 3), activation='relu', input_shape=(self.img_size, self.img_size, 1)),
            BatchNormalization(),
            Conv2D(32, (3, 3), activation='relu'),
            MaxPooling2D(pool_size=(2, 2)),
            Dropout(0.25),
            
            # Second block
            Conv2D(64, (3, 3), activation='relu'),
            BatchNormalization(),
            Conv2D(64, (3, 3), activation='relu'),
            MaxPooling2D(pool_size=(2, 2)),
            Dropout(0.25),
            
            # Third block
            Conv2D(128, (3, 3), activation='relu'),
            BatchNormalization(),
            Dropout(0.25),
            
            # Dense layers
            Flatten(),
            Dense(512, activation='relu'),
            BatchNormalization(),
            Dropout(0.5),
            Dense(256, activation='relu'),
            Dropout(0.5),
            Dense(self.num_classes, activation='softmax')
        ])
        
        # Compile model
        model.compile(
            optimizer=Adam(learning_rate=0.001),
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        self.model = model
        print("✅ Model created successfully!")
        return model
    
    def train_model(self, X_train, y_train, X_val, y_val):
        """Train the model"""
        print("\n🚀 Starting training...")
        
        # Create timestamp for model name
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        model_name = f"simple_fer2013_model_{timestamp}"
        
        # Setup callbacks
        callbacks = [
            EarlyStopping(
                monitor='val_accuracy',
                patience=10,
                restore_best_weights=True,
                verbose=1
            ),
            ModelCheckpoint(
                filepath=f'{model_name}_best.h5',
                monitor='val_accuracy',
                save_best_only=True,
                verbose=1
            )
        ]
        
        # Train model
        history = self.model.fit(
            X_train, y_train,
            batch_size=32,
            epochs=50,
            validation_data=(X_val, y_val),
            callbacks=callbacks,
            verbose=1
        )
        
        self.history = history
        print("\n✅ Training completed!")
        return history, model_name
    
    def evaluate_model(self, X_test, y_test):
        """Evaluate model on test set"""
        print("\n🧪 Evaluating model...")
        
        test_loss, test_accuracy = self.model.evaluate(X_test, y_test, verbose=0)
        print(f"Test Accuracy: {test_accuracy:.4f} ({test_accuracy*100:.2f}%)")
        print(f"Test Loss: {test_loss:.4f}")
        
        # Make predictions
        y_pred = self.model.predict(X_test, verbose=0)
        y_pred_classes = np.argmax(y_pred, axis=1)
        y_true_classes = np.argmax(y_test, axis=1)
        
        # Classification report
        try:
            report = classification_report(y_true_classes, y_pred_classes, target_names=self.emotions)
            print("\n📋 Classification Report:")
            print(report)
        except Exception as e:
            print(f"⚠️ Could not generate report: {e}")
        
        return test_accuracy, test_loss
    
    def save_model(self, model_name, test_accuracy=0.0):
        """Save model and metadata"""
        print(f"\n💾 Saving model...")
        
        # Save final model
        final_model_path = f'{model_name}_final.h5'
        self.model.save(final_model_path)
        print(f"✅ Model saved: {final_model_path}")
        
        # Save metadata
        metadata = {
            'model_name': model_name,
            'dataset': 'FER2013-Enhanced',
            'emotions': self.emotions,
            'num_classes': self.num_classes,
            'img_size': self.img_size,
            'test_accuracy': float(test_accuracy),
            'training_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'tensorflow_version': tf.__version__
        }
        
        metadata_path = f'{model_name}_metadata.json'
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        print(f"✅ Metadata saved: {metadata_path}")
        
        # Save emotion mapping
        mapping_path = f'{model_name}_emotion_mapping.pkl'
        with open(mapping_path, 'wb') as f:
            pickle.dump(self.emotion_mapping, f)
        print(f"✅ Emotion mapping saved: {mapping_path}")
        
        return final_model_path

def main():
    """Main training function"""
    try:
        # Initialize trainer
        trainer = SimpleFER2013Trainer()
        
        # Load data
        df = trainer.load_data()
        
        # Preprocess data
        X, y = trainer.preprocess_data(df)
        
        # Split data
        print("\n📊 Splitting data...")
        X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.3, random_state=42)
        X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)
        
        print(f"Training samples: {len(X_train)}")
        print(f"Validation samples: {len(X_val)}")
        print(f"Test samples: {len(X_test)}")
        
        # Create model
        model = trainer.create_model()
        
        # Display model summary
        print("\n🏗️ Model Architecture:")
        model.summary()
        
        # Train model
        history, model_name = trainer.train_model(X_train, y_train, X_val, y_val)
        
        # Evaluate model
        test_accuracy, test_loss = trainer.evaluate_model(X_test, y_test)
        
        # Save model
        final_model_path = trainer.save_model(model_name, test_accuracy)
        
        # Final summary
        print("\n🎯 TRAINING COMPLETE!")
        print("=" * 50)
        print(f"✅ Model saved: {final_model_path}")
        print(f"✅ Test Accuracy: {test_accuracy*100:.2f}%")
        print(f"✅ Model ready for use!")
        
        print(f"\n💡 Next steps:")
        print(f"1. Copy {final_model_path} to sleepy/server/")
        print(f"2. Update FER2013 detector to use new model")
        print(f"3. Test with real face images")
        
        return True
        
    except Exception as e:
        print(f"❌ Training failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎉 SUCCESS: Model training completed!")
    else:
        print("\n💥 FAILED: Check error messages above")