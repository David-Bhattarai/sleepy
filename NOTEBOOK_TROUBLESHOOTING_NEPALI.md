# 🔧 Jupyter Notebook Troubleshooting Guide (Nepali)

## ❌ Common Errors & Solutions

### Error 1: `NameError: name 'model' is not defined`

**Problem:** Model variable create bhako chaina

**Solution:**
```python
# Step 2 cell run gara pehila
# Yo cell le model load garcha
```

**Correct Order:**
1. ✅ Run Step 1 (Import Libraries)
2. ✅ Run Step 2 (Load Model) ← IMPORTANT!
3. ✅ Run Step 3 (Helper Functions)
4. ✅ Then run other cells

---

### Error 2: `No trained model found!`

**Problem:** Model file exist gardaina

**Solution:**
```bash
# Train model first
python train_high_accuracy_fer2013.py

# Wait 2-3 hours
# Model will be saved to server/high_accuracy_emotion_model.h5
```

**Check if model exists:**
```python
import os
print(os.path.exists('server/high_accuracy_emotion_model.h5'))
```

---

### Error 3: `Image not found: path/to/your/image.jpg`

**Problem:** Image path galat cha

**Solution:**
```python
# Update image path
test_image_path = 'C:/Users/YourName/Pictures/face.jpg'  # Windows
# OR
test_image_path = 'images/test.jpg'  # Relative path
# OR
test_image_path = '/home/user/images/face.jpg'  # Linux/Mac
```

**Tips:**
- Use forward slashes `/` (not backslashes `\`)
- Use absolute path if relative path doesn't work
- Check if file actually exists

---

### Error 4: `ModuleNotFoundError: No module named 'tensorflow'`

**Problem:** TensorFlow install chaina

**Solution:**
```bash
pip install tensorflow
pip install numpy pandas matplotlib seaborn opencv-python pillow
```

---

### Error 5: `Could not load image`

**Problem:** Image corrupt cha ya format supported chaina

**Solution:**
- Check image format (use .jpg, .png, .bmp)
- Try different image
- Ensure image is not corrupted

---

### Error 6: `plt.style.use('seaborn-v0_8-darkgrid')` fails

**Problem:** Matplotlib version issue

**Solution:**
```python
# Replace in Step 1:
# plt.style.use('seaborn-v0_8-darkgrid')
# With:
plt.style.use('seaborn-darkgrid')
# OR
plt.style.use('default')
```

---

### Error 7: Webcam not working

**Problem:** Webcam access denied ya not available

**Solution:**
```python
# Try different camera index
cap = cv2.VideoCapture(0)  # Try 0, 1, 2

# Check if webcam is available
if not cap.isOpened():
    print("Webcam not available")
```

---

### Error 8: `Kernel died` or `Out of Memory`

**Problem:** Not enough RAM

**Solution:**
- Restart kernel: Kernel → Restart
- Close other applications
- Reduce batch size
- Process fewer images at once

---

## 🚀 Quick Fixes

### Fix 1: Restart Everything
```
Kernel → Restart & Clear Output
Then run all cells from top to bottom
```

### Fix 2: Check Dependencies
```python
# Run this in a cell to check:
import sys
print(f"Python: {sys.version}")

import tensorflow as tf
print(f"TensorFlow: {tf.__version__}")

import cv2
print(f"OpenCV: {cv2.__version__}")

import numpy as np
print(f"NumPy: {np.__version__}")
```

### Fix 3: Verify Model Path
```python
# Run this to check model:
import os
model_paths = [
    'server/high_accuracy_emotion_model.h5',
    'high_accuracy_emotion_model.h5',
    'server/emotion_model.h5'
]

for path in model_paths:
    if os.path.exists(path):
        print(f"✅ Found: {path}")
    else:
        print(f"❌ Not found: {path}")
```

---

## 📋 Correct Cell Execution Order

```
1. Step 1: Import Libraries ✅
   ↓
2. Step 2: Load Model ✅ (Creates 'model' variable)
   ↓
3. Step 3: Helper Functions ✅
   ↓
4. Step 4: Test Image (Optional)
   ↓
5. Step 5: Batch Processing (Optional)
   ↓
6. Step 6: Webcam Detection (Optional)
   ↓
7. Step 7: Model Analysis ✅
   ↓
8. Step 8: Save to CSV (Optional)
   ↓
9. Step 9: Examples (Optional)
```

---

## 💡 Best Practices

### 1. Always Run Cells in Order
```
Don't skip cells!
Run from top to bottom
```

### 2. Check Output After Each Cell
```
Make sure no errors before proceeding
```

### 3. Save Your Work
```
File → Save and Checkpoint
Regularly save your notebook
```

### 4. Restart Kernel if Confused
```
Kernel → Restart & Clear Output
Start fresh
```

### 5. Use Absolute Paths
```python
# Instead of:
test_image_path = 'image.jpg'

# Use:
test_image_path = 'C:/full/path/to/image.jpg'
```

---

## 🔍 Debugging Tips

### Tip 1: Print Variables
```python
# Check if variable exists
print('model' in globals())
print('EMOTIONS' in globals())

# Check variable value
print(type(model))
print(EMOTIONS)
```

### Tip 2: Test Small First
```python
# Test with one image first
# Then try batch processing
```

### Tip 3: Use Try-Except
```python
try:
    results = predict_emotion(image_path, model)
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
```

---

## 📊 Expected Output Examples

### Step 1 Output:
```
✅ Libraries imported successfully!
TensorFlow version: 2.13.0
NumPy version: 1.24.3
```

### Step 2 Output:
```
✅ Model loaded: server/high_accuracy_emotion_model.h5

📊 Model Summary:
Total parameters: 5,234,567
Input shape: (None, 48, 48, 1)
Output shape: (None, 7)
```

### Step 3 Output:
```
✅ Helper functions defined!
```

### Step 4 Output (with valid image):
```
🔍 Analyzing image: test.jpg

🎯 Results:
Dominant Emotion: HAPPY
Confidence: 95.23%

All Emotions:
  happy     : 95.23%
  surprise  :  2.39%
  neutral   :  1.82%
  ...

[Shows visualization]
```

---

## 🆘 Still Having Issues?

### Check These:

1. **Model Trained?**
   ```bash
   ls -lh server/high_accuracy_emotion_model.h5
   ```

2. **Dependencies Installed?**
   ```bash
   pip list | grep tensorflow
   pip list | grep opencv
   ```

3. **Python Version?**
   ```bash
   python --version
   # Should be 3.8+
   ```

4. **Jupyter Working?**
   ```bash
   jupyter --version
   ```

---

## 📚 Summary

### Most Common Issues:

1. ❌ Not running cells in order
   ✅ Run Step 1, 2, 3 first

2. ❌ Model not trained
   ✅ Run: `python train_high_accuracy_fer2013.py`

3. ❌ Wrong image path
   ✅ Use absolute path

4. ❌ Dependencies missing
   ✅ Install all packages

5. ❌ Kernel issues
   ✅ Restart kernel

---

## 🎯 Quick Checklist

Before running notebook:
- [ ] Model trained and exists
- [ ] All dependencies installed
- [ ] Jupyter notebook running
- [ ] Image paths correct
- [ ] Running cells in order

If error occurs:
- [ ] Read error message carefully
- [ ] Check which cell failed
- [ ] Verify all previous cells ran successfully
- [ ] Try restarting kernel
- [ ] Check this troubleshooting guide

---

**Yo guide follow garera sabai errors fix huna sakcha!** 🎉
