#!/usr/bin/env python3
"""
=============================================================================
EMOTION DETECTION MODEL TRAINING - NEPALI EXPLANATION
=============================================================================

Yo file ma emotion detection model kasto train gareko cha tyo detail ma 
explain gareko cha Nepali ma.

PROJECT: AuraBot Chatbot - Emotion Detection System
DATASET: FER-2013 (Facial Expression Recognition 2013)
MODEL TYPE: CNN (Convolutional Neural Network)
=============================================================================
"""

# ============================================================================
# STEP 1: LIBRARIES IMPORT (Jaruri libraries haru import garne)
# ============================================================================

import numpy as np              # Mathematical operations ko lagi
import pandas as pd             # CSV data read garna ko lagi
import tensorflow as tf         # Deep learning framework
from tensorflow.keras.models import Sequential  # Model banauney
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Dense, Dropout, Flatten, BatchNormalization
from tensorflow.keras.optimizers import Adam    # Optimizer
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from tensorflow.keras.utils import to_categorical  # Labels lai categorical banauney
from sklearn.model_selection import train_test_split  # Data split garna
from sklearn.metrics import classification_report, confusion_matrix  # Evaluation
import matplotlib.pyplot as plt  # Graphs banauney
import pickle                    # Data save garna
import json                      # Metadata save garna
from datetime import datetime    # Timestamp ko lagi


# ============================================================================
# STEP 2: DATASET PREPARATION (Data tayar garne)
# ============================================================================

"""
FER-2013 DATASET KO BARE MA:
----------------------------
- Total Images: 35,887 grayscale images
- Image Size: 48x48 pixels (sano size, fast processing ko lagi)
- Emotions: 7 types
  1. angry (risaeko)
  2. disgust (ghrina)
  3. fear (dar)
  4. happy (khusi)
  5. neutral (normal)
  6. sad (dukhi)
  7. surprise (acharya)

- Format: CSV file ma pixels ko values stored cha
- Each row: ek image ko 2304 pixel values (48x48 = 2304)
"""

def load_fer2013_dataset():
    """
    FER-2013 dataset load garne function
    
    KE HUNCHA:
    1. CSV file bata data read garcha
    2. Pixels lai image format ma convert garcha
    3. Labels (emotions) lai numbers ma map garcha
    """
    
    # CSV file path
    dataset_path = 'emotion_datasets/fer2013/fer2013_enhanced.csv'
    
    # CSV load garne
    df = pd.read_csv(dataset_path)
    print(f"✅ Dataset loaded: {len(df)} images")
    
    # Emotion mapping (text lai number ma convert garne)
    emotions = ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']
    emotion_mapping = {emotion: idx for idx, emotion in enumerate(emotions)}
    
    return df, emotions, emotion_mapping


# ============================================================================
# STEP 3: DATA PREPROCESSING (Data lai clean ra ready banauney)
# ============================================================================

def preprocess_data(df, emotion_mapping):
    """
    Data lai model ko lagi tayar garne
    
    PREPROCESSING STEPS:
    1. Pixel string lai array ma convert garne
    2. 48x48 shape ma reshape garne
    3. Normalize garne (0-255 lai 0-1 ma convert)
    4. Labels lai categorical format ma convert garne
    """
    
    pixels = []
    labels = []
    
    # Har ek row (image) ko lagi
    for idx, row in df.iterrows():
        # Pixel string lai list ma convert
        # Example: "0 1 2 3..." -> [0, 1, 2, 3, ...]
        pixel_values = [int(p) for p in str(row['pixels']).split()]
        
        # 48x48 array ma reshape
        pixel_array = np.array(pixel_values).reshape(48, 48)
        pixels.append(pixel_array)
        
        # Emotion label
        labels.append(row['emotion'])
    
    # NumPy arrays ma convert
    X = np.array(pixels, dtype='float32')
    y = np.array([emotion_mapping[emotion] for emotion in labels])
    
    # NORMALIZATION: 0-255 pixel values lai 0-1 ma convert
    # Kina? Neural networks lai small values ramro lagcha
    X = X / 255.0
    
    # CNN ko lagi shape: (samples, height, width, channels)
    # Grayscale image ho so channel = 1
    X = X.reshape(-1, 48, 48, 1)
    
    # Labels lai one-hot encoding ma convert
    # Example: 3 -> [0, 0, 0, 1, 0, 0, 0] (happy emotion)
    y = to_categorical(y, num_classes=7)
    
    print(f"✅ Data preprocessed: {X.shape}")
    return X, y


