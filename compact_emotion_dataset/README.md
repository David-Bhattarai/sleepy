# 50MB Emotion Detection Dataset

## Dataset Details
- **Total Samples**: 17500
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
- `processed/compact_train.npz` - Training data
- `processed/compact_val.npz` - Validation data  
- `processed/compact_test.npz` - Test data
- `processed/emotion_mapping.pkl` - Emotion labels
- `compact_emotion_model_50mb.h5` - CNN model optimized for 50MB dataset

## Usage
```python
import numpy as np

# Load training data
train_data = np.load('processed/compact_train.npz')
X_train, y_train = train_data['X'], train_data['y']

# Load model
from tensorflow.keras.models import load_model
model = load_model('compact_emotion_model_50mb.h5')

# Make predictions
predictions = model.predict(X_train[:5])
```

## Performance
- Optimized for 50MB size (GitHub compatible)
- 7,000 total samples for better training
- 48x48 image resolution for good quality
- Suitable for production prototyping

## License
MIT License - Feel free to use for educational purposes
