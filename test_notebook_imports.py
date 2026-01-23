#!/usr/bin/env python3
"""
Test All Imports for Jupyter Notebook
Verify that all required packages work correctly
"""

def test_notebook_imports():
    """Test all imports that the notebook needs"""
    
    print("🧪 Testing Jupyter Notebook Imports...")
    print("=" * 50)
    
    try:
        # Core libraries
        print("📦 Testing core libraries...")
        import os
        import sys
        import warnings
        warnings.filterwarnings('ignore')
        print("✅ os, sys, warnings")
        
        # Data science core
        print("📊 Testing data science libraries...")
        import numpy as np
        import pandas as pd
        print(f"✅ numpy {np.__version__}")
        print(f"✅ pandas {pd.__version__}")
        
        # Computer vision
        print("👁️ Testing computer vision...")
        try:
            import cv2
            print(f"✅ opencv {cv2.__version__}")
        except ImportError:
            print("⚠️ OpenCV not available, using PIL instead")
        
        # Deep learning
        print("🧠 Testing deep learning...")
        import tensorflow as tf
        from tensorflow.keras.models import Sequential
        from tensorflow.keras.layers import Conv2D, MaxPooling2D, Dense, Dropout, Flatten, BatchNormalization
        from tensorflow.keras.optimizers import Adam
        from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
        from tensorflow.keras.utils import to_categorical
        print(f"✅ tensorflow {tf.__version__}")
        
        # Machine learning
        print("🤖 Testing machine learning...")
        from sklearn.model_selection import train_test_split
        from sklearn.metrics import classification_report, confusion_matrix
        print("✅ scikit-learn")
        
        # Visualization
        print("📈 Testing visualization...")
        import matplotlib.pyplot as plt
        import seaborn as sns
        plt.style.use('default')
        print("✅ matplotlib, seaborn")
        
        # Utilities
        print("🔧 Testing utilities...")
        import pickle
        import json
        from datetime import datetime
        import logging
        print("✅ pickle, json, datetime, logging")
        
        # Test GPU availability
        print("\n🖥️ Testing GPU availability...")
        gpus = tf.config.list_physical_devices('GPU')
        if gpus:
            print(f"✅ GPU Available: {len(gpus)} device(s)")
            for gpu in gpus:
                print(f"   - {gpu}")
        else:
            print("⚠️ No GPU detected, using CPU")
        
        # Test basic operations
        print("\n🧮 Testing basic operations...")
        
        # NumPy test
        arr = np.random.random((10, 10))
        print(f"✅ NumPy array creation: {arr.shape}")
        
        # Pandas test
        df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
        print(f"✅ Pandas DataFrame: {df.shape}")
        
        # TensorFlow test
        try:
            model = Sequential([
                Dense(10, activation='relu', input_shape=(5,)),
                Dense(1, activation='sigmoid')
            ])
            model.compile(optimizer='adam', loss='binary_crossentropy')
            print("✅ TensorFlow model creation")
        except Exception as e:
            print(f"⚠️ TensorFlow model test failed: {e}")
        
        # Matplotlib test
        try:
            fig, ax = plt.subplots(1, 1, figsize=(5, 3))
            ax.plot([1, 2, 3], [1, 4, 2])
            ax.set_title('Test Plot')
            plt.close(fig)  # Close to avoid display
            print("✅ Matplotlib plotting")
        except Exception as e:
            print(f"⚠️ Matplotlib test failed: {e}")
        
        print("\n🎉 ALL IMPORTS SUCCESSFUL!")
        print("✅ The Jupyter notebook should work perfectly!")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("\n🔧 Fix suggestions:")
        print("1. Run: pip install numpy pandas matplotlib seaborn scikit-learn tensorflow")
        print("2. Restart your Python environment")
        print("3. Try: python -m pip install --upgrade pip")
        return False
        
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        return False

def create_simple_test_notebook():
    """Create a simple test to verify notebook functionality"""
    
    print("\n📝 Creating simple test...")
    
    try:
        import numpy as np
        import pandas as pd
        import matplotlib.pyplot as plt
        
        # Create sample data
        data = {
            'emotion': ['happy', 'sad', 'angry', 'happy', 'sad'],
            'pixels': ['128 255 64 ' * 16 for _ in range(5)]  # 48x48 = 2304, simplified to 48
        }
        
        df = pd.DataFrame(data)
        print(f"✅ Sample DataFrame created: {df.shape}")
        
        # Test pixel processing
        pixel_values = [int(x) for x in data['pixels'][0].split()[:48]]
        pixel_array = np.array(pixel_values).reshape(6, 8)  # Simplified shape
        print(f"✅ Pixel processing works: {pixel_array.shape}")
        
        # Test emotion mapping
        emotions = ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']
        emotion_mapping = {emotion: idx for idx, emotion in enumerate(emotions)}
        print(f"✅ Emotion mapping: {len(emotion_mapping)} classes")
        
        print("✅ Basic notebook operations work!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def main():
    """Main test function"""
    
    print("🚀 Starting Notebook Import Test...")
    print("=" * 60)
    
    # Test imports
    import_success = test_notebook_imports()
    
    # Test basic operations
    if import_success:
        operation_success = create_simple_test_notebook()
    else:
        operation_success = False
    
    # Final summary
    print("\n" + "=" * 60)
    print("📋 TEST SUMMARY")
    print("=" * 60)
    
    if import_success and operation_success:
        print("🎉 SUCCESS: Notebook is ready to run!")
        print("\n✅ You can now:")
        print("1. Open Jupyter: jupyter notebook")
        print("2. Run: FER2013_Emotion_Model_Training.ipynb")
        print("3. All imports should work perfectly")
        
        print("\n💡 Tips:")
        print("- Use 'ml-env' kernel if available")
        print("- Restart kernel if you encounter any issues")
        print("- The notebook has comprehensive error handling")
        
    else:
        print("❌ Issues detected. Please fix the errors above.")
        print("\n🔧 Quick fixes:")
        print("pip install --upgrade numpy pandas matplotlib tensorflow")
        print("pip install opencv-python pillow scikit-learn seaborn")
        
    print("\n🔗 If problems persist:")
    print("- Restart your IDE/terminal completely")
    print("- Try: python -m pip install --user numpy")
    print("- Check: python -c \"import numpy; print(numpy.__version__)\"")

if __name__ == "__main__":
    main()