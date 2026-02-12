#!/usr/bin/env python3
"""
Test Dataset Loading for Notebook
Yo script le FER2013 enhanced dataset check garcha
"""

import os
import pandas as pd
import numpy as np

def test_dataset_loading():
    """Test if the FER2013 enhanced dataset can be loaded properly"""
    print("🔍 TESTING FER2013 ENHANCED DATASET")
    print("=" * 50)
    print()
    
    dataset_path = 'emotion_datasets/fer2013/fer2013_enhanced.csv'
    
    # Check if file exists
    if not os.path.exists(dataset_path):
        print(f"❌ Dataset not found: {dataset_path}")
        print("\n💡 Make sure the dataset file exists at:")
        print("   emotion_datasets/fer2013/fer2013_enhanced.csv")
        return False
    
    # Check file size
    file_size = os.path.getsize(dataset_path) / (1024 * 1024)  # MB
    print(f"✅ Dataset file found: {dataset_path}")
    print(f"   File size: {file_size:.1f} MB")
    
    try:
        # Load dataset
        print("\n📊 Loading dataset...")
        df = pd.read_csv(dataset_path)
        
        print(f"✅ Dataset loaded successfully!")
        print(f"   Total samples: {len(df):,}")
        print(f"   Columns: {list(df.columns)}")
        print(f"   Memory usage: {df.memory_usage(deep=True).sum() / 1024 / 1024:.1f} MB")
        
        # Check data structure
        print(f"\n📋 DATA STRUCTURE:")
        print(f"   DataFrame shape: {df.shape}")
        print(f"   Data types:")
        for col in df.columns:
            print(f"     {col}: {df[col].dtype}")
        
        # Check for missing values
        missing_values = df.isnull().sum()
        if missing_values.sum() > 0:
            print(f"\n⚠️ Missing values found:")
            for col, missing in missing_values.items():
                if missing > 0:
                    print(f"     {col}: {missing} missing")
        else:
            print(f"\n✅ No missing values found")
        
        # Analyze emotion column
        if 'emotion' in df.columns:
            print(f"\n🎭 EMOTION ANALYSIS:")
            emotion_counts = df['emotion'].value_counts()
            print(f"   Unique emotions: {len(emotion_counts)}")
            print(f"   Emotion distribution:")
            
            for emotion, count in emotion_counts.items():
                percentage = (count / len(df)) * 100
                print(f"     {emotion}: {count:,} ({percentage:.1f}%)")
            
            # Check emotion data type
            sample_emotion = df['emotion'].iloc[0]
            print(f"\n   Emotion data type: {type(sample_emotion)}")
            print(f"   Sample emotion value: {sample_emotion}")
        
        # Analyze pixels column
        if 'pixels' in df.columns:
            print(f"\n🖼️ PIXELS ANALYSIS:")
            sample_pixels = str(df['pixels'].iloc[0])
            pixel_values = sample_pixels.split()
            
            print(f"   Sample pixels length: {len(pixel_values)}")
            print(f"   Expected length: {48 * 48} (48x48 image)")
            print(f"   Pixels format check: {'✅ Valid' if len(pixel_values) == 48*48 else '❌ Invalid'}")
            
            # Check pixel value range
            try:
                pixel_ints = [int(p) for p in pixel_values[:10]]  # Test first 10
                print(f"   Sample pixel values: {pixel_ints}")
                print(f"   Pixel range: 0-255 (grayscale)")
            except ValueError as e:
                print(f"   ❌ Error parsing pixels: {e}")
        
        # Analyze Usage column (if exists)
        if 'Usage' in df.columns:
            print(f"\n📊 USAGE SPLIT ANALYSIS:")
            usage_counts = df['Usage'].value_counts()
            print(f"   Data splits:")
            for usage, count in usage_counts.items():
                percentage = (count / len(df)) * 100
                print(f"     {usage}: {count:,} ({percentage:.1f}%)")
        
        # Test data preprocessing
        print(f"\n🔧 TESTING DATA PREPROCESSING:")
        test_sample = df.iloc[0]
        
        try:
            # Test pixel parsing
            pixels_str = str(test_sample['pixels'])
            pixel_values = [int(p) for p in pixels_str.split()]
            
            if len(pixel_values) == 48 * 48:
                # Test reshaping
                pixel_array = np.array(pixel_values, dtype='uint8').reshape(48, 48)
                print(f"   ✅ Pixel parsing successful")
                print(f"   ✅ Image reshape successful: {pixel_array.shape}")
                
                # Test normalization
                normalized = pixel_array.astype('float32') / 255.0
                print(f"   ✅ Normalization successful: range [{normalized.min():.3f}, {normalized.max():.3f}]")
                
                # Test CNN format
                cnn_format = normalized.reshape(48, 48, 1)
                print(f"   ✅ CNN format successful: {cnn_format.shape}")
                
            else:
                print(f"   ❌ Invalid pixel count: {len(pixel_values)} (expected {48*48})")
                
        except Exception as e:
            print(f"   ❌ Preprocessing error: {e}")
        
        # Test emotion label processing
        try:
            emotion = test_sample['emotion']
            if isinstance(emotion, (int, float)):
                emotion_map = {0: 'angry', 1: 'disgust', 2: 'fear', 3: 'happy', 
                              4: 'neutral', 5: 'sad', 6: 'surprise'}
                emotion_str = emotion_map.get(int(emotion), 'neutral')
                print(f"   ✅ Emotion conversion: {emotion} → {emotion_str}")
            else:
                print(f"   ✅ Emotion already string: {emotion}")
                
        except Exception as e:
            print(f"   ❌ Emotion processing error: {e}")
        
        print(f"\n" + "=" * 50)
        print(f"🎉 DATASET TEST COMPLETED SUCCESSFULLY!")
        print(f"✅ Your FER2013 enhanced dataset is ready for the notebook")
        print(f"📊 Total samples available: {len(df):,}")
        print("=" * 50)
        
        return True
        
    except Exception as e:
        print(f"❌ Error loading dataset: {e}")
        print(f"\n💡 Troubleshooting:")
        print(f"1. Check if the file is corrupted")
        print(f"2. Verify CSV format")
        print(f"3. Check file permissions")
        return False

def main():
    """Main test function"""
    success = test_dataset_loading()
    
    if success:
        print(f"\n🚀 READY TO RUN NOTEBOOK!")
        print(f"Your dataset is properly formatted and ready for:")
        print(f"- Real accuracy testing")
        print(f"- Confusion matrix generation")
        print(f"- Performance analysis")
    else:
        print(f"\n⚠️ DATASET ISSUES FOUND")
        print(f"Please fix the dataset issues before running the notebook")

if __name__ == "__main__":
    main()