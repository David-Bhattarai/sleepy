#!/usr/bin/env python3
"""
Test script for mood intelligence system integration
Tests the mood intelligence system without DeepFace dependencies
"""

import sys
import os
import json

def test_mood_intelligence():
    """Test mood intelligence system functionality"""
    print("🧪 Testing Mood Intelligence System Integration...")
    
    # Change to server directory and add to path
    original_dir = os.getcwd()
    server_dir = os.path.join(original_dir, 'sleepy', 'server')
    
    try:
        os.chdir(server_dir)
        sys.path.insert(0, server_dir)
        
        # Test mood intelligence import
        import mood_intelligence
        mood_intel = mood_intelligence.get_mood_intelligence()
        print("✅ Mood intelligence system loaded successfully")
        
        # Test database initialization
        print(f"📊 Database path: {mood_intel.db_path}")
        print(f"📊 Mood categories: {len(mood_intel.mood_categories)}")
        print(f"📊 Mood patterns: {len(mood_intel.mood_patterns)}")
        
        # Test mood logging functionality
        test_user_id = "test_user_123"
        test_mood_data = {
            'mood_rating': 4,
            'mood_notes': 'Feeling good today! Had a productive morning.',
            'energy_level': 4,
            'sleep_quality': 3,
            'stress_level': 2,
            'social_interaction': 4,
            'physical_activity': 3
        }
        
        print("\n🔄 Testing mood logging...")
        result = mood_intel.log_advanced_mood(test_user_id, test_mood_data)
        
        if result['success']:
            print("✅ Mood logging successful!")
            print(f"   Entry ID: {result['entry_id']}")
            print(f"   Mood Category: {result['mood_category']['label']} {result['mood_category']['emoji']}")
            
            # Test insights generation
            insights = result['immediate_insights']
            print(f"   Wellness Score: {insights['mood_interpretation']['wellness_score']}")
            print(f"   State: {insights['mood_interpretation']['state']}")
            print(f"   Recommendations: {len(insights['recommendations'])}")
            
        else:
            print(f"❌ Mood logging failed: {result.get('error', 'Unknown error')}")
            return False
        
        # Test analytics generation
        print("\n🔄 Testing analytics generation...")
        analytics = mood_intel.get_comprehensive_analytics(test_user_id, days=30)
        
        if 'error' not in analytics:
            print("✅ Analytics generation successful!")
            if 'summary' in analytics:
                summary = analytics['summary']
                print(f"   Total entries: {summary['total_entries']}")
                print(f"   Average mood: {summary['average_mood']}")
                print(f"   Mood trend: {summary['mood_trend']}")
        else:
            print(f"❌ Analytics generation failed: {analytics.get('error', 'Unknown error')}")
        
        # Test ML model integration
        print("\n🔄 Testing ML model integration...")
        try:
            import ml_model_realistic
            ml_model = ml_model_realistic.get_realistic_ml_model()
            
            if ml_model and hasattr(ml_model, 'model') and ml_model.model:
                print("✅ ML model loaded and trained successfully")
                
                # Test ML response generation
                test_message = "I'm feeling anxious about work today"
                response, confidence, tag = ml_model.generate_ml_response(test_message)
                print(f"   Test message: '{test_message}'")
                print(f"   ML Response: '{response[:50]}...'")
                print(f"   Confidence: {confidence:.3f}")
                print(f"   Predicted tag: {tag}")
            else:
                print("⚠️  ML model not properly trained")
                
        except Exception as e:
            print(f"❌ ML model test failed: {e}")
        
        print("\n🎉 Mood Intelligence System Integration Test Complete!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        # Restore original directory
        os.chdir(original_dir)

if __name__ == "__main__":
    success = test_mood_intelligence()
    sys.exit(0 if success else 1)