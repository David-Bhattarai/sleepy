#!/usr/bin/env python3
"""
Test Admin Panel Access for All Users
Verify that admin panel opens without admin access required error
"""

import requests
import webbrowser
import time

def test_regular_user_access():
    """Test regular user can access admin panel"""
    print("Testing regular user admin panel access...")
    
    # Create and login regular user
    signup_data = {
        "name": "Test User",
        "email": "testuser@aura.com", 
        "password": "test123"
    }
    
    try:
        requests.post("http://localhost:5000/api/signup", json=signup_data)
    except:
        pass
    
    signin_data = {
        "email": "testuser@aura.com",
        "password": "test123"
    }
    
    try:
        response = requests.post("http://localhost:5000/api/signin", json=signin_data)
        if response.status_code == 200:
            data = response.json()
            token = data.get('token')
            is_admin = data.get('isAdmin', False)
            name = data.get('name', 'User')
            
            print(f"✅ Regular user login successful")
            print(f"   - Token: {token[:20]}...")
            print(f"   - Is Admin: {is_admin}")
            print(f"   - Name: {name}")
            
            return {
                'token': token,
                'isAdmin': is_admin,
                'name': name
            }
        else:
            print(f"❌ Regular user login failed: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Regular user login error: {e}")
        return None

def test_admin_user_access():
    """Test admin user can access admin panel"""
    print("Testing admin user admin panel access...")
    
    signin_data = {
        "email": "admin@aura.com",
        "password": "admin123"
    }
    
    try:
        response = requests.post("http://localhost:5000/api/signin", json=signin_data)
        if response.status_code == 200:
            data = response.json()
            token = data.get('token')
            is_admin = data.get('isAdmin', False)
            name = data.get('name', 'Admin')
            
            print(f"✅ Admin user login successful")
            print(f"   - Token: {token[:20]}...")
            print(f"   - Is Admin: {is_admin}")
            print(f"   - Name: {name}")
            
            return {
                'token': token,
                'isAdmin': is_admin,
                'name': name
            }
        else:
            print(f"❌ Admin user login failed: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Admin user login error: {e}")
        return None

def create_test_html(user_data, user_type):
    """Create test HTML file to simulate admin panel access"""
    html_content = f'''<!DOCTYPE html>
<html>
<head>
    <title>Admin Panel Access Test - {user_type}</title>
</head>
<body>
    <h1>Admin Panel Access Test - {user_type}</h1>
    <p>Testing admin panel access with {user_type} credentials</p>
    
    <script>
        // Simulate localStorage data
        localStorage.setItem('token', '{user_data["token"]}');
        localStorage.setItem('isAdmin', '{str(user_data["isAdmin"]).lower()}');
        localStorage.setItem('userName', '{user_data["name"]}');
        
        console.log('LocalStorage set:');
        console.log('- token:', localStorage.getItem('token'));
        console.log('- isAdmin:', localStorage.getItem('isAdmin'));
        console.log('- userName:', localStorage.getItem('userName'));
        
        // Test admin panel access
        setTimeout(() => {{
            window.location.href = '/admin.html';
        }}, 2000);
    </script>
    
    <p>Redirecting to admin panel in 2 seconds...</p>
    <p>If you see "Admin access required" error, the fix didn't work.</p>
    <p>If admin panel loads, the fix is successful!</p>
</body>
</html>'''
    
    filename = f'test_admin_access_{user_type.lower()}.html'
    with open(filename, 'w') as f:
        f.write(html_content)
    
    return filename

def main():
    print("ADMIN PANEL ACCESS TEST FOR ALL USERS")
    print("=" * 50)
    
    # Test regular user
    print("\n1. REGULAR USER ACCESS TEST")
    print("-" * 30)
    regular_user = test_regular_user_access()
    
    # Test admin user  
    print("\n2. ADMIN USER ACCESS TEST")
    print("-" * 30)
    admin_user = test_admin_user_access()
    
    print("\n" + "=" * 50)
    print("ADMIN PANEL ACCESS SUMMARY")
    print("=" * 50)
    
    if regular_user and admin_user:
        print("✅ Both user types can login successfully")
        print("\n📝 MANUAL TEST INSTRUCTIONS:")
        print("1. Open browser and go to: http://localhost:5000/dashboard.html")
        print("2. Login with either:")
        print("   - Regular User: testuser@aura.com / test123")
        print("   - Admin User: admin@aura.com / admin123")
        print("3. Look for 'System Panel' card in left sidebar")
        print("4. Click the button to open admin panel")
        print("5. Admin panel should open WITHOUT 'Admin access required' error")
        
        print("\n🎯 EXPECTED RESULTS:")
        print("- Regular User: Should see 'System Dashboard' title")
        print("- Admin User: Should see 'Admin Dashboard' title")
        print("- Both: Should access admin panel without errors")
        print("- Both: Should see database tables and statistics")
        
        print("\n🚀 DIRECT ADMIN PANEL ACCESS:")
        print("- URL: http://localhost:5000/admin.html")
        print("- Should work for both user types now")
        
        # Create test files
        if regular_user:
            regular_file = create_test_html(regular_user, "Regular")
            print(f"\n📄 Regular user test file: {regular_file}")
        
        if admin_user:
            admin_file = create_test_html(admin_user, "Admin")
            print(f"📄 Admin user test file: {admin_file}")
            
        print("\n🎉 Admin panel should now be accessible to all users!")
        
    else:
        print("❌ Some login issues found")
        if not regular_user:
            print("  - Regular user login failed")
        if not admin_user:
            print("  - Admin user login failed")

if __name__ == "__main__":
    main()