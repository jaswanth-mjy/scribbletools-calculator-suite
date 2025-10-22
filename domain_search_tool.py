#!/usr/bin/env python3
"""
Domain Search and Analysis Tool
This script searches for all domain references in the project and categorizes them
to help identify any domains that might need updating or reviewing.
"""

import os
import glob
import re
from collections import defaultdict

def search_domains_in_file(file_path):
    """Search for domain patterns in a single file"""
    domain_patterns = {
        'project_domains': [
            r'scribbletools\.[a-zA-Z]{2,10}',
            r'studenttools\.[a-zA-Z]{2,10}',
            r'allinone[.-]?tools\.[a-zA-Z]{2,10}',
            r'calculator[.-]?tools\.[a-zA-Z]{2,10}',
            r'mathtools\.[a-zA-Z]{2,10}',
            r'healthtools\.[a-zA-Z]{2,10}',
            r'toolsuite\.[a-zA-Z]{2,10}',
            r'toolbox\.[a-zA-Z]{2,10}',
        ],
        'github_domains': [
            r'[a-zA-Z0-9.-]*\.github\.io',
            r'github\.com/[a-zA-Z0-9.-]+',
        ],
        'external_domains': [
            r'https?://[a-zA-Z0-9.-]+\.[a-zA-Z]{2,10}',
            r'[a-zA-Z0-9.-]+\.(com|net|org|io|dev|app|co|me|biz|info|tv|cc|ly|tk|ml|ga|cf|edu|gov)',
        ],
        'suspicious_domains': [
            r'[a-zA-Z0-9.-]*\.(tk|ml|ga|cf|cc)',  # Free domains
            r'localhost:[0-9]+',
            r'127\.0\.0\.1:[0-9]+',
            r'[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}',  # IP addresses
        ]
    }
    
    found_domains = defaultdict(list)
    
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        for category, patterns in domain_patterns.items():
            for pattern in patterns:
                matches = re.finditer(pattern, content, re.IGNORECASE)
                for match in matches:
                    # Get line number
                    line_num = content[:match.start()].count('\n') + 1
                    found_domains[category].append({
                        'domain': match.group(),
                        'line': line_num,
                        'context': get_line_context(content, match.start())
                    })
    
    except Exception as e:
        print(f"❌ Error reading {file_path}: {str(e)}")
    
    return found_domains

def get_line_context(content, position):
    """Get the line containing the match for context"""
    lines = content.split('\n')
    line_num = content[:position].count('\n')
    if 0 <= line_num < len(lines):
        return lines[line_num].strip()
    return ""

def get_files_to_search():
    """Get all files that might contain domain references"""
    file_patterns = [
        '**/*.html', '**/*.css', '**/*.js', '**/*.php', '**/*.xml', '**/*.md',
        '**/*.json', '**/*.txt', '**/*.py', '**/*.config', '**/*.conf', '**/*.yml', '**/*.yaml'
    ]
    
    files = []
    for pattern in file_patterns:
        files.extend(glob.glob(pattern, recursive=True))
    
    # Filter out unwanted files and directories
    filtered_files = []
    exclude_dirs = ['node_modules', '.git', '__pycache__', '.vscode', 'vendor']
    exclude_files = ['.DS_Store', 'Thumbs.db']
    
    for file_path in files:
        # Skip directories, hidden files, and certain file types
        if (os.path.isfile(file_path) and 
            not any(exclude_dir in file_path for exclude_dir in exclude_dirs) and
            not any(exclude_file in file_path for exclude_file in exclude_files) and
            not file_path.startswith('.')):
            filtered_files.append(file_path)
    
    return sorted(filtered_files)

def categorize_domains(all_findings):
    """Categorize and analyze found domains"""
    categorized = {
        'needs_review': [],
        'external_safe': [],
        'project_correct': [],
        'project_incorrect': [],
        'suspicious': []
    }
    
    safe_external_domains = [
        'fonts.googleapis.com', 'fonts.gstatic.com', 'cdnjs.cloudflare.com',
        'cdn.tailwindcss.com', 'schema.org', 'w3.org', 'mozilla.org',
        'github.com', 'api.brevo.com', 'app.brevo.com'
    ]
    
    for file_path, findings in all_findings.items():
        for category, domains in findings.items():
            for domain_info in domains:
                domain = domain_info['domain'].lower()
                
                # Check if it's a correct project domain
                if 'scribbletools.in' in domain:
                    categorized['project_correct'].append({
                        'file': file_path,
                        'domain': domain,
                        'line': domain_info['line'],
                        'context': domain_info['context']
                    })
                
                # Check for incorrect project domains
                elif any(proj in domain for proj in ['scribbletools', 'studenttools', 'allinone']):
                    if not domain.endswith('.in'):
                        categorized['project_incorrect'].append({
                            'file': file_path,
                            'domain': domain,
                            'line': domain_info['line'],
                            'context': domain_info['context']
                        })
                
                # Check for suspicious domains
                elif category == 'suspicious_domains':
                    categorized['suspicious'].append({
                        'file': file_path,
                        'domain': domain,
                        'line': domain_info['line'],
                        'context': domain_info['context']
                    })
                
                # Check for safe external domains
                elif any(safe_domain in domain for safe_domain in safe_external_domains):
                    categorized['external_safe'].append({
                        'file': file_path,
                        'domain': domain,
                        'line': domain_info['line'],
                        'context': domain_info['context']
                    })
                
                # Everything else needs review
                else:
                    # Skip if it's just a file extension or common programming pattern
                    if not any(skip in domain for skip in ['.min.', '.js', '.css', '.html', '.php']):
                        categorized['needs_review'].append({
                            'file': file_path,
                            'domain': domain,
                            'line': domain_info['line'],
                            'context': domain_info['context']
                        })
    
    return categorized

