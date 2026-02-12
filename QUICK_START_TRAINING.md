# 🚀 Quick Start - Training Notebook

## One-Command Start

```cmd
.venv\Scripts\activate && jupyter notebook
```

Then click: **EMOTION_TRAINING_COMPLETE.ipynb** → Cell → Run All

---

## What You'll See

### 📊 Real-Time Visualizations:

1. **Dataset Distribution** - Bar + Pie charts
2. **Sample Images** - 14 emotion samples
3. **Training Progress** - Live accuracy/loss
4. **Training History** - 4 graphs
5. **Confusion Matrix** - 2 heatmaps
6. **Per-Emotion Stats** - 4 charts
7. **Sample Predictions** - Test results

---

## Timeline

```
Cell 1-2:  1 min   - Setup + Load data
Cell 3-5:  2 min   - Preprocess + Create model
Cell 6:    30-60m  - TRAINING (watch progress!)
Cell 7-12: 2 min   - Visualizations + Save
Total:     35-65m
```

---

## Files Created

```
✅ emotion_model_YYYYMMDD_HHMMSS_final.h5
✅ server/emotion_model_trained.h5
✅ *_training_history.png
✅ *_confusion_matrix.png
✅ *_statistics.png
✅ *_sample_predictions.png
✅ *_metadata.json
```

---

## Expected Accuracy

- **Training**: 65-75%
- **Validation**: 60-70%
- **Test**: 60-70%

---

## Troubleshooting

### Error: Module not found
```cmd
pip install tensorflow numpy pandas matplotlib seaborn opencv-python
```

### Error: Dataset not found
Check: `emotion_datasets/fer2013/fer2013_enhanced.csv`

### Error: Out of memory
Change in Cell 5: `BATCH_SIZE = 16`

---

## Full Guide

See: **TRAINING_NOTEBOOK_GUIDE_NEPALI.md**

---

**Ready? Let's train! 🎯**
