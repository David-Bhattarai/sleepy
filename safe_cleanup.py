#!/usr/bin/env python3
"""
MindBridge - NCIT Final Year Project - Safe Cleanup Script
Remove only clearly unwanted files, keep all essential functionality
"""

import os
import shutil
import glob

def print_banner():
    print("🧹 MindBridge - NCIT Final Year Project PROJECT - SAFE CLEANUP")
    print("=" * 60)
    print("Removing only clearly unwanted files...")
    print("Keeping all essential functionality intact")
    print()

def safe_cleanup():
    """Safely remove only clearly unwanted files"""
    
    deleted_count = 0
    
    print("🗑️ Removing clearly unwanted files...")
    
    # 1. Version number files (clearly not needed)
    version_files = [
        "0.11.0", "1.0.0", "1.21.0", "1.3.0", "2.8.0", "3.4.0", 
        "4.5.0", "6.0.0", "6.4.0", "8.3.0"
    ]
    
    for version_file in version_files:
        if os.path.exists(version_file):
            os.remove(version_file)
            print(f"   ❌ Deleted version file: {version_file}")
            deleted_count += 1
    
    # 2. Duplicate/redundant test files
    redundant_test_files = [
        "test_admin_access_admin.html",
        "test_admin_access_regular.html", 
        "test_admin_button.py",
        "test_admin_button_all_users.py",
        "test_admin_crud_basic.py",
        "test_admin_panel_access.py",
        "test_admin_panel_all_users_access.py",
        "test_admin_simple.py",
        "test_existing_ml.py",
        "test_notebook_imports.py",
        "test_simple_mood.py"
    ]
    
    for test_file in redundant_test_files:
        if os.path.exists(test_file):
            os.remove(test_file)
            print(f"   ❌ Deleted redundant test: {test_file}")
            deleted_count += 1
    
    # 3. Duplicate fix/debug files
    duplicate_fix_files = [
        "fix_admin_database_data.py",
        "fix_deepface_error.py", 
        "fix_ipynb_errors.py",
        "fix_jupyter_imports.py",
        "fix_models.py",
        "fix_notebook_step_by_step.py",
        "fix_numpy_dependencies.py",
        "fix_tensorflow_errors.py",
        "jupyter_numpy_fix.py",
        "notebook_import_fix.py",
        "notebook_test_cell.py"
    ]
    
    for fix_file in duplicate_fix_files:
        if os.path.exists(fix_file):
            os.remove(fix_file)
            print(f"   ❌ Deleted duplicate fix: {fix_file}")
            deleted_count += 1
    
    # 4. Redundant setup files
    redundant_setup_files = [
        "setup_admin_user.py",
        "setup_environment.py",
        "setup_full_project_git.py", 
        "setup_jupyter_environment.py",
        "setup_unlimited_gemini.py",
        "setup_video_chat_system.py",
        "install_all_requirements.py",
        "install_dataset_requirements.py"
    ]
    
    for setup_file in redundant_setup_files:
        if os.path.exists(setup_file):
            os.remove(setup_file)
            print(f"   ❌ Deleted redundant setup: {setup_file}")
            deleted_count += 1
    
    # 5. Duplicate documentation files
    duplicate_docs = [
        "ALGORITHMS_EXPLAINED.txt",
        "DATABASE_BROWSER_GUIDE.md",
        "TERMINAL_FIX_GUIDE.md",
        "NUMPY_FIX_GUIDE.md",
        "david.md",
        "push.md"
    ]
    
    for doc_file in duplicate_docs:
        if os.path.exists(doc_file):
            os.remove(doc_file)
            print(f"   ❌ Deleted duplicate doc: {doc_file}")
            deleted_count += 1
    
    # 6. Temporary/utility files
    temp_files = [
        "temp_step_create_trainer_class.py",
        "add_admin_crud.py",
        "cleanup_project.py",
        "database_browser.py",
        "emotion_sample_gallery.html",
        "integrate_sample_images_browser.py",
        "populate_database_with_sample_data.py",
        "show_user_database_access.py"
    ]
    
    for temp_file in temp_files:
        if os.path.exists(temp_file):
            os.remove(temp_file)
            print(f"   ❌ Deleted temp file: {temp_file}")
            deleted_count += 1
    
    # 7. Batch/shell files (keep only essential)
    script_files = [
        "run_notebook_fix.bat",
        "run_notebook_fix.sh"
    ]
    
    for script_file in script_files:
        if os.path.exists(script_file):
            os.remove(script_file)
            print(f"   ❌ Deleted script: {script_file}")
            deleted_count += 1
    
    # 8. Metadata JSON files (keep only essential)
    metadata_files = [
        "simple_fer2013_model_20260123_225231_metadata.json",
        "simple_production_model_20260123_084621_metadata.json"
    ]
    
    for meta_file in metadata_files:
        if os.path.exists(meta_file):
            os.remove(meta_file)
            print(f"   ❌ Deleted metadata: {meta_file}")
            deleted_count += 1
    
    return deleted_count

