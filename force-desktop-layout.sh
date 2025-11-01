#!/bin/bash

# Script to force desktop layout for all student tools
# This script updates the viewport meta tag to prevent mobile scaling

echo "🔧 Updating all student tools to force desktop layout..."
echo ""

# Counter for files processed
count=0

# Find all HTML files in student tools directory
find client/tools/student -name "*.html" -type f | while read file; do
    # Check if file contains the standard viewport meta tag
    if grep -q 'name="viewport" content="width=device-width, initial-scale=1.0"' "$file"; then
        # Replace with desktop-forced viewport
        sed -i '' 's/<meta name="viewport" content="width=device-width, initial-scale=1.0">/<meta name="viewport" content="width=1200, initial-scale=1.0, minimum-scale=1.0, user-scalable=yes">/' "$file"
        
        echo "✅ Updated: $file"
        ((count++))
    fi
done

echo ""
echo "🎉 Completed! Updated $count student tool files."
echo ""
echo "Changes made:"
echo "- Set minimum viewport width to 1200px (desktop width)"
echo "- Disabled mobile-responsive scaling"
echo "- Student tools will always display in desktop layout"
echo ""
echo "You can now commit these changes to git."
