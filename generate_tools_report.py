#!/usr/bin/env python3
"""
Comprehensive Tools Report Generator
This script generates a detailed report of all tools in the project,
their URLs, and verifies domain consistency.
"""

import os
import re
import json
from pathlib import Path
from urllib.parse import urljoin

def extract_tool_info(file_path):
    """Extract tool information from HTML files"""
    tool_info = {
        'file': file_path,
        'title': 'Unknown Tool',
        'description': '',
        'canonical_url': '',
        'og_url': '',
        'domains_found': [],
        'category': '',
        'tool_name': ''
    }
    
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Extract title
        title_match = re.search(r'<title[^>]*>(.*?)</title>', content, re.IGNORECASE | re.DOTALL)
        if title_match:
            tool_info['title'] = title_match.group(1).strip()
        
        # Extract meta description
        desc_match = re.search(r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']*)["\']', content, re.IGNORECASE)
        if desc_match:
            tool_info['description'] = desc_match.group(1).strip()
        
        # Extract canonical URL
        canonical_match = re.search(r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']*)["\']', content, re.IGNORECASE)
        if canonical_match:
            tool_info['canonical_url'] = canonical_match.group(1).strip()
        
        # Extract Open Graph URL
        og_match = re.search(r'<meta\s+property=["\']og:url["\']\s+content=["\']([^"\']*)["\']', content, re.IGNORECASE)
        if og_match:
            tool_info['og_url'] = og_match.group(1).strip()
        
        # Find all domain references
        domain_patterns = [
            r'https?://[a-zA-Z0-9.-]+\.[a-zA-Z]{2,10}',
            r'[a-zA-Z0-9.-]+\.(?:com|net|org|in|io|dev|app|co|me|tools)',
        ]
        
        all_domains = set()
        for pattern in domain_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                # Filter out common external domains we don't want to track
                if not any(exclude in match.lower() for exclude in [
                    'fonts.googleapis.com', 'fonts.gstatic.com', 'cdnjs.cloudflare.com',
                    'schema.org', 'w3.org', 'mozilla.org', 'github.com', 'google.com',
                    'brevo.com', 'mailchimp.com', 'tailwindcss.com'
                ]):
                    all_domains.add(match)
        
        tool_info['domains_found'] = sorted(list(all_domains))
        
        # Determine category from file path
        path_parts = Path(file_path).parts
        if 'financial' in path_parts:
            tool_info['category'] = 'Financial'
        elif 'health' in path_parts:
            tool_info['category'] = 'Health & Fitness'
        elif 'math' in path_parts:
            tool_info['category'] = 'Math & Statistics'
        elif 'image' in path_parts:
            tool_info['category'] = 'Image Tools'
        elif 'text' in path_parts:
            tool_info['category'] = 'Text Tools'
        elif 'student' in path_parts:
            if 'career' in path_parts:
                tool_info['category'] = 'Student - Career'
            elif 'academic' in path_parts:
                tool_info['category'] = 'Student - Academic'
            elif 'finance' in path_parts:
                tool_info['category'] = 'Student - Finance'
            elif 'productivity' in path_parts:
                tool_info['category'] = 'Student - Productivity'
            elif 'writing' in path_parts:
                tool_info['category'] = 'Student - Writing'
            elif 'skills' in path_parts:
                tool_info['category'] = 'Student - Skills'
            elif 'planning' in path_parts:
                tool_info['category'] = 'Student - Planning'
            elif 'wellness' in path_parts:
                tool_info['category'] = 'Student - Wellness'
            else:
                tool_info['category'] = 'Student Tools'
        elif 'other' in path_parts:
            tool_info['category'] = 'Other Tools'
        else:
            tool_info['category'] = 'General'
        
        # Extract tool name from file name
        tool_info['tool_name'] = Path(file_path).stem.replace('-', ' ').title()
        
    except Exception as e:
        print(f"❌ Error processing {file_path}: {str(e)}")
    
    return tool_info

def find_all_tools():
    """Find all HTML tool files in the project"""
    tool_files = []
    
    # Search for HTML files in client/tools directory
    tools_dir = Path('client/tools')
    if tools_dir.exists():
        for html_file in tools_dir.rglob('*.html'):
            tool_files.append(str(html_file))
    
    # Also check for main index.html
    if os.path.exists('index.html'):
        tool_files.append('index.html')
    
    return sorted(tool_files)

