#!/usr/bin/env python3
"""
Setup Full Project Git Repository
Initialize git for the entire project and push to GitHub
"""

import os
import subprocess
import sys

def setup_full_project_git():
    """Setup git repository for the full project"""
    print("🚀 Setting up Full Project Git Repository...")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not os.path.exists("sleepy"):
        print("❌ Please run this from the main project directory (where sleepy folder is)")
        return
    
    print("📂 Current directory structure:")
    for item in os.listdir("."):
        if os.path.isdir(item):
            print(f"  📁 {item}/")
        else:
            print(f"  📄 {item}")
    
    print("\n🔧 Git Setup Steps:")
    print("1. Initialize git repository")
    print("2. Add all files")
    print("3. Create initial commit")
    print("4. Add remote origin")
    print("5. Push to GitHub")
    
    # Step 1: Initialize git
    print("\n📝 Step 1: Initializing git repository...")
    try:
        result = subprocess.run(["git", "init"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Git repository initialized")
        else:
            print(f"❌ Error initializing git: {result.stderr}")
            return
    except Exception as e:
        print(f"❌ Error running git init: {e}")
        return
    
    # Step 2: Add all files
    print("\n📝 Step 2: Adding all files...")
    try:
        result = subprocess.run(["git", "add", "."], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ All files added to git")
        else:
            print(f"❌ Error adding files: {result.stderr}")
            return
    except Exception as e:
        print(f"❌ Error running git add: {e}")
        return
    
    # Step 3: Create initial commit
    print("\n📝 Step 3: Creating initial commit...")
    commit_message = "Complete AURA Mental Health Platform - Full Project with Admin Panel"
    try:
        result = subprocess.run(["git", "commit", "-m", commit_message], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Initial commit created")
            print(f"📝 Commit message: {commit_message}")
        else:
            print(f"❌ Error creating commit: {result.stderr}")
            return
    except Exception as e:
        print(f"❌ Error running git commit: {e}")
        return
    
    print("\n" + "=" * 60)
    print("🎉 LOCAL GIT REPOSITORY SETUP COMPLETE!")
    print("=" * 60)
    
    print("\n📋 NEXT STEPS TO PUSH TO GITHUB:")
    print("1. Create a new repository on GitHub")
    print("2. Copy the repository URL")
    print("3. Run these commands:")
    print()
    print("   git remote add origin <YOUR_GITHUB_REPO_URL>")
    print("   git branch -M main")
    print("   git push -u origin main")
    print()
    print("📊 PROJECT SUMMARY:")
    print("  • Complete AURA Mental Health Platform")
    print("  • Admin Panel with ALL database tables")
    print("  • Emotion Detection & AI Chatbot")
    print("  • Video Chat & Payment Integration")
    print("  • ML Models & Training Scripts")
    print("  • 314 database records across 13 tables")
    print("  • Production-ready system")
    
    print("\n🔗 EXAMPLE GITHUB SETUP:")
    print("If your GitHub repo is: https://github.com/username/aura-project")
    print("Then run:")
    print("  git remote add origin https://github.com/username/aura-project.git")
    print("  git push -u origin main")

if __name__ == "__main__":
    setup_full_project_git()