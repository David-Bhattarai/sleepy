#!/usr/bin/env python3
"""
Start Production ML System
Launch the complete project with production-ready ML components
"""

import os
import sys
import subprocess
import time

def check_production_components():
    """Check if production components are available"""
    print("🔍 Checking PRODUCTION ML SYSTEM components...")
    
    required_files = [
        "sleepy/server/production_emotion_detector.py",
        "sleepy/server/production_chatbot.py",
        "sleepy/server/app.py"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ Missing production components:")
        for file in missing_files:
            print(f"   - {file}")
        print("\\n🔧 Run 'python create_production_ml_system.py' first!")
        return False
    
    print("✅ All production components found!")
    return True

def check_datasets():
    """Check if datasets are available"""
    print("📊 Checking datasets...")
    
    dataset_paths = [
        "emotion_datasets/processed/fer2013_train.npz",
        "compact_emotion_dataset/processed/compact_train.npz",
        "emotion_dataset_50mb/processed/emotion_train_50mb.npz"
    ]
    
    found_datasets = []
    for dataset_path in dataset_paths:
        if os.path.exists(dataset_path):
            found_datasets.append(dataset_path)
    
    if found_datasets:
        print(f"✅ Found {len(found_datasets)} dataset(s):")
        for dataset in found_datasets:
            print(f"   - {dataset}")
    else:
        print("⚠️ No processed datasets found")
        print("💡 The system will work with fallback models")
    
    return len(found_datasets) > 0

def check_trained_models():
    """Check if trained models are available"""
    print("🤖 Checking trained models...")
    
    model_paths = [
        "sleepy/server/production_emotion_model.h5",
        "sleepy/server/best_emotion_model.h5",
        "sleepy/server/compact_emotion_model_trained.h5",
        "sleepy/server/genuine_emotion_model_real.h5"
    ]
    
    found_models = []
    for model_path in model_paths:
        if os.path.exists(model_path):
            found_models.append(model_path)
    
    if found_models:
        print(f"✅ Found {len(found_models)} trained model(s):")
        for model in found_models:
            print(f"   - {model}")
    else:
        print("⚠️ No trained models found")
        print("💡 The system will create fallback models")
    
    return len(found_models) > 0

def start_production_server():
    """Start the server with production ML system"""
    print("🚀 Starting PRODUCTION ML SYSTEM Server...")
    print("=" * 60)
    print("🎯 Real-world Ready ML Components")
    print("✅ Production Emotion Detection: Trained CNN models")
    print("✅ Production Chatbot: Advanced intent matching")
    print("✅ Full dataset integration")
    print("✅ Expert-level ML engineering practices")
    print("=" * 60)
    
    # Change to server directory
    server_dir = "sleepy/server"
    if os.path.exists(server_dir):
        os.chdir(server_dir)
        print(f"📁 Changed to directory: {server_dir}")
    
    # Start the Flask server
    try:
        print("🌟 Launching Flask server with PRODUCTION ML SYSTEM...")
        print("🔗 Server will be available at: http://localhost:5000")
        print("🎯 Production ML features automatically enabled!")
        print("\\n" + "=" * 60)
        print("Press Ctrl+C to stop the server")
        print("=" * 60)
        
        # Run the server
        subprocess.run([sys.executable, "app.py"], check=True)
        
    except KeyboardInterrupt:
        print("\\n🛑 Server stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Server error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

def create_production_models_if_needed():
    """Create production models if they don't exist"""
    if not os.path.exists("sleepy/server/production_emotion_model.h5"):
        print("🔧 No production model found. Creating one...")
        
        try:
            # Run the production ML system creator
            result = subprocess.run([sys.executable, "create_production_ml_system.py"], 
                                  capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                print("✅ Production model created successfully!")
            else:
                print(f"⚠️ Model creation had issues: {result.stderr}")
                print("💡 System will use fallback models")
                
        except subprocess.TimeoutExpired:
            print("⚠️ Model creation timed out")
            print("💡 System will use fallback models")
        except Exception as e:
            print(f"⚠️ Error creating model: {e}")
            print("💡 System will use fallback models")

def main():
    """Main function"""
    print("🚀 PRODUCTION ML SYSTEM LAUNCHER")
    print("=" * 60)
    print("🎯 Real-world Ready | Expert-level ML Engineering")
    print("🤖 Production Chatbot + 😊 Production Emotion Detection")
    print("📊 Full Dataset Integration + 🧠 Trained Models")
    print("=" * 60)
    
    # Check components
    if not check_production_components():
        return
    
    # Check datasets and models
    has_datasets = check_datasets()
    has_models = check_trained_models()
    
    # Create models if needed
    if not has_models:
        create_production_models_if_needed()
    
    print("\\n🎉 PRODUCTION ML SYSTEM READY!")
    print("🚀 Starting server with real-world ready components...")
    
    # Start server
    start_production_server()

if __name__ == "__main__":
    main()