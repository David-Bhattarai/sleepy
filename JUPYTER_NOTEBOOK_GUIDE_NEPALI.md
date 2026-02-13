# 📓 Jupyter Notebook Guide - Emotion Detection (Nepali)

## 🎯 Overview

Timro trained model lai Jupyter Notebook ma use garna ko lagi complete notebook create gareko chu.

---

## 📁 File Created

**File:** `emotion_detection_notebook.ipynb`

**Location:** Project root directory

---

## 🚀 How to Use

### Step 1: Install Jupyter
```bash
pip install jupyter notebook
```

### Step 2: Start Jupyter
```bash
jupyter notebook
```

### Step 3: Open Notebook
```
Browser ma automatically open huncha
Navigate to: emotion_detection_notebook.ipynb
Click to open
```

### Step 4: Run Cells
```
Cell by cell run gara (Shift + Enter)
Ya "Run All" click gara
```

---

## 📊 Notebook Contents

### Cell 1: Import Libraries
```python
# Core libraries import
import numpy as np
import tensorflow as tf
import cv2
import matplotlib.pyplot as plt
```

### Cell 2: Load Trained Model
```python
# Automatically loads:
# - server/high_accuracy_emotion_model.h5 (90%+ accuracy)
# - Or other trained models
```

### Cell 3: Helper Functions
```python
# Functions for:
# - Image preprocessing
# - Emotion prediction
# - Result visualization
```

### Cell 4: Single Image Test
```python
# Test with one image
test_image_path = 'path/to/your/image.jpg'
results = predict_emotion(test_image_path, model)
visualize_prediction(results)
```

### Cell 5: Batch Processing
```python
# Process multiple images
results_list = process_multiple_images('path/to/folder')
```

### Cell 6: Webcam Detection
```python
# Real-time emotion detection
webcam_emotion_detection(duration=30)
```

### Cell 7: Model Analysis
```python
# View model architecture
model.summary()
```

### Cell 8: Export Results
```python
# Save to CSV
save_predictions_to_csv(results_list, 'predictions.csv')
```

---

## 🎓 Features

### ✅ What Notebook Can Do:

1. **Load Trained Model**
   - Automatically finds and loads model
   - Shows model info and metadata
   - Displays accuracy

2. **Single Image Prediction**
   - Upload any image
   - Detect emotion
   - Show confidence scores
   - Visualize results

3. **Batch Processing**
   - Process entire folder
   - Get statistics
   - Export to CSV

4. **Real-time Webcam**
   - Live emotion detection
   - Face detection
   - Real-time overlay

5. **Visualization**
   - Bar charts
   - Confidence scores
   - Model architecture

6. **Export Results**
   - CSV format
   - All emotions
   - Confidence scores

---

## 💻 Example Usage

### Example 1: Test Single Image
```python
# In notebook cell:
test_image = 'test_images/happy_face.jpg'
results = predict_emotion(test_image, model)
visualize_prediction(results)

# Output:
# Dominant Emotion: HAPPY
# Confidence: 95.23%
# [Shows image + bar chart]
```

### Example 2: Process Folder
```python
# In notebook cell:
results = process_multiple_images('test_images/')

# Output:
# ✅ image1.jpg → happy (95.2%)
# ✅ image2.jpg → sad (87.5%)
# ✅ image3.jpg → angry (82.1%)
# 
# Summary:
#   happy: 10 images (50%)
#   sad: 5 images (25%)
#   angry: 5 images (25%)
```

### Example 3: Webcam Detection
```python
# In notebook cell:
webcam_emotion_detection(duration=30)

# Opens webcam window
# Shows real-time emotion detection
# Press 'q' to quit
```

### Example 4: Export Results
```python
# In notebook cell:
results = process_multiple_images('test_images/')
df = save_predictions_to_csv(results, 'results.csv')

# Creates CSV with:
# filename, dominant_emotion, confidence, angry_prob, disgust_prob, ...
```

---

## 📊 Output Examples

### Visualization Output:
```
┌─────────────────────────────────────────────────────────┐
│  Image                    │  Emotion Probabilities      │
│  [Face photo]             │  happy    ████████ 95.2%   │
│                           │  surprise ██ 2.5%           │
│  Detected: HAPPY          │  neutral  █ 1.8%            │
│  Confidence: 95.2%        │  sad      █ 0.3%            │
│                           │  angry    █ 0.1%            │
│                           │  fear     █ 0.1%            │
│                           │  disgust  █ 0.0%            │
└─────────────────────────────────────────────────────────┘
```

### CSV Output:
```csv
filename,dominant_emotion,confidence,angry_prob,disgust_prob,fear_prob,happy_prob,neutral_prob,sad_prob,surprise_prob
image1.jpg,happy,95.23,0.12,0.05,0.08,95.23,1.82,0.31,2.39
image2.jpg,sad,87.45,2.15,0.18,3.21,1.23,2.45,87.45,3.33
```

---

