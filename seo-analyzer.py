#!/usr/bin/env python3
"""
SEO Optimization Script for ScribbleTools
Automatically adds SEO meta tags and structured content to all tool pages
"""

import os
import re
import json
from pathlib import Path

# Tool categories and their SEO templates
SEO_TEMPLATES = {
    'text': {
        'title_suffix': 'Free Text Tool - ScribbleTools',
        'description_template': 'Free online {tool_name} tool. Process and analyze text quickly with our professional text utilities. No registration required.',
        'keywords': 'text tool, text processing, online text utility, free text tool, text analysis'
    },
    'math': {
        'title_suffix': 'Free Math Calculator - ScribbleTools', 
        'description_template': 'Free {tool_name} calculator. Solve mathematical problems quickly and accurately with our professional calculators.',
        'keywords': 'calculator, math calculator, online calculator, free calculator, mathematical tool'
    },
    'financial': {
        'title_suffix': 'Free Financial Calculator - ScribbleTools',
        'description_template': 'Free {tool_name} calculator. Calculate financial metrics and planning with our professional financial tools.',
        'keywords': 'financial calculator, finance tool, money calculator, investment calculator'
    },
    'health': {
        'title_suffix': 'Free Health Calculator - ScribbleTools',
        'description_template': 'Free {tool_name} calculator. Calculate health metrics and wellness indicators with our professional health tools.',
        'keywords': 'health calculator, fitness calculator, wellness tool, health metrics'
    },
    'image': {
        'title_suffix': 'Free Image Tool - ScribbleTools',
        'description_template': 'Free online {tool_name} tool. Process and edit images with our professional image utilities.',
        'keywords': 'image tool, photo editor, image converter, online image tool'
    },
    'student': {
        'title_suffix': 'Free Student Calculator - ScribbleTools', 
        'description_template': 'Free {tool_name} calculator for students. Calculate grades and academic metrics with our educational tools.',
        'keywords': 'student calculator, GPA calculator, grade calculator, academic tool'
    }
}

def format_tool_name(filename):
    """Convert filename to readable tool name"""
    name = filename.replace('.html', '').replace('-', ' ')
    return ' '.join(word.capitalize() for word in name.split())

def generate_seo_head(tool_name, category, file_path):
    """Generate complete SEO-optimized HTML head section"""
    template = SEO_TEMPLATES.get(category, SEO_TEMPLATES['text'])
    formatted_name = format_tool_name(tool_name)
    
    title = f"{formatted_name} - {template['title_suffix']}"
    description = template['description_template'].format(tool_name=formatted_name)
    canonical_url = f"https://scribbletools.com/{file_path}"
    
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{description}">
    <meta name="keywords" content="{template['keywords']}, {formatted_name.lower()}">
    <meta name="author" content="ScribbleTools Team">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="{canonical_url}">
    <meta name="theme-color" content="#D9534F">
    
    <!-- Open Graph / Facebook -->
    <meta property="og:type" content="website">
    <meta property="og:url" content="{canonical_url}">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{description}">
    <meta property="og:image" content="https://scribbletools.com/assets/og-image.svg">
    <meta property="og:site_name" content="ScribbleTools">
    
    <!-- Twitter -->
    <meta property="twitter:card" content="summary_large_image">
    <meta property="twitter:url" content="{canonical_url}">
    <meta property="twitter:title" content="{title}">
    <meta property="twitter:description" content="{description}">
    <meta property="twitter:image" content="https://scribbletools.com/assets/og-image.svg">
    <meta property="twitter:site" content="@scribbletools">
    
    <!-- JSON-LD Structured Data -->
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "WebApplication",
      "name": "{formatted_name}",
      "url": "{canonical_url}",
      "description": "{description}",
      "applicationCategory": "UtilityApplication",
      "operatingSystem": "Any",
      "offers": {{
        "@type": "Offer",
        "price": "0",
        "priceCurrency": "USD"
      }},
      "publisher": {{
        "@type": "Organization",
        "name": "ScribbleTools",
        "url": "https://scribbletools.com"
      }}
    }}
    </script>
    
    <!-- Performance Optimization -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="dns-prefetch" href="https://cdn.tailwindcss.com">
    <script src="https://cdn.tailwindcss.com"></script>
