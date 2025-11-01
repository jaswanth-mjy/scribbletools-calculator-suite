#!/bin/bash

# Script to add desktop layout enforcement CSS and notice banner to student tools

echo "🔧 Adding desktop layout CSS and notice banner to all student tools..."
echo ""

count=0
css_added=0
banner_added=0

# CSS link to add in <head> section
CSS_LINK='    <link rel="stylesheet" href="../force-desktop-layout.css">'

# Desktop notice banner to add after <body> tag
NOTICE_BANNER='    <!-- Desktop Layout Notice for Mobile Users -->
    <div class="mobile-desktop-notice">
        <span class="icon">🖥️</span>
        <strong>Best viewed on desktop:</strong> This tool is optimized for desktop viewing. Pinch to zoom for better mobile experience.
    </div>'

# Find all HTML files in student tools directory
find client/tools/student -name "*.html" -type f | while read file; do
    modified=false
    
    # Add CSS link if not already present
    if ! grep -q "force-desktop-layout.css" "$file"; then
        # Find the closing </head> tag and insert CSS link before it
        if grep -q "</head>" "$file"; then
            # Create temp file with CSS added
            awk -v css="$CSS_LINK" '
                /<\/head>/ {
                    print css
                }
                { print }
            ' "$file" > "$file.tmp" && mv "$file.tmp" "$file"
            
            modified=true
            ((css_added++))
        fi
    fi
    
    # Add desktop notice banner if not already present
    if ! grep -q "mobile-desktop-notice" "$file"; then
        # Find the opening <body> tag and insert banner after it
        if grep -q "<body" "$file"; then
            # Create temp file with banner added
            awk -v banner="$NOTICE_BANNER" '
                /<body[^>]*>/ {
                    print
                    print banner
                    next
                }
                { print }
            ' "$file" > "$file.tmp" && mv "$file.tmp" "$file"
            
            modified=true
            ((banner_added++))
        fi
    fi
    
    if [ "$modified" = true ]; then
        echo "✅ Updated: $file"
        ((count++))
    fi
done

echo ""
echo "🎉 Completed!"
echo "- Total files processed: $count"
echo "- CSS link added to: $css_added files"
echo "- Desktop notice banner added to: $banner_added files"
echo ""
echo "All student tools now enforce desktop layout on all devices!"
