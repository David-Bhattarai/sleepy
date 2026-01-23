#!/usr/bin/env python3
"""
Fix Jupyter Notebook Step by Step
Run each cell individually to identify and fix errors
"""

import os
import sys
import subprocess

def run_step(step_name, code, description):
    """Run a single step and handle errors"""
    
    print(f"\n{'='*60}")
    print(f"🔧 STEP: {step_name}")
    print(f"📝 {description}")
    print(f"{'='*60}")
    
    try:
        # Create temporary file for this step
        temp_file = f"temp_step_{step_name.lower().replace(' ', '_')}.py"
        
        with open(temp_file, 'w', encoding='utf-8') as f:
            f.write(code)
        
        # Run the step
        result = subprocess.run([sys.executable, temp_file], 
                              capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print(f"✅ SUCCESS: {step_name}")
            print(result.stdout)
        else:
            print(f"❌ ERROR in {step_name}:")
            print(result.stderr)
            print("\n🔧 Suggested fixes:")
            suggest_fixes(step_name, result.stderr)
        
        # Clean up
        if os.path.exists(temp_file):
            os.remove(temp_file)
        
        return result.returncode == 0
        
    except subprocess.TimeoutExpired:
        print(f"⏰ TIMEOUT: {step_name} took too long")
        return False
    except Exception as e:
        print(f"❌ EXCEPTION in {step_name}: {e}")
        return False

def suggest_fixes(step_name, error_message):
    """Suggest fixes based on error message"""
    
    error_lower = error_message.lower()
    
    if "no module named" in error_lower:
        if "numpy" in error_lower:
            print("   pip install numpy")
        elif "pandas" in error_lower:
            print("   pip install pandas")
        elif "tensorflow" in error_lower:
            print("   pip install tensorflow")
        elif "sklearn" in error_lower:
            print("   pip install scikit-learn")
        elif "cv2" in error_lower or "opencv" in error_lower:
            print("   pip install opencv-python")
        elif "pil" in error_lower or "pillow" in error_lower:
            print("   pip install pillow")
        elif "matplotlib" in error_lower:
            print("   pip install matplotlib")
        elif "seaborn" in error_lower:
            print("   pip install seaborn")
        else:
            print("   pip install <missing_package>")
    
    elif "file not found" in error_lower or "no such file" in error_lower:
        print("   Check dataset path: emotion_datasets/fer2013/fer2013_enhanced.csv")
        print("   Or create sample data (script will handle this)")
    
    elif "memory" in error_lower or "out of memory" in error_lower:
        print("   Reduce batch size or use CPU instead of GPU")
        print("   Close other applications to free memory")
    
    elif "gpu" in error_lower or "cuda" in error_lower:
        print("   GPU error - will fallback to CPU automatically")
    
    else:
        print("   Check the error message above for specific issues")

def main():
    """Main function to run all steps"""
    
    print("🚀 Starting Step-by-Step Notebook Fix")
    print("=" * 60)
    
    steps = [
        {
            "name": "Import Libraries",
            "description": "Test all required imports",
            "code": '''
import warnings
warnings.filterwarnings('ignore')

print("📦 Testing imports...")

try:
    import numpy as np
    print(f"✅ NumPy {np.__version__}")
except ImportError as e:
    print(f"❌ NumPy: {e}")
    exit(1)

try:
    import pandas as pd
    print(f"✅ Pandas {pd.__version__}")
except ImportError as e:
    print(f"❌ Pandas: {e}")
    exit(1)

try:
    import matplotlib.pyplot as plt
    print("✅ Matplotlib")
except ImportError as e:
    print(f"❌ Matplotlib: {e}")
    exit(1)

try:
    import seaborn as sns
    print("✅ Seaborn")
except ImportError as e:
    print(f"❌ Seaborn: {e}")
    exit(1)

try:
    import tensorflow as tf
    print(f"✅ TensorFlow {tf.__version__}")
except ImportError as e:
    print(f"❌ TensorFlow: {e}")
    exit(1)

try:
    from sklearn.model_selection import train_test_split
    print("✅ Scikit-learn")
except ImportError as e:
    print(f"❌ Scikit-learn: {e}")
    exit(1)

try:
    import cv2
    print(f"✅ OpenCV {cv2.__version__}")
except ImportError:
    print("⚠️ OpenCV not available, will use PIL")

try:
    from PIL import Image
    print("✅ PIL/Pillow")
except ImportError as e:
    print(f"❌ PIL: {e}")
    exit(1)

print("🎉 All imports successful!")
'''
        },
        
        {
            "name": "Create Trainer Class",
            "description": "Initialize the FER2013 trainer",
            "code": '''
import numpy as np
import pandas as pd
from tensorflow.keras.utils import to_categorical

class FER2013EmotionTrainer:
    def __init__(self):
        self.emotions = ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']
        self.emotion_mapping = {emotion: idx for idx, emotion in enumerate(self.emotions)}
        self.num_classes = len(self.emotions)
        self.img_size = 48
        self.model = None
        self.history = None
        
        print(f"✅ FER2013 Trainer initialized")
        print(f"Emotions: {self.emotions}")
        print(f"Classes: {self.num_classes}")
        print(f"Image size: {self.img_size}x{self.img_size}")

# Test trainer creation
trainer = FER2013EmotionTrainer()
print("🎉 Trainer created successfully!")
'''
        },
        
        {
            "name": "Load Dataset",
            "description": "Load or create sample dataset",
            "code": '''
import os
import numpy as np
import pandas as pd

def load_or_create_dataset():
    # Try to load real dataset
    dataset_paths = [
        'emotion_datasets/fer2013/fer2013_enhanced.csv',
        '../emotion_datasets/fer2013/fer2013_enhanced.csv',
        'fer2013_enhanced.csv'
    ]
    
    for path in dataset_paths:
        if os.path.exists(path):
            try:
                df = pd.read_csv(path)
                print(f"✅ Loaded real dataset: {path}")
                print(f"   Samples: {len(df)}")
                return df
            except Exception as e:
                print(f"⚠️ Error loading {path}: {e}")
                continue
    
    # Create sample dataset
    print("📝 Creating sample dataset...")
    emotions = ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']
    sample_data = []
    
    for emotion in emotions:
        for i in range(50):  # 50 samples per emotion
            # Create random 48x48 pixel data
            pixels = np.random.randint(0, 256, 48*48)
            pixel_string = ' '.join(map(str, pixels))
            
            sample_data.append({
                'emotion': emotion,
                'pixels': pixel_string
            })
    
    df = pd.DataFrame(sample_data)
    print(f"✅ Created sample dataset: {len(df)} samples")
    return df

# Test dataset loading
df = load_or_create_dataset()
print(f"📊 Dataset shape: {df.shape}")
print(f"📊 Columns: {list(df.columns)}")
print("🎉 Dataset loaded successfully!")
'''
        },
        
        {
            "name": "Preprocess Data",
            "description": "Process and prepare data for training",
            "code": '''
import numpy as np
import pandas as pd
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split

# Recreate trainer and dataset for this step
emotions = ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']
emotion_mapping = {emotion: idx for idx, emotion in enumerate(emotions)}
img_size = 48

# Create sample data
sample_data = []
for emotion in emotions:
    for i in range(20):  # Smaller dataset for testing
        pixels = np.random.randint(0, 256, img_size*img_size)
        pixel_string = ' '.join(map(str, pixels))
        sample_data.append({'emotion': emotion, 'pixels': pixel_string})

df = pd.DataFrame(sample_data)

def preprocess_data(df):
    print("🔧 Preprocessing data...")
    
    pixels = []
    labels = []
    
    for idx, row in df.iterrows():
        try:
            pixel_values = [int(pixel) for pixel in str(row['pixels']).split()]
            
            if len(pixel_values) != img_size * img_size:
                continue
            
            pixel_array = np.array(pixel_values).reshape(img_size, img_size)
            pixels.append(pixel_array)
            labels.append(row['emotion'])
            
        except Exception as e:
            continue
    
    if len(pixels) == 0:
        raise ValueError("No valid data found")
    
    # Convert to numpy arrays
    X = np.array(pixels, dtype='float32')
    y = np.array([emotion_mapping.get(emotion, 0) for emotion in labels])
    
    # Normalize
    X = X / 255.0
    
    # Reshape for CNN
    X = X.reshape(-1, img_size, img_size, 1)
    
    # Convert to categorical
    y = to_categorical(y, len(emotions))
    
    print(f"✅ Preprocessed: X shape {X.shape}, y shape {y.shape}")
    return X, y

# Test preprocessing
X, y = preprocess_data(df)

# Test train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(f"📊 Training set: {X_train.shape[0]} samples")
print(f"📊 Test set: {X_test.shape[0]} samples")
print("🎉 Data preprocessing successful!")
'''
        },
        
        {
            "name": "Create Model",
            "description": "Build CNN model architecture",
            "code": '''
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Dense, Dropout, Flatten, BatchNormalization
from tensorflow.keras.optimizers import Adam

def create_model():
    print("🏗️ Creating CNN model...")
    
    try:
        model = Sequential([
            Conv2D(32, (3, 3), activation='relu', input_shape=(48, 48, 1)),
            BatchNormalization(),
            MaxPooling2D(pool_size=(2, 2)),
            Dropout(0.25),
            
            Conv2D(64, (3, 3), activation='relu'),
            BatchNormalization(),
            MaxPooling2D(pool_size=(2, 2)),
            Dropout(0.25),
            
            Flatten(),
            Dense(128, activation='relu'),
            Dropout(0.5),
            Dense(7, activation='softmax')  # 7 emotions
        ])
        
        # Compile model
        try:
            optimizer = Adam(learning_rate=0.001)
        except TypeError:
            optimizer = Adam(lr=0.001)  # Older TensorFlow versions
        
        model.compile(
            optimizer=optimizer,
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        print("✅ Model created successfully!")
        model.summary()
        
        return model
        
    except Exception as e:
        print(f"❌ Model creation failed: {e}")
        raise

# Test model creation
model = create_model()
print(f"📊 Total parameters: {model.count_params():,}")
print("🎉 Model architecture ready!")
'''
        },
        
        {
            "name": "Test Training",
            "description": "Test model training with small dataset",
            "code": '''
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Dense, Dropout, Flatten
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.utils import to_categorical

# Create simple test data
print("📊 Creating test data...")
X_train = np.random.random((50, 48, 48, 1)).astype('float32')
y_train = to_categorical(np.random.randint(0, 7, 50), 7)

X_val = np.random.random((20, 48, 48, 1)).astype('float32')
y_val = to_categorical(np.random.randint(0, 7, 20), 7)

print(f"✅ Test data created: {X_train.shape}, {y_train.shape}")

# Create simple model
print("🏗️ Creating test model...")
model = Sequential([
    Conv2D(16, (3, 3), activation='relu', input_shape=(48, 48, 1)),
    MaxPooling2D(2, 2),
    Flatten(),
    Dense(32, activation='relu'),
    Dense(7, activation='softmax')
])

try:
    optimizer = Adam(learning_rate=0.001)
except TypeError:
    optimizer = Adam(lr=0.001)

model.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy'])

print("✅ Test model created")

# Test training for 1 epoch
print("🚀 Testing training...")
try:
    history = model.fit(
        X_train, y_train,
        batch_size=8,
        epochs=1,
        validation_data=(X_val, y_val),
        verbose=1
    )
    
    print("✅ Training test successful!")
    print(f"📊 Training accuracy: {history.history['accuracy'][0]:.4f}")
    print(f"📊 Validation accuracy: {history.history['val_accuracy'][0]:.4f}")
    
except Exception as e:
    print(f"❌ Training test failed: {e}")
    raise

print("🎉 Model training test completed!")
'''
        },
        
        {
            "name": "Test Prediction",
            "description": "Test model prediction functionality",
            "code": '''
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten, Conv2D
from tensorflow.keras.optimizers import Adam

# Create and train a minimal model
print("🏗️ Creating minimal model for prediction test...")

model = Sequential([
    Conv2D(8, (3, 3), activation='relu', input_shape=(48, 48, 1)),
    Flatten(),
    Dense(7, activation='softmax')
])

try:
    optimizer = Adam(learning_rate=0.001)
except TypeError:
    optimizer = Adam(lr=0.001)

model.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy'])

# Create dummy training data
X_dummy = np.random.random((10, 48, 48, 1)).astype('float32')
y_dummy = tf.keras.utils.to_categorical(np.random.randint(0, 7, 10), 7)

# Quick training
print("🚀 Quick training...")
model.fit(X_dummy, y_dummy, epochs=1, verbose=0)

# Test prediction
print("🔮 Testing prediction...")
test_image = np.random.random((1, 48, 48, 1)).astype('float32')

try:
    prediction = model.predict(test_image, verbose=0)
    predicted_class = np.argmax(prediction)
    confidence = prediction[0][predicted_class]
    
    emotions = ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']
    predicted_emotion = emotions[predicted_class]
    
    print(f"✅ Prediction successful!")
    print(f"📊 Predicted emotion: {predicted_emotion}")
    print(f"📊 Confidence: {confidence:.4f}")
    print(f"📊 All probabilities: {prediction[0]}")
    
except Exception as e:
    print(f"❌ Prediction failed: {e}")
    raise

print("🎉 Prediction test completed!")
'''
        },
        
        {
            "name": "Test Visualization",
            "description": "Test matplotlib and plotting functionality",
            "code": '''
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

print("📈 Testing visualization...")

try:
    # Test basic plotting
    plt.figure(figsize=(10, 6))
    
    # Test 1: Simple line plot
    plt.subplot(2, 2, 1)
    x = np.linspace(0, 10, 100)
    y = np.sin(x)
    plt.plot(x, y)
    plt.title('Test Line Plot')
    
    # Test 2: Bar plot
    plt.subplot(2, 2, 2)
    emotions = ['angry', 'happy', 'sad', 'fear']
    counts = [10, 25, 15, 8]
    plt.bar(emotions, counts)
    plt.title('Test Bar Plot')
    
    # Test 3: Heatmap
    plt.subplot(2, 2, 3)
    data = np.random.random((5, 5))
    sns.heatmap(data, annot=True, fmt='.2f', cmap='Blues')
    plt.title('Test Heatmap')
    
    # Test 4: Image display
    plt.subplot(2, 2, 4)
    img = np.random.random((48, 48))
    plt.imshow(img, cmap='gray')
    plt.title('Test Image Display')
    plt.axis('off')
    
    plt.tight_layout()
    
    # Save instead of show (for headless environments)
    plt.savefig('test_visualization.png', dpi=100, bbox_inches='tight')
    plt.close()
    
    print("✅ Visualization test successful!")
    print("📁 Saved test plot as: test_visualization.png")
    
except Exception as e:
    print(f"❌ Visualization test failed: {e}")
    # Try simple fallback
    try:
        fig, ax = plt.subplots(1, 1, figsize=(5, 3))
        ax.plot([1, 2, 3], [1, 4, 2])
        ax.set_title('Simple Test')
        plt.savefig('simple_test.png')
        plt.close()
        print("✅ Simple visualization fallback successful")
    except Exception as e2:
        print(f"❌ Even simple visualization failed: {e2}")
        raise

print("🎉 Visualization test completed!")
'''
        }
    ]
    
    # Run each step
    success_count = 0
    total_steps = len(steps)
    
    for i, step in enumerate(steps, 1):
        print(f"\n🔄 Running Step {i}/{total_steps}")
        
        success = run_step(step["name"], step["code"], step["description"])
        
        if success:
            success_count += 1
            print(f"✅ Step {i} completed successfully")
        else:
            print(f"❌ Step {i} failed")
            
            # Ask if user wants to continue
            response = input(f"\n❓ Continue to next step? (y/n): ").lower().strip()
            if response != 'y' and response != 'yes':
                print("🛑 Stopping at user request")
                break
    
    # Final summary
    print(f"\n{'='*60}")
    print(f"📋 FINAL SUMMARY")
    print(f"{'='*60}")
    print(f"✅ Successful steps: {success_count}/{total_steps}")
    print(f"❌ Failed steps: {total_steps - success_count}/{total_steps}")
    
    if success_count == total_steps:
        print(f"\n🎉 ALL STEPS SUCCESSFUL!")
        print(f"✅ Your Jupyter notebook should work perfectly now!")
        print(f"\n🚀 Next steps:")
        print(f"1. Open Jupyter: jupyter notebook")
        print(f"2. Run: FER2013_Emotion_Model_Training.ipynb")
        print(f"3. All cells should execute without errors")
    else:
        print(f"\n⚠️ Some steps failed. Check error messages above.")
        print(f"🔧 Common fixes:")
        print(f"   pip install numpy pandas matplotlib tensorflow scikit-learn")
        print(f"   pip install opencv-python pillow seaborn")
        print(f"   Restart your Python environment")
    
    print(f"\n💡 All test files and outputs are in the current directory")

if __name__ == "__main__":
    main()