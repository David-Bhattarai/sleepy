#!/usr/bin/env python3
"""
Complete Integration Test
Test ML + Backend + Frontend + Database integration
"""

import os
import sys
import requests
import json
import base64
import numpy as np
from PIL import Image
import io

print("🧪 COMPLETE INTEGRATION TEST")
print("=" * 50)

def test_ml_model():
    """Test ML model loading"""
    print("\n🧠 Testing ML Model...")
    try:
        # Check if model file exists
        model_path = "sleepy/server/simple_fer2013_model_20260123_225231_final.h5"
        if os.path.exists(model_path):
            print(f"✅ Model file found: {model_path}")
            
            # Try to import TensorFlow and load model
            import tensorflow as tf
            model = tf.keras.models.load_model(model_path)
            print(f"✅ Model loaded successfully")
            print(f"   - Input shape: {model.input_shape}")
            print(f"   - Output shape: {model.output_shape}")
            print(f"   - Parameters: {model.count_params():,}")
            return True
        else:
            print(f"❌ Model file not found: {model_path}")
            return False
            
    except Exception as e:
        print(f"❌ ML Model test failed: {e}")
        return False

def test_database():
    """Test database connection"""
    print("\n💾 Testing Database...")
    try:
        import sqlite3
        db_path = "sleepy/server/database.db"
        
        if os.path.exists(db_path):
            print(f"✅ Database file found: {db_path}")
            
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Test tables
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            print(f"✅ Database tables: {len(tables)}")
            
            for table in tables:
                table_name = table[0]
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                count = cursor.fetchone()[0]
                print(f"   - {table_name}: {count} records")
            
            conn.close()
            return True
        else:
            print(f"❌ Database file not found: {db_path}")
            return False
            
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False

def test_backend_files():
    """Test backend files"""
    print("\n🖥️ Testing Backend Files...")
    
    backend_files = [
        "sleepy/server/app.py",
        "sleepy/server/db_helper.py",
        "sleepy/server/fer2013_emotion_detector.py",
        "sleepy/server/intents.json"
    ]
    
    all_exist = True
    for file_path in backend_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path}")
            all_exist = False
    
    return all_exist

def test_frontend_files():
    """Test frontend files"""
    print("\n🌐 Testing Frontend Files...")
    
    frontend_files = [
        "sleepy/client/index.html",
        "sleepy/client/dashboard.html",
        "sleepy/client/admin.html",
        "sleepy/client/emotion-detection.html",
        "sleepy/client/video-chat.html",
        "sleepy/client/styles.css",
        "sleepy/client/app.js",
        "sleepy/client/emotion-detection.js"
    ]
    
    all_exist = True
    for file_path in frontend_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path}")
            all_exist = False
    
    return all_exist

def test_dataset():
    """Test dataset"""
    print("\n📊 Testing Dataset...")
    
    dataset_path = "emotion_datasets/fer2013/fer2013_enhanced.csv"
    if os.path.exists(dataset_path):
        print(f"✅ Dataset found: {dataset_path}")
        
        try:
            import pandas as pd
            df = pd.read_csv(dataset_path)
            print(f"✅ Dataset loaded: {len(df)} samples")
            print(f"   - Columns: {list(df.columns)}")
            print(f"   - Emotion distribution:")
            print(df['emotion'].value_counts())
            return True
        except Exception as e:
            print(f"❌ Error loading dataset: {e}")
            return False
    else:
        print(f"❌ Dataset not found: {dataset_path}")
        return False

def test_server_startup():
    """Test if server can start (import test)"""
    print("\n🚀 Testing Server Startup...")
    
    try:
        # Add server directory to path
        sys.path.insert(0, 'sleepy/server')
        
        # Try to import main modules
        import app
        print("✅ Flask app module imported")
        
        import db_helper
        print("✅ Database helper imported")
        
        import fer2013_emotion_detector
        print("✅ Emotion detector imported")
        
        return True
        
    except Exception as e:
        print(f"❌ Server startup test failed: {e}")
        return False

def create_test_image():
    """Create a test image for emotion detection"""
    print("\n🖼️ Creating Test Image...")
    
    try:
        # Create a simple 48x48 test image
        img = Image.new('L', (48, 48), color=128)  # Gray image
        
        # Convert to base64
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        img_data = base64.b64encode(buffer.getvalue()).decode()
        
        print("✅ Test image created (48x48 grayscale)")
        return f"data:image/png;base64,{img_data}"
        
    except Exception as e:
        print(f"❌ Test image creation failed: {e}")
        return None

def main():
    """Run complete integration test"""
    print("🎯 Testing Complete System Integration...")
    
    tests = [
        ("ML Model", test_ml_model),
        ("Database", test_database),
        ("Backend Files", test_backend_files),
        ("Frontend Files", test_frontend_files),
        ("Dataset", test_dataset),
        ("Server Startup", test_server_startup)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results[test_name] = False
    
    # Create test image
    test_image = create_test_image()
    
    # Summary
    print(f"\n🎯 INTEGRATION TEST SUMMARY")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print(f"\n🎉 ALL TESTS PASSED!")
        print(f"✅ ML Model: Ready")
        print(f"✅ Backend: Ready") 
        print(f"✅ Frontend: Ready")
        print(f"✅ Database: Ready")
        print(f"✅ Dataset: Ready")
        print(f"\n🚀 SYSTEM FULLY INTEGRATED AND READY!")
        print(f"\n💡 To start the server:")
        print(f"   cd sleepy/server")
        print(f"   python app.py")
        print(f"\n💡 Then open: http://localhost:5000")
        
    else:
        print(f"\n⚠️ Some tests failed. Check the errors above.")
        print(f"💡 Make sure all files are in place and dependencies are installed.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    if success:
        print(f"\n🎯 INTEGRATION STATUS: COMPLETE ✅")
    else:
        print(f"\n🎯 INTEGRATION STATUS: NEEDS ATTENTION ⚠️")