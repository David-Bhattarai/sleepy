#!/usr/bin/env python3
"""
FER-2013 Dataset Processor for AURA Emotion Detection
Processes downloaded FER-2013 dataset for training
"""

import os
import sys
import pandas as pd
import numpy as np
import cv2
from tqdm import tqdm
import json

def process_fer2013_dataset():
    """Process FER-2013 dataset from organized folder structure"""
    print(" Processing FER-2013 Dataset for AURA...")
    
    # Dataset paths
    fer_dir = "emotion_datasets/fer2013_real"
    train_dir = os.path.join(fer_dir, "train")
    test_dir = os.path.join(fer_dir, "test")
    
    # Check if dataset exists
    if not os.path.exists(train_dir):
        print(" FER-2013 dataset not found!")
        print("Please ensure the dataset is extracted to emotion_datasets/fer2013_real/")
        return False
    
    # Emotion labels (matching FER-2013 standard)
    emotions = ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']
    
    print(f" Processing organized FER-2013 dataset...")
    print(f"   Train directory: {train_dir}")
    print(f"   Test directory: {test_dir}")
    
    # Count images in each category
    processed_count = 0
    train_count = 0
    test_count = 0
    emotion_counts = {}
    
    # Process training images
    print(" Counting training images...")
    for emotion in emotions:
        emotion_dir = os.path.join(train_dir, emotion)
        if os.path.exists(emotion_dir):
            count = len([f for f in os.listdir(emotion_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
            emotion_counts[f"train_{emotion}"] = count
            train_count += count
            print(f"   {emotion}: {count} training images")
    
    # Process test images
    print(" Counting test images...")
    for emotion in emotions:
        emotion_dir = os.path.join(test_dir, emotion)
        if os.path.exists(emotion_dir):
            count = len([f for f in os.listdir(emotion_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
            emotion_counts[f"test_{emotion}"] = count
            test_count += count
            print(f"   {emotion}: {count} test images")
    
    processed_count = train_count + test_count
    
    # Create dataset info
    dataset_info = {
        'name': 'FER-2013 Real Dataset (Organized)',
        'source': 'Kaggle - FER-2013 Dataset',
        'total_images': processed_count,
        'training_images': train_count,
        'test_images': test_count,
        'emotions': emotions,
        'emotion_counts': emotion_counts,
        'image_size': '48x48',
        'format': 'grayscale',
        'processed_by': 'AURA Emotion Detection System',
        'dataset_structure': 'organized_folders'
    }
    
    # Save dataset info
    info_path = os.path.join(fer_dir, 'dataset_info.json')
    with open(info_path, 'w') as f:
        json.dump(dataset_info, f, indent=2)
    
    # Create numpy arrays for training
    print(" Creating numpy arrays from organized dataset...")
    
    all_images = []
    all_labels = []
    all_splits = []  
    
    # Process training data
    print(" Loading training images...")
    for emotion_idx, emotion in enumerate(emotions):
        emotion_dir = os.path.join(train_dir, emotion)
        
        if os.path.exists(emotion_dir):
            image_files = [f for f in os.listdir(emotion_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
            
            for img_file in tqdm(image_files, desc=f"Loading {emotion} training"):
                img_path = os.path.join(emotion_dir, img_file)
                img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
                
                if img is not None:
                    # Resize to 48x48 if needed
                    if img.shape != (48, 48):
                        img = cv2.resize(img, (48, 48))
                    
                    all_images.append(img)
                    all_labels.append(emotion_idx)
                    all_splits.append('train')
    
    # Process test data
    print(" Loading test images...")
    for emotion_idx, emotion in enumerate(emotions):
        emotion_dir = os.path.join(test_dir, emotion)
        
        if os.path.exists(emotion_dir):
            image_files = [f for f in os.listdir(emotion_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
            
            for img_file in tqdm(image_files, desc=f"Loading {emotion} test"):
                img_path = os.path.join(emotion_dir, img_file)
                img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
                
                if img is not None:
                    # Resize to 48x48 if needed
                    if img.shape != (48, 48):
                        img = cv2.resize(img, (48, 48))
                    
                    all_images.append(img)
                    all_labels.append(emotion_idx)
                    all_splits.append('test')
    
    # Save as numpy arrays
    if all_images:
        X = np.array(all_images)
        y = np.array(all_labels)
        splits = np.array(all_splits)
        
        # Normalize images
        X = X.astype('float32') / 255.0
        
        # Save arrays with split information
        arrays_path = os.path.join(fer_dir, 'fer2013_processed.npz')
        np.savez_compressed(arrays_path, X=X, y=y, splits=splits, emotions=emotions)
        
        print(f"Saved numpy arrays: {X.shape[0]} images")
        
        # Create separate train/test arrays
        train_mask = splits == 'train'
        test_mask = splits == 'test'
        
        X_train = X[train_mask]
        y_train = y[train_mask]
        X_test = X[test_mask]
        y_test = y[test_mask]
        
        # Save separate arrays for easier loading
        train_path = os.path.join(fer_dir, 'fer2013_train.npz')
        test_path = os.path.join(fer_dir, 'fer2013_test.npz')
        
        np.savez_compressed(train_path, X=X_train, y=y_train, emotions=emotions)
        np.savez_compressed(test_path, X=X_test, y=y_test, emotions=emotions)
        
        print(f" Saved training arrays: {X_train.shape[0]} images")
        print(f" Saved test arrays: {X_test.shape[0]} images")
    
    # Print summary
    print("\n FER-2013 Dataset Processing Complete!")
    print(f" Dataset Summary:")
    print(f"   Total processed: {processed_count} images")
    print(f"   Training images: {train_count}")
    print(f"   Test images: {test_count}")
    print(f"   Emotions: {len(emotions)}")
    print(f"   Saved to: {fer_dir}")
    
    # Print emotion distribution
    print(f"\n Emotion Distribution:")
    for emotion in emotions:
        train_key = f"train_{emotion}"
        test_key = f"test_{emotion}"
        train_cnt = emotion_counts.get(train_key, 0)
        test_cnt = emotion_counts.get(test_key, 0)
        total_cnt = train_cnt + test_cnt
        print(f"   {emotion}: {total_cnt} total ({train_cnt} train, {test_cnt} test)")
    
    return True

def verify_dataset():
    """Verify processed dataset"""
    print("Verifying processed dataset...")
    
    fer_dir = "emotion_datasets/fer2013_real"
    train_dir = os.path.join(fer_dir, "train")
    test_dir = os.path.join(fer_dir, "test")
    emotions = ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']
    
    total_train_images = 0
    total_test_images = 0
    
    print("Training Images:")
    for emotion in emotions:
        emotion_dir = os.path.join(train_dir, emotion)
        if os.path.exists(emotion_dir):
            count = len([f for f in os.listdir(emotion_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
            print(f"   {emotion}: {count} images")
            total_train_images += count
    
    print(" Test Images:")
    for emotion in emotions:
        emotion_dir = os.path.join(test_dir, emotion)
        if os.path.exists(emotion_dir):
            count = len([f for f in os.listdir(emotion_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
            print(f"   {emotion}: {count} images")
            total_test_images += count
    
    print(f" Total: {total_train_images + total_test_images} images ({total_train_images} train, {total_test_images} test)")
    
    # Check numpy arrays
    arrays_path = os.path.join(fer_dir, 'fer2013_processed.npz')
    if os.path.exists(arrays_path):
        data = np.load(arrays_path)
        print(f" Numpy arrays: {data['X'].shape[0]} images")
        print(f"   Image shape: {data['X'].shape[1:]}")
        print(f"   Labels shape: {data['y'].shape}")
        
        # Check train/test split arrays
        train_path = os.path.join(fer_dir, 'fer2013_train.npz')
        test_path = os.path.join(fer_dir, 'fer2013_test.npz')
        
        if os.path.exists(train_path):
            train_data = np.load(train_path)
            print(f"   Train arrays: {train_data['X'].shape[0]} images")
        
        if os.path.exists(test_path):
            test_data = np.load(test_path)
            print(f"   Test arrays: {test_data['X'].shape[0]} images")
    
    return (total_train_images + total_test_images) > 0

def main():
    """Main processing function"""
    print(" FER-2013 Dataset Processor for AURA")
    print("=" * 50)
    
    try:
        # Process dataset
        success = process_fer2013_dataset()
        
        if success:
            # Verify dataset
            verify_dataset()
            
            print("\n Dataset ready for training!")
            print("\n Next Steps:")
            print("1. Run: python server/advanced_emotion_detection.py")
            print("2. Test: python test_advanced_emotion.py")
            print("3. Use: Navigate to /emotion-detection.html")
            
            return True
        else:
            print(" Dataset processing failed")
            return False
            
    except Exception as e:
        print(f" Error: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)