# ============================================================================
# STEP 4: DATA SPLITTING (Train, Validation, Test ma divide garne)
# ============================================================================

def split_data(X, y):
    """
    Data lai 3 parts ma divide garne:
    
    1. TRAINING SET (70%): Model lai train garna use huncha
    2. VALIDATION SET (15%): Training time ma performance check garna
    3. TEST SET (15%): Final evaluation ko lagi
    
    Kina split garne?
    - Training data ma model sikcha
    - Validation data le training time ma guide garcha
    - Test data le final accuracy measure garcha
    """
    
    # Pehila 70% train, 30% temp
    X_train, X_temp, y_train, y_temp = train_test_split(
        X, y, test_size=0.3, random_state=42
    )
    
    # Temp lai 50-50 validation ra test ma divide
    X_val, X_test, y_val, y_test = train_test_split(
        X_temp, y_temp, test_size=0.5, random_state=42
    )
    
    print(f"Training samples: {len(X_train)}")
    print(f"Validation samples: {len(X_val)}")
    print(f"Test samples: {len(X_test)}")
    
    return (X_train, y_train), (X_val, y_val), (X_test, y_test)


# ============================================================================
# STEP 5: CNN MODEL ARCHITECTURE (Model ko structure banauney)
# ============================================================================

def create_cnn_model():
    """
    CNN (Convolutional Neural Network) model banauney
    
    CNN KO LAYERS:
    --------------
    1. CONVOLUTIONAL LAYERS: Image bata features extract garcha
       - Edges, shapes, patterns detect garcha
       
    2. POOLING LAYERS: Image size reduce garcha
       - Computation fast banaucha
       
    3. DROPOUT LAYERS: Overfitting rokcha
       - Random neurons lai temporarily off garcha
       
    4. DENSE LAYERS: Final classification garcha
       - Extracted features bata emotion predict garcha
    
    MODEL ARCHITECTURE:
    -------------------
    """
    
    model = Sequential([
        
        # ===== BLOCK 1: First Convolutional Block =====
        # 32 filters le basic features detect garcha (edges, lines)
        Conv2D(32, (3, 3), activation='relu', input_shape=(48, 48, 1)),
        BatchNormalization(),  # Training stable banaucha
        Conv2D(32, (3, 3), activation='relu'),
        MaxPooling2D(pool_size=(2, 2)),  # Size reduce: 48x48 -> 24x24
        Dropout(0.25),  # 25% neurons randomly off (overfitting rokney)
        
        # ===== BLOCK 2: Second Convolutional Block =====
        # 64 filters le complex features detect garcha (nose, eyes)
        Conv2D(64, (3, 3), activation='relu'),
        BatchNormalization(),
        Conv2D(64, (3, 3), activation='relu'),
        MaxPooling2D(pool_size=(2, 2)),  # Size reduce: 24x24 -> 12x12
        Dropout(0.25),
        
        # ===== BLOCK 3: Third Convolutional Block =====
        # 128 filters le high-level features detect garcha (facial expressions)
        Conv2D(128, (3, 3), activation='relu'),
        BatchNormalization(),
        Dropout(0.25),
        
        # ===== FLATTEN =====
        # 2D feature maps lai 1D vector ma convert garcha
        Flatten(),
        
        # ===== DENSE LAYERS: Classification =====
        # 512 neurons - complex patterns learn garcha
        Dense(512, activation='relu'),
        BatchNormalization(),
        Dropout(0.5),  # 50% dropout (overfitting strongly prevent)
        
        # 256 neurons - refined features
        Dense(256, activation='relu'),
        Dropout(0.5),
        
        # ===== OUTPUT LAYER =====
        # 7 neurons - 7 emotions ko lagi
        # Softmax: probability distribution dincha (sum = 1)
        Dense(7, activation='softmax')
    ])
    
    # ===== MODEL COMPILATION =====
    model.compile(
        # Adam optimizer: adaptive learning rate use garcha
        optimizer=Adam(learning_rate=0.001),
        
        # Categorical crossentropy: multi-class classification ko lagi
        loss='categorical_crossentropy',
        
        # Accuracy metric: performance measure garna
        metrics=['accuracy']
    )
    
    print("✅ CNN Model created!")
    print(f"Total parameters: {model.count_params():,}")
    
    return model


