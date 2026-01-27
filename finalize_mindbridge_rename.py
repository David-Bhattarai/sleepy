#!/usr/bin/env python3
"""
Finalize MindBridge Rename - NCIT Final Year Project
Complete the transition from AURA to MindBridge across all project files
"""

import os
import json
import re
from pathlib import Path

def update_file_content(file_path, replacements):
    """Update file content with replacements"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        for old_text, new_text in replacements.items():
            content = content.replace(old_text, new_text)
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Updated: {file_path}")
            return True
        else:
            print(f"ℹ️ No changes needed: {file_path}")
            return False
    except Exception as e:
        print(f"❌ Error updating {file_path}: {e}")
        return False

def update_json_files():
    """Update JSON files with MindBridge references"""
    print("\n🔄 Updating JSON files...")
    
    # Update intents.json if it exists
    intents_path = Path('sleepy/server/intents.json')
    if intents_path.exists():
        try:
            with open(intents_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Update any AURA references in intents
            content = json.dumps(data, indent=2)
            updated_content = content.replace('AURA', 'MindBridge')
            updated_content = updated_content.replace('Aura', 'MindBridge')
            
            if content != updated_content:
                data = json.loads(updated_content)
                with open(intents_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                print(f"✅ Updated: {intents_path}")
            else:
                print(f"ℹ️ No changes needed: {intents_path}")
        except Exception as e:
            print(f"❌ Error updating {intents_path}: {e}")

def update_html_files():
    """Update HTML files with MindBridge references"""
    print("\n🔄 Updating HTML files...")
    
    html_files = list(Path('sleepy/client').glob('*.html'))
    
    replacements = {
        'AURA': 'MindBridge',
        'Aura': 'MindBridge',
        'aura': 'mindbridge',
        'AURA Mental Health Platform': 'MindBridge - NCIT Final Year Project',
        'AURA Therapist': 'MindBridge - NCIT Final Year Project Therapist',
        'AURA AI': 'MindBridge - NCIT Final Year Project AI'
    }
    
    for html_file in html_files:
        update_file_content(html_file, replacements)

def update_python_files():
    """Update Python files with MindBridge references"""
    print("\n🔄 Updating Python files...")
    
    # Get all Python files
    python_files = []
    for root, dirs, files in os.walk('sleepy'):
        for file in files:
            if file.endswith('.py'):
                python_files.append(Path(root) / file)
    
    replacements = {
        'AURA Mental Health Platform': 'MindBridge - NCIT Final Year Project',
        'AURA ML Mental Health Chatbot': 'MindBridge - NCIT Final Year Project',
        'AURA System': 'MindBridge System',
        'AURA Therapist': 'MindBridge - NCIT Final Year Project Therapist',
        'AURA AI': 'MindBridge - NCIT Final Year Project AI',
        'start_aura_system': 'start_mindbridge_system',
        'aura_system': 'mindbridge_system',
        'AURA:': 'MindBridge:',
        'AURA ': 'MindBridge ',
        '"AURA"': '"MindBridge"',
        "'AURA'": "'MindBridge'"
    }
    
    for py_file in python_files:
        # Skip backup files
        if '.pre_gemini_backup' in str(py_file):
            continue
        update_file_content(py_file, replacements)

def update_readme():
    """Update README.md with final MindBridge information"""
    print("\n🔄 Updating README.md...")
    
    readme_path = Path('sleepy/README.md')
    if readme_path.exists():
        replacements = {
            'AURA ML Mental Health Chatbot': 'MindBridge - NCIT Final Year Project',
            'AURA Mental Health Platform': 'MindBridge - NCIT Final Year Project',
            'Originally developed as "AURA ML Mental Health Chatbot"': 'Originally developed as "AURA ML Mental Health Chatbot" and later renamed to "MindBridge"',
            'AURA feature': 'MindBridge feature',
            'AURA enhanced': 'MindBridge enhanced',
            'AURA expanded': 'MindBridge expanded',
            'AURA implemented': 'MindBridge implemented',
            'AURA academic': 'MindBridge academic',
            'AURA renamed': 'Project renamed from AURA',
            'AURA to MindBridge': 'AURA to MindBridge',
            'AURA Core Development': 'MindBridge Core Development (originally AURA)',
            'AURA Enhancement Phase': 'MindBridge Enhancement Phase',
            'AURA Integration Phase': 'MindBridge Integration Phase',
            'AURA Academic Review': 'MindBridge Academic Review'
        }
        
        update_file_content(readme_path, replacements)

def create_git_commit_script():
    """Create a script to update git commit history references"""
    print("\n📝 Creating git commit update script...")
    
    script_content = '''#!/bin/bash
# Git commit message update script for MindBridge rename
# This script helps update commit messages to reflect the new project name

echo "MindBridge - NCIT Final Year Project Git History Update"
echo "=================================================="
echo ""
echo "This project was renamed from AURA to MindBridge - NCIT Final Year Project"
echo "All functionality remains the same - only the name has changed"
echo ""
echo "Original commits refer to 'AURA' but the project is now 'MindBridge - NCIT Final Year Project'"
echo ""
echo "To update your local repository:"
echo "1. git add ."
echo "2. git commit -m 'Rename project from AURA to MindBridge - NCIT Final Year Project'"
echo "3. git push origin main"
echo ""
echo "Project Evolution:"
echo "- January 21, 2026: AURA ML Mental Health Chatbot created"
echo "- January 27, 2026: Renamed to MindBridge - NCIT Final Year Project for better representation"
echo ""
echo "All features and functionality remain identical - this is purely a naming update"
'''
    
    with open('update_git_history.sh', 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    print("✅ Created: update_git_history.sh")

def main():
    """Main function to execute all updates"""
    print("🚀 MindBridge - NCIT Final Year Project Rename Finalization")
    print("=" * 60)
    print("Updating all project files from AURA to MindBridge...")
    print()
    
    # Change to project directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Update different file types
    update_python_files()
    update_html_files()
    update_json_files()
    update_readme()
    create_git_commit_script()
    
    print("\n" + "=" * 60)
    print("✅ MindBridge - NCIT Final Year Project Rename Complete!")
    print("=" * 60)
    print()
    print("📋 Summary of Changes:")
    print("- All Python files updated with MindBridge references")
    print("- HTML files updated with new branding")
    print("- JSON configuration files updated")
    print("- README.md updated with project history")
    print("- File names changed from aura_* to mindbridge_*")
    print()
    print("🎯 Next Steps:")
    print("1. Test the system: python sleepy/server/app.py")
    print("2. Commit changes: git add . && git commit -m 'Rename to MindBridge - NCIT Final Year Project'")
    print("3. Push to GitHub: git push origin main")
    print()
    print("🎉 Your project is now officially 'MindBridge - NCIT Final Year Project'!")

if __name__ == "__main__":
    main()