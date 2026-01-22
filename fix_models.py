#!/usr/bin/env python3
"""
Fix Model Compatibility Issues
Removes problematic model files and recreates them
"""

import os
import sys

def fix_models():
    """Remove problematic model files to force recreation"""
    print("🔧 Fixing model compatibility issues...")
    
    # List of potentially problematic model files
    model_files = [
        'server/advanced_emotion_model.h5',
        'server/advanced_emotion_model_fer2013.h5'
    ]
    
    removed_count = 0
    
    for model_file in model_files:
        if os.path.exists(model_file):
            try:
                os.remove(model_file)
                print(f"✅ Removed: {model_file}")
                removed_count += 1
            except Exception as e:
                print(f"❌ Could not remove {model_file}: {e}")
        else:
            print(f"ℹ️  File not found: {model_file}")
    
    print(f"\n🎯 Summary:")
    print(f"   Removed {removed_count} model files")
    print(f"   Models will be recreated on next run")
    
    print(f"\n📝 Next Steps:")
    print(f"1. Run: python server/advanced_emotion_detection.py")
    print(f"2. Or run: python server/app.py")
    print(f"3. Models will be automatically recreated")
    
    return True

if __name__ == "__main__":
    success = fix_models()
    sys.exit(0 if success else 1)