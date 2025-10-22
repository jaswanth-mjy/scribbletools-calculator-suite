#!/usr/bin/env python3
"""
Fix malformed domains that were incorrectly replaced
This script fixes scribbletools.in to scribbletools.in
"""

import os
import glob
import re

def fix_malformed_domains(file_path):
    """Fix malformed domain references in a single file"""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        original_content = content
        
        # Fix the malformed domains
        content = content.replace('scribbletools.in', 'scribbletools.in')
        content = content.replace('https://scribbletools.in/', 'https://scribbletools.in/')
        
        # Check if any changes were made
        if content != original_content:
            # Write the updated content back to the file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
    except Exception as e:
        print(f"❌ Error processing {file_path}: {str(e)}")
        return False

def get_files_to_process():
    """Get all files that might contain domain references"""
    file_patterns = [
        '**/*.html', '**/*.css', '**/*.js', '**/*.php', '**/*.xml', '**/*.md',
        '**/*.json', '**/*.txt', '**/*.py', '**/*.config', '**/*.conf'
    ]
    
    files = []
    for pattern in file_patterns:
        files.extend(glob.glob(pattern, recursive=True))
    
    # Filter out unwanted files and directories
    filtered_files = []
    for file_path in files:
        # Skip directories, hidden files, and certain file types
        if (os.path.isfile(file_path) and 
            not file_path.startswith('.') and
            'node_modules' not in file_path and
            '.git' not in file_path and
            '__pycache__' not in file_path):
            filtered_files.append(file_path)
    
    return sorted(filtered_files)

def main():
    """Main function to fix malformed domains"""
    print("🔧 Fixing Malformed Domain References")
    print("=" * 50)
    print("Fixing scribbletools.in → scribbletools.in")
    print(f"📂 Project root: {os.getcwd()}")
    print()
    
    files_to_process = get_files_to_process()
    print(f"🔍 Found {len(files_to_process)} files to check")
    print()
    
    updated_files = []
    skipped_files = []
    
    for i, file_path in enumerate(files_to_process, 1):
        relative_path = os.path.relpath(file_path)
        
        if fix_malformed_domains(file_path):
            print(f"🔧 Processing: {relative_path}... ✅ Fixed")
            updated_files.append(relative_path)
        else:
            print(f"🔧 Processing: {relative_path}... ⏭️  No changes needed")
            skipped_files.append(relative_path)
    
    print()
    print("📊 Fix Summary")
    print("=" * 30)
    print(f"✅ Files fixed: {len(updated_files)}")
    print(f"⏭️  Files skipped: {len(skipped_files)}")
    print(f"📁 Total files processed: {len(files_to_process)}")
    
    if updated_files:
        print()
        print("📝 Fixed files:")
        for file_path in updated_files:
            print(f"   • {file_path}")
    
    print()
    print("🎉 Domain fix completed successfully!")
    print("🌐 All malformed references now point to: scribbletools.in")

if __name__ == "__main__":
    main()