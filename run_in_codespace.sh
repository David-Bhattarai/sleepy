#!/bin/bash

# This script automates the setup and execution of the Sleepy project
# in a standard Linux environment like GitHub Codespaces.

echo "--- Starting Sleepy Project Setup for Codespaces ---"

# Step 1: Install system dependencies (ffmpeg for deepface)
echo "[INFO] Step 1: Installing system dependencies (ffmpeg, tk)..."
sudo apt-get update && sudo apt-get install -y ffmpeg tk
if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to install system dependencies. Please check permissions and try again. Aborting."
    exit 1
fi
echo "[SUCCESS] System dependencies installed."

# Step 2: Create a Python virtual environment
echo "[INFO] Step 2: Creating Python virtual environment ('venv')..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to create a virtual environment. Aborting."
    exit 1
fi
echo "[SUCCESS] Virtual environment created."

# Step 3: Activate the virtual environment and install Python packages
echo "[INFO] Step 3: Activating environment and installing packages from requirements.txt..."
source venv/bin/activate && pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to install Python packages. Aborting."
    exit 1
fi
echo "[SUCCESS] All Python packages installed."

# Step 4: Run the application
echo "[INFO] Step 4: Starting the Flask server..."
echo "---"
echo "Server is starting now. Access the application through the URL provided in the 'Ports' tab of your Codespace."
echo "---"
python3 server/app.py
