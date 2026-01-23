#!/usr/bin/env python3
"""
Project Cleanup Script
Remove unwanted files and keep only main project files
"""

import os
import shutil
import glob

print("🧹 CLEANING UP PROJECT - KEEPING ONLY MAIN FILES")
print("=" * 50)

# Files to keep (essential project files)
KEEP_FILES = [
    # Main project files
    "README.md",
    "requirements.txt",
    "push.md",
    ".env.example",
    ".gitignore",
    
    # Main Python scripts
    "simple_model_trainer.py",
    "quick_start.py",
    
    # Sleepy main application
    "sleepy/server/app.py",
    "sleepy/server/db_helper.py",
    "sleepy/server/database.db",
    "sleepy/server/fer2013_emotion_detector.py",
    "sleepy/server/simple_fer2013_model_20260123_225231_final.h5",
    "sleepy/server/intents.json",
    
    # Client files
    "sleepy/client/index.html",
    "sleepy/client/signin.html",
    "sleepy/client/signup.html",
    "sleepy/client/dashboard.html",
    "sleepy/client/admin.html",
    "sleepy/client/emotion-detection.html",
    "sleepy/client/video-chat.html",
    "sleepy/client/aura-chatbot.html",
    "sleepy/client/styles.css",
    "sleepy/client/app.js",
    "sleepy/client/admin.js",
    "sleepy/client/emotion-detection.js",
    "sleepy/client/video-chat.js",
    "sleepy/client/dashboard.js",
    
    # Dataset
    "emotion_datasets/fer2013/fer2013_enhanced.csv",
    
    # Sample images
    "emotion_sample_images/",
    "test_human_faces/",
    
    # Main Jupyter notebook (fixed version)
    "FER2013_Emotion_Model_Training_FIXED.ipynb",
]

# Directories to keep completely
KEEP_DIRS = [
    "sleepy/client/",
    "emotion_sample_images/",
    "test_human_faces/",
    "emotion_datasets/fer2013/",
]

# Files/patterns to delete (unwanted files)
DELETE_PATTERNS = [
    # Test files
    "test_*.py",
    "check_*.py",
    "debug_*.py",
    "verify_*.py",
    
    # Fix files
    "fix_*.py",
    "install_*.py",
    "setup_*.py",
    "update_*.py",
    
    # Create files (temporary)
    "create_*.py",
    
    # Cell files
    "cell_*.py",
    
    # Start files (except main ones)
    "start_*.py",
    
    # Complete files
    "complete_*.py",
    
    # Jupyter fix files
    "jupyter_*.py",
    "notebook_*.py",
    "run_*.py",
    
    # Other temporary files
    "populate_*.py",
    "migrate_*.py",
    "open_*.py",
    "add_*.py",
    "get_*.py",
    
    # Markdown documentation files (keep only main ones)
    "*_COMPLETE.md",
    "*_FIXED.md",
    "*_SUCCESS.md",
    "*_CONFIRMED.md",
    "*_SUMMARY.md",
    "*_GUIDE.md",
    "*_INTEGRATION_*.md",
    
    # Version files
    "[0-9].*",
    
    # Backup files
    "*.backup",
    "*.bak",
    "*_backup.*",
    "*_old.*",
    "*_corrupted.*",
    
    # Temporary model files (keep only the final one)
    "advanced_emotion_model.h5",
    "compact_emotion_model_best.h5",
    "genuine_emotion_model.h5",
    "simple_production_model_*.h5",
    
    # Other unwanted files
    "david.md",
    "Environment_Test.ipynb",
    "FER2013_Emotion_Model_Training.ipynb",  # Keep only FIXED version
]

def should_keep_file(filepath):
    """Check if file should be kept"""
    # Check if it's in the keep list
    for keep_file in KEEP_FILES:
        if filepath.endswith(keep_file) or filepath == keep_file:
            return True
    
    # Check if it's in a directory we want to keep
    for keep_dir in KEEP_DIRS:
        if filepath.startswith(keep_dir):
            return True
    
    return False

