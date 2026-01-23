#!/usr/bin/env python3
"""
Test script to check actual accuracy of intents.json dataset
"""

import json
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, classification_report
from collections import Counter
import re

def preprocess_text(text):
    """Simple text preprocessing"""
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    return text.strip()

def load_and_test_intents():
    """Load intents and test actual accuracy"""
    
    # Load intents
    with open('server/intents.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    intents = data['intents']
    print(f" Loaded {len(intents)} intents")
    
    # Prepare data
    patterns = []
    tags = []
    
    for intent in intents:
        tag = intent['tag']
        for pattern in intent['patterns']:
            if pattern.strip():
                patterns.append(preprocess_text(pattern))
                tags.append(tag)
    
    print(f" Total patterns: {len(patterns)}")
    print(f" Unique intents: {len(set(tags))}")
    
    # Check class distribution
    class_counts = Counter(tags)
    print(f"\n Class distribution:")
    print(f"  Classes with 1 sample: {sum(1 for count in class_counts.values() if count == 1)}")
    print(f"  Classes with 2+ samples: {sum(1 for count in class_counts.values() if count >= 2)}")
    print(f"  Average samples per class: {np.mean(list(class_counts.values())):.1f}")
    
    # Show some examples
    print(f"\n Sample patterns:")
    for i in range(min(5, len(patterns))):
        print(f"  '{patterns[i]}' -> {tags[i]}")
    
    if len(patterns) < 10:
        print(" Dataset too small for meaningful ML training")
        return
    
    # Create model
    model = Pipeline([
        ('tfidf', TfidfVectorizer(
            ngram_range=(1, 2),
            max_features=min(500, len(patterns)),
            stop_words='english',
            min_df=1
        )),
        ('classifier', MultinomialNB(alpha=1.0))
    ])
    
    X = np.array(patterns)
    y = np.array(tags)
    
    # Check if we can do train-test split
    min_samples = min(class_counts.values())
    
    if min_samples >= 2 and len(patterns) >= 20:
        # Train-test split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        print(f"\n Train-Test Split Results:")
        print(f"  Training samples: {len(X_train)}")
        print(f"  Testing samples: {len(X_test)}")
        print(f"  Test Accuracy: {accuracy:.3f} ({accuracy*100:.1f}%)")
        
    else:
        print(f"\n Dataset too small for train-test split")
        print(f"   Using full dataset training...")
        
        model.fit(X, y)
        y_pred = model.predict(X)
        accuracy = accuracy_score(y, y_pred)
        
        print(f"  Training Accuracy: {accuracy:.3f} ({accuracy*100:.1f}%)")
    
    # Cross-validation if possible
    if len(set(y)) >= 3 and len(patterns) >= 15:
        try:
            cv_scores = cross_val_score(model, X, y, cv=min(3, len(patterns)//5), scoring='accuracy')
            print(f"\n Cross-Validation Results:")
            print(f"  CV Scores: {[f'{score:.3f}' for score in cv_scores]}")
            print(f"  Mean CV Accuracy: {cv_scores.mean():.3f} ± {cv_scores.std():.3f}")
            print(f"  CV Accuracy: {cv_scores.mean()*100:.1f}% ± {cv_scores.std()*100:.1f}%")
        except Exception as e:
            print(f"   Cross-validation failed: {e}")
    
    # Test with sample inputs
    print(f"\n🧪 Testing with sample inputs:")
    test_messages = [
        "Hi there",
        "I feel sad",
        "I am stressed",
        "Thank you",
        "What is depression?",
        "I need help"
    ]
    
    for msg in test_messages:
        try:
            processed_msg = preprocess_text(msg)
            predicted_tag = model.predict([processed_msg])[0]
            confidence = model.predict_proba([processed_msg])[0].max()
            print(f"  '{msg}' -> {predicted_tag} (confidence: {confidence:.3f})")
        except Exception as e:
            print(f"  '{msg}' -> Error: {e}")
    
    return accuracy if 'accuracy' in locals() else 0.0

if __name__ == "__main__":
    print(" AURA Intents.json Dataset Accuracy Test")
    print("=" * 50)
    
    try:
        final_accuracy = load_and_test_intents()
        
        print(f"\n" + "=" * 50)
        print(f" FINAL RESULTS:")
        if final_accuracy >= 0.90:
            print(f" Accuracy: {final_accuracy*100:.1f}% - EXCELLENT!")
        elif final_accuracy >= 0.80:
            print(f" Accuracy: {final_accuracy*100:.1f}% - GOOD!")
        elif final_accuracy >= 0.70:
            print(f" Accuracy: {final_accuracy*100:.1f}% - ACCEPTABLE")
        else:
            print(f" Accuracy: {final_accuracy*100:.1f}% - NEEDS IMPROVEMENT")
        
        print("=" * 50)
        
    except Exception as e:
        print(f" Error: {e}")
        import traceback
        traceback.print_exc()