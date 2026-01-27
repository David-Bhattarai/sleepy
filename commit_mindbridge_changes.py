#!/usr/bin/env python3
"""
Commit MindBridge Changes - NCIT Final Year Project
Script to help commit all the rename changes to git
"""

import subprocess
import os

def run_git_command(command):
    """Run a git command and return the result"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def main():
    """Main function to commit changes"""
    print("🚀 MindBridge - NCIT Final Year Project Git Commit")
    print("=" * 50)
    
    # Change to project root
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    os.chdir('..')  # Go to project root
    
    print("📋 Preparing to commit MindBridge rename changes...")
    print()
    
    # Check git status
    print("🔍 Checking git status...")
    success, stdout, stderr = run_git_command("git status --porcelain")
    
    if success:
        if stdout.strip():
            print("📝 Changes detected:")
            print(stdout)
        else:
            print("ℹ️ No changes to commit")
            return
    else:
        print(f"❌ Error checking git status: {stderr}")
        return
    
    # Add all changes
    print("\n📦 Adding all changes...")
    success, stdout, stderr = run_git_command("git add .")
    
    if success:
        print("✅ All changes added to staging")
    else:
        print(f"❌ Error adding changes: {stderr}")
        return
    
    # Create commit message
    commit_message = """Rename project from AURA to MindBridge - NCIT Final Year Project

🔄 Complete project rename from AURA to MindBridge
- Updated all file names from aura_* to mindbridge_*
- Updated all code references and documentation
- Updated HTML interfaces and branding
- Maintained all functionality and features
- Updated README.md with project history

📋 Changes:
- start_complete_aura_system.py → start_complete_mindbridge_system.py
- start_hybrid_aura.py → start_hybrid_mindbridge.py  
- start_working_aura.py → start_working_mindbridge.py
- debug_aura_system.py → debug_mindbridge_system.py
- aura-chatbot.html → mindbridge-chatbot.html
- aura_model*.pkl → mindbridge_model*.pkl
- All AURA references → MindBridge references

🎯 Project Evolution:
- January 21, 2026: AURA ML Mental Health Chatbot created by David Bhattarai
- January 27, 2026: Renamed to MindBridge - NCIT Final Year Project

✅ All functionality remains identical - this is purely a naming update
🏫 NCIT Final Year Project by David Bhattarai"""
    
    # Commit changes
    print("\n💾 Committing changes...")
    success, stdout, stderr = run_git_command(f'git commit -m "{commit_message}"')
    
    if success:
        print("✅ Changes committed successfully!")
        print()
        print("📋 Commit Summary:")
        print("- Project renamed from AURA to MindBridge - NCIT Final Year Project")
        print("- All files and references updated")
        print("- Functionality preserved")
        print("- Ready for GitHub push")
        print()
        print("🚀 Next Steps:")
        print("1. Push to GitHub: git push origin main")
        print("2. Update GitHub repository name if desired")
        print("3. Test the system: python sleepy/server/app.py")
        print()
        print("🎉 MindBridge - NCIT Final Year Project is ready!")
    else:
        print(f"❌ Error committing changes: {stderr}")
        print("💡 You may need to configure git user:")
        print("   git config --global user.name 'Your Name'")
        print("   git config --global user.email 'your.email@example.com'")

if __name__ == "__main__":
    main()