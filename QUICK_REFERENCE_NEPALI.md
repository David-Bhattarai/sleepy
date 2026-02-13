# 🚀 AuraBot Model Training - Quick Reference (Nepali)

## 📍 Main Training Files

### 1. **train_fer2013_emotion_model.py** ⭐ (MAIN FILE)
```bash
# Yo file run garera model train gareko
python train_fer2013_emotion_model.py
```

**Ke garcha:**
- FER-2013 dataset load
- CNN model banaucha
- 50 epochs train garcha
- Model save garcha: `server/emotion_model.h5`

---

### 2. **train_real_emotion_model.py** (Alternative)
```bash
python train_real_emotion_model.py
```

**Ke garcha:**
- Real FER-2013 processed data use
- Advanced CNN architecture
- Data augmentation
- Better accuracy target

---

### 3. **simple_model_trainer.py** (Simple Version)
```bash
python simple_model_trainer.py
```

**Ke garcha:**
- Simple training without complications
- Terminal ma direct run
- Quick testing ko lagi

---

## 🎯 Model Training Process (Simple Steps)

### Step 1: Dataset Load
```python
# FER-2013 CSV file bata
df = pd.read_csv('fer2013_enhanced.csv')
# 35,887 images, 7 emotions
```

### Step 2: Preprocess
```python
# Pixels normalize (0-1)
X = X / 255.0
# Reshape (48x48x1)
X = X.reshape(-1, 48, 48, 1)
# Labels one-hot encode
y = to_categorical(y, 7)
```

### Step 3: Split Data
```python
# 70% train, 15% validation, 15% test
train_test_split(X, y, test_size=0.3)
```

### Step 4: Create CNN
```python
model = Sequential([
    Conv2D(32, (3,3)),  # Features extract
    MaxPooling2D(),      # Size reduce
    Dropout(0.25),       # Overfitting prevent
    # ... more layers
    Dense(7, softmax)    # 7 emotions output
])
```

### Step 5: Train
```python
model.fit(
    X_train, y_train,
    epochs=50,
    batch_size=32,
    validation_data=(X_val, y_val)
)
```

### Step 6: Save
```python
model.save('server/emotion_model.h5')
```

---

## 🔑 Key Concepts (1-Line Explanation)

| Concept | Nepali Explanation |
|---------|-------------------|
| **CNN** | Image bata automatically features extract garne network |
| **Conv2D** | Image ma filter apply garera patterns detect garne |
| **MaxPooling** | Image size reduce garera important features retain garne |
| **Dropout** | Random neurons off garera overfitting rokney |
| **BatchNorm** | Training stable banauney normalization |
| **ReLU** | Negative values zero banauney activation |
| **Softmax** | Output lai probability ma convert garne |
| **Adam** | Learning rate automatically adjust garne optimizer |
| **Categorical Crossentropy** | Multi-class classification ko loss function |
| **Epochs** | Pura dataset kitna choti herney |
| **Batch Size** | Ek choti ma kitna images process garne |
| **Overfitting** | Training data ma ramro, test ma kharab |
| **Validation** | Training time ma performance check garne data |

---

## 📊 Model Architecture (Visual)

```
INPUT (48x48x1)
    ↓
CONV1 (32 filters) → Features: edges, lines
    ↓
POOL1 → Size: 24x24
    ↓
CONV2 (64 filters) → Features: eyes, nose
    ↓
POOL2 → Size: 12x12
    ↓
CONV3 (128 filters) → Features: expressions
    ↓
FLATTEN → 1D vector
    ↓
DENSE1 (512) → Pattern learning
    ↓
DENSE2 (256) → Refinement
    ↓
OUTPUT (7) → Emotion probabilities
```

---

## 🎭 7 Emotions

| Emotion | Nepali | Emoji | Typical Accuracy |
|---------|--------|-------|------------------|
| happy | khusi | 😊 | 85-90% |
| sad | dukhi | 😢 | 60-70% |
| angry | risaeko | 😠 | 55-65% |
| surprise | acharya | 😲 | 70-75% |
| fear | dar | 😨 | 50-60% |
| disgust | ghrina | 🤢 | 45-55% |
| neutral | normal | 😐 | 60-70% |

---

## 💻 How to Use Trained Model

### In Python:
```python
import tensorflow as tf
import numpy as np

# Load model
model = tf.keras.models.load_model('server/emotion_model.h5')

# Prepare image (48x48 grayscale)
image = preprocess_image(image)  # normalize, reshape

# Predict
prediction = model.predict(image)
emotion_idx = np.argmax(prediction)
confidence = prediction[0][emotion_idx]

print(f"Emotion: {emotions[emotion_idx]}")
print(f"Confidence: {confidence*100:.2f}%")
```

### In AuraBot:
```
1. Open: http://localhost:5000/emotion-detection.html
2. Allow webcam access
3. Click "Detect Emotion"
4. See result with confidence score
```

---

## 📈 Training Results

```
Dataset: FER-2013 (35,887 images)
Training Time: 2-3 hours
Model Size: ~10-15 MB
Parameters: ~2-3 million

Accuracy:
- Training: 70-75%
- Validation: 60-65%
- Test: 60-65%

Best Emotion: Happy (85-90%)
Worst Emotion: Disgust (45-55%)
```

---

## 🛠️ Troubleshooting

### Problem: Low Accuracy
```
Solution:
- More training data
- Data augmentation
- Increase epochs
- Try transfer learning
```

### Problem: Overfitting
```
Solution:
- Increase dropout
- Add more data
- Reduce model complexity
- Early stopping
```

### Problem: Slow Training
```
Solution:
- Use GPU
- Reduce batch size
- Smaller model
- Mixed precision training
```

---

## 📁 Important Files Location

```
Project Root/
├── train_fer2013_emotion_model.py    ← Main training script
├── train_real_emotion_model.py       ← Alternative training
├── simple_model_trainer.py           ← Simple version
│
├── server/
│   ├── emotion_model.h5              ← DEPLOYED MODEL ⭐
│   ├── emotion_mapping.pkl           ← Emotion labels
│   └── server.py                     ← Flask API
│
├── emotion_datasets/
│   └── fer2013/
│       └── fer2013_enhanced.csv      ← Training data
│
└── client/
    └── emotion-detection.html        ← Frontend UI
```

---

## 🎯 Quick Commands

```bash
# Train new model
python train_fer2013_emotion_model.py

# Test model
python test_emotion_model.py

# Start server
python server/server.py

# Open emotion detection
# Browser: http://localhost:5000/emotion-detection.html
```

---

## 💡 Key Takeaways

1. ✅ **Model**: CNN with 3 conv blocks
2. ✅ **Dataset**: FER-2013 (35,887 images)
3. ✅ **Emotions**: 7 types
4. ✅ **Accuracy**: 60-65%
5. ✅ **Deployed**: server/emotion_model.h5
6. ✅ **Usage**: Real-time webcam detection

---

## 📚 Learn More

- **Full Explanation**: `AURABOT_MODEL_TRAINING_SUMMARY_NEPALI.md`
- **Code with Comments**: `MODEL_TRAINING_EXPLAINED_NEPALI.py`
- **Original Files**: `train_fer2013_emotion_model.py`

---

**Yo quick reference le timro model training ko sabai important points cover garyo. Detail explanation ko lagi other files hera!** 🚀
