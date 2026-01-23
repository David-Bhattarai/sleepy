#!/usr/bin/env python3
"""
Test Production ML System
Comprehensive testing of production-ready components
"""

import os
import sys
import base64
import json
import numpy as np
from datetime import datetime

def test_production_emotion_detector():
    """Test production emotion detector"""
    print("🧪 Testing PRODUCTION Emotion Detector...")
    
    try:
        # Add server path
        sys.path.append("sleepy/server")
        
        from production_emotion_detector import get_production_emotion_detector
        
        detector = get_production_emotion_detector()
        
        # Test model info
        model_info = detector.get_model_info()
        print(f"✅ Model Status: {model_info['status']}")
        
        if model_info['status'] == 'loaded':
            print(f"   📊 Input Shape: {model_info['input_shape']}")
            print(f"   📊 Parameters: {model_info.get('parameters', 'unknown'):,}")
            print(f"   👁️ Face Detection: {model_info['face_detection']}")
        
        # Test validation
        validation = detector.validate_model_performance()
        print(f"✅ Validation: {validation['status']}")
        
        if validation['status'] == 'validated':
            print(f"   📊 Average Confidence: {validation['average_confidence']:.1f}%")
        
        # Create a test image (base64 encoded 1x1 pixel)
        test_image = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChAI9jU77zgAAAABJRU5ErkJggg=="
        
        # Test emotion detection
        result = detector.detect_emotion_from_image(test_image)
        
        print(f"✅ Detection Result:")
        print(f"   🎯 Emotion: {result['dominant_emotion']}")
        print(f"   📊 Confidence: {result['confidence']:.1f}%")
        print(f"   🔧 Method: {result.get('method', 'unknown')}")
        print(f"   ✅ Success: {result['success']}")
        print(f"   👁️ Face Detected: {result['face_detected']}")
        
        # Verify production quality
        if result['confidence'] >= 60.0 and result['success']:
            print("🎉 PRODUCTION EMOTION DETECTOR: PASSED")
            return True
        else:
            print(f"⚠️ PRODUCTION EMOTION DETECTOR: LOW QUALITY")
            return False
            
    except Exception as e:
        print(f"❌ Production emotion detector error: {e}")
        return False

def test_production_chatbot():
    """Test production chatbot"""
    print("\\n🧪 Testing PRODUCTION Chatbot...")
    
    try:
        # Add server path
        sys.path.append("sleepy/server")
        
        from production_chatbot import get_production_chatbot
        
        chatbot = get_production_chatbot()
        
        # Test system info
        system_info = chatbot.get_system_info()
        print(f"✅ System Status: {system_info['status']}")
        print(f"   📚 Intents Loaded: {system_info['intents_loaded']}")
        print(f"   🤖 ML Model: {system_info['ml_model_available']}")
        print(f"   🚨 Crisis Detection: {system_info['crisis_detection']}")
        print(f"   💭 Cache Size: {system_info['cache_size']}")
        
        # Test messages with different emotions
        test_cases = [
            {"message": "Hello", "expected_emotion": None},
            {"message": "I am feeling very sad today", "expected_emotion": "sad"},
            {"message": "I need help with my anxiety", "expected_emotion": "fear"},
            {"message": "Good morning, I'm happy!", "expected_emotion": "happy"},
            {"message": "I'm so angry about this situation", "expected_emotion": "angry"},
            {"message": "Thank you for your help", "expected_emotion": None}
        ]
        
        all_passed = True
        
        for i, test_case in enumerate(test_cases, 1):
            message = test_case["message"]
            expected_emotion = test_case["expected_emotion"]
            
            # Test without emotion context
            response1 = chatbot.generate_response(message)
            
            # Test with emotion context
            response2 = chatbot.generate_response(message, user_emotion=expected_emotion)
            
            print(f"✅ Test {i}:")
            print(f"   📝 Input: '{message}'")
            print(f"   🤖 Response (no emotion): '{response1[:60]}...'")
            print(f"   🎭 Response (with emotion): '{response2[:60]}...'")
            
            # Verify response quality
            if (len(response1) > 10 and response1 != message and 
                len(response2) > 10 and response2 != message):
                print(f"   ✅ Quality: PASSED")
            else:
                print(f"   ⚠️ Quality: LOW")
                all_passed = False
        
        # Test conversation context
        summary = chatbot.get_conversation_summary()
        print(f"\\n✅ Conversation Summary:")
        print(f"   📊 Status: {summary['status']}")
        print(f"   💬 Total Exchanges: {summary.get('total_exchanges', 0)}")
        print(f"   🎯 Dominant Theme: {summary.get('dominant_theme', 'none')}")
        
        if all_passed:
            print("🎉 PRODUCTION CHATBOT: PASSED")
            return True
        else:
            print("⚠️ PRODUCTION CHATBOT: SOME ISSUES DETECTED")
            return False
            
    except Exception as e:
        print(f"❌ Production chatbot error: {e}")
        return False