# ============================================================================
# STEP 6: TRAINING CALLBACKS (Training control garne tools)
# ============================================================================

def setup_callbacks(model_name):
    """
    Training callbacks setup garne
    
    CALLBACKS KE HUN?
    -----------------
    Training process lai control garne tools
    """
    
    callbacks = [
        # 1. EARLY STOPPING
        # Kina: Validation accuracy improve na bhaye training stop garcha
        # Benefit: Time save huncha, overfitting rokcha
        EarlyStopping(
            monitor='val_accuracy',  # Validation accuracy hercha
            patience=10,  # 10 epochs samma wait garcha
            restore_best_weights=True,  # Best weights restore garcha
            verbose=1
        ),
        
        # 2. MODEL CHECKPOINT
        # Kina: Best performing model save garcha
        # Benefit: Training crash bhaye pani best model bachcha
        ModelCheckpoint(
            filepath=f'{model_name}_best.h5',
            monitor='val_accuracy',
            save_best_only=True,  # Best model matra save garcha
            verbose=1
        )
    ]
    
    return callbacks


# ============================================================================
# STEP 7: MODEL TRAINING (Model lai train garne)
# ============================================================================

def train_model(model, train_data, val_data, epochs=50, batch_size=32):
    """
    Model training process
    
    TRAINING PROCESS:
    -----------------
    1. Model le training images hercha
    2. Predictions banaucha
    3. Error calculate garcha (loss)
    4. Weights update garcha (backpropagation)
    5. Process repeat huncha
    
    HYPERPARAMETERS:
    ----------------
    - EPOCHS: Pura dataset kitna choti herney (50 times)
    - BATCH SIZE: Ek choti ma kitna images process garne (32 images)
    - LEARNING RATE: Weights kitna fast update garne (0.001)
    """
    
    X_train, y_train = train_data
    X_val, y_val = val_data
    
    # Model name with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    model_name = f"fer2013_emotion_model_{timestamp}"
    
    # Callbacks setup
    callbacks = setup_callbacks(model_name)
    
    print("🚀 Starting training...")
    print(f"Training samples: {len(X_train):,}")
    print(f"Validation samples: {len(X_val):,}")
    print(f"Batch size: {batch_size}")
    print(f"Max epochs: {epochs}")
    
    # TRAINING START
    history = model.fit(
        X_train, y_train,
        batch_size=batch_size,
        epochs=epochs,
        validation_data=(X_val, y_val),
        callbacks=callbacks,
        verbose=1  # Progress bar dekhaucha
    )
    
    print("✅ Training completed!")
    return history, model_name


# ============================================================================
# STEP 8: MODEL EVALUATION (Model ko performance check garne)
# ============================================================================