def should_delete_file(filepath):
    """Check if file matches delete patterns"""
    filename = os.path.basename(filepath)
    
    for pattern in DELETE_PATTERNS:
        if "*" in pattern:
            # Use glob pattern matching
            import fnmatch
            if fnmatch.fnmatch(filename, pattern):
                return True
        else:
            if filename == pattern:
                return True
    
    return False

def cleanup_project():
    """Clean up the project"""
    deleted_count = 0
    kept_count = 0
    
    # Get all files in project
    all_files = []
    for root, dirs, files in os.walk("."):
        # Skip hidden directories and __pycache__
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
        
        for file in files:
            filepath = os.path.join(root, file).replace("\\", "/")
            if filepath.startswith("./"):
                filepath = filepath[2:]
            all_files.append(filepath)
    
    print(f"📊 Found {len(all_files)} files to analyze")
    
    # Analyze each file
    for filepath in all_files:
        try:
            # Skip if it's a directory
            if os.path.isdir(filepath):
                continue
            
            # Check if we should keep this file
            if should_keep_file(filepath):
                print(f"✅ KEEP: {filepath}")
                kept_count += 1
                continue
            
            # Check if we should delete this file
            if should_delete_file(filepath):
                print(f"🗑️  DELETE: {filepath}")
                try:
                    os.remove(filepath)
                    deleted_count += 1
                except Exception as e:
                    print(f"⚠️  Could not delete {filepath}: {e}")
                continue
            
            # For files not in either list, ask what to do
            print(f"❓ UNKNOWN: {filepath}")
            kept_count += 1
            
        except Exception as e:
            print(f"⚠️  Error processing {filepath}: {e}")
    
    print(f"\n📊 CLEANUP SUMMARY:")
    print(f"✅ Files kept: {kept_count}")
    print(f"🗑️  Files deleted: {deleted_count}")
    
    # Clean up empty directories
    print(f"\n🧹 Cleaning up empty directories...")
    empty_dirs_removed = 0
    
    for root, dirs, files in os.walk(".", topdown=False):
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            try:
                if not os.listdir(dir_path):  # Directory is empty
                    os.rmdir(dir_path)
                    print(f"🗑️  Removed empty directory: {dir_path}")
                    empty_dirs_removed += 1
            except Exception as e:
                pass  # Directory not empty or other error
    
    print(f"🗑️  Empty directories removed: {empty_dirs_removed}")

def create_gitignore():
    """Create .gitignore file"""
    gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Logs
*.log

# Database
*.db-journal

# Model files (optional - uncomment if models are too large)
# *.h5
# *.pkl

# Temporary files
*.tmp
*.temp
*.bak
*.backup

# Node modules (if any)
node_modules/
"""
    
    with open(".gitignore", "w") as f:
        f.write(gitignore_content)
    
    print("✅ Created .gitignore file")

def main():
    """Main cleanup function"""
    print("🚨 WARNING: This will delete many files!")
    print("Make sure you have a backup of your project before proceeding.")
    
    response = input("\nDo you want to continue? (yes/no): ").lower().strip()
    
    if response in ['yes', 'y', 'ha', 'हो']:
        cleanup_project()
        create_gitignore()
        
        print(f"\n🎉 PROJECT CLEANUP COMPLETE!")
        print(f"\n📁 Your clean project now contains only:")
        print(f"   • Main application files (sleepy/)")
        print(f"   • Essential Python scripts")
        print(f"   • Dataset and sample images")
        print(f"   • Trained model file")
        print(f"   • Documentation (README.md, push.md)")
        print(f"   • Configuration files")
        
        print(f"\n🚀 Ready for GitHub push!")
        print(f"   Run: git add .")
        print(f"   Run: git commit -m 'Clean project with main files only'")
        print(f"   Run: git push")
        
    else:
        print("❌ Cleanup cancelled. No files were deleted.")

if __name__ == "__main__":
    main()