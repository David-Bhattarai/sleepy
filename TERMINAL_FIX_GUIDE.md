# Terminal Fix Guide - Model Training Notebook

## 🚀 Quick Terminal Commands

### Method 1: Run Complete Fix
```bash
python fix_notebook_step_by_step.py
```

### Method 2: Run Individual Cells
```bash
python cell_01_imports.py
python cell_02_trainer_class.py
python cell_03_load_dataset.py
```

### Method 3: Run All Cells in Order
```bash
python run_all_cells.py
```

### Method 4: Use Batch Script (Windows)
```bash
run_notebook_fix.bat
```

### Method 5: Use Shell Script (Linux/Mac)
```bash
chmod +x run_notebook_fix.sh
./run_notebook_fix.sh
```

## 🔧 Manual Step-by-Step Fix

### Step 1: Install Dependencies
```bash
pip install numpy pandas matplotlib seaborn scikit-learn tensorflow opencv-python pillow jupyter notebook ipykernel
```

### Step 2: Test Imports
```bash
python cell_01_imports.py
```
**Expected Output:** ✅ All imports successful

### Step 3: Test Trainer Class
```bash
python cell_02_trainer_class.py
```
**Expected Output:** ✅ Trainer created successfully

### Step 4: Test Dataset Loading
```bash
python cell_03_load_dataset.py
```
**Expected Output:** ✅ Dataset loaded with samples

### Step 5: Run Complete Test
```bash
python fix_notebook_step_by_step.py
```

## 🐛 Common Errors and Fixes

### Error: "No module named numpy"
```bash
pip install numpy
# or
python -m pip install numpy
# or
pip install --user numpy
```

### Error: "No module named tensorflow"
```bash
pip install tensorflow
# or for CPU only
pip install tensorflow-cpu
```

### Error: "No module named cv2"
```bash
pip install opencv-python
# or headless version
pip install opencv-python-headless
```

### Error: "Dataset not found"
- The scripts will automatically create sample data
- No action needed, this is handled automatically

### Error: "GPU not available"
- This is normal, the scripts will use CPU
- No action needed

## 📊 What Each Script Does

### `cell_01_imports.py`
- Tests all required imports
- Shows which packages are missing
- Provides specific fix commands

### `cell_02_trainer_class.py`
- Creates the FER2013 trainer class
- Tests basic functionality
- Validates class methods

### `cell_03_load_dataset.py`
- Loads dataset or creates sample data
- Shows dataset statistics
- Validates data format

### `fix_notebook_step_by_step.py`
- Runs all tests in sequence
- Provides detailed error messages
- Suggests specific fixes

### `run_all_cells.py`
- Executes all cell scripts in order
- Shows progress and results
- Allows continuing after errors

## ✅ Success Indicators

You'll know it's working when you see:
- ✅ All imports successful
- ✅ Trainer created successfully  
- ✅ Dataset loaded with X samples
- ✅ All steps completed

## 🚀 After Fixing

Once all scripts run successfully:

1. **Start Jupyter:**
   ```bash
   jupyter notebook
   ```

2. **Open the notebook:**
   - Navigate to `FER2013_Emotion_Model_Training.ipynb`
   - Click to open

3. **Run all cells:**
   - Click "Cell" → "Run All"
   - Or run each cell individually with Shift+Enter

## 🆘 Still Having Issues?

### Complete Environment Reset
```bash
# Create new virtual environment
python -m venv ml_env

# Activate it
# Windows:
ml_env\Scripts\activate
# Linux/Mac:
source ml_env/bin/activate

# Install everything fresh
pip install --upgrade pip
pip install numpy pandas matplotlib seaborn scikit-learn tensorflow opencv-python pillow jupyter notebook ipykernel

# Test again
python fix_notebook_step_by_step.py
```

### Alternative Installation Methods
```bash
# Using conda
conda install numpy pandas matplotlib seaborn scikit-learn tensorflow opencv pillow jupyter

# Using pip with specific versions
pip install numpy==1.21.0 pandas==1.3.0 tensorflow==2.8.0

# Force reinstall
pip install --force-reinstall numpy pandas tensorflow
```

## 📞 Quick Diagnostic Commands

```bash
# Check Python version
python --version

# Check pip version  
pip --version

# List installed packages
pip list

# Check specific package
pip show numpy

# Test numpy quickly
python -c "import numpy; print('NumPy works:', numpy.__version__)"

# Test tensorflow quickly
python -c "import tensorflow; print('TensorFlow works:', tensorflow.__version__)"
```

## 🎯 Expected Final Result

After running all fixes, you should see:
```
🎉 ALL STEPS SUCCESSFUL!
✅ Your Jupyter notebook should work perfectly now!

🚀 Next steps:
1. Open Jupyter: jupyter notebook
2. Run: FER2013_Emotion_Model_Training.ipynb
3. All cells should execute without errors
```

---

## 💡 Pro Tips

1. **Always run scripts in order** - each builds on the previous
2. **Check output carefully** - look for ✅ success indicators
3. **Install missing packages immediately** - don't skip dependencies
4. **Restart terminal** after installing packages
5. **Use virtual environments** for clean installs

The notebook has comprehensive error handling, so even if some issues remain, it will guide you through the fixes!