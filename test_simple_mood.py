#!/usr/bin/env python3
"""
Test script for simple mood tracker
Tests basic database operations without ML logic
"""

import sys
import os

def test_simple_mood_tracker():
    """Test simple mood tracker functionality"""
    print("🧪 Testing Simple Mood Tracker...")
    
    # Change to server directory and add to path
    original_dir = os.getcwd()
    server_dir = os.path.join(original_dir, 'sleepy', 'server')
    
    try:
        os.chdir(server_dir)
        sys.path.insert(0, server_dir)
        
        # Test simple mood tracker import
        import simple_mood_tracker
        tracker = simple_mood_tracker.get_simple_mood_tracker()
        print("✅ Simple mood tracker loaded successfully")
        
        # Test mood logging
        test_user_id = "test_user_simple"
        
        print("\n🔄 Testing mood logging...")
        result1 = tracker.add_mood_entry(test_user_id, 4, "Feeling good today!")
        result2 = tracker.add_mood_entry(test_user_id, 3, "Just okay")
        result3 = tracker.add_mood_entry(test_user_id, 5, "Amazing day!")
        
        if all(r['success'] for r in [result1, result2, result3]):
            print("✅ Mood logging successful!")
            print(f"   Entry 1: {result1['mood_info']['label']} {result1['mood_info']['emoji']}")
            print(f"   Entry 2: {result2['mood_info']['label']} {result2['mood_info']['emoji']}")
            print(f"   Entry 3: {result3['mood_info']['label']} {result3['mood_info']['emoji']}")
        else:
            print("❌ Mood logging failed")
            return False
        
        # Test getting user moods
        print("\n🔄 Testing mood retrieval...")
        moods = tracker.get_user_moods(test_user_id, days=30)
        print(f"✅ Retrieved {len(moods)} mood entries")
        
        # Test mood statistics
        print("\n🔄 Testing mood statistics...")
        stats = tracker.get_mood_stats(test_user_id, days=30)
        
        if 'error' not in stats:
            print("✅ Mood statistics generated!")
            print(f"   Total entries: {stats['total_entries']}")
            print(f"   Average mood: {stats['average_mood']}")
            print(f"   Highest mood: {stats['highest_mood']}")
            print(f"   Lowest mood: {stats['lowest_mood']}")
            print(f"   Mood counts: {stats['mood_counts']}")
        else:
            print(f"❌ Statistics failed: {stats.get('error')}")
        
        # Test chart data
        print("\n🔄 Testing chart data...")
        chart_data = tracker.get_mood_chart_data(test_user_id, days=30)
        
        if chart_data['labels'] and chart_data['data']:
            print("✅ Chart data generated!")
            print(f"   Data points: {len(chart_data['data'])}")
            print(f"   Labels: {chart_data['labels']}")
            print(f"   Data: {chart_data['data']}")
        else:
            print("⚠️  No chart data available")
        
        # Test mood deletion
        print("\n🔄 Testing mood deletion...")
        if moods:
            entry_id = moods[0]['id']
            delete_result = tracker.delete_mood_entry(test_user_id, entry_id)
            
            if delete_result['success']:
                print("✅ Mood deletion successful!")
            else:
                print(f"❌ Mood deletion failed: {delete_result.get('message')}")
        
        print("\n🎉 Simple Mood Tracker Test Complete!")
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
    success = test_simple_mood_tracker()
    sys.exit(0 if success else 1)