#!/usr/bin/env python3
"""
Test script for comprehensive database integration
Tests all database functions and API endpoints
"""

import sys
import os
import time

def test_database_integration():
    """Test comprehensive database integration"""
    print("🧪 Testing Comprehensive Database Integration...")
    
    # Change to server directory and add to path
    original_dir = os.getcwd()
    server_dir = os.path.join(original_dir, 'server')
    
    try:
        os.chdir(server_dir)
        sys.path.insert(0, server_dir)
        
        # Test database helper import
        import db_helper
        from db_helper import (
            initialize_database, create_user, get_user_by_id, get_all_doctors,
            create_appointment, get_user_appointments, create_payment, update_payment_status,
            create_mood_entry, get_mood_stats, create_chat_history, get_recent_chat_history,
            create_face_emotion_record, get_face_emotion_history, save_ei_scores, get_ei_history,
            get_platform_analytics
        )
        print("✅ Database helper imported successfully")
        
        # Test database initialization
        initialize_database()
        print("✅ Database initialized successfully")
        
        # Test user functions
        print("\n🔄 Testing user functions...")
        test_user_id = f"test_user_db_{int(time.time())}"  # Unique ID with timestamp
        user_created = create_user(
            user_id=test_user_id,
            name="Test User",
            email=f"test_{int(time.time())}@example.com",  # Unique email
            password="hashed_password",
            phone="+1-555-0123",
            gender="Other"
        )
        
        if user_created:
            print(" User creation successful")
            
            # Test user retrieval
            user = get_user_by_id(test_user_id)
            if user:
                print(f" User retrieval successful: {user['name']}")
            else:
                print(" User retrieval failed")
        else:
            print(" User creation failed")
        
        # Test doctor functions
        print("\n Testing doctor functions...")
        doctors = get_all_doctors()
        print(f" Retrieved {len(doctors)} doctors")
        
        if doctors:
            doctor = doctors[0]
            print(f"   Sample doctor: {doctor['name']} - {doctor['specialty']} (${doctor['price_per_session']})")
        
        # Test appointment functions
        print("\n Testing appointment functions...")
        if doctors and user_created:
            appointment_id = create_appointment(
                user_id=test_user_id,
                doctor_id=doctors[0]['id'],
                appointment_date="2024-02-01",
                appointment_time="10:00",
                notes="Test appointment"
            )
            
            if appointment_id:
                print(f" Appointment creation successful: {appointment_id}")
                
                # Test appointment retrieval
                user_appointments = get_user_appointments(test_user_id)
                print(f" Retrieved {len(user_appointments)} appointments for user")
                
                # Test payment creation
                payment_id = create_payment(
                    user_id=test_user_id,
                    appointment_id=appointment_id,
                    amount=doctors[0]['price_per_session'],
                    payment_method="card",
                    transaction_id="test_txn_123",
                    card_last_four="1234"
                )
                
                if payment_id:
                    print(f" Payment creation successful: {payment_id}")
                    
                    # Update payment status
                    payment_updated = update_payment_status(payment_id, "completed")
                    if payment_updated:
                        print(" Payment status update successful")
                else:
                    print(" Payment creation failed")
            else:
                print(" Appointment creation failed")
        
        # Test mood tracking functions
        print("\n Testing mood tracking functions...")
        mood_entry_id = create_mood_entry(test_user_id, 4, "Feeling good today!")
        if mood_entry_id:
            print(f" Mood entry creation successful: {mood_entry_id}")
            
            # Test mood statistics
            mood_stats = get_mood_stats(test_user_id)
            print(f" Mood statistics: {mood_stats['total_entries']} entries, avg: {mood_stats.get('average_mood', 'N/A')}")
        else:
            print(" Mood entry creation failed")
        
        # Test chat history functions
        print("\n Testing chat history functions...")
        chat_id = create_chat_history(
            user_id=test_user_id,
            user_message="Hello, I need help",
            ai_response="I'm here to help you. How are you feeling?",
            sentiment="neutral"
        )
        
        if chat_id:
            print(f" Chat history creation successful: {chat_id}")
            
            # Test chat retrieval
            chat_history = get_recent_chat_history(test_user_id, 5)
            print(f" Retrieved {len(chat_history)} chat messages")
        else:
            print(" Chat history creation failed")
        
        # Test emotion detection functions
        print("\n Testing emotion detection functions...")
        emotion_id = create_face_emotion_record(
            user_id=test_user_id,
            detected_emotion="happy",
            confidence_score=0.85
        )
        
        if emotion_id:
            print(f" Emotion record creation successful: {emotion_id}")
            
            # Test emotion history
            emotion_history = get_face_emotion_history(test_user_id, 5)
            print(f" Retrieved {len(emotion_history)} emotion records")
        else:
            print(" Emotion record creation failed")
        
        # Test EI functions
        print("\n Testing emotional intelligence functions...")
        ei_id = save_ei_scores(test_user_id, 75.5, 68.2)
        if ei_id:
            print(f" EI scores saved successfully: {ei_id}")
            
            # Test EI history
            ei_history = get_ei_history(test_user_id)
            print(f" Retrieved {len(ei_history)} EI records")
        else:
            print(" EI scores saving failed")
        
        # Test analytics functions
        print("\n Testing analytics functions...")
        analytics = get_platform_analytics()
        print(" Platform analytics retrieved:")
        print(f"   Users: {analytics['users']['total']} total, {analytics['users']['new_today']} new today")
        print(f"   Appointments: {analytics['appointments']['total']} total, {analytics['appointments']['completed']} completed")
        print(f"   Revenue: ${analytics['revenue']['total']} {analytics['revenue']['currency']}")
        print(f"   Mood entries: {analytics['mood_tracking']['total_entries']}")
        
        print("\n🎉 Comprehensive Database Integration Test Complete!")
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
    success = test_database_integration()
    sys.exit(0 if success else 1)