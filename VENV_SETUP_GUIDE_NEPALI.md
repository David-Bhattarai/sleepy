# 🐍 Virtual Environment Setup Guide (Nepali)

## 🎯 Goal
`.venv` virtual environment activate garera sabai packages install garne

---

## 📋 Step-by-Step Commands

### Step 1: Navigate to Project Directory
```bash
cd C:\Users\DELL\sleepy\sleepy
```

### Step 2: Check if .venv exists
```bash
# Check if .venv folder exists
dir .venv
```

**If .venv doesn't exist, create it:**
```bash
python -m venv .venv
```

### Step 3: Activate Virtual Environment

**Windows (Command Prompt):**
```bash
.venv\Scripts\activate
```

**Windows (PowerShell):**
```powershell
.venv\Scripts\Activate.ps1
```

**If PowerShell gives error:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.venv\Scripts\Activate.ps1
```

### Step 4: Verify Activation
```bash
# You should see (.venv) at the beginning of prompt
# Example: (.venv) PS C:\Users\DELL\sleepy\sleepy>

# Check Python path
python --version
where python
```

### Step 5: Upgrade pip
```bash
python -m pip install --upgrade pip
```

### Step 6: Install All Packages
```bash
pip install numpy pandas matplotlib seaborn opencv-python pillow tensorflow jupyter
```

**Or use requirements.txt:**
```bash
pip install -r requirements.txt
```

### Step 7: Verify Installation
```bash
pip list
```

### Step 8: Install Jupyter Kernel
```bash
python -m ipykernel install --user --name=emotion-detection --display-name="Python (Emotion Detection)"
```

### Step 9: Start Jupyter with venv
```bash
jupyter notebook
```

---

## 🚀 Complete Command Sequence (Copy-Paste)

```bash
# Navigate to project
cd C:\Users\DELL\sleepy\sleepy

# Activate venv
.venv\Scripts\activate

# Upgrade pip
python -m pip install --upgrade pip

# Install packages
pip install numpy pandas matplotlib seaborn opencv-python pillow tensorflow jupyter ipykernel

# Install Jupyter kernel
python -m ipykernel install --user --name=emotion-detection --display-name="Python (Emotion Detection)"

# Start Jupyter
jupyter notebook
```

---

## 📝 PowerShell Script (Automated)

**Save as `setup_venv.ps1`:**

```powershell
# Navigate to project
Set-Location "C:\Users\DELL\sleepy\sleepy"

# Check if .venv exists
if (-Not (Test-Path ".venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv .venv
}

# Activate venv
Write-Host "Activating virtual environment..." -ForegroundColor Green
.\.venv\Scripts\Activate.ps1

# Upgrade pip
Write-Host "Upgrading pip..." -ForegroundColor Green
python -m pip install --upgrade pip

# Install packages
Write-Host "Installing packages..." -ForegroundColor Green
pip install numpy pandas matplotlib seaborn opencv-python pillow tensorflow jupyter ipykernel

# Install Jupyter kernel
Write-Host "Installing Jupyter kernel..." -ForegroundColor Green
python -m ipykernel install --user --name=emotion-detection --display-name="Python (Emotion Detection)"

Write-Host "✅ Setup complete!" -ForegroundColor Green
Write-Host "Run: jupyter notebook" -ForegroundColor Cyan
```

**Run:**
```powershell
powershell -ExecutionPolicy Bypass -File setup_venv.ps1
```

---

## 🔧 Troubleshooting

### Problem 1: Cannot activate venv
```bash
# Solution: Use full path
C:\Users\DELL\sleepy\sleepy\.venv\Scripts\activate
```

### Problem 2: PowerShell execution policy error
```powershell
# Solution: Change policy
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then activate
.venv\Scripts\Activate.ps1
```

### Problem 3: Wrong Python version
```bash
# Check Python in venv
.venv\Scripts\python.exe --version

# Use venv Python explicitly
.venv\Scripts\python.exe -m pip install numpy
```

### Problem 4: Jupyter doesn't use venv
```bash
# Install ipykernel in venv
pip install ipykernel

# Register kernel
python -m ipykernel install --user --name=emotion-detection

# In Jupyter: Kernel → Change Kernel → Python (Emotion Detection)
```

---

## 📊 Verify Everything Works

**After activation, run:**

```bash
# Check venv is active
echo $env:VIRTUAL_ENV  # PowerShell
echo %VIRTUAL_ENV%     # CMD

# Check Python location
where python
# Should show: C:\Users\DELL\sleepy\sleepy\.venv\Scripts\python.exe

# Check installed packages
pip list

# Test imports
python -c "import numpy; import tensorflow; print('✅ All imports work!')"
```

---

## 🎯 Using Jupyter with venv

### Method 1: Start Jupyter from activated venv
```bash
# Activate venv
.venv\Scripts\activate

# Start Jupyter
jupyter notebook

# Jupyter will automatically use venv packages
```

### Method 2: Select kernel in Jupyter
```
1. Open Jupyter notebook
2. Click: Kernel → Change Kernel
3. Select: Python (Emotion Detection)
4. Now using venv!
```

---

## 📁 Project Structure

```
C:\Users\DELL\sleepy\sleepy\
├── .venv\                          ← Virtual environment
│   ├── Scripts\
│   │   ├── activate                ← Activation script
│   │   ├── python.exe              ← Python in venv
│   │   └── pip.exe                 ← pip in venv
│   └── Lib\
│       └── site-packages\          ← Installed packages here
├── server\
├── emotion_detection_notebook.ipynb
├── requirements.txt
└── ... other files
```

---

## 💡 Quick Reference

### Activate venv:
```bash
.venv\Scripts\activate              # CMD
.venv\Scripts\Activate.ps1          # PowerShell
```

### Deactivate venv:
```bash
deactivate
```

### Install package in venv:
```bash
pip install package-name
```

### Check venv packages:
```bash
pip list
pip freeze > requirements.txt
```

### Remove venv:
```bash
deactivate
rmdir /s .venv                      # CMD
Remove-Item -Recurse -Force .venv   # PowerShell
```

---

## 🎓 Best Practices

1. **Always activate venv before working**
   ```bash
   .venv\Scripts\activate
   ```

2. **Install packages only in activated venv**
   ```bash
   # Check venv is active (should see (.venv) in prompt)
   pip install package-name
   ```

3. **Use requirements.txt**
   ```bash
   # Save packages
   pip freeze > requirements.txt
   
   # Install from file
   pip install -r requirements.txt
   ```

4. **Use venv-specific Jupyter kernel**
   ```bash
   python -m ipykernel install --user --name=emotion-detection
   ```

---

## ✅ Success Checklist

After setup, verify:

- [ ] `.venv` folder exists
- [ ] Can activate venv (see `(.venv)` in prompt)
- [ ] `python --version` shows correct version
- [ ] `where python` shows venv path
- [ ] All packages installed (`pip list`)
- [ ] Jupyter kernel registered
- [ ] Can import packages in Jupyter
- [ ] No import errors

---

## 🚀 Final Commands Summary

```bash
# 1. Navigate
cd C:\Users\DELL\sleepy\sleepy

# 2. Activate
.venv\Scripts\activate

# 3. Install
pip install -r requirements.txt

# 4. Setup Jupyter
python -m ipykernel install --user --name=emotion-detection

# 5. Start
jupyter notebook

# 6. In Jupyter: Kernel → Change Kernel → Python (Emotion Detection)
```

---

**Yo guide follow garera venv ma sabai packages install huncha!** 🎉
