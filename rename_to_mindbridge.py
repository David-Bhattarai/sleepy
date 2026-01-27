#!/usr/bin/env python3
"""
Rename MindBridge - NCIT Final Year Project to MindBridge - NCIT Final Year Project throughout the entire project
Replace all references in files, comments, documentation, and UI
"""

import os
import re
import glob

def print_banner():
    print("🔄 MindBridge - NCIT Final Year Project → MindBridge - NCIT Final Year Project Renaming Script")
    print("=" * 50)
    print("Replacing all MindBridge - NCIT Final Year Project references with MindBridge - NCIT Final Year Project...")
    print()

def get_files_to_update():
    """Get all files that need to be updated"""
    
    file_patterns = [
        "*.py",
        "*.html", 
        "*.js",
        "*.css",
        "*.md",
        "*.txt",
        "*.json"
    ]
    
    files_to_update = []
    
    # Get files in root directory
    for pattern in file_patterns:
        files_to_update.extend(glob.glob(pattern))
    
    # Get files in subdirectories
    for root, dirs, files in os.walk('.'):
        # Skip hidden directories and cache
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
        
        for file in files:
            file_path = os.path.join(root, file)
            if any(file.endswith(pattern[1:]) for pattern in file_patterns):
                files_to_update.append(file_path)
    
    return list(set(files_to_update))  # Remove duplicates

def create_replacement_map():
    """Create mapping of MindBridge - NCIT Final Year Project variations to MindBridge - NCIT Final Year Project variations"""
    
    return {
        # Exact matches
        'MindBridge': 'MindBridge',
        'MindBridge': 'MindBridge', 
        'mindbridge': 'mindbridge',
        
        # With spaces/punctuation
        'MindBridge - NCIT Final Year Project ': 'MindBridge - NCIT Final Year Project ',
        'MindBridge - NCIT Final Year Project ': 'MindBridge - NCIT Final Year Project ',
        'mindbridge ': 'mindbridge ',
        
        # In titles/headers
        'MindBridge - NCIT Final Year Project': 'MindBridge - NCIT Final Year Project',
        'MindBridge - NCIT Final Year Project': 'MindBridge - NCIT Final Year Project',
        'MindBridge - NCIT Final Year Project': 'MindBridge - NCIT Final Year Project',
        'MindBridge - NCIT Final Year Project': 'MindBridge - NCIT Final Year Project',
        'MindBridge - NCIT Final Year Project': 'MindBridge - NCIT Final Year Project',
        'MindBridge - NCIT Final Year Project': 'MindBridge - NCIT Final Year Project',
        
        # In descriptions
        'MindBridge - NCIT Final Year Project chatbot': 'MindBridge - NCIT Final Year Project chatbot',
        'MindBridge - NCIT Final Year Project system': 'MindBridge - NCIT Final Year Project system',
        'MindBridge - NCIT Final Year Project platform': 'MindBridge - NCIT Final Year Project platform',
        'MindBridge - NCIT Final Year Project': 'MindBridge - NCIT Final Year Project',
        
        # In code/variables (be careful with these)
        'mindbridge_': 'mindbridge_',
        'MindBridge_': 'MINDBRIDGE_',
        
        # In URLs/paths
        '/mindbridge': '/mindbridge',
        'mindbridge.': 'mindbridge.',
        
        # In quotes
        '"MindBridge"': '"MindBridge"',
        "'MindBridge'": "'MindBridge'",
        '"MindBridge"': '"MindBridge"',
        "'MindBridge'": "'MindBridge'",
        
        # In HTML/JS
        'MindBridge</': 'MindBridge</',
        'MindBridge</': 'MindBridge</',
        '>MindBridge - NCIT Final Year Project<': '>MindBridge - NCIT Final Year Project<',
        '>MindBridge - NCIT Final Year Project<': '>MindBridge - NCIT Final Year Project<',
        
        # Special cases
        'I am MindBridge - NCIT Final Year Project, an NCIT Final Year Project - NCIT Final Year Project, an NCIT Final Year Project': 'I am MindBridge - NCIT Final Year Project, an NCIT Final Year Project - NCIT Final Year Project, an NCIT Final Year Project',
        'I\'m MindBridge': 'I\'m MindBridge',
        'Hello! I am MindBridge - NCIT Final Year Project, developed as an NCIT Final Year Project, an NCIT Final Year Project - NCIT Final Year Project, developed as an NCIT Final Year Project, an NCIT Final Year Project': 'Hello! I am MindBridge - NCIT Final Year Project, developed as an NCIT Final Year Project, an NCIT Final Year Project - NCIT Final Year Project, developed as an NCIT Final Year Project, an NCIT Final Year Project',
        'Conversation with MindBridge - NCIT Final Year Project': 'Conversation with MindBridge - NCIT Final Year Project',
        'with MindBridge': 'with MindBridge',
        'MindBridge - NCIT Final Year Project,': 'MindBridge - NCIT Final Year Project,',
        'MindBridge - NCIT Final Year Project,': 'MindBridge - NCIT Final Year Project,',
        'MindBridge - NCIT Final Year Project.': 'MindBridge - NCIT Final Year Project.',
        'MindBridge - NCIT Final Year Project.': 'MindBridge - NCIT Final Year Project.'
    }

