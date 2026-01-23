#!/usr/bin/env python3
"""
Environment Setup for AURA System
Sets required environment variables to fix TensorFlow warnings
"""

import os

# Disable TensorFlow oneDNN warnings
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

# Disable TensorFlow GPU warnings (if no GPU)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# Set Keras backend
os.environ['KERAS_BACKEND'] = 'tensorflow'

print("Environment variables set for AURA system")
print("- TF_ENABLE_ONEDNN_OPTS=0 (disables oneDNN warnings)")
print("- TF_CPP_MIN_LOG_LEVEL=2 (reduces TensorFlow logging)")
print("- KERAS_BACKEND=tensorflow (sets Keras backend)")