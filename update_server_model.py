#!/usr/bin/env python3
"""
Update Server to Use Compact Dataset Model
This will modify the server to use the better trained model
"""

import os
import shutil
import pickle

def update_genuine_emotion_detector():
    """Update the genuine emotion detector to use compact model"""
    print("🔄 Updating genuine emotion detector...")
    
    # Path to the genuine emotion detector
    detector_path = "sleepy/server/genuine_emotion_detector.py"
    
    # Read the current file
    with open(detector_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Update the load_or_create_model method to prioritize compact model
    updated_content = content.replace(
        "real_model_path = 'genuine_emotion_model_real.h5'",
        """# Try compact model first (best accuracy)
        compact_model_path = 'compact_emotion_model_trained.h5'
        real_model_path = 'genuine_emotion_model_real.h5'"""
    )
    
    # Update the loading logic
    updated_content = updated_content.replace(
        """try:
            if os.path.exists(real_model_path):
                print("🔄 Loading REAL trained emotion model...")
                self.model = load_model(real_model_path)
                
                # Load real emotion mapping if available
                mapping_path = 'emotion_mapping_real.pkl'
                if os.path.exists(mapping_path):
                    import pickle
                    with open(mapping_path, 'rb') as f:
                        emotion_mapping = pickle.load(f)
                        self.emotions = list(emotion_mapping.values())
                
                print("✅ REAL emotion model loaded successfully!")
                print(f"🎭 Using emotions: {self.emotions}")
                return""",
        """try:
            # First try compact model (best accuracy)
            if os.path.exists(compact_model_path):
                print("🔄 Loading COMPACT trained emotion model (BEST ACCURACY)...")
                self.model = load_model(compact_model_path)
                
                # Load compact emotion mapping
                compact_mapping_path = 'compact_emotion_mapping.pkl'
                if os.path.exists(compact_mapping_path):
                    import pickle
                    with open(compact_mapping_path, 'rb') as f:
                        emotion_mapping = pickle.load(f)
                        self.emotions = list(emotion_mapping.values())
                
                print("✅ COMPACT emotion model loaded successfully!")
                print(f"🎭 Using emotions: {self.emotions}")
                print("🎯 This model has MUCH BETTER accuracy!")
                return
                
            elif os.path.exists(real_model_path):
                print("🔄 Loading REAL trained emotion model...")
                self.model = load_model(real_model_path)
                
                # Load real emotion mapping if available
                mapping_path = 'emotion_mapping_real.pkl'
                if os.path.exists(mapping_path):
                    import pickle
                    with open(mapping_path, 'rb') as f:
                        emotion_mapping = pickle.load(f)
                        self.emotions = list(emotion_mapping.values())
                
                print("✅ REAL emotion model loaded successfully!")
                print(f"🎭 Using emotions: {self.emotions}")
                return"""
    )
    
    # Write the updated content
    with open(detector_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)
    
    print("✅ Genuine emotion detector updated!")

def copy_compact_model_to_server():
    """Copy compact model files to server directory"""
    print("🔄 Copying compact model to server...")
    
    server_dir = "sleepy/server"
    
    # Copy model file if it exists
    if os.path.exists("compact_emotion_model_best.h5"):
        shutil.copy("compact_emotion_model_best.h5", 
                   os.path.join(server_dir, "compact_emotion_model_trained.h5"))
        print("✅ Compact model copied to server")
    
    # Copy emotion mapping
    compact_mapping = "compact_emotion_dataset/processed/emotion_mapping.pkl"
    if os.path.exists(compact_mapping):
        shutil.copy(compact_mapping, 
                   os.path.join(server_dir, "compact_emotion_mapping.pkl"))
        print("✅ Compact emotion mapping copied to server")

def create_test_script():
    """Create a test script to verify the update"""
    test_content = '''#!/usr/bin/env python3
"""
Test Updated Emotion Detection
Verify that the server is using the compact model
"""

import sys
import os
sys.path.append('sleepy/server')

from genuine_emotion_detector import get_genuine_emotion_detector
import base64
from PIL import Image
import numpy as np
from io import BytesIO

def create_test_image():
    """Create a test image"""
    # Create a simple test image
    img = np.ones((200, 200, 3), dtype=np.uint8) * 128
    
    # Add simple face features for happy emotion
    # Eyes
    img[60:80, 60:80] = [0, 0, 0]  # Left eye
    img[60:80, 120:140] = [0, 0, 0]  # Right eye
    
    # Smile
    img[140:150, 80:120] = [0, 0, 0]  # Mouth
    
    # Convert to base64
    pil_img = Image.fromarray(img)
    buffer = BytesIO()
    pil_img.save(buffer, format='JPEG')
    img_str = base64.b64encode(buffer.getvalue()).decode()
    
    return f"data:image/jpeg;base64,{img_str}"

def test_updated_detector():
    """Test the updated detector"""
    print("🧪 Testing Updated Emotion Detector")
    print("=" * 50)
    
    try:
        # Get detector
        detector = get_genuine_emotion_detector()
        
        print(f"✅ Detector loaded")
        print(f"🎭 Available emotions: {detector.emotions}")
        print(f"📊 Number of emotions: {len(detector.emotions)}")
        
        # Test with image
        test_image = create_test_image()
        result = detector.detect_emotion_from_image(test_image)
        
        print(f"\\n📊 Test Results:")
        print(f"Success: {result.get('success')}")
        print(f"Dominant emotion: {result.get('dominant_emotion')}")
        print(f"Confidence: {result.get('confidence'):.2f}%")
        print(f"Model type: {result.get('model_type')}")
        
        if result.get('emotions'):
            print(f"\\n🎭 All emotions:")
            for emotion, score in result['emotions'].items():
                print(f"  {emotion}: {score:.1f}%")
        
        # Check if using compact model
        if "COMPACT" in str(result.get('model_type', '')).upper():
            print("\\n🎉 SUCCESS! Using compact model with better accuracy!")
        else:
            print("\\n⚠️ Still using old model. Make sure to train compact model first.")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_updated_detector()
'''
    
    with open("test_updated_emotion.py", 'w', encoding='utf-8') as f:
        f.write(test_content)
    
    print("✅ Test script created: test_updated_emotion.py")

def main():
    """Main update function"""
    print("🚀 Updating Server to Use Compact Model")
    print("=" * 60)
    
    # Update the detector code
    update_genuine_emotion_detector()
    
    # Copy model files
    copy_compact_model_to_server()
    
    # Create test script
    create_test_script()
    
    print("=" * 60)
    print("🎉 SERVER UPDATE COMPLETED!")
    print("✅ Server will now use compact model (better accuracy)")
    print("✅ Restart the server to apply changes")
    print("✅ Run test_updated_emotion.py to verify")

if __name__ == "__main__":
    main()