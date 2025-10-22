#!/usr/bin/env python3
"""
Domain Update Script for Scribble Tools
This script updates all domain references from scribbletools.com to scribbletools.in
across all files in the project.
"""

import os
import re
import glob
from pathlib import Path

def update_domain_in_file(file_path):
    """
    Update domain references in a single file.
    
    Args:
        file_path (str): Path to the file to update
        
    Returns:
        bool: True if file was modified, False otherwise
    """
    try:
        # Read the file
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Store original content to check if changes were made
        original_content = content
        
        # Replace all variations of the old domain with new domain
        replacements = [
            # HTTPS URLs
            ('https://scribbletools.com', 'https://scribbletools.in'),
            ('https://www.scribbletools.com', 'https://scribbletools.in'),
            
            # HTTP URLs
            ('http://scribbletools.com', 'http://scribbletools.in'),
            ('http://www.scribbletools.com', 'http://scribbletools.in'),
            
            # Domain only (without protocol)
            ('scribbletools.com', 'scribbletools.in'),
            ('www.scribbletools.com', 'scribbletools.in'),
            
            # scribbletools.net variations
            ('https://scribbletools.net', 'https://scribbletools.in'),
            ('https://www.scribbletools.net', 'https://scribbletools.in'),
            ('http://scribbletools.net', 'http://scribbletools.in'),
            ('http://www.scribbletools.net', 'http://scribbletools.in'),
            ('scribbletools.net', 'scribbletools.in'),
            ('www.scribbletools.net', 'scribbletools.in'),
            
            # scribbletools.netlify.app variations
            ('https://scribbletools.netlify.app', 'https://scribbletools.in'),
            ('https://www.scribbletools.netlify.app', 'https://scribbletools.in'),
            ('http://scribbletools.netlify.app', 'http://scribbletools.in'),
            ('http://www.scribbletools.netlify.app', 'http://scribbletools.in'),
            ('scribbletools.netlify.app', 'scribbletools.in'),
            ('www.scribbletools.netlify.app', 'scribbletools.in'),
            
            # scribbletools.org variations
            ('https://scribbletools.org', 'https://scribbletools.in'),
            ('https://www.scribbletools.org', 'https://scribbletools.in'),
            ('http://scribbletools.org', 'http://scribbletools.in'),
            ('http://www.scribbletools.org', 'http://scribbletools.in'),
            ('scribbletools.org', 'scribbletools.in'),
            ('www.scribbletools.org', 'scribbletools.in'),
            
        # Also handle any studenttools.com references that might exist
        ('https://studenttools.com', 'https://scribbletools.in'),
        ('https://www.studenttools.com', 'https://scribbletools.in'),
        ('http://studenttools.com', 'http://scribbletools.in'),
        ('http://www.studenttools.com', 'http://scribbletools.in'),
        ('studenttools.com', 'scribbletools.in'),
        ('www.studenttools.com', 'scribbletools.in'),
        
        # Handle allinone.tools and allinone-tools.com variations
        ('https://allinone.tools', 'https://scribbletools.in'),
        ('https://www.allinone.tools', 'https://scribbletools.in'),
        ('http://allinone.tools', 'http://scribbletools.in'),
        ('http://www.allinone.tools', 'http://scribbletools.in'),
        ('allinone.tools', 'scribbletools.in'),
        ('www.allinone.tools', 'scribbletools.in'),
        
        ('https://allinone-tools.com', 'https://scribbletools.in'),
        ('https://www.allinone-tools.com', 'https://scribbletools.in'),
        ('http://allinone-tools.com', 'http://scribbletools.in'),
        ('http://www.allinone-tools.com', 'http://scribbletools.in'),
        ('allinone-tools.com', 'scribbletools.in'),
        ('www.allinone-tools.com', 'scribbletools.in'),
        
        # Handle variations in capitalization and branding
        ('AllInOne.Tools', 'Scribble Tools'),
        ('AllInOne-Tools', 'Scribble Tools'),
        ('AllInOne Tools', 'Scribble Tools'),
        ('allinone.tools', 'scribbletools.in'),
        ('Allinone.Tools', 'Scribble Tools'),
        ('allinone-tools', 'scribbletools'),            # Handle GitHub Pages references
            ('https://jaswanth-mjy.github.io/allinone.github.io', 'https://scribbletools.in'),
            ('https://allinone-tools.github.io', 'https://scribbletools.in'),
            ('https://allinone.github.io', 'https://scribbletools.in'),
            ('https://jaswanth-mjy.github.io/scribbletools-calculator-suite', 'https://scribbletools.in'),
            ('jaswanth-mjy.github.io/allinone.github.io', 'scribbletools.in'),
            ('allinone-tools.github.io', 'scribbletools.in'),
            ('allinone.github.io', 'scribbletools.in'),
            ('jaswanth-mjy.github.io/scribbletools-calculator-suite', 'scribbletools.in'),
        ]
        
        # Apply all replacements
        for old_domain, new_domain in replacements:
            content = content.replace(old_domain, new_domain)
        
        # Check if any changes were made
        if content != original_content:
            # Write the updated content back to the file
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
            return True
        
        return False
        
    except Exception as e:
        print(f"Error processing {file_path}: {str(e)}")
        return False