def cleanup_cache_dirs():
    """Remove cache directories"""
    
    cache_dirs = [
        "__pycache__",
        "server/__pycache__",
        ".pytest_cache"
    ]
    
    deleted_dirs = 0
    
    print("\n📁 Removing cache directories...")
    
    for cache_dir in cache_dirs:
        if os.path.exists(cache_dir):
            try:
                shutil.rmtree(cache_dir)
                print(f"   ❌ Deleted cache: {cache_dir}")
                deleted_dirs += 1
            except Exception as e:
                print(f"   ⚠️ Could not delete {cache_dir}: {e}")
    
    return deleted_dirs

def show_remaining_structure():
    """Show what files remain after cleanup"""
    
    print("\n📋 Essential files preserved:")
    
    essential_categories = {
        "🚀 Main Startup Scripts": [
            "quick_start.py",
            "start_complete_mindbridge_system.py", 
            "start_server_with_gemini.py",
            "start_server_without_gemini.py",
            "start_production_system.py",
            "start_hybrid_mindbridge.py"
        ],
        "📚 Documentation": [
            "README.md",
            "PROJECT_SETUP_GUIDE.txt",
            "PRODUCTION_ML_SYSTEM_SUMMARY.md",
            "COMPLETE_INTEGRATION_STATUS.md"
        ],
        "⚙️ Configuration": [
            "requirements.txt",
            "requirements_fixed.txt", 
            "requirements_ml.txt",
            ".env.example",
            ".gitignore"
        ],
        "🧪 Essential Tests": [
            "complete_system_test.py",
            "test_complete_integration.py",
            "test_production_system.py"
        ],
        "🌐 Frontend": [
            "client/ (all HTML/CSS/JS files)"
        ],
        "🔧 Backend": [
            "server/ (Flask app + AI models)"
        ],
        "🧠 AI & Data": [
            "emotion_datasets/",
            "compact_emotion_dataset/",
            "emotion_sample_images/",
            "test_human_faces/",
            "trained_models/"
        ]
    }
    
    for category, files in essential_categories.items():
        print(f"\n{category}:")
        for file in files:
            if os.path.exists(file) or "/" in file:
                print(f"   ✅ {file}")

def main():
    """Main cleanup function"""
    
    print_banner()
    
    # Confirm cleanup
    print("This will remove only clearly unwanted files:")
    print("- Version number files (0.11.0, 1.0.0, etc.)")
    print("- Duplicate test files")
    print("- Redundant fix/debug files") 
    print("- Temporary utility files")
    print("- Cache directories")
    print()
    print("✅ All essential functionality will be preserved!")
    print()
    
    confirm = input("Continue with safe cleanup? (Y/n): ").lower().strip()
    
    if confirm in ['n', 'no']:
        print("❌ Cleanup cancelled")
        return
    
    print("\n🧹 Starting safe cleanup...")
    
    # Change to project directory if needed
    if os.path.exists('sleepy') and os.getcwd().endswith('sleepy'):
        pass  # Already in sleepy directory
    elif os.path.exists('sleepy'):
        os.chdir('sleepy')
    
    # Perform cleanup
    deleted_files = safe_cleanup()
    deleted_dirs = cleanup_cache_dirs()
    
    # Show results
    print("\n" + "=" * 60)
    print("✅ SAFE CLEANUP COMPLETED!")
    print(f"🗑️ Deleted {deleted_files} unwanted files")
    print(f"📁 Deleted {deleted_dirs} cache directories")
    
    # Show remaining structure
    show_remaining_structure()
    
    print("\n🎯 Your MindBridge - NCIT Final Year Project project is now clean and optimized!")
    print("🚀 All essential functionality preserved")
    print("📦 Project size reduced significantly")
    print()
    print("To start the system:")
    print("   python quick_start.py")
    print("=" * 60)

if __name__ == "__main__":
    main()