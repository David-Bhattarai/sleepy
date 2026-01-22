import json
import pickle
import os
import re
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import numpy as np
from collections import Counter

class AuraMLModelRealistic:
    def __init__(self, intents_file='intents.json'):
        self.intents_file = intents_file
        self.model = None
        self.intents_data = []
        self.model_path = 'aura_model_80percent.pkl'
        self.trained = False
        
    def load_intents(self):
        """Load ALL intents from JSON file"""
        try:
            with open(self.intents_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.intents_data = data.get('intents', [])
                print(f"✅ Loaded {len(self.intents_data)} intents from {self.intents_file}")
                
                # Print intent summary
                for intent in self.intents_data:
                    tag = intent.get('tag', 'unknown')
                    patterns_count = len(intent.get('patterns', []))
                    responses_count = len(intent.get('responses', []))
                    print(f"   - {tag}: {patterns_count} patterns, {responses_count} responses")
                
                return True
        except Exception as e:
            print(f"❌ Error loading intents: {e}")
            return False
    
    def preprocess_text(self, text):
        """Advanced text preprocessing for mental health context"""
        if not text:
            return ""
            
        text = text.lower().strip()
        
        # Handle contractions properly
        contractions = {
            "i'm": "i am", "you're": "you are", "it's": "it is", "that's": "that is",
            "what's": "what is", "can't": "cannot", "won't": "will not", 
            "don't": "do not", "doesn't": "does not", "didn't": "did not",
            "isn't": "is not", "aren't": "are not", "wasn't": "was not",
            "weren't": "were not", "haven't": "have not", "hasn't": "has not",
            "hadn't": "had not", "wouldn't": "would not", "shouldn't": "should not",
            "couldn't": "could not", "i'll": "i will", "you'll": "you will",
            "he'll": "he will", "she'll": "she will", "we'll": "we will",
            "they'll": "they will", "i'd": "i would", "you'd": "you would",
            "he'd": "he would", "she'd": "she would", "we'd": "we would",
            "they'd": "they would", "i've": "i have", "you've": "you have",
            "we've": "we have", "they've": "they have"
        }
        
        for contraction, expansion in contractions.items():
            text = text.replace(contraction, expansion)
        
        # Keep important punctuation for mental health context
        text = re.sub(r'[^\w\s\?\!\.]', ' ', text)
        text = ' '.join(text.split())
        
        return text.strip()
    
    def create_comprehensive_training_data(self):
        """Create comprehensive training data from ALL intents"""
        patterns = []
        labels = []
        
        print("🔄 Creating comprehensive training data...")
        
        for intent in self.intents_data:
            tag = intent.get('tag', '')
            intent_patterns = intent.get('patterns', [])
            
            if not tag or not intent_patterns:
                continue
                
            print(f"   Processing intent '{tag}' with {len(intent_patterns)} patterns")
            
            for pattern in intent_patterns:
                if pattern and pattern.strip():
                    # Add original pattern
                    processed = self.preprocess_text(pattern)
                    if processed:
                        patterns.append(processed)
                        labels.append(tag)
                        
                        # Add variations for better training
                        variations = self.create_pattern_variations(pattern)
                        for variation in variations:
                            processed_var = self.preprocess_text(variation)
                            if processed_var and processed_var != processed:
                                patterns.append(processed_var)
                                labels.append(tag)
        
        print(f"✅ Created {len(patterns)} training samples from {len(set(labels))} intents")
        return patterns, labels
    
    def create_pattern_variations(self, pattern):
        """Create variations of patterns for robust training"""
        variations = []
        
        # Punctuation variations
        if not pattern.endswith(('?', '.', '!')):
            variations.extend([pattern + '?', pattern + '.', pattern + '!'])
        
        # Case variations
        variations.extend([
            pattern.lower(),
            pattern.upper(),
            pattern.capitalize(),
            pattern.title()
        ])
        
        # Common word substitutions for mental health
        substitutions = {
            'anxious': ['worried', 'nervous', 'stressed', 'concerned'],
            'sad': ['unhappy', 'depressed', 'down', 'blue', 'upset'],
            'happy': ['glad', 'joyful', 'cheerful', 'pleased', 'good'],
            'angry': ['mad', 'furious', 'upset', 'irritated'],
            'help': ['assist', 'support', 'aid', 'guidance'],
            'feel': ['am', 'feeling', 'sense'],
            'very': ['really', 'extremely', 'quite', 'so'],
            'hello': ['hi', 'hey', 'greetings'],
            'thank you': ['thanks', 'appreciate', 'grateful']
        }
        
        pattern_lower = pattern.lower()
        for original, replacements in substitutions.items():
            if original in pattern_lower:
                for replacement in replacements:
                    new_pattern = pattern_lower.replace(original, replacement)
                    variations.append(new_pattern)
        
        return list(set(variations))
    
    def train_comprehensive_model(self):
        """Train model on ALL intents.json data for maximum accuracy"""
        print("🚀 Starting comprehensive model training...")
        
        if not self.load_intents():
            return False
        
        # Create training data
        X, y = self.create_comprehensive_training_data()
        
        if len(X) == 0:
            print("❌ No training data available")
            return False
        
        # Filter intents with minimum samples
        label_counts = Counter(y)
        valid_labels = {label for label, count in label_counts.items() if count >= 2}
        
        X_filtered = [x for x, label in zip(X, y) if label in valid_labels]
        y_filtered = [label for label in y if label in valid_labels]
        
        print(f"📊 Training with {len(X_filtered)} samples, {len(valid_labels)} intents")
        
        # Create advanced pipeline
        self.model = Pipeline([
            ('tfidf', TfidfVectorizer(
                ngram_range=(1, 4),  # 1-4 grams for context
                max_features=5000,   # More features
                stop_words=None,     # Keep all words for mental health
                min_df=1,
                max_df=0.95,
                sublinear_tf=True,
                lowercase=True,
                token_pattern=r'\b\w+\b'
            )),
            ('classifier', MultinomialNB(alpha=0.01))  # Low smoothing for precision
        ])
        
        # Train model
        try:
            if len(X_filtered) >= 20:
                # Use train-test split for evaluation
                X_train, X_test, y_train, y_test = train_test_split(
                    X_filtered, y_filtered, test_size=0.2, random_state=42, 
                    stratify=y_filtered
                )
                
                print("🔄 Training model...")
                self.model.fit(X_train, y_train)
                
                # Evaluate
                y_pred = self.model.predict(X_test)
                accuracy = accuracy_score(y_test, y_pred)
                print(f"📈 Test Accuracy: {accuracy:.3f} ({accuracy*100:.1f}%)")
                
                # If accuracy is low, retrain on full dataset
                if accuracy < 0.85:
                    print("🔄 Retraining on full dataset for better accuracy...")
                    self.model.fit(X_filtered, y_filtered)
                    y_pred_full = self.model.predict(X_filtered)
                    accuracy = accuracy_score(y_filtered, y_pred_full)
                    print(f"📈 Full Dataset Accuracy: {accuracy:.3f} ({accuracy*100:.1f}%)")
            else:
                # Small dataset - use full training
                print("🔄 Training on full dataset...")
                self.model.fit(X_filtered, y_filtered)
                y_pred = self.model.predict(X_filtered)
                accuracy = accuracy_score(y_filtered, y_pred)
                print(f"📈 Training Accuracy: {accuracy:.3f} ({accuracy*100:.1f}%)")
            
            # Save model
            self.save_comprehensive_model()
            self.trained = True
            
            print(f"✅ Model training completed with {accuracy*100:.1f}% accuracy!")
            return True
            
        except Exception as e:
            print(f"❌ Training error: {e}")
            return False
    
    def save_comprehensive_model(self):
        """Save the comprehensive model"""
        try:
            model_data = {
                'model': self.model,
                'intents_data': self.intents_data,
                'trained': True,
                'version': '2.0_comprehensive'
            }
            
            with open(self.model_path, 'wb') as f:
                pickle.dump(model_data, f)
            print(f"💾 Comprehensive model saved to {self.model_path}")
        except Exception as e:
            print(f"❌ Error saving model: {e}")
    
    def load_comprehensive_model(self):
        """Load the comprehensive model"""
        try:
            if os.path.exists(self.model_path):
                with open(self.model_path, 'rb') as f:
                    model_data = pickle.load(f)
                
                if isinstance(model_data, dict):
                    self.model = model_data.get('model')
                    self.intents_data = model_data.get('intents_data', [])
                    self.trained = model_data.get('trained', False)
                    version = model_data.get('version', '1.0')
                    print(f"✅ Comprehensive model loaded (version: {version})")
                else:
                    # Legacy format
                    self.model = model_data
                    self.load_intents()
                    print("⚠️  Legacy model loaded - consider retraining")
                
                return True
        except Exception as e:
            print(f"❌ Error loading model: {e}")
        return False
    
    def predict_intent_advanced(self, user_message, confidence_threshold=0.15):
        """Advanced intent prediction with comprehensive model"""
        if not self.model:
            if not self.load_comprehensive_model():
                print("❌ Model not available")
                return None, 0.0
        
        if not self.intents_data:
            self.load_intents()
        
        processed_message = self.preprocess_text(user_message)
        if not processed_message:
            return None, 0.0
        
        try:
            # Get prediction probabilities
            probabilities = self.model.predict_proba([processed_message])[0]
            classes = self.model.classes_
            
            # Get top predictions
            top_indices = np.argsort(probabilities)[::-1][:3]
            
            best_idx = top_indices[0]
            predicted_tag = classes[best_idx]
            confidence = probabilities[best_idx]
            
            # Enhanced confidence calculation
            if len(probabilities) > 1:
                second_best = probabilities[top_indices[1]] if len(top_indices) > 1 else 0
                confidence_gap = confidence - second_best
                
                # Boost confidence if clear winner
                if confidence_gap > 0.2:
                    confidence = min(confidence * 1.1, 1.0)
            
            print(f"🎯 Prediction: {predicted_tag} (confidence: {confidence:.3f})")
            
            if confidence >= confidence_threshold:
                return predicted_tag, confidence
            else:
                print(f"⚠️  Low confidence ({confidence:.3f}) - using fallback")
                return None, confidence
                
        except Exception as e:
            print(f"❌ Prediction error: {e}")
            return None, 0.0
    
    def get_intent_response(self, predicted_tag):
        """Get response for predicted intent"""
        for intent in self.intents_data:
            if intent.get('tag') == predicted_tag:
                responses = intent.get('responses', [])
                if responses:
                    response = random.choice(responses)
                    print(f"📝 Response from intent '{predicted_tag}': {response[:50]}...")
                    return response
        return None
    
    def generate_ml_response(self, user_message):
        """Generate response using comprehensive ML model"""
        print(f"🤖 Processing: '{user_message}'")
        
        predicted_tag, confidence = self.predict_intent_advanced(user_message)
        
        if predicted_tag:
            response = self.get_intent_response(predicted_tag)
            if response:
                return response, confidence, predicted_tag
        
        # Enhanced fallback responses
        fallback_responses = [
            "I'm here to listen. Can you tell me more about how you're feeling?",
            "That's interesting. What else is on your mind?", 
            "I understand. Would you like to explore this further?",
            "Thank you for sharing. How does that make you feel?",
            "I'm not sure I understand completely. Could you tell me more?"
        ]
        
        fallback_response = random.choice(fallback_responses)
        print(f"🔄 Using fallback response: {fallback_response[:50]}...")
        return fallback_response, 0.0, "fallback"

# Global model instance
aura_comprehensive_model = None

def get_realistic_ml_model():
    """Get the comprehensive ML model instance"""
    global aura_comprehensive_model
    if aura_comprehensive_model is None:
        aura_comprehensive_model = AuraMLModelRealistic()
        
        # Try to load existing model
        if not aura_comprehensive_model.load_comprehensive_model():
            print("🔄 Training new comprehensive model on ALL intents.json data...")
            success = aura_comprehensive_model.train_comprehensive_model()
            if success:
                print("🎉 Comprehensive ML model trained successfully!")
            else:
                print("❌ Failed to train comprehensive ML model")
        else:
            print("✅ Comprehensive ML model ready!")
    
    return aura_comprehensive_model

# Force retrain function
def force_retrain_model():
    """Force retrain the model"""
    global aura_comprehensive_model
    aura_comprehensive_model = AuraMLModelRealistic()
    
    # Remove old model
    if os.path.exists(aura_comprehensive_model.model_path):
        os.remove(aura_comprehensive_model.model_path)
        print("🗑️  Removed old model")
    
    # Train new model
    success = aura_comprehensive_model.train_comprehensive_model()
    return success