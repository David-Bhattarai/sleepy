
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
