#!/usr/bin/env python3
"""
Cell 2: FER2013 Trainer Class (Error-Free Version)
"""

print("🏗️ Cell 2: Creating FER2013 Trainer Class...")

# Import required modules
try:
    import numpy as np
    import pandas as pd
    import os
    from tensorflow.keras.utils import to_categorical
    print("✅ Required imports loaded")
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("🔧 Run cell_01_imports_fixed.py first")
    exit(1)

class FER2013EmotionTrainer:
    """FER-2013 Enhanced Dataset Emotion Model Trainer (Error-Free Version)"""
    
    def __init__(self):
        self.emotions = ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']
        self.emotion_mapping = {emotion: idx for idx, emotion in enumerate(self.emotions)}
        self.num_classes = len(self.emotions)
        self.img_size = 48
        self.model = None
        self.history = None
        
        print(f"✅ FER2013 Trainer initialized")
        print(f"📊 Emotions: {self.emotions}")
        print(f"📊 Classes: {self.num_classes}")
        print(f"📊 Image size: {self.img_size}x{self.img_size}")
    
    def load_fer2013_data(self):
        """Load FER-2013 enhanced dataset with error handling"""
        print("📊 Loading FER-2013 Enhanced Dataset...")
        
        dataset_paths = [
            'emotion_datasets/fer2013/fer2013_enhanced.csv',
            '../emotion_datasets/fer2013/fer2013_enhanced.csv',
            'fer2013_enhanced.csv'
        ]
        
        df = None
        for dataset_path in dataset_paths:
            if os.path.exists(dataset_path):
                try:
                    df = pd.read_csv(dataset_path)
                    print(f"✅ Loaded {len(df)} samples from {dataset_path}")
                    break
                except Exception as e:
                    print(f"⚠️ Error loading {dataset_path}: {e}")
                    continue
        
        if df is None:
            print("❌ Real dataset not found. Creating sample data...")
            df = self.create_sample_data()
        
        # Validate dataset
        required_columns = ['emotion', 'pixels']
        if not all(col in df.columns for col in required_columns):
            raise ValueError(f"Dataset must contain columns: {required_columns}")
        
        print("\n📈 Dataset Statistics:")
        print(df['emotion'].value_counts())
        
        return df
    
    def create_sample_data(self):
        """Create sample data for demonstration"""
        print("🔧 Creating sample dataset...")
        
        sample_data = []
        samples_per_emotion = 50
        
        for emotion in self.emotions:
            for i in range(samples_per_emotion):
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
        """Preprocess dataset with comprehensive error handling"""
        print("🔧 Preprocessing data...")
        
        pixels = []
        labels = []
        skipped_rows = 0
        
        for idx, row in df.iterrows():
            try:
                pixel_values = [int(pixel) for pixel in str(row['pixels']).split()]
                
                if len(pixel_values) != self.img_size * self.img_size:
                    skipped_rows += 1
                    continue
                
                pixel_array = np.array(pixel_values).reshape(self.img_size, self.img_size)
                pixels.append(pixel_array)
                labels.append(row['emotion'])
                
            except Exception as e:
                skipped_rows += 1
                continue
        
        if len(pixels) == 0:
            raise ValueError("No valid data found after preprocessing")
        
        if skipped_rows > 0:
            print(f"⚠️ Skipped {skipped_rows} invalid rows")
        
        # Convert to numpy arrays
        X = np.array(pixels, dtype='float32')
        y = np.array([self.emotion_mapping.get(emotion, 0) for emotion in labels])
        
        # Normalize
        X = X / 255.0
        
        # Reshape for CNN
        X = X.reshape(-1, self.img_size, self.img_size, 1)
        
        # Convert to categorical
        y = to_categorical(y, self.num_classes)
        
        print(f"✅ Preprocessed: X {X.shape}, y {y.shape}")
        print(f"   Range: [{X.min():.3f}, {X.max():.3f}]")
        
        return X, y
    
    def create_model(self):
        """Create CNN model with error handling"""
        print("🏗️ Creating CNN model...")
        
        try:
            from tensorflow.keras.models import Sequential
            from tensorflow.keras.layers import Conv2D, MaxPooling2D, Dense, Dropout, Flatten, BatchNormalization
            from tensorflow.keras.optimizers import Adam
            
            model = Sequential([
                Conv2D(32, (3, 3), activation='relu', input_shape=(self.img_size, self.img_size, 1)),
                BatchNormalization(),
                Conv2D(32, (3, 3), activation='relu'),
                MaxPooling2D(pool_size=(2, 2)),
                Dropout(0.25),
                
                Conv2D(64, (3, 3), activation='relu'),
                BatchNormalization(),
                Conv2D(64, (3, 3), activation='relu'),
                MaxPooling2D(pool_size=(2, 2)),
                Dropout(0.25),
                
                Conv2D(128, (3, 3), activation='relu'),
                BatchNormalization(),
                Dropout(0.25),
                
                Flatten(),
                Dense(512, activation='relu'),
                BatchNormalization(),
                Dropout(0.5),
                Dense(256, activation='relu'),
                Dropout(0.5),
                Dense(self.num_classes, activation='softmax')
            ])
            
            # Compile with version compatibility
            try:
                optimizer = Adam(learning_rate=0.001)
            except TypeError:
                optimizer = Adam(lr=0.001)
            
            model.compile(
                optimizer=optimizer,
                loss='categorical_crossentropy',
                metrics=['accuracy']
            )
            
            self.model = model
            print("✅ Model created successfully!")
            return model
            
        except Exception as e:
            print(f"❌ Model creation failed: {e}")
            raise

# Test trainer creation
try:
    trainer = FER2013EmotionTrainer()
    print("\n🎯 Trainer ready!")
    
    # Test with sample data
    print("\n🧪 Testing with sample data...")
    sample_df = trainer.create_sample_data()
    print(f"Sample data: {sample_df.shape}")
    
    # Test preprocessing
    X_sample, y_sample = trainer.preprocess_data(sample_df.head(20))
    print(f"Preprocessed sample: X {X_sample.shape}, y {y_sample.shape}")
    
    print("\n✅ Cell 2 completed successfully!")
    
except Exception as e:
    print(f"❌ Error in Cell 2: {e}")
    trainer = None