def find_files_to_update(root_dir):
    """
    Find all files that should be updated.
    
    Args:
        root_dir (str): Root directory to search from
        
    Returns:
        list: List of file paths to update
    """
    # File extensions to check
    extensions = [
        '*.html', '*.htm', '*.php', '*.js', '*.css', '*.json', 
        '*.xml', '*.txt', '*.md', '*.yml', '*.yaml', '*.htaccess',
        '*.py', '*.config', '*.conf'
    ]
    
    files_to_update = []
    
    # Search for files with specified extensions
    for ext in extensions:
        pattern = os.path.join(root_dir, '**', ext)
        files = glob.glob(pattern, recursive=True)
        files_to_update.extend(files)
    
    # Filter out certain directories and files
    exclude_patterns = [
        '.git',
        'node_modules',
        '.env',
        '__pycache__',
        '.DS_Store',
        'update_domain.py'  # Don't update this script itself
    ]
    
    filtered_files = []
    for file_path in files_to_update:
        # Check if file should be excluded
        should_exclude = False
        for exclude_pattern in exclude_patterns:
            if exclude_pattern in file_path:
                should_exclude = True
                break
        
        if not should_exclude and os.path.isfile(file_path):
            filtered_files.append(file_path)
    
    return filtered_files

def main():
    """Main function to run the domain update process."""
    
    print("🔄 Scribble Tools Domain Update Script")
    print("=" * 50)
    print("Updating all domain references from scribbletools.com to scribbletools.in")
    print()
    
    # Get the current directory (project root)
    root_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"📂 Project root: {root_dir}")
    print()
    
    # Find all files to update
    print("🔍 Searching for files to update...")
    files_to_update = find_files_to_update(root_dir)
    
    if not files_to_update:
        print("❌ No files found to update.")
        return
    
    print(f"📋 Found {len(files_to_update)} files to check")
    print()
    
    # Process each file
    updated_files = []
    skipped_files = []
    
    for file_path in files_to_update:
        relative_path = os.path.relpath(file_path, root_dir)
        print(f"🔧 Processing: {relative_path}... ", end="")
        
        if update_domain_in_file(file_path):
            print("✅ Updated")
            updated_files.append(relative_path)
        else:
            print("⏭️  No changes needed")
            skipped_files.append(relative_path)
    
    # Print summary
    print()
    print("📊 Update Summary")
    print("=" * 30)
    print(f"✅ Files updated: {len(updated_files)}")
    print(f"⏭️  Files skipped: {len(skipped_files)}")
    print(f"📁 Total files processed: {len(files_to_update)}")
    
    if updated_files:
        print()
        print("📝 Updated files:")
        for file_path in updated_files:
            print(f"   • {file_path}")
    
    print()
    print("🎉 Domain update completed successfully!")
    print("🌐 All references now point to: scribbletools.in")

if __name__ == "__main__":
    main()