def check_domain_consistency(tools_data):
    """Check for domain consistency across all tools"""
    domain_issues = {
        'correct_scribbletools_in': 0,
        'incorrect_domains': [],
        'missing_canonical': [],
        'missing_og_url': [],
        'inconsistent_urls': []
    }
    
    for tool in tools_data:
        # Check for correct scribbletools.in usage
        scribbletools_in_count = sum(1 for domain in tool['domains_found'] 
                                   if 'scribbletools.in' in domain)
        if scribbletools_in_count > 0:
            domain_issues['correct_scribbletools_in'] += 1
        
        # Check for incorrect domains
        for domain in tool['domains_found']:
            if any(incorrect in domain.lower() for incorrect in [
                'allinone.tools', 'allinone-tools.com', 'scribbletools.com',
                'scribbletools.net', 'scribbletools.org'
            ]):
                domain_issues['incorrect_domains'].append({
                    'file': tool['file'],
                    'domain': domain,
                    'tool_name': tool['tool_name']
                })
        
        # Check for missing canonical URLs
        if not tool['canonical_url']:
            domain_issues['missing_canonical'].append({
                'file': tool['file'],
                'tool_name': tool['tool_name']
            })
        
        # Check for missing OG URLs
        if not tool['og_url']:
            domain_issues['missing_og_url'].append({
                'file': tool['file'],
                'tool_name': tool['tool_name']
            })
        
        # Check for inconsistent URLs
        if tool['canonical_url'] and tool['og_url']:
            if tool['canonical_url'] != tool['og_url']:
                domain_issues['inconsistent_urls'].append({
                    'file': tool['file'],
                    'canonical': tool['canonical_url'],
                    'og_url': tool['og_url'],
                    'tool_name': tool['tool_name']
                })
    
    return domain_issues

def generate_markdown_report(tools_data, domain_issues):
    """Generate a comprehensive markdown report"""
    report = []
    
    # Header
    report.append("# 🛠️ Scribble Tools - Comprehensive Tools Report")
    report.append("=" * 60)
    report.append(f"📅 **Generated:** {os.popen('date').read().strip()}")
    report.append(f"📂 **Project Root:** {os.getcwd()}")
    report.append(f"🌐 **Domain:** scribbletools.in")
    report.append("")
    
    # Summary Statistics
    total_tools = len(tools_data)
    categories = {}
    for tool in tools_data:
        category = tool['category']
        categories[category] = categories.get(category, 0) + 1
    
    report.append("## 📊 Summary Statistics")
    report.append("-" * 30)
    report.append(f"- **Total Tools:** {total_tools}")
    report.append(f"- **Categories:** {len(categories)}")
    report.append(f"- **Tools with scribbletools.in:** {domain_issues['correct_scribbletools_in']}")
    report.append(f"- **Domain Issues Found:** {len(domain_issues['incorrect_domains'])}")
    report.append("")
    
    # Category Breakdown
    report.append("### 📋 Tools by Category")
    for category, count in sorted(categories.items()):
        report.append(f"- **{category}:** {count} tools")
    report.append("")
    
    # Domain Consistency Report
    report.append("## 🔍 Domain Consistency Analysis")
    report.append("-" * 40)
    
    if domain_issues['incorrect_domains']:
        report.append("### ⚠️ Incorrect Domains Found")
        for issue in domain_issues['incorrect_domains']:
            report.append(f"- **{issue['tool_name']}** (`{issue['file']}`)")
            report.append(f"  - ❌ Found: `{issue['domain']}`")
        report.append("")
    else:
        report.append("### ✅ Domain Consistency Check")
        report.append("🎉 **Excellent!** No incorrect domains found. All tools use scribbletools.in consistently.")
        report.append("")
    
    if domain_issues['inconsistent_urls']:
        report.append("### 🔗 URL Inconsistencies")
        for issue in domain_issues['inconsistent_urls']:
            report.append(f"- **{issue['tool_name']}** (`{issue['file']}`)")
            report.append(f"  - Canonical: `{issue['canonical']}`")
            report.append(f"  - OG URL: `{issue['og_url']}`")
        report.append("")
    
    # Complete Tools Listing
    report.append("## 🛠️ Complete Tools Directory")
    report.append("-" * 40)
    
    # Group tools by category
    tools_by_category = {}
    for tool in tools_data:
        category = tool['category']
        if category not in tools_by_category:
            tools_by_category[category] = []
        tools_by_category[category].append(tool)
    
    for category in sorted(tools_by_category.keys()):
        report.append(f"\n### 📁 {category}")
        report.append("")
        
        for tool in sorted(tools_by_category[category], key=lambda x: x['tool_name']):
            report.append(f"#### 🔧 {tool['tool_name']}")
            report.append(f"- **File:** `{tool['file']}`")
            report.append(f"- **Title:** {tool['title']}")
            
            if tool['canonical_url']:
                report.append(f"- **URL:** {tool['canonical_url']}")
            elif tool['og_url']:
                report.append(f"- **URL:** {tool['og_url']}")
            else:
                # Generate expected URL
                relative_path = tool['file'].replace('client/tools/', '').replace('.html', '')
                expected_url = f"https://scribbletools.in/client/tools/{relative_path}.html"
                report.append(f"- **Expected URL:** {expected_url}")
            
            if tool['description']:
                description = tool['description'][:100] + "..." if len(tool['description']) > 100 else tool['description']
                report.append(f"- **Description:** {description}")
            
            # Show domain status
            scribbletools_domains = [d for d in tool['domains_found'] if 'scribbletools.in' in d]
            if scribbletools_domains:
                report.append(f"- **Domain Status:** ✅ Uses scribbletools.in")
            elif tool['domains_found']:
                report.append(f"- **Domain Status:** ⚠️ Other domains: {', '.join(tool['domains_found'][:3])}")
            else:
                report.append(f"- **Domain Status:** ❓ No domains detected")
            
            report.append("")
    
    # SEO and Technical Details
    report.append("## 🔧 Technical Analysis")
    report.append("-" * 30)
    
    report.append(f"### 📋 Missing Canonical URLs: {len(domain_issues['missing_canonical'])}")
    if domain_issues['missing_canonical']:
        for item in domain_issues['missing_canonical'][:10]:  # Show first 10
            report.append(f"- {item['tool_name']} (`{item['file']}`)")
        if len(domain_issues['missing_canonical']) > 10:
            report.append(f"- ... and {len(domain_issues['missing_canonical']) - 10} more")
    report.append("")
    
    report.append(f"### 📋 Missing OG URLs: {len(domain_issues['missing_og_url'])}")
    if domain_issues['missing_og_url']:
        for item in domain_issues['missing_og_url'][:10]:  # Show first 10
            report.append(f"- {item['tool_name']} (`{item['file']}`)")
        if len(domain_issues['missing_og_url']) > 10:
            report.append(f"- ... and {len(domain_issues['missing_og_url']) - 10} more")
    report.append("")
    
    # Recommendations
    report.append("## 💡 Recommendations")
    report.append("-" * 25)
    
    if not domain_issues['incorrect_domains'] and domain_issues['correct_scribbletools_in'] > 0:
        report.append("### 🎉 Excellent Domain Consistency!")
        report.append("- All tools consistently use the correct scribbletools.in domain")
        report.append("- No legacy domain references found")
        report.append("- SEO and branding consistency maintained")
    
    if domain_issues['missing_canonical'] or domain_issues['missing_og_url']:
        report.append("### 🔧 SEO Improvements Needed")
        report.append("- Add missing canonical URLs for better SEO")
        report.append("- Add missing Open Graph URLs for social media sharing")
        report.append("- Ensure URL consistency across meta tags")
    
    if not domain_issues['missing_canonical'] and not domain_issues['missing_og_url']:
        report.append("### ✅ SEO Status")
        report.append("- All tools have proper canonical URLs")
        report.append("- All tools have Open Graph URLs")
        report.append("- SEO meta tags are properly configured")
    
    report.append("")
    report.append("---")
    report.append("*Report generated by Scribble Tools Analysis Script*")
    
    return '\n'.join(report)