## 🔧 Customization

### Change Model Path:
```python
# In Cell 2, modify:
model_paths = [
    'your/custom/path/model.h5',  # Add your path
    'server/high_accuracy_emotion_model.h5',
    # ... other paths
]
```

### Change Emotions:
```python
# In Cell 2, modify:
EMOTIONS = ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']
# Add or remove emotions as needed
```

### Change Image Size:
```python
# In preprocess_image function:
resized = cv2.resize(gray, (48, 48))  # Change size here
```

### Change Visualization:
```python
# In visualize_prediction function:
# Modify colors, sizes, labels, etc.
colors = ['red' if e == results['dominant_emotion'] else 'skyblue' for e in emotions]
```

---

## 🛠️ Troubleshooting

### Problem: Jupyter not installed
```bash
# Solution:
pip install jupyter notebook
```

### Problem: Model not found
```bash
# Solution:
# Train model first:
python train_high_accuracy_fer2013.py

# Or update model path in notebook
```

### Problem: OpenCV error
```bash
# Solution:
pip install opencv-python
```

### Problem: Webcam not working
```python
# Solution:
# Check webcam index (try 0, 1, 2)
cap = cv2.VideoCapture(0)  # Change 0 to 1 or 2
```

### Problem: Image not loading
```python
# Solution:
# Check file path
# Use absolute path:
test_image = r'C:\full\path\to\image.jpg'
```

---

## 📚 Dependencies

### Required Libraries:
```bash
pip install numpy
pip install pandas
pip install matplotlib
pip install seaborn
pip install opencv-python
pip install tensorflow
pip install pillow
pip install jupyter
```

### Or install all at once:
```bash
pip install -r requirements.txt
```

---

## 🎯 Quick Start Checklist

Before using notebook:
- [ ] Jupyter installed
- [ ] Dependencies installed
- [ ] Model trained (high_accuracy_emotion_model.h5)
- [ ] Test images ready

Using notebook:
- [ ] Start Jupyter
- [ ] Open emotion_detection_notebook.ipynb
- [ ] Run Cell 1 (imports)
- [ ] Run Cell 2 (load model)
- [ ] Update image paths
- [ ] Run remaining cells
- [ ] Test with your images

---

## 💡 Tips & Tricks

### Tip 1: Fast Testing
```python
# Use small test set first
# Then process full dataset
```

### Tip 2: Save Intermediate Results
```python
# Save results after each batch
import pickle
with open('results.pkl', 'wb') as f:
    pickle.dump(results_list, f)
```

### Tip 3: GPU Acceleration
```python
# Check GPU availability
print("GPU Available:", tf.config.list_physical_devices('GPU'))
```

### Tip 4: Batch Size
```python
# For large datasets, process in batches
# Prevents memory issues
```

### Tip 5: Error Handling
```python
# Wrap predictions in try-except
try:
    results = predict_emotion(image_path, model)
except Exception as e:
    print(f"Error: {e}")
```

---

## 📊 Performance Tips

### For Faster Processing:
```python
# 1. Use GPU
# 2. Reduce image size
# 3. Batch predictions
# 4. Skip visualization for large datasets
```

### For Better Accuracy:
```python
# 1. Use high-quality images
# 2. Ensure good lighting
# 3. Clear facial expressions
# 4. Front-facing faces
```

---

## 🎓 Learning Resources

### Notebook Shortcuts:
```
Shift + Enter: Run cell and move to next
Ctrl + Enter: Run cell and stay
Alt + Enter: Run cell and insert below
A: Insert cell above
B: Insert cell below
DD: Delete cell
M: Convert to markdown
Y: Convert to code
```

### Useful Commands:
```python
# Display all variables
%whos

# Time execution
%timeit function()

# Clear output
from IPython.display import clear_output
clear_output()

# Display image
from IPython.display import Image, display
display(Image('image.jpg'))
```

---

## 📝 Summary

### What You Got:
1. ✅ Complete Jupyter Notebook
2. ✅ Trained model integration
3. ✅ Single image prediction
4. ✅ Batch processing
5. ✅ Webcam detection
6. ✅ Result visualization
7. ✅ CSV export

### How to Use:
```bash
# 1. Start Jupyter
jupyter notebook

# 2. Open notebook
emotion_detection_notebook.ipynb

# 3. Run cells
Shift + Enter

# 4. Test with images
Update paths and run

# 5. Export results
Save to CSV
```

### Files:
```
emotion_detection_notebook.ipynb  ← Main notebook
JUPYTER_NOTEBOOK_GUIDE_NEPALI.md  ← This guide
```

---

## 🎉 Conclusion

Timro trained model aba Jupyter Notebook ma fully integrated cha! 

**Features:**
- ✅ Load trained model
- ✅ Predict emotions
- ✅ Batch processing
- ✅ Webcam detection
- ✅ Visualizations
- ✅ Export results

**Just open notebook and start using!** 🚀

---

**Happy Coding! 📓**
