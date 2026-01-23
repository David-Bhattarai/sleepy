# Compact Emotion Detection Dataset

## Dataset Details
- **Total Samples**: 350
- **Image Size**: 32x32 grayscale
- **Emotions**: 7 classes
- **Size**: <10MB (GitHub friendly)

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
- `compact_emotion_model.h5` - Lightweight CNN model

## Usage
```python
import numpy as np

# Load training data
train_data = np.load('processed/compact_train.npz')
X_train, y_train = train_data['X'], train_data['y']

# Load model
from tensorflow.keras.models import load_model
model = load_model('compact_emotion_model.h5')

# Make predictions
predictions = model.predict(X_train[:5])
```

## Performance
- Optimized for GitHub upload (<100MB)
- Suitable for learning and prototyping
- Can be extended with more data for production use

## License
MIT License - Feel free to use for educational purposes
