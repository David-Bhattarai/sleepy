@echo off
REM ============================================================================
REM Virtual Environment Setup and Package Installation
REM Run this to setup everything automatically
REM ============================================================================

echo ========================================
echo Virtual Environment Setup
echo ========================================
echo.

REM Check if .venv exists
if not exist ".venv" (
    echo Creating virtual environment...
    python -m venv .venv
    echo ✅ Virtual environment created
) else (
    echo ✅ Virtual environment already exists
)
echo.

REM Activate venv
echo Activating virtual environment...
call .venv\Scripts\activate.bat
echo ✅ Virtual environment activated
echo.

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip
echo ✅ pip upgraded
echo.

REM Install packages
echo Installing required packages...
echo This may take 5-10 minutes...
echo.

pip install numpy
pip install pandas
pip install matplotlib
pip install seaborn
pip install opencv-python
pip install pillow
pip install tensorflow
pip install jupyter
pip install ipykernel

echo.
echo ✅ All packages installed
echo.

REM Install Jupyter kernel
echo Installing Jupyter kernel...
python -m ipykernel install --user --name=emotion-detection --display-name="Python (Emotion Detection)"
echo ✅ Jupyter kernel installed
echo.

REM Verify installation
echo ========================================
echo Verification
echo ========================================
echo.
echo Installed packages:
pip list
echo.

echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Run: jupyter notebook
echo 2. Open: emotion_detection_NO_ERRORS.ipynb
echo 3. In Jupyter: Kernel → Change Kernel → Python (Emotion Detection)
echo 4. Run cells!
echo.
echo Virtual environment is activated.
echo To deactivate: deactivate
echo.

pause
