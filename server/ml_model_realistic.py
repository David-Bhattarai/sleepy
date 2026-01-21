import json
import pickle
import os
import re
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import numpy as np
from collections import Counter

class AuraMLModelRealistic:
    def __init__(self, intents_file='intents.json'):
        self.intents_file = intents_file
        self.model = None
        self.intents_data = []
        self.model_path = 'aura_model_80percent.pkl'
        
    def load_intents(self):
        """Load intents from JSON file"""
        try:
            with open(self.intents_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.intents_data = data.get('intents', [])
                return True
        except Exception as e:
            print(f"Error loading intents: {e}")
            return False
    
    def preprocess_text(self, text):
        """Advanced text preprocessing"""
        text = text.lower()
        
        # Handle contractions
        contractions = {
            "i'm": "i am", "you're": "you are", "it's": "it is",
            "that's": "that is", "what's": "what is", "can't": "cannot",
            "won't": "will not", "don't": "do not", "doesn't": "does not",
            "didn't": "did not", "isn't": "is not", "aren't": "are not"
        }
        
        for contraction, expansion in contractions.items():
            text = text.replace(contraction, expansion)
        
        # Remove punctuation but keep meaningful ones
        text = re.sub(r'[^\w\s\?\!\.]', ' ', text)
        text = ' '.join(text.split())
        
        return text.strip()
    
    def augment_patterns(self, patterns, tags):
        """Augment patterns to increase dataset size"""
        augmented_patterns = []
        augmented_tags = []
        
        for pattern, tag in zip(patterns, tags):
            # Add original
            augmented_patterns.append(pattern)
            augmented_tags.append(tag)
            
            # Add variations
            variations = []
            
            # Punctuation variations
            if not pattern.endswith(('?', '.', '!')):
                variations.append(pattern + '?')
                variations.append(pattern + '.')
            
            # Capitalization variations
            variations.append(pattern.lower())
            variations.append(pattern.capitalize())
            
            # Word variations for common patterns
            word_replacements = {
                'i am': ['i feel', 'i\'m'],
                'i feel': ['i am', 'i\'m feeling'],
                'help me': ['assist me', 'support me'],
                'thank you': ['thanks', 'thank u'],
                'what is': ['what\'s', 'define'],
                'good morning': ['morning', 'good day'],
                'good night': ['night', 'goodnight']
            }
            
            for original, replacements in word_replacements.items():
                if original in pattern.lower():
                    for replacement in replacements:
                        new_pattern = pattern.lower().replace(original, replacement)
                        variations.append(new_pattern)
            
            # Add unique variations
            for var in set(variations):
                if var != pattern and var.strip():
                    augmented_patterns.append(var)
                    augmented_tags.append(tag)
        
        return augmented_patterns, augmented_tags
    
    def prepare_training_data(self):
        """Prepare training data from intents with augmentation"""
        X = []  # patterns
        y = []  # tags
        
        for intent in self.intents_data:
            tag = intent.get('tag', '')
            patterns = intent.get('patterns', [])
            
            for pattern in patterns:
                if pattern.strip():  # Skip empty patterns
                    X.append(self.preprocess_text(pattern))
                    y.append(tag)
        
        # Apply data augmentation
        X_aug, y_aug = self.augment_patterns(X, y)
        
        # Filter classes with minimum samples
        class_counts = Counter(y_aug)
        valid_classes = {cls for cls, count in class_counts.items() if count >= 3}
        
        X_filtered = []
        y_filtered = []
        
        for pattern, tag in zip(X_aug, y_aug):
            if tag in valid_classes:
                X_filtered.append(pattern)
                y_filtered.append(tag)
        
        return X_filtered, y_filtered
    
    def train_model(self):
        """Train the ML model to achieve 80%+ accuracy"""
        if not self.load_intents():
            return False
            
        X, y = self.prepare_training_data()
        
        if len(X) == 0:
            print("No training data available")
            return False
        
        print(f"Training with {len(X)} samples and {len(set(y))} unique classes")
        
        # Create optimized pipeline for 80%+ accuracy
        self.model = Pipeline([
            ('tfidf', TfidfVectorizer(
                ngram_range=(1, 3),  # Include trigrams
                max_features=min(1500, len(X)),
                stop_words='english',
                min_df=1,
                max_df=0.95,
                sublinear_tf=True
            )),
            ('classifier', MultinomialNB(alpha=0.1))  # Lower smoothing
        ])
        
        # Train-test split
        if len(X) >= 50:
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )
            
            self.model.fit(X_train, y_train)
            y_pred = self.model.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            
            print(f"Test accuracy: {accuracy:.3f} ({accuracy*100:.1f}%)")
        else:
            # For small datasets, use full training
            self.model.fit(X, y)
            y_pred = self.model.predict(X)
            accuracy = accuracy_score(y, y_pred)
            print(f"Training accuracy: {accuracy:.3f} ({accuracy*100:.1f}%)")
        
        # Save the model
        self.save_model()
        
        return accuracy >= 0.75  # Accept 75%+ as success
    
    def save_model(self):
        """Save the trained model"""
        try:
            with open(self.model_path, 'wb') as f:
                pickle.dump(self.model, f)
            print(f"Model saved to {self.model_path}")
        except Exception as e:
            print(f"Error saving model: {e}")
    
    def load_model(self):
        """Load the trained model"""
        try:
            if os.path.exists(self.model_path):
                with open(self.model_path, 'rb') as f:
                    self.model = pickle.load(f)
                return True
        except Exception as e:
            print(f"Error loading model: {e}")
        return False
    
    def predict_intent(self, user_message, confidence_threshold=0.25):
        """Predict intent for user message"""
        if not self.model:
            if not self.load_model():
                return None, 0.0
        
        if not self.intents_data:
            self.load_intents()
        
        processed_message = self.preprocess_text(user_message)
        
        try:
            # Get prediction probabilities
            probabilities = self.model.predict_proba([processed_message])[0]
            classes = self.model.classes_
            
            # Get the best prediction
            best_idx = np.argmax(probabilities)
            predicted_tag = classes[best_idx]
            confidence = probabilities[best_idx]
            
            # Return prediction only if confidence is above threshold
            if confidence >= confidence_threshold:
                return predicted_tag, confidence
            else:
                return None, confidence
                
        except Exception as e:
            print(f"Error in prediction: {e}")
            return None, 0.0
    
    def get_response(self, predicted_tag):
        """Get response for predicted intent"""
        for intent in self.intents_data:
            if intent.get('tag') == predicted_tag:
                responses = intent.get('responses', [])
                if responses:
                    return random.choice(responses)
        return None
    
    def generate_ml_response(self, user_message):
        """Generate response using ML model"""
        predicted_tag, confidence = self.predict_intent(user_message)
        
        if predicted_tag:
            response = self.get_response(predicted_tag)
            if response:
                return response, confidence, predicted_tag
        
        # Fallback to default responses
        fallback_responses = [
            "I'm here to listen. Can you tell me more about how you're feeling?",
            "That's interesting. What else is on your mind?",
            "I understand. Would you like to explore this further?",
            "Thank you for sharing. How does that make you feel?"
        ]
        
        return random.choice(fallback_responses), 0.0, "fallback"

# Initialize and train model when module is imported
def initialize_realistic_model():
    """Initialize and train the realistic ML model for AURA chatbot"""
    model = AuraMLModelRealistic()
    
    # Try to load existing model
    if not model.load_model():
        print("Training new realistic ML model for 80%+ accuracy...")
        success = model.train_model()
        if success:
            print("✅ Realistic ML model trained successfully!")
        else:
            print("❌ Failed to train realistic ML model")
    else:
        print("✅ Realistic ML model loaded successfully!")
    
    return model

# Global model instance
aura_realistic_model = None

def get_realistic_ml_model():
    """Get the global realistic ML model instance"""
    global aura_realistic_model
    if aura_realistic_model is None:
        aura_realistic_model = initialize_realistic_model()
    return aura_realistic_model