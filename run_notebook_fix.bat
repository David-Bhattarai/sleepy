@echo off
echo 🚀 Starting Jupyter Notebook Fix...
echo =====================================

echo 📦 Step 1: Installing dependencies...
pip install numpy pandas matplotlib seaborn scikit-learn tensorflow opencv-python pillow jupyter notebook ipykernel

echo.
echo 🔧 Step 2: Running step-by-step fix...
python fix_notebook_step_by_step.py

echo.
echo ✅ Fix completed! Check the output above for any errors.
echo.
echo 💡 Next steps:
echo 1. If all steps passed, run: jupyter notebook
echo 2. Open: FER2013_Emotion_Model_Training.ipynb
echo 3. Run all cells in the notebook
echo.
pause