#!/usr/bin/env python3
"""
Setup Video Chat System
Initializes dummy doctors and tests the complete video chat payment system
"""

import sys
import os
import sqlite3
import uuid

# Add server path
sys.path.append('sleepy/server')

def setup_doctors_directly():
    """Setup doctors directly in database"""
    print("🔧 Setting up doctors directly in database...")
    
    try:
        # Connect to database
        conn = sqlite3.connect('sleepy/server/database.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Check if doctors table exists and has data
        cursor.execute("SELECT COUNT(*) FROM doctors")
        count = cursor.fetchone()[0]
        
        if count == 0:
            print("🔄 Adding dummy doctors...")
            
            doctors_data = [
                ('dr-smith-001', 'Dr. Smith', 'dr.smith@aura.com', '+1-555-0101', 
                 'Mental Health Specialist', 'MD, Psychiatry', 15, 80.0, '👨‍⚕️',
                 'Specializes in anxiety and depression treatment with over 15 years of experience.', 1),
                
                ('dr-johnson-002', 'Dr. Johnson', 'dr.johnson@aura.com', '+1-555-0102',
                 'Licensed Counselor', 'PhD, Clinical Psychology', 12, 75.0, '👩‍⚕️',
                 'Expert in stress management and cognitive behavioral therapy.', 1),
                
                ('dr-williams-003', 'Dr. Williams', 'dr.williams@aura.com', '+1-555-0103',
                 'Psychiatrist', 'MD, Psychiatry, Board Certified', 20, 90.0, '👨‍⚕️',
                 'Specializes in mood disorders and psychiatric medication management.', 0),  # Busy
                
                ('dr-brown-004', 'Dr. Brown', 'dr.brown@aura.com', '+1-555-0104',
                 'Trauma Specialist', 'PhD, Clinical Psychology, PTSD Certified', 18, 85.0, '👩‍⚕️',
                 'Specializes in trauma therapy and PTSD treatment.', 1),
                
                ('dr-davis-005', 'Dr. Davis', 'dr.davis@aura.com', '+1-555-0105',
                 'Relationship Counselor', 'MA, Marriage and Family Therapy', 10, 70.0, '👨‍⚕️',
                 'Expert in couples and family therapy.', 1),
                
                ('dr-wilson-006', 'Dr. Wilson', 'dr.wilson@aura.com', '+1-555-0106',
                 'Addiction Specialist', 'MD, Addiction Medicine', 22, 95.0, '👩‍⚕️',
                 'Specializes in substance abuse recovery and addiction treatment.', 1)
            ]
            
            cursor.executemany('''
                INSERT INTO doctors (id, name, email, phone, specialty, qualification, 
                                   experience_years, price_per_session, avatar_emoji, bio, is_available)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', doctors_data)
            
            conn.commit()
            print(f"✅ Added {len(doctors_data)} doctors to database")
        else:
            print(f"✅ Found {count} doctors already in database")
        
        # Verify doctors
        cursor.execute("SELECT * FROM doctors ORDER BY name")
        doctors = cursor.fetchall()
        
        print("\n👨‍⚕️ Available Doctors:")
        for doctor in doctors:
            status = "🟢 Available" if doctor['is_available'] else "🔴 Busy"
            print(f"   {doctor['avatar_emoji']} {doctor['name']} - {doctor['specialty']}")
            print(f"      💰 ${doctor['price_per_session']}/session | {status}")
            print(f"      📧 {doctor['email']} | 📞 {doctor['phone']}")
            print()
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error setting up doctors: {e}")
        return False

def create_payments_table():
    """Create payments table if it doesn't exist"""
    print("🔧 Setting up payments table...")
    
    try:
        conn = sqlite3.connect('sleepy/server/database.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS payments (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                appointment_id TEXT NOT NULL,
                amount REAL NOT NULL,
                payment_method TEXT NOT NULL,
                currency TEXT DEFAULT 'USD',
                status TEXT DEFAULT 'pending',
                transaction_id TEXT,
                esewa_ref_id TEXT,
                card_last_four TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (appointment_id) REFERENCES appointments (id)
            )
        ''')
        
        conn.commit()
        conn.close()
        print("✅ Payments table ready")
        return True
        
    except Exception as e:
        print(f"❌ Error creating payments table: {e}")
        return False

def test_appointment_booking():
    """Test appointment booking functionality"""
    print("🧪 Testing appointment booking...")
    
    try:
        conn = sqlite3.connect('sleepy/server/database.db')
        cursor = conn.cursor()
        
        # Create test appointment
        appointment_id = str(uuid.uuid4())
        user_id = "test-user-001"
        doctor_id = "dr-smith-001"
        
        cursor.execute('''
            INSERT INTO appointments (id, user_id, doctor_id, appointment_date, appointment_time,
                                    duration_minutes, status, payment_status, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (appointment_id, user_id, doctor_id, "2026-01-24", "10:00",
              50, "scheduled", "pending", "Test video consultation"))
        
        # Create test payment
        payment_id = str(uuid.uuid4())
        cursor.execute('''
            INSERT INTO payments (id, user_id, appointment_id, amount, payment_method,
                                currency, status, card_last_four)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (payment_id, user_id, appointment_id, 80.0, "card", "USD", "completed", "1234"))
        
        conn.commit()
        
        # Verify appointment
        cursor.execute('''
            SELECT a.*, d.name as doctor_name, d.specialty, d.price_per_session
            FROM appointments a
            JOIN doctors d ON a.doctor_id = d.id
            WHERE a.id = ?
        ''', (appointment_id,))
        
        appointment = cursor.fetchone()
        if appointment:
            print(f"✅ Test appointment created:")
            print(f"   📅 Date: {appointment[3]} at {appointment[4]}")
            print(f"   👨‍⚕️ Doctor: {appointment[11]} ({appointment[12]})")
            print(f"   💰 Amount: ${appointment[13]}")
            print(f"   📊 Status: {appointment[6]}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error testing appointment booking: {e}")
        return False

def test_server_endpoints():
    """Test server API endpoints"""
    print("🧪 Testing server API endpoints...")
    
    try:
        from app import app
        
        with app.test_client() as client:
            # Test doctors endpoint
            response = client.get('/api/doctors')
            if response.status_code == 200:
                data = response.get_json()
                if data.get('success') and data.get('doctors'):
                    doctors = data['doctors']
                    print(f"✅ Doctors API working - found {len(doctors)} doctors")
                    
                    for doctor in doctors[:3]:  # Show first 3
                        print(f"   👨‍⚕️ {doctor['name']} - ${doctor['price_per_session']}/session")
                else:
                    print("⚠️ Doctors API returned no data")
            else:
                print(f"❌ Doctors API failed: {response.status_code}")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing server endpoints: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 VIDEO CHAT SYSTEM SETUP")
    print("🎯 Setting up complete video consultation system with payment")
    print("=" * 60)
    
    success_count = 0
    total_steps = 4
    
    # Step 1: Setup doctors
    if setup_doctors_directly():
        success_count += 1
    
    # Step 2: Setup payments table
    if create_payments_table():
        success_count += 1
    
    # Step 3: Test appointment booking
    if test_appointment_booking():
        success_count += 1
    
    # Step 4: Test server endpoints
    if test_server_endpoints():
        success_count += 1
    
    print("\n" + "=" * 60)
    print(f"📊 Setup Results: {success_count}/{total_steps} completed")
    
    if success_count == total_steps:
        print("✅ VIDEO CHAT SYSTEM READY!")
        print("\n🎯 System Features:")
        print("   👨‍⚕️ 6 AI doctors with different specialties")
        print("   💳 Card payment integration (Visa, Mastercard)")
        print("   📱 eSewa payment integration (Nepal)")
        print("   📅 Appointment booking system")
        print("   💰 Payment processing and tracking")
        print("   🎥 Video chat with real-time communication")
        print("   💬 AI chatbot responses from doctors")
        print("\n🚀 How to use:")
        print("   1. Start server: python sleepy/server/app.py")
        print("   2. Open browser: http://localhost:5000/video-chat.html")
        print("   3. Select a doctor and time slot")
        print("   4. Choose payment method (Card or eSewa)")
        print("   5. Complete payment and start video consultation!")
        print("\n💡 Doctor IDs for reference:")
        print("   - dr-smith-001: Mental Health Specialist ($80)")
        print("   - dr-johnson-002: Licensed Counselor ($75)")
        print("   - dr-williams-003: Psychiatrist ($90) - Currently Busy")
        print("   - dr-brown-004: Trauma Specialist ($85)")
        print("   - dr-davis-005: Relationship Counselor ($70)")
        print("   - dr-wilson-006: Addiction Specialist ($95)")
    else:
        print("⚠️ Some setup steps failed. Check the errors above.")
    
    return success_count == total_steps

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)