def evaluate_model(model, test_data, emotions):
    """
    Test data ma model evaluate garne
    
    EVALUATION METRICS:
    -------------------
    1. ACCURACY: Kitna correct predictions (overall)
    2. PRECISION: Predicted positive ma kitna actually positive
    3. RECALL: Actual positive ma kitna correctly detected
    4. F1-SCORE: Precision ra recall ko balance
    5. CONFUSION MATRIX: Kun emotion kun ma confused huncha
    """
    
    X_test, y_test = test_data
    
    # Test accuracy calculate
    test_loss, test_accuracy = model.evaluate(X_test, y_test, verbose=0)
    
    print(f"\n📊 TEST RESULTS:")
    print(f"Test Accuracy: {test_accuracy*100:.2f}%")
    print(f"Test Loss: {test_loss:.4f}")
    
    # Predictions banauney
    y_pred = model.predict(X_test, verbose=0)
    y_pred_classes = np.argmax(y_pred, axis=1)
    y_true_classes = np.argmax(y_test, axis=1)
    
    # Classification report
    print("\n📋 CLASSIFICATION REPORT:")
    print("(Har ek emotion ko lagi detailed metrics)")
    report = classification_report(
        y_true_classes, 
        y_pred_classes,
        target_names=emotions,
        digits=4
    )
    print(report)
    
    # Confusion matrix
    cm = confusion_matrix(y_true_classes, y_pred_classes)
    print("\n🔍 CONFUSION MATRIX:")
    print("(Kun emotion kun ma confused huncha)")
    print(cm)
    
    return test_accuracy, test_loss


# ============================================================================
# STEP 9: MODEL SAVING (Trained model save garne)
# ============================================================================

def save_model(model, model_name, test_accuracy, emotions):
    """
    Trained model ra metadata save garne
    
    SAVE HUNE FILES:
    ----------------
    1. .h5 file: Complete trained model
    2. .json file: Model metadata (accuracy, date, etc.)
    3. .pkl file: Emotion mapping
    """
    
    # Model save
    model_path = f'{model_name}_final.h5'
    model.save(model_path)
    print(f"✅ Model saved: {model_path}")
    
    # Server directory ma pani copy (direct use ko lagi)
    server_path = 'server/emotion_model.h5'
    model.save(server_path)
    print(f"✅ Server model saved: {server_path}")
    
    # Metadata save
    metadata = {
        'model_name': model_name,
        'dataset': 'FER-2013',
        'emotions': emotions,
        'num_classes': len(emotions),
        'image_size': 48,
        'test_accuracy': float(test_accuracy),
        'training_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'framework': 'TensorFlow/Keras'
    }
    
    metadata_path = f'{model_name}_metadata.json'
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=2)
    print(f"✅ Metadata saved: {metadata_path}")
    
    return model_path


# ============================================================================
# STEP 10: COMPLETE TRAINING PIPELINE
# ============================================================================

def complete_training_pipeline():
    """
    Complete training process - sabai steps ek saath
    
    PIPELINE STEPS:
    ---------------
    1. Load dataset
    2. Preprocess data
    3. Split data
    4. Create model
    5. Train model
    6. Evaluate model
    7. Save model
    """
    
    print("=" * 70)
    print("🎯 EMOTION DETECTION MODEL TRAINING - COMPLETE PIPELINE")
    print("=" * 70)
    
    # Step 1: Load dataset
    print("\n📊 STEP 1: Loading FER-2013 Dataset...")
    df, emotions, emotion_mapping = load_fer2013_dataset()
    
    # Step 2: Preprocess
    print("\n🔧 STEP 2: Preprocessing data...")
    X, y = preprocess_data(df, emotion_mapping)
    
    # Step 3: Split data
    print("\n✂️ STEP 3: Splitting data...")
    train_data, val_data, test_data = split_data(X, y)
    
    # Step 4: Create model
    print("\n🏗️ STEP 4: Creating CNN model...")
    model = create_cnn_model()
    model.summary()
    
    # Step 5: Train model
    print("\n🚀 STEP 5: Training model...")
    history, model_name = train_model(model, train_data, val_data, epochs=50)
    
    # Step 6: Evaluate
    print("\n🧪 STEP 6: Evaluating model...")
    test_accuracy, test_loss = evaluate_model(model, test_data, emotions)
    
    # Step 7: Save model
    print("\n💾 STEP 7: Saving model...")
    model_path = save_model(model, model_name, test_accuracy, emotions)
    
    # Final summary
    print("\n" + "=" * 70)
    print("🎉 TRAINING COMPLETED SUCCESSFULLY!")
    print("=" * 70)
    print(f"✅ Final Test Accuracy: {test_accuracy*100:.2f}%")
    print(f"✅ Model saved: {model_path}")
    print(f"✅ Ready for deployment in AuraBot!")
    print("\n💡 Next Steps:")
    print("1. Model server/emotion_model.h5 ma save bhayo")
    print("2. Server restart gara")
    print("3. Emotion detection test gara")
    print("=" * 70)


