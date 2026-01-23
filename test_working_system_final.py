#!/usr/bin/env python3
"""
Test Working System Final
Test the actual working components
"""

import os
import sys
import base64
from PIL import Image
import io

# Add server directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'sleepy', 'server'))

def test_working_emotion_detector():
    """Test the working emotion detector"""
    print("Testing Working Emotion Detector...")
    
    try:
        from simple_working_detector import get_simple_working_detector
        detector = get_simple_working_detector()
        
        # Create test image
        test_image = Image.new('L', (48, 48), color=128)
        buffer = io.BytesIO()
        test_image.save(buffer, format='PNG')
        image_data = base64.b64encode(buffer.getvalue()).decode()
        image_data = f"data:image/png;base64,{image_data}"
        
        # Test detection
        result = detector.detect_emotion_from_image(image_data)
        
        print(f"SUCCESS: {result['dominant_emotion']} ({result['confidence']:.1f}%)")
        print(f"Method: {result['method']}")
        
        return True
        
    except Exception as e:
        print(f"FAILED: {e}")
        return False

def test_working_chatbot():
    """Test the working chatbot"""
    print("\nTesting Working Chatbot...")
    
    try:
        from simple_working_chatbot import get_simple_working_chatbot
        chatbot = get_simple_working_chatbot()
        
        # Test messages
        test_messages = [
            "Hello, how are you?",
            "I feel sad today",
            "I'm happy",
            "Thank you"
        ]
        
        for message in test_messages:
            response = chatbot.generate_response(message)
            print(f"'{message}' -> '{response[:50]}...'")
        
        return True
        
    except Exception as e:
        print(f"FAILED: {e}")
        return False

def main():
    """Main test"""
    print("TESTING WORKING SYSTEM")
    print("=" * 40)
    
    # Set environment
    os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
    
    # Test components
    emotion_working = test_working_emotion_detector()
    chatbot_working = test_working_chatbot()
    
    print("\n" + "=" * 40)
    print("RESULTS:")
    print(f"Emotion Detection: {'WORKING' if emotion_working else 'FAILED'}")
    print(f"Chatbot: {'WORKING' if chatbot_working else 'FAILED'}")
    
    if emotion_working and chatbot_working:
        print("\nSUCCESS! System is working!")
        print("Start server: python sleepy/server/app.py")
        print("Test at: http://127.0.0.1:5000")
    else:
        print("\nSome components failed - check errors above")

if __name__ == "__main__":
    main()