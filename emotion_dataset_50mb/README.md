# 50MB Emotion Detection Dataset

## Dataset Details
- **Total Samples**: 24,500
- **Image Size**: 48x48 grayscale
- **Emotions**: 7 classes
- **Size**: ~50MB (GitHub compatible)

## Emotion Classes
- 0: angry
- 1: disgust
- 2: fear
- 3: happy
- 4: sad
- 5: surprise
- 6: neutral

## Files
- `processed/emotion_train_50mb.npz` - Training data
- `processed/emotion_val_50mb.npz` - Validation data  
- `processed/emotion_test_50mb.npz` - Test data
- `processed/emotion_mapping.pkl` - Emotion labels

## Usage
```python
import numpy as np
import pickle

# Load training data
train_data = np.load('processed/emotion_train_50mb.npz')
X_train, y_train = train_data['X'], train_data['y']

# Load emotion mapping
with open('processed/emotion_mapping.pkl', 'rb') as f:
    emotions = pickle.load(f)

print(f"Training samples: {X_train.shape[0]}")
print(f"Emotions: {list(emotions.values())}")
```

## Performance
- Optimized for 50MB size (GitHub compatible)
- 24,500 total samples for quality training
- 48x48 image resolution for good detail
- Suitable for production prototyping

## License
MIT License - Feel free to use for educational purposes