def test_server_integration():
    """Test server integration"""
    print("\\n🧪 Testing SERVER Integration...")
    
    try:
        # Add server path
        sys.path.append("sleepy/server")
        
        # Test imports
        from production_emotion_detector import get_production_emotion_detector
        from production_chatbot import get_production_chatbot
        
        print("✅ Production imports: SUCCESS")
        
        # Check if app.py has production integration
        app_path = "sleepy/server/app.py"
        if os.path.exists(app_path):
            with open(app_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if "PRODUCTION_ML_AVAILABLE" in content:
                print("✅ App.py integration: SUCCESS")
                
                # Check for proper integration
                if ("get_production_emotion_detector" in content and 
                    "get_production_chatbot" in content):
                    print("✅ Production components integrated: SUCCESS")
                    return True
                else:
                    print("⚠️ Production components not fully integrated")
                    return False
            else:
                print("⚠️ App.py integration: MISSING")
                return False
        else:
            print("❌ App.py not found")
            return False
            
    except Exception as e:
        print(f"❌ Integration test error: {e}")
        return False

def test_dataset_integration():
    """Test dataset integration"""
    print("\\n🧪 Testing DATASET Integration...")
    
    dataset_paths = [
        "emotion_datasets/processed/fer2013_train.npz",
        "compact_emotion_dataset/processed/compact_train.npz",
        "emotion_dataset_50mb/processed/emotion_train_50mb.npz"
    ]
    
    found_datasets = 0
    total_samples = 0
    
    for dataset_path in dataset_paths:
        if os.path.exists(dataset_path):
            try:
                data = np.load(dataset_path)
                samples = len(data['X'])
                found_datasets += 1
                total_samples += samples
                
                print(f"✅ Dataset found: {dataset_path}")
                print(f"   📊 Samples: {samples:,}")
                print(f"   📐 Shape: {data['X'].shape}")
                
            except Exception as e:
                print(f"⚠️ Error loading {dataset_path}: {e}")
    
    if found_datasets > 0:
        print(f"\\n✅ Dataset Integration: SUCCESS")
        print(f"   📊 Total Datasets: {found_datasets}")
        print(f"   📊 Total Samples: {total_samples:,}")
        return True
    else:
        print(f"\\n⚠️ Dataset Integration: NO DATASETS FOUND")
        print("💡 System will use fallback models")
        return False

def test_model_integration():
    """Test model integration"""
    print("\\n🧪 Testing MODEL Integration...")
    
    model_paths = [
        "sleepy/server/production_emotion_model.h5",
        "sleepy/server/best_emotion_model.h5",
        "sleepy/server/compact_emotion_model_trained.h5",
        "sleepy/server/genuine_emotion_model_real.h5"
    ]
    
    found_models = 0
    
    for model_path in model_paths:
        if os.path.exists(model_path):
            try:
                # Get file size
                size_mb = os.path.getsize(model_path) / (1024 * 1024)
                found_models += 1
                
                print(f"✅ Model found: {model_path}")
                print(f"   📊 Size: {size_mb:.1f} MB")
                
            except Exception as e:
                print(f"⚠️ Error checking {model_path}: {e}")
    
    if found_models > 0:
        print(f"\\n✅ Model Integration: SUCCESS")
        print(f"   🤖 Total Models: {found_models}")
        return True
    else:
        print(f"\\n⚠️ Model Integration: NO MODELS FOUND")
        print("💡 System will create fallback models")
        return False

def test_frontend_integration():
    """Test frontend integration"""
    print("\\n🧪 Testing FRONTEND Integration...")
    
    frontend_files = [
        "sleepy/client/emotion-detection.html",
        "sleepy/client/emotion-detection.js",
        "sleepy/client/dashboard.html"
    ]
    
    found_files = 0
    
    for file_path in frontend_files:
        if os.path.exists(file_path):
            found_files += 1
            print(f"✅ Frontend file found: {file_path}")
            
            # Check for API integration
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if "/api/emotion_detection_advanced" in content:
                print(f"   🔗 API integration: SUCCESS")
            elif "/api/doctor_chat" in content:
                print(f"   🔗 Chat API integration: SUCCESS")
        else:
            print(f"⚠️ Frontend file missing: {file_path}")
    
    if found_files >= 2:
        print(f"\\n✅ Frontend Integration: SUCCESS")
        print(f"   📱 Files Found: {found_files}/{len(frontend_files)}")
        return True
    else:
        print(f"\\n⚠️ Frontend Integration: INCOMPLETE")
        return False

def generate_test_report(results):
    """Generate comprehensive test report"""
    print("\\n" + "=" * 60)
    print("📊 PRODUCTION ML SYSTEM TEST REPORT")
    print("=" * 60)
    
    total_tests = len(results)
    passed_tests = sum(results.values())
    
    print(f"📈 Overall Score: {passed_tests}/{total_tests} ({(passed_tests/total_tests)*100:.1f}%)")
    print()
    
    for test_name, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name}: {status}")
    
    print("\\n" + "=" * 60)
    
    if passed_tests == total_tests:
        print("🎉 ALL TESTS PASSED!")
        print("🚀 Production ML System is ready for deployment!")
        print("\\n🔥 Start with: python start_production_system.py")
    elif passed_tests >= total_tests * 0.7:
        print("⚠️ MOST TESTS PASSED")
        print("💡 System is functional but may have some limitations")
        print("\\n🔥 Start with: python start_production_system.py")
    else:
        print("❌ MULTIPLE TESTS FAILED")
        print("🔧 Please fix the issues before deployment")
        print("\\n💡 Run: python create_production_ml_system.py")
    
    print("=" * 60)

def main():
    """Main test function"""
    print("🧪 PRODUCTION ML SYSTEM TESTING")
    print("=" * 60)
    print("🎯 Testing real-world ready components")
    print("🔬 Comprehensive quality assurance")
    print("=" * 60)
    
    # Run all tests
    results = {
        "Production Emotion Detector": test_production_emotion_detector(),
        "Production Chatbot": test_production_chatbot(),
        "Server Integration": test_server_integration(),
        "Dataset Integration": test_dataset_integration(),
        "Model Integration": test_model_integration(),
        "Frontend Integration": test_frontend_integration()
    }
    
    # Generate report
    generate_test_report(results)

if __name__ == "__main__":
    main()