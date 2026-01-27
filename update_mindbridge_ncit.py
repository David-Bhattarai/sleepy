#!/usr/bin/env python3
"""
Update MindBridge - NCIT Final Year Project to MindBridge - NCIT Final Year Project
Simple replacement throughout the project
"""

import os
import glob

def print_banner():
    print("🎓 MindBridge - NCIT Final Year Project → MindBridge - NCIT Final Year Project")
    print("=" * 60)
    print("Updating all MindBridge - NCIT Final Year Project references...")
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
    """Create simple replacement mapping"""
    
    return {
        # Main replacements
        'MindBridge - NCIT Final Year Project | AI Mental Health Companion': 'MindBridge - NCIT Final Year Project | AI Mental Health Companion',
        'MindBridge - NCIT Final Year Project': 'MindBridge - NCIT Final Year Project',
        'MindBridge - NCIT Final Year Project': 'MindBridge - NCIT Final Year Project',
        'MindBridge - NCIT Final Year Project': 'MindBridge - NCIT Final Year Project',
        'MindBridge - NCIT Final Year Project': 'MindBridge - NCIT Final Year Project',
        'MindBridge - NCIT Final Year Project': 'MindBridge - NCIT Final Year Project',
        'MindBridge - NCIT Final Year Project': 'MindBridge - NCIT Final Year Project',
        
        # Title updates
        '<title>MindBridge - NCIT Final Year Project': '<title>MindBridge - NCIT Final Year Project',
        'title="MindBridge - NCIT Final Year Project': 'title="MindBridge - NCIT Final Year Project',
        
        # Navigation and headers
        '>MindBridge - NCIT Final Year Project<': '>MindBridge - NCIT Final Year Project<',
        'Welcome to MindBridge - NCIT Final Year Project': 'Welcome to MindBridge - NCIT Final Year Project',
        
        # Chatbot identity
        'I am MindBridge - NCIT Final Year Project, an NCIT Final Year Project - NCIT Final Year Project, an NCIT Final Year Project': 'I am MindBridge - NCIT Final Year Project, an NCIT Final Year Project - NCIT Final Year Project, an NCIT Final Year Project, an NCIT Final Year Project',
        'I\'m MindBridge': 'I\'m MindBridge - NCIT Final Year Project, an NCIT Final Year Project',
        'Hello! I am MindBridge - NCIT Final Year Project, developed as an NCIT Final Year Project, an NCIT Final Year Project - NCIT Final Year Project, developed as an NCIT Final Year Project, an NCIT Final Year Project': 'Hello! I am MindBridge - NCIT Final Year Project, developed as an NCIT Final Year Project, an NCIT Final Year Project - NCIT Final Year Project, developed as an NCIT Final Year Project, an NCIT Final Year Project, developed as an NCIT Final Year Project',
        
        # Dashboard and admin
        'MindBridge - NCIT Final Year Project | Dashboard': 'MindBridge - NCIT Final Year Project | Dashboard',
        'Database Dashboard - MindBridge - NCIT Final Year Project NCIT Final Year Project - NCIT Final Year Project NCIT Final Year Project': 'Database Dashboard - MindBridge - NCIT Final Year Project NCIT Final Year Project - NCIT Final Year Project NCIT Final Year Project NCIT Final Year Project',
        'Conversation with MindBridge - NCIT Final Year Project': 'Conversation with MindBridge - NCIT Final Year Project',
        
        # Documentation
        'MindBridge - NCIT Final Year Project is an NCIT Final Year Project - a web-based': 'MindBridge - NCIT Final Year Project is an NCIT Final Year Project - a web-based',
        'Your MindBridge - NCIT Final Year Project': 'Your MindBridge - NCIT Final Year Project',
        'the MindBridge - NCIT Final Year Project': 'the MindBridge - NCIT Final Year Project',
        
        # Simple standalone replacements
        'MindBridge - NCIT Final Year Project.': 'MindBridge - NCIT Final Year Project.',
        'MindBridge - NCIT Final Year Project,': 'MindBridge - NCIT Final Year Project,',
        'MindBridge - NCIT Final Year Project ': 'MindBridge - NCIT Final Year Project ',
        
        # Avoid double replacement
        'MindBridge - NCIT Final Year Project': 'MindBridge - NCIT Final Year Project'
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
                replacements_made += 1
        
        # Fix any double replacements
        content = content.replace('MindBridge - NCIT Final Year Project', 'MindBridge - NCIT Final Year Project')
        
        # Write back if changes were made
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return replacements_made
        
        return 0
        
    except Exception as e:
        print(f"   ⚠️ Error updating {file_path}: {e}")
        return 0

def update_readme():
    """Update README.md with NCIT project header"""
    
    if not os.path.exists('README.md'):
        return
    
    try:
        with open('README.md', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Update the main header
        new_header = """# MindBridge - NCIT Final Year Project
## AI Mental Health Companion with Machine Learning

**🎓 Final Year Project - Nepal College of Information Technology (NCIT)**

MindBridge - NCIT Final Year Project is an NCIT Final Year Project - a web-based AI-powered application designed to provide mental health support. It features an advanced machine learning model trained on therapeutic conversation patterns, achieving 90%+ accuracy in intent recognition. The app functions as an empathetic companion with intelligent conversation capabilities.

**🌉 MindBridge - NCIT Final Year Project** - Connecting minds, bridging hearts, healing together.
"""
        
        # Replace the existing header section
        lines = content.split('\n')
        new_lines = []
        skip_header = False
        
        for i, line in enumerate(lines):
            if line.startswith('# MindBridge'):
                # Add new header
                new_lines.extend(new_header.strip().split('\n'))
                skip_header = True
            elif line.startswith('---') and skip_header:
                skip_header = False
                new_lines.append(line)
            elif not skip_header:
                new_lines.append(line)
        
        with open('README.md', 'w', encoding='utf-8') as f:
            f.write('\n'.join(new_lines))
        
        print("   ✅ Updated README.md with NCIT project header")
        
    except Exception as e:
        print(f"   ⚠️ Error updating README.md: {e}")

def main():
    """Main update function"""
    
    print_banner()
    
    # Confirm update
    print("This will update all 'MindBridge' references to 'MindBridge - NCIT Final Year Project'")
    print("throughout the entire project including:")
    print("- All HTML/JS/CSS files")
    print("- All Python files")
    print("- All documentation")
    print("- UI text and titles")
    print("- Chatbot identity")
    print()
    
    confirm = input("Continue with NCIT Final Year Project branding? (Y/n): ").lower().strip()
    
    if confirm in ['n', 'no']:
        print("❌ Update cancelled")
        return
    
    print("\n🎓 Starting NCIT Final Year Project updates...")
    
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
    
    # Update README specifically
    print("\n🎯 Updating README.md...")
    update_readme()
    
    print("\n" + "=" * 60)
    print("✅ NCIT FINAL YEAR PROJECT BRANDING COMPLETED!")
    print(f"📁 Updated {updated_files} files")
    print(f"🔄 Made {total_replacements} replacements")
    print()
    print("🎓 Your project is now branded as:")
    print("   'MindBridge - NCIT Final Year Project'")
    print()
    print("Updated components:")
    print("- ✅ Project titles and headers")
    print("- ✅ Navigation and UI text")
    print("- ✅ Chatbot identity")
    print("- ✅ Documentation")
    print("- ✅ Admin panel branding")
    print("- ✅ All user-facing text")
    print()
    print("🚀 Your NCIT Final Year Project is ready!")
    print("Start with: python quick_start.py")
    print("=" * 60)

if __name__ == "__main__":
    main()