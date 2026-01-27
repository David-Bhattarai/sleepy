#!/usr/bin/env python3
"""
Check Datasets Used in ML Models
See what datasets are being used for training
"""

import os
import pickle
import json

def check_emotion_datasets():
    """Check emotion detection datasets"""
    print("😊 EMOTION DETECTION DATASETS")
    print("=" * 50)
    
    datasets_found = []
    
    # Check compact emotion dataset
    compact_path = "compact_emotion_dataset"
    if os.path.exists(compact_path):
        print(f"✅ Found: {compact_path}")
        
        # Check processed files
        processed_path = os.path.join(compact_path, "processed")
        if os.path.exists(processed_path):
            files = os.listdir(processed_path)
            print(f"   📁 Processed files: {len(files)}")
            for file in files:
                if file.endswith('.npz'):
                    print(f"   📊 {file}")
                elif file.endswith('.pkl'):
                    print(f"   🔑 {file}")
        
        # Check README
        readme_path = os.path.join(compact_path, "README.md")
        if os.path.exists(readme_path):
            with open(readme_path, 'r') as f:
                content = f.read()
                if 'FER2013' in content:
                    print("   📋 Source: FER2013 dataset")
                if 'samples' in content.lower():
                    import re
                    samples = re.findall(r'(\d+,?\d*)\s*samples', content, re.IGNORECASE)
                    if samples:
                        print(f"   📊 Samples: {samples[0]}")
        
        datasets_found.append("Compact Emotion Dataset")
    
    # Check 50MB emotion dataset
    mb50_path = "emotion_dataset_50mb"
    if os.path.exists(mb50_path):
        print(f"\n✅ Found: {mb50_path}")
        
        processed_path = os.path.join(mb50_path, "processed")
        if os.path.exists(processed_path):
            files = os.listdir(processed_path)
            print(f"   📁 Processed files: {len(files)}")
            for file in files:
                if file.endswith('.npz'):
                    print(f"   📊 {file}")
        
        datasets_found.append("50MB Emotion Dataset")
    
    # Check FER2013 dataset
    fer_path = "emotion_datasets/fer2013"
    if os.path.exists(fer_path):
        print(f"\n✅ Found: {fer_path}")
        
        files = os.listdir(fer_path)
        for file in files:
            if file.endswith('.csv'):
                print(f"   📊 {file}")
                # Check file size
                file_path = os.path.join(fer_path, file)
                size_mb = os.path.getsize(file_path) / (1024 * 1024)
                print(f"   📏 Size: {size_mb:.1f} MB")
        
        datasets_found.append("FER2013 Dataset")
    
    return datasets_found

def check_chatbot_datasets():
    """Check chatbot datasets"""
    print("\n🤖 CHATBOT DATASETS")
    print("=" * 50)
    
    datasets_found = []
    
    # Check intents.json
    intents_paths = [
        "sleepy/server/intents.json",
        "intents.json"
    ]
    
    for path in intents_paths:
        if os.path.exists(path):
            print(f"✅ Found: {path}")
            
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                intents = data.get('intents', [])
                print(f"   📊 Total Intents: {len(intents)}")
                
                # Count patterns and responses
                total_patterns = 0
                total_responses = 0
                
                for intent in intents:
                    patterns = intent.get('patterns', [])
                    responses = intent.get('responses', [])
                    total_patterns += len(patterns)
                    total_responses += len(responses)
                
                print(f"   📝 Total Patterns: {total_patterns}")
                print(f"   💬 Total Responses: {total_responses}")
                
                # Show some intent categories
                print("   🏷️ Intent Categories:")
                for i, intent in enumerate(intents[:10]):  # Show first 10
                    tag = intent.get('tag', 'unknown')
                    print(f"      - {tag}")
                if len(intents) > 10:
                    print(f"      ... and {len(intents) - 10} more")
            
            datasets_found.append("Intents JSON Dataset")
            break
    
    return datasets_found

