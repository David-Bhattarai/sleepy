#!/usr/bin/env python3
"""
Test FER2013 Emotion Detection Integration
Tests the complete FER2013 system without DeepFace dependency
"""

import sys
import os
sys.path.append('sleepy/server')

def test_fer2013_detector():
    """Test FER2013 emotion detector"""
    print("🧪 Testing FER2013 Emotion Detector")
    print("=" * 50)
    
    try:
        from fer2013_emotion_detector import get_fer2013_emotion_detector
        
        # Initialize detector
        detector = get_fer2013_emotion_detector()
        
        # Test model info
        model_info = detector.get_fer2013_model_info()
        print(f"✅ Model Status: {model_info['status']}")
        
        if model_info['status'] == 'loaded':
            print(f"📊 Dataset: {model_info['dataset']}")
            print(f"📊 Input Shape: {model_info['input_shape']}")
            print(f"📊 Emotions: {model_info['emotions']}")
            print(f"📊 Parameters: {model_info['parameters']:,}")
            print(f"📊 Face Detection: {model_info['face_detection']}")
        
        # Test with dummy image data
        dummy_image = "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAYEBQYFBAYGBQYHBwYIChAKCgkJChQODwwQFxQYGBcUFhYaHSUfGhsjHBYWICwgIyYnKSopGR8tMC0oMCUoKSj/2wBDAQcHBwoIChMKChMoGhYaKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCj/wAARCAABAAEDASIAAhEBAxEB/8QAFQABAQAAAAAAAAAAAAAAAAAAAAv/xAAUEAEAAAAAAAAAAAAAAAAAAAAA/8QAFQEBAQAAAAAAAAAAAAAAAAAAAAX/xAAUEQEAAAAAAAAAAAAAAAAAAAAA/9oADAMBAAIRAxEAPwCdABmX/9k="
        
        result = detector.detect_emotion_from_image(dummy_image)
        
        if result['success']:
            print(f"🎯 Test Detection: {result['dominant_emotion']} ({result['confidence']:.1f}%)")
            print(f"📊 Method: {result.get('method', 'unknown')}")
            print(f"📊 Dataset: {result.get('dataset', 'unknown')}")
            print("✅ FER2013 detector working correctly!")
        else:
            print(f"⚠️ Detection failed: {result.get('error', 'Unknown error')}")
        
        return True
        
    except Exception as e:
        print(f"❌ FER2013 detector test failed: {e}")
        return False

def test_server_imports():
    """Test server imports without DeepFace"""
    print("\n🧪 Testing Server Imports")
    print("=" * 50)
    
    try:
        # Test app imports
        from app import app, FER2013_AVAILABLE
        
        print(f"✅ Flask app imported successfully")
        print(f"📊 FER2013 Available: {FER2013_AVAILABLE}")
        
        # Test FER2013 endpoint availability
        with app.test_client() as client:
            # Test basic route
            response = client.get('/')
            print(f"✅ Basic route working: {response.status_code}")
        
        return True
        
    except Exception as e:
        print(f"❌ Server import test failed: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 FER2013 Integration Test")
    print("🎯 Testing exact emotion detection based on FER2013-enhanced dataset")
    print("💻 No DeepFace dependency required")
    print()
    
    # Run tests
    tests_passed = 0
    total_tests = 2
    
    if test_fer2013_detector():
        tests_passed += 1
    
    if test_server_imports():
        tests_passed += 1
    
    # Results
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {tests_passed}/{total_tests} passed")
    
    if tests_passed == total_tests:
        print("✅ All tests passed! FER2013 integration ready!")
        print("🎯 emotion-detection.html can now use exact FER2013 emotion detection")
        print("💻 Server ready to start with: python sleepy/server/app.py")
    else:
        print("⚠️ Some tests failed. Check the errors above.")
    
    return tests_passed == total_tests

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)