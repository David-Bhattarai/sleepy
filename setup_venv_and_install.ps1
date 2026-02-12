# ============================================================================
# Virtual Environment Setup and Package Installation (PowerShell)
# Run this to setup everything automatically
# ============================================================================

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Virtual Environment Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if .venv exists
if (-Not (Test-Path ".venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv .venv
    Write-Host "✅ Virtual environment created" -ForegroundColor Green
} else {
    Write-Host "✅ Virtual environment already exists" -ForegroundColor Green
}
Write-Host ""

# Activate venv
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& .\.venv\Scripts\Activate.ps1
Write-Host "✅ Virtual environment activated" -ForegroundColor Green
Write-Host ""

# Upgrade pip
Write-Host "Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip | Out-Null
Write-Host "✅ pip upgraded" -ForegroundColor Green
Write-Host ""

# Install packages
Write-Host "Installing required packages..." -ForegroundColor Yellow
Write-Host "This may take 5-10 minutes..." -ForegroundColor Yellow
Write-Host ""

$packages = @(
    "numpy",
    "pandas",
    "matplotlib",
    "seaborn",
    "opencv-python",
    "pillow",
    "tensorflow",
    "jupyter",
    "ipykernel"
)

foreach ($package in $packages) {
    Write-Host "Installing $package..." -ForegroundColor Cyan
    pip install $package --quiet
    Write-Host "✅ $package installed" -ForegroundColor Green
}

Write-Host ""
Write-Host "✅ All packages installed" -ForegroundColor Green
Write-Host ""

# Install Jupyter kernel
Write-Host "Installing Jupyter kernel..." -ForegroundColor Yellow
python -m ipykernel install --user --name=emotion-detection --display-name="Python (Emotion Detection)" | Out-Null
Write-Host "✅ Jupyter kernel installed" -ForegroundColor Green
Write-Host ""

# Verify installation
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Verification" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Python version:" -ForegroundColor Yellow
python --version
Write-Host ""

Write-Host "Python location:" -ForegroundColor Yellow
Get-Command python | Select-Object -ExpandProperty Source
Write-Host ""

Write-Host "Installed packages:" -ForegroundColor Yellow
pip list
Write-Host ""

# Test imports
Write-Host "Testing imports..." -ForegroundColor Yellow
$testScript = @"
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import cv2
from PIL import Image
import tensorflow as tf
print('✅ All imports successful!')
print(f'NumPy: {np.__version__}')
print(f'TensorFlow: {tf.__version__}')
print(f'OpenCV: {cv2.__version__}')
"@

python -c $testScript
Write-Host ""

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Run: jupyter notebook" -ForegroundColor White
Write-Host "2. Open: emotion_detection_NO_ERRORS.ipynb" -ForegroundColor White
Write-Host "3. In Jupyter: Kernel → Change Kernel → Python (Emotion Detection)" -ForegroundColor White
Write-Host "4. Run cells!" -ForegroundColor White
Write-Host ""

Write-Host "Virtual environment is activated." -ForegroundColor Green
Write-Host "To deactivate: deactivate" -ForegroundColor Yellow
Write-Host ""

Read-Host "Press Enter to continue"
