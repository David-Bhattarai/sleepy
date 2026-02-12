#!/usr/bin/env python3
"""
🎯 AuraBot Model Accuracy Checker
Timro trained models ko accuracy check garne script
"""

import json
import os
from datetime import datetime
from pathlib import Path

def print_header():
    """Print report header"""
    print("\n" + "=" * 70)
    print("🎯 AURABOT EMOTION DETECTION - MODEL ACCURACY REPORT")
    print("=" * 70)
    print(f"📅 Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70 + "\n")

def check_model_file(filepath, model_num):
    """Check individual model file"""
    if not os.path.exists(filepath):
        return False
    
    print(f"📊 Model {model_num}: {os.path.basename(filepath)}")
    print("-" * 70)
    
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        # Model name
        if 'model_name' in data:
            print(f"   📝 Name: {data['model_name']}")
        
        # Accuracy
        accuracy_found = False
        if 'accuracy' in data:
            acc = data['accuracy']
            if isinstance(acc, str):
                print(f"   ✅ Accuracy: {acc}")
            else:
                print(f"   ✅ Accuracy: {acc:.2f}%")
            accuracy_found = True
        elif 'test_accuracy' in data:
            acc = data['test_accuracy']
            print(f"   ✅ Test Accuracy: {acc*100:.2f}%")
            accuracy_found = True
        
        if not accuracy_found:
            print(f"   ⚠️  Accuracy: Not found")
        
        # Loss
        if 'test_loss' in data:
            print(f"   📉 Test Loss: {data['test_loss']:.4f}")
        
        # Dataset
        if 'dataset' in data:
            print(f"   📊 Dataset: {data['dataset']}")
        
        # Emotions
        if 'emotions' in data:
            emotions = data['emotions']
            print(f"   🎭 Emotions: {len(emotions)} types")
            print(f"      {', '.join(emotions)}")
        
        # Model type
        if 'model_type' in data:
            print(f"   🏗️  Architecture: {data['model_type']}")
        
        # Date/Time
        if 'updated' in data:
            print(f"   📅 Updated: {data['updated']}")
        elif 'training_time' in data:
            print(f"   📅 Trained: {data['training_time']}")
        elif 'timestamp' in data:
            print(f"   📅 Timestamp: {data['timestamp']}")
        
        # TensorFlow version
        if 'tensorflow_version' in data:
            print(f"   ⚙️  TensorFlow: {data['tensorflow_version']}")
        
        # File size
        if 'model_file' in data:
            model_path = os.path.join('server', data['model_file'])
            if os.path.exists(model_path):
                size_mb = os.path.getsize(model_path) / (1024 * 1024)
                print(f"   💾 Model Size: {size_mb:.2f} MB")
        
        print()
        return True
        
    except Exception as e:
        print(f"   ❌ Error reading file: {e}\n")
        return False

def check_model_files_exist():
    """Check if model .h5 files exist"""
    print("🔍 CHECKING MODEL FILES:")
    print("-" * 70)
    
    model_files = [
        'server/fer2013_emotion_model.h5',
        'server/emotion_model.h5',
        'server/production_emotion_model.h5',
        'server/genuine_emotion_model_real.h5'
    ]
    
    found_models = []
    for filepath in model_files:
        if os.path.exists(filepath):
            size_mb = os.path.getsize(filepath) / (1024 * 1024)
            print(f"   ✅ {filepath} ({size_mb:.2f} MB)")
            found_models.append(filepath)
        else:
            print(f"   ❌ {filepath} (Not found)")
    
    print()
    return found_models

def get_recommendation(accuracies):
    """Get model recommendation based on accuracies"""
    if not accuracies:
        return "⚠️  No accuracy data found"
    
    best = max(accuracies, key=lambda x: x[1])
    model_name, accuracy = best
    
    if accuracy >= 90:
        return f"✅ EXCELLENT: Use {model_name} ({accuracy:.2f}% accuracy)"
    elif accuracy >= 70:
        return f"✅ GOOD: Use {model_name} ({accuracy:.2f}% accuracy)"
    elif accuracy >= 50:
        return f"⚠️  MODERATE: {model_name} ({accuracy:.2f}% accuracy) - Consider retraining"
    else:
        return f"❌ POOR: {model_name} ({accuracy:.2f}% accuracy) - Retrain required"

def main():
    """Main function"""
    print_header()
    
    # Check model files
    found_models = check_model_files_exist()
    
    # Metadata files to check
    metadata_files = [
        'server/emotion_detector_config.json',
        'server/fer2013_emotion_metadata.json',
        'server/production_emotion_model_metadata.json',
        'simple_fer2013_model_20260123_225231_metadata.json',
        'simple_production_model_20260123_084621_metadata.json'
    ]
    
    print("📋 CHECKING METADATA FILES:")
    print("-" * 70)
    print()
    
    accuracies = []
    model_num = 1
    
    for filepath in metadata_files:
        if check_model_file(filepath, model_num):
            # Extract accuracy for recommendation
            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)
                
                if 'accuracy' in data:
                    acc = data['accuracy']
                    if not isinstance(acc, str):
                        accuracies.append((os.path.basename(filepath), acc))
                elif 'test_accuracy' in data:
                    acc = data['test_accuracy'] * 100
                    accuracies.append((os.path.basename(filepath), acc))
            except:
                pass
            
            model_num += 1
    
    # Summary
    print("=" * 70)
    print("📊 SUMMARY")
    print("=" * 70)
    print(f"   Total Models Found: {len(found_models)}")
    print(f"   Metadata Files: {model_num - 1}")
    print()
    
    # Accuracy comparison
    if accuracies:
        print("📈 ACCURACY COMPARISON:")
        print("-" * 70)
        accuracies.sort(key=lambda x: x[1], reverse=True)
        for name, acc in accuracies:
            bar_length = int(acc / 2)  # Scale to 50 chars max
            bar = "█" * bar_length
            print(f"   {name[:40]:40} {acc:6.2f}% {bar}")
        print()
    
    # Recommendation
    print("💡 RECOMMENDATION:")
    print("-" * 70)
    recommendation = get_recommendation(accuracies)
    print(f"   {recommendation}")
    print()
    
    # Quick commands
    print("🔧 QUICK COMMANDS:")
    print("-" * 70)
    print("   Check main model:")
    print("   $ cat server/emotion_detector_config.json | grep accuracy")
    print()
    print("   Test live:")
    print("   $ python server/server.py")
    print("   $ Open: http://localhost:5000/emotion-detection.html")
    print()
    
    print("=" * 70)
    print("✅ Report Complete!")
    print("=" * 70 + "\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Report cancelled by user.\n")
    except Exception as e:
        print(f"\n❌ Error: {e}\n")