def main():
    """Main function to generate the comprehensive tools report"""
    print("🛠️ Scribble Tools - Comprehensive Analysis")
    print("=" * 50)
    print("Analyzing all tools in the project...")
    print()
    
    # Find all tool files
    tool_files = find_all_tools()
    print(f"📂 Found {len(tool_files)} HTML files to analyze")
    
    # Extract information from each tool
    tools_data = []
    for i, file_path in enumerate(tool_files, 1):
        print(f"🔄 Processing ({i}/{len(tool_files)}): {file_path}")
        tool_info = extract_tool_info(file_path)
        tools_data.append(tool_info)
    
    print(f"\n✅ Analysis complete! Processed {len(tools_data)} tools")
    
    # Check domain consistency
    print("🔍 Checking domain consistency...")
    domain_issues = check_domain_consistency(tools_data)
    
    # Generate report
    print("📄 Generating comprehensive report...")
    report_content = generate_markdown_report(tools_data, domain_issues)
    
    # Save report
    report_filename = "TOOLS_COMPREHENSIVE_REPORT.md"
    try:
        with open(report_filename, 'w', encoding='utf-8') as f:
            f.write(report_content)
        print(f"✅ Report saved to: {report_filename}")
    except Exception as e:
        print(f"❌ Error saving report: {str(e)}")
    
    # Display summary
    print("\n📊 Quick Summary:")
    print(f"   • Total Tools: {len(tools_data)}")
    print(f"   • Tools with scribbletools.in: {domain_issues['correct_scribbletools_in']}")
    print(f"   • Domain Issues: {len(domain_issues['incorrect_domains'])}")
    print(f"   • Missing Canonical URLs: {len(domain_issues['missing_canonical'])}")
    print(f"   • Missing OG URLs: {len(domain_issues['missing_og_url'])}")
    
    if not domain_issues['incorrect_domains']:
        print("\n🎉 Domain Status: EXCELLENT - All tools use scribbletools.in!")
    else:
        print(f"\n⚠️  Domain Status: {len(domain_issues['incorrect_domains'])} issues found")
    
    return {
        'tools_count': len(tools_data),
        'domain_issues': domain_issues,
        'report_file': report_filename
    }

if __name__ == "__main__":
    main()