</head>

<body class="bg-gray-50 font-sans">
    <div class="max-w-4xl mx-auto p-4">
        <header class="text-center mb-8">
            <h1 class="text-3xl md:text-4xl font-bold text-red-600 mb-4">{formatted_name}</h1>
            <p class="text-lg text-gray-700 leading-relaxed max-w-2xl mx-auto">
                {description}
            </p>
        </header>
        
        <main class="bg-white rounded-lg shadow-lg p-6 mb-8">
'''

def analyze_tools_structure():
    """Analyze current tools structure and generate optimization report"""
    tools_dir = Path("client/tools")
    report = {
        'total_tools': 0,
        'optimized_tools': 0,
        'categories': {},
        'needs_optimization': []
    }
    
    for category_dir in tools_dir.iterdir():
        if category_dir.is_dir():
            category = category_dir.name
            report['categories'][category] = {
                'total': 0,
                'optimized': 0,
                'tools': []
            }
            
            for tool_file in category_dir.glob('*.html'):
                report['total_tools'] += 1
                report['categories'][category]['total'] += 1
                report['categories'][category]['tools'].append(tool_file.name)
                
                # Check if tool is already SEO optimized
                with open(tool_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    if '<title>' in content and 'og:title' in content:
                        report['optimized_tools'] += 1
                        report['categories'][category]['optimized'] += 1
                    else:
                        report['needs_optimization'].append(str(tool_file))
    
    return report

def print_optimization_report():
    """Print current SEO optimization status"""
    if not os.path.exists('client/tools'):
        print("❌ Tools directory not found. Make sure you're in the right directory.")
        return
        
    report = analyze_tools_structure()
    
    print("🎯 SEO OPTIMIZATION REPORT")
    print("=" * 50)
    print(f"📊 Total Tools: {report['total_tools']}")
    print(f"✅ Optimized: {report['optimized_tools']}")
    print(f"❌ Need Optimization: {len(report['needs_optimization'])}")
    print(f"📈 Optimization Rate: {(report['optimized_tools']/report['total_tools']*100):.1f}%")
    print()
    
    print("📂 BY CATEGORY:")
    for category, data in report['categories'].items():
        print(f"  {category.upper()}: {data['optimized']}/{data['total']} optimized")
    print()
    
    print("🔧 OPTIMIZATION RECOMMENDATIONS:")
    print("1. Start with high-traffic tools (word-counter, calculator, bmi-calculator)")
    print("2. Focus on financial and health calculators next")
    print("3. Add structured data to all tools")
    print("4. Optimize meta descriptions for search snippets")
    print("5. Add internal linking between related tools")
    print()
    
    if report['needs_optimization']:
        print("⚠️  TOOLS NEEDING OPTIMIZATION (first 10):")
        for tool in report['needs_optimization'][:10]:
            print(f"  - {tool}")
        if len(report['needs_optimization']) > 10:
            print(f"  ... and {len(report['needs_optimization']) - 10} more")

if __name__ == "__main__":
    print("🚀 ScribbleTools SEO Optimizer")
    print("This script analyzes and helps optimize your tools for SEO")
    print()
    
    print_optimization_report()
    
    print()
    print("💡 NEXT STEPS:")
    print("1. Review the SEO-OPTIMIZATION-GUIDE.md for detailed instructions")
    print("2. Use the word-counter.html as a template for other tools") 
    print("3. Prioritize high-traffic tools for optimization")
    print("4. Test tools with Google's Rich Results Test")
    print("5. Monitor search performance in Google Search Console")