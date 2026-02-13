# 🎨 Emotion Detection - ML Files Integration Diagram (Nepali)

## 📊 Complete System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                              │
│                   (client/emotion-detection.html)                   │
└─────────────────────────────────────────────────────────────────────┘
                              ↓
        ┌─────────────────────────────────────────┐
        │  3 Detection Methods:                   │
        │  1. 📷 Camera Capture                   │
        │  2. 📁 Image Upload                     │
        │  3. 🎯 Sample Images                    │
        └─────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│                    FRONTEND JAVASCRIPT                              │
│              (client/emotion-detection.js)                          │
│                                                                     │
│  Functions:                                                         │
│  - captureAndDetectEmotion()                                       │
│  - detectUploadedEmotion()                                         │
│  - detectSelectedSample()                                          │
│  - detectEmotion(imageData, source)  ← Main function              │
└─────────────────────────────────────────────────────────────────────┘
                              ↓
                    API Call (POST)
                              ↓
        ┌─────────────────────────────────────────┐
        │  Endpoint:                              │
        │  /api/emotion_detection_gemini          │
        │                                         │
        │  Headers:                               │
        │  - Authorization: Bearer {token}        │
        │  - Content-Type: application/json       │
        │                                         │
        │  Body:                                  │
        │  {                                      │
        │    image: "base64_data",                │
        │    timestamp: "2026-01-23...",          │
        │    source: "camera/upload/sample"       │
        │  }                                      │
        └─────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│                      FLASK SERVER                                   │
│                    (server/app.py)                                  │
│                                                                     │
│  @app.route('/api/emotion_detection_gemini')                       │
│  def gemini_emotion_detection():                                   │
└─────────────────────────────────────────────────────────────────────┘
                              ↓
                    ┌─────────────────┐
                    │  DETECTION FLOW │
                    └─────────────────┘
                              ↓
        ┌─────────────────────────────────────────┐
        │  PRIORITY 1: Try Gemini AI             │
        └─────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│                    GEMINI AI SYSTEM                                 │
│           (server/gemini_ai_integration.py)                         │
│                           