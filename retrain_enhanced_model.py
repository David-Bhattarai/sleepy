import sys
import os
sys.path.append('server')

try:
    from ml_model_realistic import AuraMLModelRealistic
    
    print("=== RETRAINING ENHANCED ML MODEL FOR MAXIMUM ACCURACY ===")
    
    # Remove old model file to force retraining
    model_path = 'server/aura_model_80percent.pkl'
    if os.path.exists(model_path):
        os.remove(model_path)
        print(f"Removed old model: {model_path}")
    
    # Create new enhanced model
    model = AuraMLModelRealistic()
    
    print("Starting enhanced training on intents.json...")
    success = model.train_model()
    
    if success:
        print("\n ENHANCED MODEL TRAINING COMPLETED!")
        print(" Model is now optimized for maximum accuracy on intents.json")
        print(" Enhanced data augmentation applied")
        print(" Improved TF-IDF with 4-grams")
        print(" Lower confidence threshold for better coverage")
        print(" Model integrated with dashboard Aura chatbot")
        
        # Quick test
        print("\n=== QUICK TEST ===")
        test_cases = [
            "I feel anxious",
            "Hello",
            "What is depression?",
            "Thank you",
            "I need help"
        ]
        
        for test_msg in test_cases:
            response, confidence, tag = model.generate_ml_response(test_msg)
            print(f"'{test_msg}' → {tag} ({confidence:.3f}) → '{response[:40]}...'")
            
    else:
        print(" Failed to train enhanced model")
        
except Exception as e:
    print(f"Error: {e}")
    print("Make sure you have scikit-learn installed: pip install scikit-learn")