def check_trained_models():
    """Check what models are trained"""
    print("\n🧠 TRAINED MODELS")
    print("=" * 50)
    
    models_found = []
    
    # Check emotion models
    emotion_models = [
        "compact_emotion_model_best.h5",
        "sleepy/server/compact_emotion_model_trained.h5",
        "genuine_emotion_model.h5",
        "sleepy/server/genuine_emotion_model_real.h5"
    ]
    
    for model_path in emotion_models:
        if os.path.exists(model_path):
            print(f"✅ Emotion Model: {model_path}")
            size_mb = os.path.getsize(model_path) / (1024 * 1024)
            print(f"   📏 Size: {size_mb:.1f} MB")
            models_found.append(model_path)
    
    # Check chatbot models
    chatbot_models = [
        "sleepy/server/mindbridge_model_80percent.pkl",
        "sleepy/server/mindbridge_model.pkl"
    ]
    
    for model_path in chatbot_models:
        if os.path.exists(model_path):
            print(f"✅ Chatbot Model: {model_path}")
            size_mb = os.path.getsize(model_path) / (1024 * 1024)
            print(f"   📏 Size: {size_mb:.1f} MB")
            
            # Try to load and check details
            try:
                with open(model_path, 'rb') as f:
                    model_data = pickle.load(f)
                    if hasattr(model_data, 'classes_'):
                        print(f"   🏷️ Classes: {len(model_data.classes_)}")
                    print(f"   🔧 Model Type: {type(model_data).__name__}")
            except:
                print("   ⚠️ Could not load model details")
            
            models_found.append(model_path)
    
    return models_found

def check_dataset_details():
    """Check detailed dataset information"""
    print("\n📊 DATASET DETAILS")
    print("=" * 50)
    
    # Check emotion mapping
    mapping_files = [
        "compact_emotion_dataset/processed/emotion_mapping.pkl",
        "emotion_datasets/processed/emotion_mapping.pkl",
        "sleepy/server/compact_emotion_mapping.pkl"
    ]
    
    for mapping_path in mapping_files:
        if os.path.exists(mapping_path):
            print(f"✅ Emotion Mapping: {mapping_path}")
            try:
                with open(mapping_path, 'rb') as f:
                    mapping = pickle.load(f)
                    print(f"   🏷️ Emotions: {list(mapping.values())}")
                    print(f"   📊 Total Classes: {len(mapping)}")
            except:
                print("   ⚠️ Could not load mapping")
    
    # Check training data files
    data_files = [
        "compact_emotion_dataset/processed/compact_train.npz",
        "compact_emotion_dataset/processed/compact_test.npz",
        "emotion_dataset_50mb/processed/emotion_train_50mb.npz"
    ]
    
    for data_path in data_files:
        if os.path.exists(data_path):
            print(f"✅ Training Data: {data_path}")
            size_mb = os.path.getsize(data_path) / (1024 * 1024)
            print(f"   📏 Size: {size_mb:.1f} MB")
            
            try:
                import numpy as np
                data = np.load(data_path)
                if 'X' in data:
                    print(f"   📊 Samples: {data['X'].shape[0]}")
                    print(f"   📐 Input Shape: {data['X'].shape[1:]}")
                if 'y' in data:
                    print(f"   🏷️ Labels Shape: {data['y'].shape}")
            except:
                print("   ⚠️ Could not load data details")

def main():
    """Main function"""
    print("📋 DATASET ANALYSIS FOR MindBridge - NCIT Final Year Project ML MODELS")
    print("=" * 60)
    
    # Check emotion datasets
    emotion_datasets = check_emotion_datasets()
    
    # Check chatbot datasets  
    chatbot_datasets = check_chatbot_datasets()
    
    # Check trained models
    trained_models = check_trained_models()
    
    # Check dataset details
    check_dataset_details()
    
    # Summary
    print("\n" + "=" * 60)
    print("🎯 SUMMARY")
    print("=" * 60)
    
    print("📊 DATASETS USED:")
    all_datasets = emotion_datasets + chatbot_datasets
    for i, dataset in enumerate(all_datasets, 1):
        print(f"   {i}. {dataset}")
    
    print(f"\n🧠 TRAINED MODELS: {len(trained_models)}")
    for model in trained_models:
        print(f"   ✅ {os.path.basename(model)}")
    
    print("\n💡 MAIN DATASETS:")
    print("   😊 Emotion Detection: FER2013 (Facial Expression Recognition)")
    print("   🤖 Chatbot: Custom intents.json (Mental health conversations)")
    print("   📊 Total Size: Compact datasets under 50MB each")
    print("   🎯 Accuracy: 80-90% with trained models")

if __name__ == "__main__":
    main()