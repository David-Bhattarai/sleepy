#!/usr/bin/env python3
"""
Cell 2: Create FER2013 Trainer Class
"""

print("🏗️ Cell 2: Creating FER2013 Trainer Class...")

try:
    import numpy as np
    import pandas as pd
    import os
    from tensorflow.keras.utils import to_categorical
    print("✅ Required imports loaded")
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("🔧 Run cell_01_imports.py first to fix imports")
    exit(1)

class FER2013EmotionTrainer:
    """FER-2013 Enhanced Dataset Emotion Model Trainer"""
    
    def __init__(self):
        self.emotions = ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']
        self.emotion_mapping = {emotion: idx for idx, emotion in enumerate(self.emotions)}
        self.num_classes = len(self.emotions)
        self.img_size = 48
        self.model = None
        self.history = None
        
        print(f"✅ FER2013 Trainer initialized")
        print(f"📊 Emotions: {self.emotions}")
        print(f"📊 Number of classes: {self.num_classes}")
        print(f"📊 Image size: {self.img_size}x{self.img_size}")
    
    def load_fer2013_data(self):
        """Load FER-2013 enhanced dataset"""
        print("📊 Loading FER-2013 Enhanced Dataset...")
        
        # Dataset file paths to try
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
            print("❌ Dataset not found. Creating sample data for demonstration...")
            df = self.create_sample_data()
        
        # Validate dataset structure
        required_columns = ['emotion', 'pixels']
        if not all(col in df.columns for col in required_columns):
            raise ValueError(f"Dataset must contain columns: {required_columns}")
        
        # Display dataset info
        print("\\n📈 Dataset Statistics:")
        print(df['emotion'].value_counts())
        
        return df
    
    def create_sample_data(self):
        """Create sample data for demonstration if dataset not found"""
        print("🔧 Creating sample dataset for demonstration...")
        
        sample_data = []
        samples_per_emotion = 50
        
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
        print("🔧 Preprocessing data...")
        
        # Extract pixel data and labels
        pixels = []
        labels = []
        
        for idx, row in df.iterrows():
            try:
                # Convert pixel string to array
                pixel_values = [int(pixel) for pixel in str(row['pixels']).split()]
                
                # Ensure we have the right number of pixels
                if len(pixel_values) != self.img_size * self.img_size:
                    print(f"⚠️ Skipping row {idx}: expected {self.img_size * self.img_size} pixels, got {len(pixel_values)}")
                    continue
                
                pixel_array = np.array(pixel_values).reshape(self.img_size, self.img_size)
                
                pixels.append(pixel_array)
                labels.append(row['emotion'])
                
            except Exception as e:
                print(f"⚠️ Error processing row {idx}: {e}")
                continue
        
        if len(pixels) == 0:
            raise ValueError("No valid data found after preprocessing")
        
        # Convert to numpy arrays
        X = np.array(pixels, dtype='float32')
        y = np.array([self.emotion_mapping.get(emotion, 0) for emotion in labels])
        
        # Normalize pixel values
        X = X / 255.0
        
        # Reshape for CNN (add channel dimension)
        X = X.reshape(-1, self.img_size, self.img_size, 1)
        
        # Convert labels to categorical
        y = to_categorical(y, self.num_classes)
        
        print(f"✅ Data preprocessed: X shape {X.shape}, y shape {y.shape}")
        print(f"   X data type: {X.dtype}, range: [{X.min():.3f}, {X.max():.3f}]")
        
        return X, y

# Test trainer creation
try:
    trainer = FER2013EmotionTrainer()
    print("\\n🎯 Trainer ready for use!")
    
    # Test sample data creation
    print("\\n🧪 Testing sample data creation...")
    sample_df = trainer.create_sample_data()
    print(f"📊 Sample data shape: {sample_df.shape}")
    print(f"📊 Sample columns: {list(sample_df.columns)}")
    
    # Test preprocessing with sample data
    print("\\n🧪 Testing data preprocessing...")
    X_sample, y_sample = trainer.preprocess_data(sample_df.head(10))  # Test with first 10 rows
    print(f"📊 Preprocessed sample: X {X_sample.shape}, y {y_sample.shape}")
    
    print("\\n✅ Cell 2 completed successfully!")
    
except Exception as e:
    print(f"❌ Error in Cell 2: {e}")
    print("🔧 Check that all imports are working from Cell 1")
    exit(1)