# ============================================================================
# KEY CONCEPTS SUMMARY (Mukhya concepts ko summary)
# ============================================================================

"""
🎓 MACHINE LEARNING CONCEPTS USED:
===================================

1. CNN (Convolutional Neural Network):
   - Image recognition ko lagi best architecture
   - Automatically features extract garcha
   - Hierarchical learning: simple -> complex features

2. SUPERVISED LEARNING:
   - Labeled data use garcha (image + emotion label)
   - Model le examples bata sikcha

3. BACKPROPAGATION:
   - Error calculate garera weights update garcha
   - Gradient descent algorithm use garcha

4. REGULARIZATION:
   - Dropout: Overfitting rokcha
   - BatchNormalization: Training stable banaucha

5. OPTIMIZATION:
   - Adam optimizer: Adaptive learning rate
   - Automatically learning rate adjust garcha

6. EVALUATION:
   - Train/Val/Test split: Proper evaluation ko lagi
   - Multiple metrics: Accuracy, Precision, Recall, F1

📊 TRAINING RESULTS:
====================
- Dataset: FER-2013 (35,887 images)
- Emotions: 7 types
- Model: CNN with 3 conv blocks
- Training time: ~2-3 hours (GPU ma)
- Expected accuracy: 60-70%
- Model size: ~10-15 MB

🚀 DEPLOYMENT:
==============
- Trained model: server/emotion_model.h5
- Used in: emotion-detection.html
- Real-time detection: Webcam bata
- Response time: <100ms per image

💡 IMPROVEMENTS POSSIBLE:
=========================
1. More data: Accuracy increase
2. Data augmentation: Rotation, flip, zoom
3. Transfer learning: Pre-trained models use
4. Ensemble methods: Multiple models combine
5. Hyperparameter tuning: Better parameters find

"""


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    """
    Yo script run garda complete training pipeline execute huncha
    
    COMMAND: python MODEL_TRAINING_EXPLAINED_NEPALI.py
    """
    complete_training_pipeline()


"""
=============================================================================
📚 ADDITIONAL RESOURCES:
=============================================================================

1. FER-2013 Dataset:
   - Paper: "Challenges in Representation Learning: Facial Expression Recognition Challenge"
   - Kaggle: https://www.kaggle.com/c/challenges-in-representation-learning-facial-expression-recognition-challenge

2. CNN Architecture:
   - LeNet, AlexNet, VGGNet concepts use gareko
   - Modern architecture: ResNet, EfficientNet pani use garna sakincha

3. TensorFlow/Keras:
   - Official docs: https://www.tensorflow.org/
   - Keras guide: https://keras.io/

4. Emotion Recognition:
   - Facial Action Coding System (FACS)
   - Ekman's 7 basic emotions

=============================================================================
🎯 YO FILE KO PURPOSE:
=============================================================================

Yo file le AuraBot chatbot ko emotion detection model kasto train gareko cha
tyo detail ma Nepali ma explain gareko cha. Har ek step, concept, ra code
ko meaning clearly bujhaeko cha.

Model training ko complete process - data loading dekhi model saving samma -
sabai kura yo file ma documented cha.

=============================================================================
"""
