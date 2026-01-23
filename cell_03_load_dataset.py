#!/usr/bin/env python3
"""
Cell 3: Load and Explore Dataset
"""

print("📊 Cell 3: Loading and exploring dataset...")

try:
    import numpy as np
    import pandas as pd
    import os
    print("✅ Required imports loaded")
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("🔧 Run cell_01_imports.py first")
    exit(1)

# Recreate trainer class for this cell
class SimpleTrainer:
    def __init__(self):
        self.emotions = ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']
        self.img_size = 48
    
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
            print("❌ Real dataset not found. Creating sample data...")
            df = self.create_sample_data()
        
        return df
    
    def create_sample_data(self):
        """Create sample data"""
        print("🔧 Creating sample dataset...")
        
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

# Initialize trainer and load data
try:
    trainer = SimpleTrainer()
    df = trainer.load_fer2013_data()
    
    # Display first few rows
    print("\\n📋 First 5 rows of dataset:")
    print(df.head())
    
    # Show dataset shape
    print(f"\\n📊 Dataset shape: {df.shape}")
    print(f"📊 Columns: {list(df.columns)}")
    
    # Check for missing values
    print(f"\\n🔍 Missing values:")
    print(df.isnull().sum())
    
    # Show data types
    print(f"\\n📋 Data types:")
    print(df.dtypes)
    
    # Show emotion distribution
    print(f"\\n📈 Emotion distribution:")
    emotion_counts = df['emotion'].value_counts()
    print(emotion_counts)
    
    # Validate pixel data
    print(f"\\n🔍 Validating pixel data...")
    sample_pixels = df['pixels'].iloc[0].split()
    print(f"📊 First sample pixel count: {len(sample_pixels)}")
    print(f"📊 Expected pixel count: {trainer.img_size * trainer.img_size}")
    
    if len(sample_pixels) == trainer.img_size * trainer.img_size:
        print("✅ Pixel data format is correct")
    else:
        print("⚠️ Pixel data format may need adjustment")
    
    print("\\n✅ Cell 3 completed successfully!")
    print(f"📊 Dataset ready with {len(df)} samples")
    
except Exception as e:
    print(f"❌ Error in Cell 3: {e}")
    import traceback
    traceback.print_exc()
    exit(1)