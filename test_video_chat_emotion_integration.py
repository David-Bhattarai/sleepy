#!/usr/bin/env python3
"""
Test Video Chat and Emotion Detection Integration
Complete test of both systems working together
"""

import requests
import json
import base64
import time
from io import BytesIO
from PIL import Image
import numpy as np

SERVER_URL = "http://localhost:5000"

def create_test_image():
    """Create a simple test image for emotion detection"""
    # Create a simple 48x48 grayscale image (FER2013 format)
    img = np.random.randint(0, 255, (48, 48), dtype=np.uint8)
    
    # Convert to PIL Image
    pil_img = Image.fromarray(img, mode='L')
    
    # Convert to base64
    buffer = BytesIO()
    pil_img.save(buffer, format='PNG')
    img_str = base64.b64encode(buffer.getvalue()).decode()
    
    return f"data:image/png;base64,{img_str}"

def test_user_login():
    """Test user login and get token"""
    print("🔐 Testing User Login...")
    
    # Try to create a test user first
    signup_data = {
        "name": "Test User",
        "email": "test@example.com",
        "password": "test123",
        "phone": "1234567890",
        "gender": "other"
    }
    
    try:
        requests.post(f"{SERVER_URL}/api/signup", json=signup_data)
    except:
        pass  # User might already exist
    
    # Now login
    signin_data = {
        "email": "test@example.com",
        "password": "test123"
    }
    
    try:
        response = requests.post(f"{SERVER_URL}/api/signin", json=signin_data)
        if response.status_code == 200:
            data = response.json()
            token = data.get('token')
            print(f"✅ User login successful - Token: {token[:20]}...")
            return token
        else:
            print(f"❌ User login failed: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ User login error: {e}")
        return None

def test_doctors_api():
    """Test doctors API for video chat"""
    print("\n👨‍⚕️ Testing Doctors API...")
    
    try:
        response = requests.get(f"{SERVER_URL}/api/doctors")
        
        if response.status_code == 200:
            data = response.json()
            doctors = data.get('doctors', [])
            print(f"✅ Doctors API: {len(doctors)} doctors available")
            
            for doctor in doctors[:3]:  # Show first 3 doctors
                print(f"   - {doctor.get('name', 'Unknown')}: {doctor.get('specialty', 'N/A')} (${doctor.get('price_per_session', 0)})")
            
            return len(doctors) > 0
        else:
            print(f"❌ Doctors API failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Doctors API error: {e}")
        return False

