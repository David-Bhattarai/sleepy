# 🗄️ AURA Database Access Guide

## Step-by-Step Guide to View Database

### 📍 Database File Location:
```
D:\final proj\sleepy\server\database.db
```

---

## Method 1: Command Line (Terminal/CMD)

### Step 1: Open Terminal/CMD
- Press Windows Key + R
- Type `cmd` and press Enter

### Step 2: Navigate to Project Directory
```bash
cd "D:\final proj\sleepy"
```

### Step 3: Run SQLite Commands

#### To View All Tables:
```bash
sqlite3 server/database.db ".tables"
```

#### To View Users Table:
```bash
sqlite3 server/database.db "SELECT * FROM users;"
```

#### To View Doctors Table:
```bash
sqlite3 server/database.db "SELECT name, specialty, price_per_session FROM doctors;"
```

#### To View Appointments:
```bash
sqlite3 server/database.db "SELECT * FROM appointments;"
```

#### To View Mood Entries:
```bash
sqlite3 server/database.db "SELECT mood_rating, mood_notes, timestamp FROM simple_mood_entries ORDER BY timestamp DESC LIMIT 10;"
```

#### To View Chat History:
```bash
sqlite3 server/database.db "SELECT user_message, ai_response, timestamp FROM chat_history ORDER BY timestamp DESC LIMIT 5;"
```

#### To View Payments:
```bash
sqlite3 server/database.db "SELECT amount, payment_method, payment_status FROM payments;"
```

---

## Method 2: Python Script (Easy Way)

### Step 1: Navigate to Project Directory in Terminal
```bash
cd "D:\final proj\sleepy"
```

### Step 2: Run Database Viewer Script
```bash
python view_database.py
```

---

## Method 3: DB Browser for SQLite (GUI Tool)

### Step 1: Download & Install
- Website: https://sqlitebrowser.org/
- Download and install the application

### Step 2: Open Database File
1. Open DB Browser for SQLite
2. Click "Open Database"
3. Navigate to: `D:\final proj\sleepy\server\database.db`
4. Select the file and click Open

### Step 3: Browse Data
- Click "Browse Data" tab
- Select any table from the dropdown
- Data will be displayed automatically

---

## Method 4: Direct SQLite Commands

### Interactive SQLite Shell:
```bash
sqlite3 server/database.db
```

### Commands in SQLite Shell:
```sql
-- To view all tables
.tables

-- To view table structure
.schema users

-- To select data
SELECT * FROM users;
SELECT * FROM doctors;
SELECT * FROM appointments;
SELECT * FROM simple_mood_entries;
SELECT * FROM chat_history;
SELECT * FROM payments;

-- To exit
.quit
```

---

## 📊 Important Tables & Their Data:

### 1. **users** - User Accounts
- `id` - Unique user ID
- `name` - User name
- `email` - Email address
- `password` - Encrypted password
- `phone` - Phone number
- `is_admin` - Admin status (0/1)
- `created_at` - Registration date

### 2. **doctors** - Professional Doctors
- `id` - Doctor ID
- `name` - Doctor name
- `specialty` - Medical specialty
- `price_per_session` - Session price
- `experience_years` - Years of experience
- `bio` - Doctor biography

### 3. **appointments** - Video Consultations
- `id` - Appointment ID
- `user_id` - Patient ID
- `doctor_id` - Doctor ID
- `appointment_date` - Booking date
- `appointment_time` - Booking time
- `status` - Appointment status
- `payment_status` - Payment status

### 4. **simple_mood_entries** - Daily Mood Tracking
- `id` - Entry ID
- `user_id` - User ID
- `mood_rating` - Rating (1-5)
- `mood_notes` - User notes
- `timestamp` - Entry time

### 5. **chat_history** - AI Chatbot Conversations
- `id` - Chat ID
- `user_id` - User ID
- `user_message` - User's message
- `ai_response` - AI's response
- `sentiment` - Message sentiment
- `timestamp` - Chat time

### 6. **payments** - Payment Records
- `id` - Payment ID
- `user_id` - User ID
- `appointment_id` - Related appointment
- `amount` - Payment amount
- `payment_method` - Card/eSewa
- `payment_status` - Status
- `transaction_id` - Transaction reference

---

## 🔍 Useful SQL Queries:

### User Statistics:
```sql
SELECT COUNT(*) as total_users FROM users;
SELECT COUNT(*) as admin_users FROM users WHERE is_admin = 1;
```

### Revenue Statistics:
```sql
SELECT SUM(amount) as total_revenue FROM payments WHERE payment_status = 'completed';
SELECT payment_method, COUNT(*) as count FROM payments GROUP BY payment_method;
```

### Mood Analysis:
```sql
SELECT mood_rating, COUNT(*) as count FROM simple_mood_entries GROUP BY mood_rating;
SELECT AVG(mood_rating) as average_mood FROM simple_mood_entries;
```

### Popular Doctors:
```sql
SELECT d.name, COUNT(a.id) as bookings 
FROM doctors d 
LEFT JOIN appointments a ON d.id = a.doctor_id 
GROUP BY d.id 
ORDER BY bookings DESC;
```

---

## 💡 Tips:

1. **Backup Database**: Copy `database.db` file before making changes
2. **Read-Only Access**: Use SELECT queries to view data safely
3. **GUI Tool**: DB Browser is easiest for beginners
4. **Python Script**: `view_database.py` shows formatted data
5. **Command Line**: Fastest for quick queries

---

## 🚨 Important Notes:

- **Never delete** the `database.db` file
- **Always backup** before making changes
- **Use SELECT** queries to view data safely
- **Avoid DELETE/DROP** commands unless sure
- **Database location**: `sleepy/server/database.db`

---

## 📞 Quick Commands Summary:

```bash
# View all data (formatted)
python view_database.py

# View specific table
sqlite3 server/database.db "SELECT * FROM users;"

# Count records
sqlite3 server/database.db "SELECT COUNT(*) FROM appointments;"

# Recent activity
sqlite3 server/database.db "SELECT * FROM simple_mood_entries ORDER BY timestamp DESC LIMIT 5;"
```

Happy Database Browsing! 🎯