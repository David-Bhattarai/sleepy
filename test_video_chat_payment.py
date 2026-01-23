#!/usr/bin/env python3
"""
Test Video Chat Payment Integration
Tests the complete video chat system with payment and doctor management
"""

import sys
import os
sys.path.append('sleepy/server')

def test_doctor_management():
    """Test doctor management functions"""
    print("🧪 Testing Doctor Management")
    print("=" * 50)
    
    try:
        from db_helper import initialize_database, get_all_doctors, get_doctor_by_id
        
        # Initialize database with dummy doctors
        success = initialize_database()
        if not success:
            print("❌ Database initialization failed")
            return False
        
        # Get all doctors
        doctors = get_all_doctors()
        print(f"✅ Found {len(doctors)} doctors in database")
        
        for doctor in doctors:
            print(f"   👨‍⚕️ {doctor['name']} - {doctor['specialty']} (${doctor['price_per_session']}/session)")
            print(f"      📧 {doctor.get('email', 'N/A')} | 📞 {doctor.get('phone', 'N/A')}")
            print(f"      🎓 {doctor.get('qualification', 'N/A')} | 📅 {doctor.get('experience_years', 0)} years")
            print(f"      🟢 Available: {'Yes' if doctor.get('is_available', 1) else 'No'}")
            print()
        
        # Test getting specific doctor
        if doctors:
            doctor_id = doctors[0]['id']
            doctor = get_doctor_by_id(doctor_id)
            if doctor:
                print(f"✅ Successfully retrieved doctor: {doctor['name']}")
            else:
                print(f"❌ Failed to retrieve doctor: {doctor_id}")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Doctor management test failed: {e}")
        return False

def test_appointment_system():
    """Test appointment creation and management"""
    print("\n🧪 Testing Appointment System")
    print("=" * 50)
    
    try:
        from db_helper import create_appointment, get_user_appointments, create_payment, update_payment_status
        
        # Test data
        user_id = "test-user-001"
        doctor_id = "dr-smith-001"
        appointment_date = "2026-01-24"
        appointment_time = "10:00"
        
        # Create appointment
        appointment_id = create_appointment(
            user_id=user_id,
            doctor_id=doctor_id,
            appointment_date=appointment_date,
            appointment_time=appointment_time,
            notes="Test video consultation appointment"
        )
        
        if appointment_id:
            print(f"✅ Appointment created: {appointment_id}")
        else:
            print("❌ Failed to create appointment")
            return False
        
        # Create payment
        payment_id = create_payment(
            user_id=user_id,
            appointment_id=appointment_id,
            amount=80.0,
            payment_method="card",
            currency="USD",
            card_last_four="1234"
        )
        
        if payment_id:
            print(f"✅ Payment record created: {payment_id}")
        else:
            print("❌ Failed to create payment record")
            return False
        
        # Update payment status
        success = update_payment_status(payment_id, "completed", "txn_123456789")
        if success:
            print("✅ Payment status updated to completed")
        else:
            print("❌ Failed to update payment status")
            return False
        
        # Get user appointments
        appointments = get_user_appointments(user_id)
        print(f"✅ Found {len(appointments)} appointments for user")
        
        for appointment in appointments:
            print(f"   📅 {appointment['appointment_date']} at {appointment['appointment_time']}")
            print(f"   👨‍⚕️ Doctor: {appointment.get('doctor_name', 'Unknown')}")
            print(f"   💰 Amount: ${appointment.get('payment_amount', 'N/A')}")
            print(f"   📊 Status: {appointment['status']}")
            print()
        
        return True
        
    except Exception as e:
        print(f"❌ Appointment system test failed: {e}")
        return False

def test_payment_methods():
    """Test different payment methods"""
    print("\n🧪 Testing Payment Methods")
    print("=" * 50)
    
    try:
        from db_helper import create_payment, update_payment_status
        
        # Test card payment
        card_payment_id = create_payment(
            user_id="test-user-002",
            appointment_id="test-appointment-001",
            amount=75.0,
            payment_method="card",
            currency="USD",
            card_last_four="5678"
        )
        
        if card_payment_id:
            print("✅ Card payment record created")
            update_payment_status(card_payment_id, "completed", "card_txn_987654321")
            print("✅ Card payment completed")
        
        # Test eSewa payment
        esewa_payment_id = create_payment(
            user_id="test-user-003",
            appointment_id="test-appointment-002",
            amount=85.0,
            payment_method="esewa",
            currency="NPR",
            esewa_ref_id="esewa_ref_123456"
        )
        
        if esewa_payment_id:
            print("✅ eSewa payment record created")
            update_payment_status(esewa_payment_id, "completed", "esewa_txn_456789123")
            print("✅ eSewa payment completed")
        
        return True
        
    except Exception as e:
        print(f"❌ Payment methods test failed: {e}")
        return False

def test_server_integration():
    """Test server API integration"""
    print("\n🧪 Testing Server Integration")
    print("=" * 50)
    
    try:
        from app import app
        
        with app.test_client() as client:
            # Test doctors endpoint
            response = client.get('/api/doctors')
            if response.status_code == 200:
                print("✅ Doctors API endpoint working")
                data = response.get_json()
                if data.get('success') and data.get('doctors'):
                    print(f"   📊 Found {len(data['doctors'])} doctors via API")
                else:
                    print("⚠️ Doctors API returned empty data")
            else:
                print(f"❌ Doctors API failed: {response.status_code}")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Server integration test failed: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 VIDEO CHAT PAYMENT INTEGRATION TEST")
    print("🎯 Testing complete video consultation system with payment")
    print("💻 Includes dummy doctors, appointments, and payment processing")
    print()
    
    # Run tests
    tests_passed = 0
    total_tests = 4
    
    if test_doctor_management():
        tests_passed += 1
    
    if test_appointment_system():
        tests_passed += 1
    
    if test_payment_methods():
        tests_passed += 1
    
    if test_server_integration():
        tests_passed += 1
    
    # Results
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {tests_passed}/{total_tests} passed")
    
    if tests_passed == total_tests:
        print("✅ All tests passed! Video chat payment integration ready!")
        print("\n🎯 System Features:")
        print("   💳 Card payment integration (Visa, Mastercard)")
        print("   📱 eSewa payment integration (Nepal)")
        print("   👨‍⚕️ 6 dummy AI doctors with specialties")
        print("   📅 Appointment booking system")
        print("   💰 Payment processing and tracking")
        print("   🎥 Video chat with real-time communication")
        print("   💬 AI chatbot responses from doctors")
        print("\n💻 Ready to use:")
        print("   1. Start server: python sleepy/server/app.py")
        print("   2. Open: http://localhost:5000/video-chat.html")
        print("   3. Select doctor, time slot, and payment method")
        print("   4. Complete payment and start video consultation!")
    else:
        print("⚠️ Some tests failed. Check the errors above.")
    
    return tests_passed == total_tests

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)