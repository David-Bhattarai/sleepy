#!/usr/bin/env python3
"""
Get Unlimited Gemini AI Access
Multiple methods to get unlimited/higher quota
"""

import webbrowser
import os

def method_1_new_api_keys():
    """Method 1: Create multiple free API keys"""
    print("🔑 METHOD 1: Multiple FREE API Keys")
    print("=" * 50)
    print("✅ Create multiple Google accounts")
    print("✅ Get 1,500 requests/day per account")
    print("✅ Total: 1,500 × accounts = unlimited!")
    print()
    print("📋 Steps:")
    print("1. Go to: https://makersuite.google.com/app/apikey")
    print("2. Create new Google account")
    print("3. Generate new API key")
    print("4. Add to unlimited_gemini_system.py")
    print()
    
    choice = input("🚀 Open Google AI Studio? (y/n): ")
    if choice.lower() == 'y':
        webbrowser.open('https://makersuite.google.com/app/apikey')

def method_2_paid_plan():
    """Method 2: Upgrade to paid plan"""
    print("\n💳 METHOD 2: Paid Plan (BEST)")
    print("=" * 50)
    print("💰 Cost: $0.001 per request (very cheap!)")
    print("📈 Quota: 1000+ requests per minute")
    print("🚀 Daily Limit: Unlimited")
    print("⚡ Speed: Much faster")
    print()
    print("📋 Steps:")
    print("1. Go to: https://ai.google.dev/pricing")
    print("2. Enable billing on Google Cloud")
    print("3. Upgrade your project")
    print("4. Get unlimited access!")
    print()
    print("💡 Example cost:")
    print("   - 1,000 requests = $1.00")
    print("   - 10,000 requests = $10.00")
    print("   - Very affordable for any project!")
    
    choice = input("🚀 Open pricing page? (y/n): ")
    if choice.lower() == 'y':
        webbrowser.open('https://ai.google.dev/pricing')

def method_3_alternative_models():
    """Method 3: Use alternative free models"""
    print("\n🤖 METHOD 3: Alternative FREE Models")
    print("=" * 50)
    print("🆓 OpenAI GPT-4o-mini: Free tier available")
    print("🆓 Anthropic Claude: Free tier available")
    print("🆓 Hugging Face: Many free models")
    print("🆓 Ollama: Run models locally")
    print()
    print("📋 Benefits:")
    print("✅ No quota limits")
    print("✅ Multiple providers")
    print("✅ Local models possible")
    print("✅ Backup options")

def method_4_optimize_usage():
    """Method 4: Optimize current usage"""
    print("\n⚡ METHOD 4: Optimize Current Usage")
    print("=" * 50)
    print("🎯 Smart caching: Cache similar responses")
    print("🎯 Batch processing: Group requests")
    print("🎯 Selective usage: Use Gemini for complex only")
    print("🎯 Fallback priority: Use trained models first")
    print()
    print("📊 Current system already does this!")
    print("✅ Hybrid system uses trained models first")
    print("✅ Only uses Gemini when needed")
    print("✅ Multiple fallback systems")

def add_new_api_key():
    """Add a new API key to the system"""
    print("\n🔑 ADD NEW API KEY")
    print("=" * 50)
    
    new_key = input("Enter new API key (AIza...): ").strip()
    
    if not new_key.startswith('AIza'):
        print("❌ Invalid API key format")
        return
    
    # Update the unlimited system file
    unlimited_file = 'sleepy/server/unlimited_gemini_system.py'
    
    if os.path.exists(unlimited_file):
        with open(unlimited_file, 'r') as f:
            content = f.read()
        
        # Find the api_keys list and add new key
        if 'self.api_keys = [' in content:
            # Add the new key
            new_line = f"            '{new_key}',  # Added key\n"
            content = content.replace(
                "            # Add more keys here:",
                f"            '{new_key}',  # Added key\n            # Add more keys here:"
            )
            
            with open(unlimited_file, 'w') as f:
                f.write(content)
            
            print(f"✅ Added new API key: {new_key[:10]}...")
            print("🚀 Restart your server to use the new key!")
        else:
            print("❌ Could not update unlimited system file")
    else:
        print("❌ Unlimited system file not found")

def show_current_status():
    """Show current API key status"""
    print("\n📊 CURRENT STATUS")
    print("=" * 50)
    
    # Check .env file
    env_file = '.env'
    if os.path.exists(env_file):
        with open(env_file, 'r') as f:
            content = f.read()
            if 'GEMINI_API_KEY' in content:
                # Extract key
                for line in content.split('\n'):
                    if 'GEMINI_API_KEY' in line and '=' in line:
                        key = line.split('=')[1].strip()
                        print(f"✅ Current API Key: {key[:10]}...")
                        break
            else:
                print("❌ No API key in .env file")
    else:
        print("❌ .env file not found")
    
    # Check unlimited system
    unlimited_file = 'sleepy/server/unlimited_gemini_system.py'
    if os.path.exists(unlimited_file):
        with open(unlimited_file, 'r') as f:
            content = f.read()
            # Count API keys
            key_count = content.count('AIza')
            print(f"🔑 API Keys in unlimited system: {key_count}")
    else:
        print("⚠️ Unlimited system not set up")

def main():
    """Main menu"""
    print("🚀 GET UNLIMITED GEMINI AI ACCESS")
    print("=" * 60)
    print("Choose your method:")
    print()
    print("1. 🔑 Multiple FREE API Keys (Recommended)")
    print("2. 💳 Paid Plan (Best Performance)")
    print("3. 🤖 Alternative Models")
    print("4. ⚡ Optimize Usage")
    print("5. ➕ Add New API Key")
    print("6. 📊 Show Current Status")
    print("7. 🚪 Exit")
    print()
    
    while True:
        choice = input("Select option (1-7): ").strip()
        
        if choice == '1':
            method_1_new_api_keys()
        elif choice == '2':
            method_2_paid_plan()
        elif choice == '3':
            method_3_alternative_models()
        elif choice == '4':
            method_4_optimize_usage()
        elif choice == '5':
            add_new_api_key()
        elif choice == '6':
            show_current_status()
        elif choice == '7':
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please select 1-7.")
        
        print("\n" + "=" * 60)

if __name__ == "__main__":
    main()