def generate_report(categorized_domains):
    """Generate a comprehensive domain analysis report"""
    report = []
    
    report.append("🔍 Domain Analysis Report")
    report.append("=" * 50)
    report.append(f"📅 Generated: {os.popen('date').read().strip()}")
    report.append(f"📂 Project root: {os.getcwd()}")
    report.append("")
    
    # Summary statistics
    total_domains = sum(len(domains) for domains in categorized_domains.values())
    report.append("📊 Summary Statistics")
    report.append("-" * 30)
    for category, domains in categorized_domains.items():
        count = len(domains)
        percentage = (count / total_domains * 100) if total_domains > 0 else 0
        report.append(f"  {category.replace('_', ' ').title()}: {count} ({percentage:.1f}%)")
    report.append(f"  Total domains found: {total_domains}")
    report.append("")
    
    # Detailed findings
    for category, domains in categorized_domains.items():
        if not domains:
            continue
            
        report.append(f"📋 {category.replace('_', ' ').title()}")
        report.append("-" * 40)
        
        if category == 'project_incorrect':
            report.append("⚠️  These domains should be updated to .in:")
        elif category == 'suspicious':
            report.append("🚨 These domains may need attention:")
        elif category == 'needs_review':
            report.append("🔎 These domains should be reviewed:")
        elif category == 'project_correct':
            report.append("✅ Correct project domains:")
        else:
            report.append("ℹ️  External domains (likely safe):")
        
        # Group by domain for better readability
        domain_groups = defaultdict(list)
        for domain_info in domains:
            domain_groups[domain_info['domain']].append(domain_info)
        
        for domain, occurrences in domain_groups.items():
            report.append(f"\n  🌐 {domain} ({len(occurrences)} occurrence{'s' if len(occurrences) > 1 else ''})")
            for occurrence in occurrences[:5]:  # Limit to first 5 occurrences
                report.append(f"     📄 {occurrence['file']}:{occurrence['line']}")
                if occurrence['context']:
                    context = occurrence['context'][:80] + "..." if len(occurrence['context']) > 80 else occurrence['context']
                    report.append(f"        💬 {context}")
            if len(occurrences) > 5:
                report.append(f"     ... and {len(occurrences) - 5} more occurrences")
        
        report.append("")
    
    # Recommendations
    report.append("💡 Recommendations")
    report.append("-" * 30)
    
    if categorized_domains['project_incorrect']:
        report.append("🔧 Action Required:")
        report.append("   • Update incorrect project domains to use .in extension")
        report.append("   • Run the domain update script to fix these issues")
        report.append("")
    
    if categorized_domains['suspicious']:
        report.append("⚠️  Review Needed:")
        report.append("   • Check suspicious domains for security issues")
        report.append("   • Verify IP addresses and localhost references")
        report.append("")
    
    if categorized_domains['needs_review']:
        report.append("🔍 Manual Review:")
        report.append("   • Examine domains in 'needs_review' category")
        report.append("   • Determine if they should be updated or are acceptable")
        report.append("")
    
    if not any([categorized_domains['project_incorrect'], 
                categorized_domains['suspicious'], 
                categorized_domains['needs_review']]):
        report.append("🎉 Excellent! No issues found.")
        report.append("   • All project domains use the correct .in extension")
        report.append("   • No suspicious domains detected")
        report.append("   • External domains appear safe")
    
    return '\n'.join(report)

def main():
    """Main function to search and analyze domains"""
    print("🔍 Domain Search and Analysis Tool")
    print("=" * 50)
    print("Searching for all domain references in the project...")
    print()
    
    files_to_search = get_files_to_search()
    print(f"📂 Found {len(files_to_search)} files to search")
    print()
    
    all_findings = {}
    processed_count = 0
    
    for file_path in files_to_search:
        findings = search_domains_in_file(file_path)
        if any(findings.values()):  # Only store files with findings
            all_findings[file_path] = findings
            processed_count += 1
        
        # Progress indicator
        if processed_count % 50 == 0:
            print(f"🔄 Processed {processed_count} files...")
    
    print(f"✅ Analysis complete! Found domains in {len(all_findings)} files")
    print()
    
    # Categorize findings
    categorized_domains = categorize_domains(all_findings)
    
    # Generate and display report
    report = generate_report(categorized_domains)
    print(report)
    
    # Save report to file
    report_filename = "domain_analysis_report.md"
    try:
        with open(report_filename, 'w', encoding='utf-8') as f:
            f.write(report)
        print()
        print(f"📄 Full report saved to: {report_filename}")
    except Exception as e:
        print(f"❌ Error saving report: {str(e)}")
    
    # Return summary for programmatic use
    return {
        'total_files_searched': len(files_to_search),
        'files_with_domains': len(all_findings),
        'categorized_domains': categorized_domains,
        'needs_attention': bool(categorized_domains['project_incorrect'] or 
                               categorized_domains['suspicious'] or 
                               categorized_domains['needs_review'])
    }

if __name__ == "__main__":
    main()