def update_file_content(file_path, replacement_map):
    """Update content of a single file"""
    
    try:
        # Read file content
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        original_content = content
        replacements_made = 0
        
        # Apply replacements
        for old_text, new_text in replacement_map.items():
            if old_text in content:
                content = content.replace(old_text, new_text)
                replacements_made += content.count(new_text) - original_content.count(new_text)
        
        # Write back if changes were made
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return replacements_made
        
        return 0
        
    except Exception as e:
        print(f"   ⚠️ Error updating {file_path}: {e}")
        return 0

def update_specific_files():
    """Update specific important files with custom replacements"""
    
    specific_updates = {
        'README.md': {
            '# MindBridge - NCIT Final Year Project | AI Mental Health Companion': '# MindBridge - NCIT Final Year Project | AI Mental Health Companion',
            'MindBridge - NCIT Final Year Project is an NCIT Final Year Project - a web-based': 'MindBridge - NCIT Final Year Project is an NCIT Final Year Project - a web-based',
            'Your complete mental health AI companion is ready to use.': 'Your complete mental health AI companion is ready to use.'
        },
        
        'client/index.html': {
            '<title>MindBridge - NCIT Final Year Project': '<title>MindBridge - NCIT Final Year Project',
            'Welcome to MindBridge - NCIT Final Year Project': 'Welcome to MindBridge - NCIT Final Year Project'
        },
        
        'server/intents.json': {
            'I\'m Pandora': 'I\'m MindBridge',
            'Call me Pandora': 'Call me MindBridge',
            'I am Pandora': 'I am MindBridge - NCIT Final Year Project, an NCIT Final Year Project - NCIT Final Year Project, an NCIT Final Year Project'
        }
    }
    
    for file_path, replacements in specific_updates.items():
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                for old, new in replacements.items():
                    content = content.replace(old, new)
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                    
                print(f"   ✅ Updated specific content in: {file_path}")
                
            except Exception as e:
                print(f"   ⚠️ Error updating {file_path}: {e}")

def main():
    """Main renaming function"""
    
    print_banner()
    
    # Confirm renaming
    print("This will replace ALL 'MindBridge' references with 'MindBridge':")
    print("- All HTML/JS/CSS files")
    print("- All Python files") 
    print("- All documentation")
    print("- All comments and strings")
    print("- UI text and titles")
    print()
    
    confirm = input("Continue with renaming? (Y/n): ").lower().strip()
    
    if confirm in ['n', 'no']:
        print("❌ Renaming cancelled")
        return
    
    print("\n🔄 Starting MindBridge - NCIT Final Year Project → MindBridge - NCIT Final Year Project renaming...")
    
    # Change to project directory if needed
    if os.path.exists('sleepy') and not os.getcwd().endswith('sleepy'):
        os.chdir('sleepy')
    
    # Get files to update
    files_to_update = get_files_to_update()
    replacement_map = create_replacement_map()
    
    print(f"📁 Found {len(files_to_update)} files to check...")
    
    total_replacements = 0
    updated_files = 0
    
    # Update each file
    for file_path in files_to_update:
        replacements = update_file_content(file_path, replacement_map)
        if replacements > 0:
            print(f"   ✅ {file_path}: {replacements} replacements")
            total_replacements += replacements
            updated_files += 1
    
    # Update specific files with custom content
    print("\n🎯 Updating specific files...")
    update_specific_files()
    
    print("\n" + "=" * 50)
    print("✅ RENAMING COMPLETED!")
    print(f"📁 Updated {updated_files} files")
    print(f"🔄 Made {total_replacements} replacements")
    print()
    print("🎯 MindBridge - NCIT Final Year Project → MindBridge - NCIT Final Year Project conversion successful!")
    print()
    print("Updated components:")
    print("- ✅ Project name and branding")
    print("- ✅ UI text and titles")
    print("- ✅ Documentation")
    print("- ✅ Code comments")
    print("- ✅ Chatbot identity")
    print("- ✅ All user-facing text")
    print()
    print("🚀 Your MindBridge - NCIT Final Year Project project is ready!")
    print("Start with: python quick_start.py")
    print("=" * 50)

if __name__ == "__main__":
    main()