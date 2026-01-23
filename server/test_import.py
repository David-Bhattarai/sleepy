#!/usr/bin/env python3

print("Testing import...")

try:
    import real_emotion_detector
    print("✅ Module imported successfully")
    print("Available functions:", dir(real_emotion_detector))
    
    if hasattr(real_emotion_detector, 'get_real_emotion_detector'):
        print("✅ Function exists")
        detector = real_emotion_detector.get_real_emotion_detector()
        print("✅ Function works:", type(detector))
    else:
        print("❌ Function not found")
        
except Exception as e:
    print(f"❌ Import error: {e}")
    import traceback
    traceback.print_exc()