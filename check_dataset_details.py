#!/usr/bin/env python3

import numpy as np
import pickle

print(" DATASET AND MODEL DETAILS")
print("=" * 50)

# Load dataset details
try:
    train_data = np.load('emotion_datasets/processed/fer2013_train.npz')
    val_data = np.load('emotion_datasets/processed/fer2013_val.npz')
    test_data = np.load('emotion_datasets/processed/fer2013_test.npz')
    
    print(" DATASET LOCATION:")
    print("   Raw dataset: emotion_datasets/fer2013/fer2013_enhanced.csv")
    print("   Processed data: emotion_datasets/processed/")
    print()
    
    print(" DATASET SIZE:")
    print(f"   Training samples: {train_data['X'].shape[0]:,}")
    print(f"   Validation samples: {val_data['X'].shape[0]:,}")
    print(f"   Test samples: {test_data['X'].shape[0]:,}")
    print(f"   Total samples: {train_data['X'].shape[0] + val_data['X'].shape[0] + test_data['X'].shape[0]:,}")
    print(f"   Image size: {train_data['X'].shape[1:]} (48x48 grayscale)")
    print(f"   Emotion classes: {len(np.unique(train_data['y']))}")
    print()
    
    # Load emotion mapping
    with open('emotion_datasets/processed/emotion_mapping.pkl', 'rb') as f:
        emotion_mapping = pickle.load(f)
    
    print(" EMOTION CLASSES:")
    for id, emotion in emotion_mapping.items():
        count = np.sum(train_data['y'] == id)
        print(f"   {id}: {emotion} ({count} training samples)")
    print()
    
except Exception as e:
    print(f" Error loading dataset: {e}")

# Load model results
try:
    with open('trained_models/real_emotion_model_20260122_212824_results.pkl', 'rb') as f:
        results = pickle.load(f)
    
    print(" MODEL PERFORMANCE:")
    print(f"   Test Accuracy: {results['test_accuracy']*100:.2f}%")
    print(f"   Test Loss: {results['test_loss']:.4f}")
    print()
    
    print(" TRAINED MODEL FILES:")
    print("   Best model: trained_models/real_emotion_model_20260122_212824_best.h5")
    print("   Final model: trained_models/real_emotion_model_20260122_212824_final.h5")
    print("   Server model: sleepy/server/genuine_emotion_model_real.h5")
    print("   Training plots: trained_models/real_emotion_model_20260122_212824_training_history.png")
    print("   Confusion matrix: trained_models/real_emotion_model_20260122_212824_confusion_matrix.png")
    print()
    
except Exception as e:
    print(f" Error loading model results: {e}")

print(" TRAINING SCRIPTS:")
print("   Dataset downloader: download_real_dataset.py")
print("   Model trainer: train_real_emotion_model.py")
print("   Emotion detector: sleepy/server/genuine_emotion_detector.py")
print()

print(" TO GET HIGHER ACCURACY:")
print("   1. Download real FER-2013 dataset (35,000+ samples)")
print("   2. Use Kaggle API: kaggle datasets download -d msambare/fer2013")
print("   3. Train for more epochs (50-100)")
print("   4. Use data augmentation and transfer learning")
print("   5. Fine-tune hyperparameters")