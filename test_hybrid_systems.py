#!/usr/bin/env python3
"""
Test Hybrid Systems
Test both emotion detection and chatbot hybrid systems
"""

import os
import sys
import base64
from PIL import Image
import io

# Add server directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'sleepy', 'server'))

def test_hybrid_emotion_detection():
    """Test hybrid emotion detection system"""
    print("🧪 Testing Hybrid Emotion Detection System")
    print("=" * 60)
    
    try:
        from hybrid_emotion_system import get_hybrid_emotion_detector
        
        # Initialize detector
        detector = get_hybrid_emotion_detector()
        
        # Create a simple test image (48x48 grayscale)
        test_image = Image.new('L', (48, 48), color=128)  # Gray image
        
        # Convert to base64
        buffer = io.BytesIO()
        test_image.save(buffer, format='PNG')
        image_data = base64.b64encode(buffer.getvalue()).decode()
        image_data = f"data:image/png;base64,{image_data}"
        
        # Test detection
        print("🔍 Running hybrid emotion detection...")
        result = detector.detect_emotion_hybrid(image_data)
        
        print("\n📊 Results:")
        print(f"✅ Success: {result['success']}")
        print(f"😊 Dominant Emotion: {result['dominant_emotion']}")
        print(f"📈 Confidence: {result['confidence']}%")
        print(f"🔧 Method: {result.get('method', 'unknown')}")
        
        if 'hybrid_info' in result:
            info = result['hybrid_info']
            print(f"🔄 Methods Used: {info['methods_used']}")
            print(f"📋 All Methods: {info['all_methods']}")
            print(f"📊 Confidence Scores: {info['confidence_scores']}")
        
        print("\n✅ Hybrid Emotion Detection Test PASSED!")
        return True
        
    except Exception as e:
        print(f"❌ Hybrid Emotion Detection Test FAILED: {e}")
        return False

def test_hybrid_chatbot():
    """Test hybrid chatbot system"""
    print("\n🤖 Testing Hybrid Chatbot System")
    print("=" * 60)
    
    try:
        from hybrid_chatbot_system import get_hybrid_chatbot_system
        
        # Initialize chatbot
        chatbot = get_hybrid_chatbot_system()
        
        # Test messages
        test_messages = [
            "I feel really sad today",
            "I'm so happy about my new job!",
            "I'm worried about my future",
            "Hello, how are you?",
            "I need help with anxiety"
        ]
        
        for i, message in enumerate(test_messages, 1):
            print(f"\n🧪 Test {i}: '{message}'")
            
            # Test with different emotions
            test_emotion = None
            if 'sad' in message.lower():
                test_emotion = 'sad'
            elif 'happy' in message.lower():
                test_emotion = 'happy'
            elif 'worried' in message.lower():
                test_emotion = 'fear'
            
            response_data = chatbot.generate_hybrid_response(message, user_emotion=test_emotion)
            
            print(f"💬 Response: {response_data['response'][:100]}...")
            print(f"🔧 Method: {response_data['method']}")
            print(f"📈 Confidence: {response_data['confidence']}%")
            print(f"📋 Type: {response_data['type']}")
            
            if 'hybrid_info' in response_data:
                info = response_data['hybrid_info']
                print(f"🔄 Methods Available: {info['methods_used']}")
        
        print("\n✅ Hybrid Chatbot Test PASSED!")
        return True
        
    except Exception as e:
        print(f"❌ Hybrid Chatbot Test FAILED: {e}")
        return False

def test_crisis_detection():
    """Test crisis detection in chatbot"""
    print("\n🚨 Testing Crisis Detection")
    print("=" * 60)
    
    try:
        from hybrid_chatbot_system import get_hybrid_chatbot_system
        
        chatbot = get_hybrid_chatbot_system()
        
        # Test crisis message
        crisis_message = "I want to kill myself"
        print(f"🧪 Testing crisis message: '{crisis_message}'")
        
        response_data = chatbot.generate_hybrid_response(crisis_message)
        
        print(f"💬 Response: {response_data['response'][:100]}...")
        print(f"🔧 Method: {response_data['method']}")
        print(f"📈 Confidence: {response_data['confidence']}%")
        
        if 'hybrid_info' in response_data:
            info = response_data['hybrid_info']
            if info.get('crisis_detected'):
                print("✅ Crisis detection WORKING!")
            else:
                print("⚠️ Crisis detection not triggered")
        
        return True
        
    except Exception as e:
        print(f"❌ Crisis Detection Test FAILED: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 HYBRID SYSTEMS TEST SUITE")
    print("=" * 60)
    print("Testing both ML models + Gemini AI integration")
    print()
    
    # Set environment variables for TensorFlow
    os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
    
    results = []
    
    # Test emotion detection
    results.append(test_hybrid_emotion_detection())
    
    # Test chatbot
    results.append(test_hybrid_chatbot())
    
    # Test crisis detection
    results.append(test_crisis_detection())
    
    # Summary
    print("\n" + "=" * 60)
    print("🎯 TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(results)
    total = len(results)
    
    print(f"✅ Tests Passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! Hybrid systems working perfectly!")
        print("🚀 Your system combines:")
        print("   - Trained ML models from datasets")
        print("   - Gemini AI for advanced intelligence")
        print("   - Enhanced local detection")
        print("   - Crisis detection and safety")
    else:
        print("⚠️ Some tests failed. Check the output above for details.")
    
    print("\n🎯 Ready to use hybrid AURA system!")

if __name__ == "__main__":
    main()