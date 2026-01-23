# 🗄️ Database Browser Guide

## How to View Database Tables in Browser

### Method 1: Using Database Browser (Recommended)
```bash
python database_browser.py
```

**Features:**
- ✅ View all database tables in clean HTML format
- ✅ See record counts for each table
- ✅ Responsive design works on any device
- ✅ Refresh button to update data
- ✅ No need to start main server

**What you'll see:**
- 📊 **Users Table**: All registered users
- 👨‍⚕️ **Doctors Table**: Available doctors
- 📅 **Appointments Table**: All appointments
- 💬 **Chat History Table**: AI conversations
- 😊 **Mood Entries Table**: User mood tracking
- 💳 **Payments Table**: Payment records
- 🎭 **Emotion Detection Table**: Face emotion results

### Method 2: Using Admin Panel
```bash
python start_admin_panel.py
```

**Features:**
- ✅ Full admin interface with CRUD operations
- ✅ Create, edit, delete records
- ✅ Export data to CSV
- ✅ Real-time statistics
- ✅ User management

**Login Credentials:**
- Email: `admin@aura.co`
- Password: `admin123`

### Method 3: Manual Server Start
```bash
cd sleepy/server
python app.py
```
Then open: `http://localhost:5000/admin.html`

## 📊 Database Tables Overview

### 1. Users Table
```
- id: User unique identifier
- name: User's full name
- email: User's email address
- password: Encrypted password
- phone: Phone number
- is_admin: Admin privileges (0/1)
- created_at: Registration date
```

### 2. Doctors Table
```
- id: Doctor unique identifier
- name: Doctor's name
- email: Doctor's email
- specialty: Medical specialty
- qualification: Medical qualifications
- experience_years: Years of experience
- price_per_session: Session cost
- avatar_emoji: Profile emoji
- bio: Doctor's biography
```

### 3. Appointments Table
```
- id: Appointment unique identifier
- user_id: Patient ID
- doctor_id: Doctor ID
- appointment_date: Appointment date
- appointment_time: Appointment time
- status: scheduled/completed/cancelled
- payment_status: pending/completed
- payment_amount: Session cost
- notes: Additional notes
```

### 4. Chat History Table
```
- id: Chat unique identifier
- user_id: User ID
- user_message: User's message
- ai_response: AI's response
- sentiment: Message sentiment analysis
- timestamp: Message time
```

### 5. Simple Mood Entries Table
```
- id: Entry unique identifier
- user_id: User ID
- mood_rating: Rating 1-5
- mood_notes: User's notes
- timestamp: Entry time
```

### 6. Face Emotion Detection Table
```
- id: Detection unique identifier
- user_id: User ID
- detected_emotion: Detected emotion
- confidence_score: Detection confidence
- timestamp: Detection time
```

### 7. Payments Table
```
- id: Payment unique identifier
- user_id: User ID
- appointment_id: Related appointment
- amount: Payment amount
- currency: Payment currency
- payment_method: Payment method
- payment_status: pending/completed
- transaction_id: Transaction reference
```

## 🎯 Sample Data Overview

Your database contains **292 sample records**:
- **15 Users**: Including admin and regular users
- **6 Doctors**: Various specialties and experience levels
- **9 Appointments**: Different statuses and dates
- **189 Chat Messages**: AI conversations with sentiment analysis
- **58 Mood Entries**: User mood tracking over time
- **4 Payment Records**: Completed transactions
- **11 Emotion Detections**: Face emotion analysis results

## 🔧 Troubleshooting

### Database Not Found
```bash
# Check if database exists
ls -la sleepy/server/database.db
# or
ls -la database.db
```

### Server Already Running
```bash
# Kill existing server
pkill -f "python app.py"
# or find and kill process
ps aux | grep "python app.py"
```

### Port Already in Use
```bash
# Check what's using port 5000
netstat -tulpn | grep :5000
# Kill process using port
sudo kill -9 <process_id>
```

## 💡 Tips

1. **Use Database Browser** for quick viewing without starting main server
2. **Use Admin Panel** for full database management
3. **Refresh regularly** to see latest data
4. **Export data** using admin panel CSV export feature
5. **Check record counts** to verify data integrity

## 🚀 Quick Commands

```bash
# View database in browser (simple)
python database_browser.py

# Start admin panel (full features)
python start_admin_panel.py

# Manual server start
cd sleepy/server && python app.py
```

## 📱 Mobile Friendly

Both database browser and admin panel work perfectly on:
- 📱 Mobile phones
- 📱 Tablets  
- 💻 Desktop computers
- 🌐 Any modern web browser

Your database is fully integrated and ready to view! 🎉