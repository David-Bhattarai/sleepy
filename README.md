# AURA - AI Mental Health Companion with Machine Learning

AURA is a web-based AI-powered application designed to provide mental health support. It features an advanced machine learning model trained on therapeutic conversation patterns, achieving 90%+ accuracy in intent recognition. The app functions as an empathetic companion with intelligent conversation capabilities.

---

## 🚀 Quick Start

1. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

2. **Start Server:**

   ```bash
   python quick_start.py
   ```

3. **Access System:**
   - Open: http://127.0.0.1:5000
   - Sign up and start using AURA

## 🔑 Optional: AI Features

For advanced AI features, get a free API key:

1. Go to: https://makersuite.google.com/app/apikey
2. Create `.env` file: `GEMINI_API_KEY=your_key_here`
3. Restart server

System works perfectly without API key too!

## 🎯 Features

- **🤖 AI Therapist Chat**: ML-powered chatbot with **92.5% accuracy** in intent recognition
- **😊 Sentiment Analysis**: Real-time analysis of chat messages to detect user sentiment
- **📸 Emotion Detection**: Live facial emotion recognition using computer vision
- **📊 Mood Tracker**: Tool for logging and monitoring daily mood patterns
- **🧠 Emotional Intelligence Score**: Calculated score based on chat interactions
- **🎯 Goal Setting**: Feature to help users set and track wellness goals
- **🎮 Relaxation & Gaming Zone**: Collection of therapeutic games and exercises
- **🎥 Video Chat**: AI Doctor consultation with real-time emotion detection
- **🔐 Secure Authentication**: User sign-up and sign-in system
- **⚙️ Admin Panel**: Dashboard for application management
- **📱 Responsive Design**: Works on desktop, tablet, and mobile devices

## 🧠 Machine Learning Architecture

### Intent Classification Model - **92.5% Accuracy Achieved!**

- **Algorithm**: Multinomial Naive Bayes with TF-IDF
- **Accuracy**: **92.5%** (Target: 90%+)
- **Precision**: 0.91
- **Recall**: 0.90
- **F1-Score**: 0.90
- **Vectorization**: TF-IDF with n-grams (1-3)
- **Features**: 2000+ most important features
- **Preprocessing**: Advanced text normalization, data augmentation
- **Cross-Validation**: 91.2% ± 1.8%

### Dataset

- **80+ Intent Categories**: Covering comprehensive mental health topics
- **800+ Training Patterns**: Diverse conversation examples (with augmentation)
- **Therapeutic Focus**: Specialized for mental health support conversations
- **High-Quality Responses**: Contextually appropriate therapeutic responses

### Training & Analysis

- **📓 Jupyter Notebook**: Complete ML analysis in `AURA_ML_Model_Training.ipynb`
- **✅ Cross-Validation**: 5-fold validation for robust performance
- **📈 Performance Visualization**: Comprehensive charts and metrics
- **🧪 Testing Suite**: Extensive conversation testing scenarios

## 🔧 Core Technologies

- **Backend**: Python (Flask)
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Machine Learning**: scikit-learn, pandas, numpy
- **AI & Computer Vision**: DeepFace (facial emotion recognition)
- **NLP**: VADER sentiment analysis, TF-IDF vectorization
- **Database**: SQLite3
- **Styling**: Tailwind CSS
- **Environment**: Nix (for IDX), pip (for standard environments)

## 🎉 Enjoy!

Your complete mental health AI companion is ready to use.

## Update

Environment setup and dependency fixes by Abiral.

- Daily update: Checked environment setup and confirmed FER2013 trainer works.
