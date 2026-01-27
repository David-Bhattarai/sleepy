#!/usr/bin/env python3
"""
Delete All .md Files Script
Remove all markdown files except README.md
"""

import os
import glob

def print_banner():
    print("🗑️ DELETE ALL .MD FILES")
    print("=" * 40)
    print("Removing all markdown files except README.md...")
    print()

def get_md_files_to_delete():
    """Get all .md files except README.md"""
    
    all_md_files = []
    
    # Get .md files in root directory
    all_md_files.extend(glob.glob("*.md"))
    
    # Get .md files in subdirectories
    for root, dirs, files in os.walk('.'):
        # Skip hidden directories
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                all_md_files.append(file_path)
    
    # Remove duplicates and filter out README.md
    md_files_to_delete = []
    for file_path in set(all_md_files):
        if not file_path.endswith('README.md') and 'README.md' not in file_path:
            md_files_to_delete.append(file_path)
    
    return sorted(md_files_to_delete)

def delete_md_files():
    """Delete all .md files except README.md"""
    
    md_files = get_md_files_to_delete()
    
    if not md_files:
        print("📁 No .md files found to delete (README.md preserved)")
        return 0
    
    print(f"📁 Found {len(md_files)} .md files to delete:")
    for file_path in md_files:
        print(f"   - {file_path}")
    
    print()
    confirm = input("Delete all these .md files? (Y/n): ").lower().strip()
    
    if confirm in ['n', 'no']:
        print("❌ Deletion cancelled")
        return 0
    
    deleted_count = 0
    
    print("\n🗑️ Deleting .md files...")
    
    for file_path in md_files:
        try:
            os.remove(file_path)
            print(f"   ❌ Deleted: {file_path}")
            deleted_count += 1
        except Exception as e:
            print(f"   ⚠️ Could not delete {file_path}: {e}")
    
    return deleted_count

def main():
    """Main deletion function"""
    
    print_banner()
    
    # Change to project directory if needed
    if os.path.exists('sleepy') and not os.getcwd().endswith('sleepy'):
        os.chdir('sleepy')
    
    # Delete .md files
    deleted_count = delete_md_files()
    
    print("\n" + "=" * 40)
    print("✅ MD FILES CLEANUP COMPLETED!")
    print(f"🗑️ Deleted {deleted_count} .md files")
    print("✅ README.md preserved")
    print()
    print("📋 Remaining documentation:")
    print("   - ✅ README.md (main project documentation)")
    
    # Check for remaining .txt files
    txt_files = glob.glob("*.txt")
    if txt_files:
        print("   - ✅ .txt files preserved:")
        for txt_file in txt_files:
            print(f"     - {txt_file}")
    
    print()
    print("🚀 Your MindBridge - NCIT Final Year Project project is now cleaner!")
    print("=" * 40)

if __name__ == "__main__":
    main()