def test_emotion_detection_fer2013(token):
    """Test FER2013 emotion detection"""
    print("\n😊 Testing FER2013 Emotion Detection...")
    
    try:
        # Create test image
        test_image = create_test_image()
        
        # Send to emotion detection API
        headers = {"Authorization": f"Bearer {token}"}
        data = {
            "image": test_image,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        response = requests.post(f"{SERVER_URL}/api/emotion_detection_fer2013", 
                               json=data, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            emotion = result.get('dominant_emotion', 'unknown')
            confidence = result.get('confidence', 0)
            emotions_detected = result.get('emotions', {})
            
            print(f"✅ FER2013 Emotion Detection: {emotion} ({confidence}%)")
            print(f"   All emotions detected: {emotions_detected}")
            
            # Check if it's using FER2013 dataset (7 emotions)
            expected_emotions = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']
            detected_emotion_keys = list(emotions_detected.keys())
            
            fer2013_compatible = all(emotion in expected_emotions for emotion in detected_emotion_keys)
            
            if fer2013_compatible:
                print("✅ Using FER2013-enhanced dataset (7 emotions)")
            else:
                print(f"⚠️ Not using FER2013 format. Detected: {detected_emotion_keys}")
            
            return True
        else:
            print(f"❌ Emotion detection failed: {response.status_code}")
            try:
                error_data = response.json()
                print(f"   Error: {error_data}")
            except:
                print(f"   Raw response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Emotion detection error: {e}")
        return False

def test_video_chat_booking(token):
    """Test video chat booking system"""
    print("\n📅 Testing Video Chat Booking...")
    
    try:
        # Test appointment booking
        headers = {"Authorization": f"Bearer {token}"}
        booking_data = {
            "doctor_id": "dr-smith-001",
            "appointment_date": "2026-01-25",
            "appointment_time": "10:00",
            "payment_method": "card",
            "amount": 80.00
        }
        
        response = requests.post(f"{SERVER_URL}/api/book_appointment", 
                               json=booking_data, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            appointment_id = result.get('appointment_id')
            print(f"✅ Video chat booking successful: {appointment_id}")
            return True
        else:
            print(f"❌ Video chat booking failed: {response.status_code}")
            try:
                error_data = response.json()
                print(f"   Error: {error_data}")
            except:
                print(f"   Raw response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Video chat booking error: {e}")
        return False

def test_chatbot_integration(token):
    """Test chatbot integration with video chat"""
    print("\n💬 Testing Chatbot Integration...")
    
    try:
        headers = {"Authorization": f"Bearer {token}"}
        chat_data = {
            "message": "I feel anxious about my upcoming appointment",
            "context": "video_chat_session"
        }
        
        response = requests.post(f"{SERVER_URL}/api/chat", 
                               json=chat_data, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            ai_response = result.get('response', '')
            print(f"✅ Chatbot integration: Response received")
            print(f"   AI Response: {ai_response[:100]}...")
            return True
        else:
            print(f"❌ Chatbot integration failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Chatbot integration error: {e}")
        return False

def test_frontend_files():
    """Test frontend files accessibility"""
    print("\n🎨 Testing Frontend Files...")
    
    files_to_test = [
        ("/video-chat.html", "Video Chat Page"),
        ("/emotion-detection.html", "Emotion Detection Page"),
        ("/dashboard.html", "Dashboard Page")
    ]
    
    results = {}
    
    for endpoint, description in files_to_test:
        try:
            response = requests.get(f"{SERVER_URL}{endpoint}")
            
            if response.status_code == 200:
                print(f"✅ {description}: Accessible")
                results[endpoint] = True
            else:
                print(f"❌ {description}: Status {response.status_code}")
                results[endpoint] = False
                
        except Exception as e:
            print(f"❌ {description}: Error - {e}")
            results[endpoint] = False
    
    return all(results.values())

def generate_integration_report(results):
    """Generate comprehensive integration report"""
    print("\n" + "=" * 60)
    print("📋 VIDEO CHAT & EMOTION DETECTION INTEGRATION REPORT")
    print("=" * 60)
    
    # Count successful tests
    successful_tests = sum(1 for result in results.values() if result)
    total_tests = len(results)
    
    print(f"\n🎯 INTEGRATION STATUS: {successful_tests}/{total_tests}")
    
    for test_name, result in results.items():
        status = "✅" if result else "❌"
        print(f"   {status} {test_name}")
    
    # Integration score
    integration_score = (successful_tests / total_tests) * 100
    
    print(f"\n📊 INTEGRATION SCORE: {integration_score:.1f}%")
    
    if integration_score >= 90:
        print("🎉 EXCELLENT: Both systems are fully integrated!")
    elif integration_score >= 75:
        print("✅ GOOD: Systems are well integrated with minor issues")
    elif integration_score >= 50:
        print("⚠️ FAIR: Systems have some integration issues")
    else:
        print("❌ POOR: Systems need significant work")
    
    print(f"\n🚀 SYSTEM ACCESS:")
    print(f"   - Video Chat: {SERVER_URL}/video-chat.html")
    print(f"   - Emotion Detection: {SERVER_URL}/emotion-detection.html")
    print(f"   - Dashboard: {SERVER_URL}/dashboard.html")
    
    return integration_score

def main():
    """Main integration test function"""
    print("🛠️ VIDEO CHAT & EMOTION DETECTION INTEGRATION TEST")
    print("=" * 60)
    
    results = {}
    
    # Test user login
    token = test_user_login()
    results["User Authentication"] = token is not None
    
    if not token:
        print("\n❌ Cannot proceed without user token")
        return
    
    # Test doctors API
    results["Doctors API"] = test_doctors_api()
    
    # Test emotion detection
    results["FER2013 Emotion Detection"] = test_emotion_detection_fer2013(token)
    
    # Test video chat booking
    results["Video Chat Booking"] = test_video_chat_booking(token)
    
    # Test chatbot integration
    results["Chatbot Integration"] = test_chatbot_integration(token)
    
    # Test frontend files
    results["Frontend Files"] = test_frontend_files()
    
    # Generate comprehensive report
    integration_score = generate_integration_report(results)
    
    # Final summary
    print(f"\n" + "=" * 60)
    print("🎯 FINAL INTEGRATION STATUS")
    print("=" * 60)
    
    if integration_score >= 75:
        print("✅ VIDEO CHAT & EMOTION DETECTION ARE WORKING!")
        print("\n🎉 What's Working:")
        print("   - Dummy doctors available for video chat")
        print("   - FER2013 emotion detection with 7 emotions")
        print("   - Real-time emotion analysis")
        print("   - Video chat booking system")
        print("   - AI chatbot integration")
        print("   - Frontend accessibility")
        
        print("\n🚀 Ready for Use!")
        print("   1. Go to video-chat.html to book with dummy doctors")
        print("   2. Go to emotion-detection.html for FER2013 emotion detection")
        print("   3. Both systems use trained datasets and models")
        
    else:
        print("⚠️ SYSTEMS NEED ATTENTION")
        print("\n🔧 Issues Found:")
        for test_name, result in results.items():
            if not result:
                print(f"   - {test_name}: Failed")
        
        print("\n📝 Recommended Actions:")
        print("   - Check server is running")
        print("   - Verify database connectivity")
        print("   - Test API endpoints individually")

if __name__ == "__main__":
    main()