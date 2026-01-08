#!/usr/bin/env python3
"""
Tool Generator Script for ShramTools
Generates placeholder pages for all 250+ tools with header/footer template
"""

import os
import re

# Base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TOOLS_DIR = os.path.join(BASE_DIR, 'tools')

# Tool categories with their tools
TOOLS = {
    'financial-calculators': [
        '401k Calculator',
        'Amortization Calculator',
        'Annuity Calculator',
        'Auto Loan Calculator',
        'Canadian Mortgage Calculator',
        'Compound Interest Calculator',
        'Currency Calculator',
        'Estate Tax Calculator',
        'Finance Calculator',
        'House Affordability Calculator',
        'Income Tax Calculator',
        'Indian GST Calculator',
        'Inflation Calculator',
        'Interest Calculator',
        'Interest Rate Calculator',
        'Investment Calculator',
        'Loan Calculator',
        'Marriage Tax Calculator',
        'Mortgage Amortization Calculator',
        'Mortgage Calculator',
        'Mortgage Calculator UK',
        'Mortgage Payoff Calculator',
        'Payment Calculator',
        'Pension Calculator',
        'Percent Off Calculator',
        'Rent Calculator',
        'Retirement Calculator',
        'Salary Calculator',
        'Savings Calculator',
        'Social Security Calculator'
    ],
    'health-calculators': [
        'Activity Calories Calculator',
        'Anorexic BMI Calculator',
        'Army Body Fat Calculator',
        'BAC Calculator',
        'Basal Insulin Calculator',
        # 'BMI Calculator', # Already exists
        'BMI for Age Calculator',
        'BMR Calculator',
        'Body Fat Calculator',
        'Body Surface Area Calculator',
        'Body Type Calculator',
        'Body Water Percentage Calculator',
        'Calorie Calculator',
        'Calories Burned Calculator',
        'Carbohydrate Calculator',
        'Daily Calorie Calculator',
        'Due Date Calculator',
        'Fat Intake Calculator',
        'GFR Calculator',
        'Healthy Weight Calculator',
        'Ideal Weight Calculator',
        'Insulin Carb Ratio Calculator',
        'Lean Body Mass Calculator',
        'Macro Calculator',
        'Max Heart Rate Calculator',
        'Medical BSA Calculator',
        'METS Calculator',
        'One Rep Max Calculator',
        'Overweight Checker',
        'Ovulation Calculator',
        'Pace Calculator',
        'Period Calculator',
        'Pregnancy Calculator',
        'Pregnancy Conception Calculator',
        'Pregnancy Weight Gain Calculator',
        'Protein Calculator',
        'Sleep Calculator',
        'Split Time Calculator',
        'Target Heart Rate Calculator',
        'TDEE Calculator',
        'VO2 Max Calculator',
        'Waist Height Ratio Calculator',
        'Waist Hip Ratio Calculator',
        'Water Intake Calculator',
        'Weight Watcher Points Calculator'
    ],
    'math-calculators': [
        'Area Calculator',
        'Average Calculator',
        'Basic Calculator',
        'Circle Calculator',
        'Confidence Interval Calculator',
        'Cuboid Calculator',
        'Cylinder Calculator',
        'Discount Calculator',
        'Exponent Calculator',
        'Fraction Calculator',
        'Lateral Surface Area Calculator',
        'Mean Median Mode Range Calculator',
        'Number Sequence Calculator',
        'Percentage Calculator',
        'Perimeter Calculator',
        'Permutation and Combination Calculator',
        'Polygon Calculator',
        'Probability Calculator',
        'Random Number Generator',
        'Rectangle Calculator',
        'Sample Size Calculator',
        'Scientific Notation Converter',
        'Simple Interest Calculator',
        'Sphere Calculator',
        'Square Root Calculator',
        'Standard Deviation Calculator',
        'Statistics Calculator',
        'Tip Calculator',
        'Total Surface Area Calculator',
        'Triangle Calculator',
        'Unit Price Calculator',
        'Volume Calculator',
        'Z-Score Calculator'
    ],
    'text-tools': [
        'Add Line Numbers',
        'Align Text',
        'Base64 Encode Decode',
        'Binary Hex Octal Converter',
        'Bubble Text Generator',
        'Change Case Converter',
        'Change Font',
        'CSV to JSON Converter',
        'Emoji Replacer Inserter',
        'Fancy Unicode Text Generator',
        'Find and Replace',
        'Find Top Words',
        'HTML Encode Decode',
        'Image from Text',
        'Join Text',
        'JSON Formatter Minifier',
        'Keyword Density Checker',
        'Lorem Ipsum Generator',
        'Mirror Text',
        'Morse Code Converter',
        'Readability Score',
        'Remove Duplicate Lines',
        'Remove Punctuation',
        'Repeat Text',
        'Reverse Text',
        'ROT13 Encoder Decoder',
        'Shuffle Lines',
        'Sort Lines',
        'Split Text',
        'Text Dedenter',
        'Text Diff Checker',
        'Text Indenter',
        'Text Justifier',
        'Text Scrambler',
        'Text Statistics',
        'Text to ASCII Art',
        'Text to QR Code',
        'Trim Whitespace',
        'Unicode Converter',
        'Unique Word Finder',
        'Upside Down Text',
        'URL Encode Decode',
        'Word Counter',
        'Word Wrap',
        'XML Formatter Minifier',
        'Zalgo Text Generator'
    ],
    'image-tools': [
        'Add Name DOB Photo',
        'Black White Image Converter',
        'Bulk Image Resizer',
        'Bulk Image Resizer with Preview',
        'Check Image DPI',
        'Circle Crop',
        'Convert DPI',
        'Flip Image',
        'Freehand Crop',
        'Generate Signature',
        'GIF Tools',
        'Grayscale Image',
        'Image Color Picker',
        'Image Compressor',
        'Image Converter',
        'Increase Image Size KB',
        'Instagram Grid Maker',
        'Join Images into One',
        'Passport Photo Maker',
        'Picture to Pixel Art',
        'Pixelate Image',
        'Reduce Image Size KB',
        'Remove Image Background',
        'Resize Image 2x2 inch',
        'Resize Image 35mm x 45mm',
        'Resize Image 3x4',
        'Resize Image 3x5cm 4x5cm',
        'Resize Image 4x6',
        'Resize Image 4x6 inch',
        'Resize Image 600x600',
        'Resize Image 6cm x 2cm 300dpi',
        'Resize Image A4',
        'Resize Image CM',
        'Resize Image Inches',
        'Resize Image MM',
        'Resize Image PAN Card',
        'Resize Image Pixel',
        'Resize Image SSC',
        'Resize Image UPSC',
        'Resize Image YouTube Banner',
        'Resize Instagram No Crop',
        'Resize Sign 50mm x 20mm',
        'Resize Signature',
        'Resize WhatsApp DP',
        'Rotate Image',
        'Split Image',
        'Super Resolution',
        'Video to GIF',
        'Watermark Images'
    ],
    'student-tools': [
        'Assignment Tracker',
        'Citation Generator',
        'Flashcard Maker',
        'GPA Calculator',
        'Grade Calculator',
        'Study Planner',
        'VIT GPA Calculator',
        'Cover Letter Generator',
        'Cover Letter Samples',
        'Job Application Tracker',
        'Resume Builder',
        'Resume Template Simple',
        'Expense Splitter',
        'Semester Cost Estimator',
        'Student Budget Calculator',
        'Student Loan Calculator',
        'Textbook Cost Optimizer',
        'Work Hour Calculator',
        'Class Schedule Builder',
        'Daily Schedule Optimizer',
        'Exam Schedule Organizer',
        'Semester Planner',
        'Study Group Scheduler',
        'Academic Performance Dashboard',
        'Assignment Priority Matrix',
        'Focus Timer',
        'Goal Progress Tracker',
        'Habit Tracker',
        'Procrastination Breaker',
        'Reflection Journal',
        'Study Effectiveness Analyzer',
        'Study Time Tracker',
        'Time Allocation Chart',
        'Skill Checklist',
        'Sleep Calculator Student',
        'Stress Monitor'
    ],
    'other-tools': [
        'Age Calculator',
        'Date Calculator',
        'Dice Roller',
        'Password Generator',
        'Personal Notes'
    ]
}

def tool_name_to_filename(name):
    """Convert tool name to filename"""
    # Remove special characters and convert to lowercase with hyphens
    filename = name.lower()
    filename = re.sub(r'[&/()]', '', filename)
    filename = re.sub(r'\s+', '-', filename)
    filename = re.sub(r'-+', '-', filename)
    filename = filename.strip('-')
    return filename + '.html'

def get_category_display_name(category):
    """Get display name for category"""
    names = {
        'financial-calculators': 'Financial Calculators',
        'health-calculators': 'Health & Fitness',
        'math-calculators': 'Math Tools',
        'text-tools': 'Text Tools',
        'image-tools': 'Image Tools',
        'student-tools': 'Student Tools',
        'other-tools': 'Other Tools'
    }
    return names.get(category, category)

def generate_tool_html(tool_name, category, filename):
    """Generate the HTML content for a tool placeholder page"""
    category_display = get_category_display_name(category)
    
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
    <meta http-equiv="Pragma" content="no-cache">
    <meta http-equiv="Expires" content="0">
    <title>{tool_name} - Free Online Tool | ShramTools</title>
    <meta name="description" content="Free {tool_name} tool by ShramTools. Easy to use, accurate results, no registration required.">
    <meta name="keywords" content="{tool_name.lower()}, free calculator, online tool, ShramTools">
    <meta name="author" content="ShramTools by Shram Kavach">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="https://shramtools.shramkavach.com/tools/{category}/{filename}">
    
    <!-- Open Graph -->
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://shramtools.shramkavach.com/tools/{category}/{filename}">
    <meta property="og:title" content="{tool_name} - Free Online Tool | ShramTools">
    <meta property="og:description" content="Free {tool_name} tool. Easy to use, accurate results.">
    <meta property="og:image" content="https://shramtools.shramkavach.com/images/og-image.jpg">
    
    <!-- Twitter -->
    <meta property="twitter:card" content="summary_large_image">
    <meta property="twitter:title" content="{tool_name} | ShramTools">
    <meta property="twitter:description" content="Free {tool_name} tool by ShramTools.">
    
    <link rel="icon" type="image/webp" href="../../images/logo.webp">
    
    <style>
        /* Reset & Base */
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        html {{
            scroll-behavior: smooth;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: linear-gradient(135deg, #f5f7fa 0%, #e8eef5 50%, #f0e7f8 100%);
            background-attachment: fixed;
            min-height: 100vh;
            color: #2d3748;
            line-height: 1.6;
        }}
        
        /* Site Header */
        .site-header {{
            background: rgba(255, 255, 255, 0.85);
            backdrop-filter: blur(20px) saturate(180%);
            -webkit-backdrop-filter: blur(20px) saturate(180%);
            padding: 0;
            position: sticky;
            top: 0;
            z-index: 1000;
            box-shadow: 0 8px 32px rgba(102, 126, 234, 0.08), 0 1px 3px rgba(0, 0, 0, 0.05);
            border-bottom: 1px solid rgba(102, 126, 234, 0.1);
        }}
        
        .site-header::before {{
            content: '';
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            height: 2px;
            background: linear-gradient(90deg, transparent, #667eea, #764ba2, #a855f7, transparent);
            animation: headerGlow 4s ease-in-out infinite;
        }}
        
        @keyframes headerGlow {{
            0%, 100% {{ opacity: 0.2; }}
            50% {{ opacity: 0.6; }}
        }}
        
        .header-content {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 1rem 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .logo {{
            display: flex;
            align-items: center;
            gap: 0.8rem;
            text-decoration: none;
        }}
        
        .logo-icon {{
            width: 45px;
            height: 45px;
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            box-shadow: 0 8px 24px rgba(102, 126, 234, 0.4);
            transition: all 0.4s;
            overflow: hidden;
        }}
        
        .logo-icon img {{
            width: 100%;
            height: 100%;
            object-fit: cover;
            border-radius: 12px;
        }}
        
        .logo-icon:hover {{
            transform: scale(1.05) rotate(5deg);
            box-shadow: 0 12px 32px rgba(102, 126, 234, 0.5);
        }}
        
        .logo-text {{
            display: flex;
            flex-direction: column;
        }}
        
        .logo-main {{
            font-size: 1.5rem;
            font-weight: 800;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #a855f7 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            letter-spacing: -0.5px;
        }}
        
        .logo-sub {{
            font-size: 0.7rem;
            color: #718096;
            letter-spacing: 2px;
            text-transform: uppercase;
            margin-top: -2px;
        }}
        
        .nav-menu {{
            display: flex;
            align-items: center;
            gap: 2rem;
        }}
        
        .nav-link {{
            color: #4a5568;
            text-decoration: none;
            font-weight: 500;
            padding: 0.6rem 1.2rem;
            border-radius: 12px;
            transition: all 0.3s;
            position: relative;
        }}
        
        .nav-link:hover {{
            color: #667eea;
            background: rgba(102, 126, 234, 0.08);
        }}
        
        .nav-link.active {{
            color: #667eea;
            background: rgba(102, 126, 234, 0.1);
        }}
        
        .nav-link-primary {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white !important;
            padding: 0.7rem 1.5rem;
            border-radius: 25px;
            font-weight: 600;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        }}
        
        .nav-link-primary:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.5);
            background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
        }}
        
        /* Main Content - Under Progress */
        .main-content {{
            max-width: 900px;
            margin: 0 auto;
            padding: 60px 20px;
            text-align: center;
        }}
        
        .progress-container {{
            background: white;
            border-radius: 24px;
            padding: 60px 40px;
            box-shadow: 0 20px 60px rgba(102, 126, 234, 0.15);
            border: 1px solid rgba(102, 126, 234, 0.1);
        }}
        
        .progress-icon {{
            width: 120px;
            height: 120px;
            margin: 0 auto 30px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            animation: pulse 2s ease-in-out infinite;
        }}
        
        @keyframes pulse {{
            0%, 100% {{ transform: scale(1); box-shadow: 0 0 0 0 rgba(102, 126, 234, 0.4); }}
            50% {{ transform: scale(1.05); box-shadow: 0 0 0 20px rgba(102, 126, 234, 0); }}
        }}
        
        .progress-icon svg {{
            width: 60px;
            height: 60px;
            fill: white;
        }}
        
        .progress-title {{
            font-size: 2.5rem;
            font-weight: 800;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #a855f7 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 15px;
        }}
        
        .progress-subtitle {{
            font-size: 1.2rem;
            color: #718096;
            margin-bottom: 30px;
        }}
        
        .progress-badge {{
            display: inline-flex;
            align-items: center;
            gap: 10px;
            background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
            color: #92400e;
            padding: 12px 24px;
            border-radius: 50px;
            font-weight: 600;
            font-size: 1rem;
            margin-bottom: 30px;
        }}
        
        .progress-badge svg {{
            width: 20px;
            height: 20px;
            fill: #f59e0b;
        }}
        
        .category-badge {{
            display: inline-block;
            background: rgba(102, 126, 234, 0.1);
            color: #667eea;
            padding: 8px 20px;
            border-radius: 25px;
            font-size: 0.9rem;
            font-weight: 500;
            margin-bottom: 30px;
        }}
        
        .progress-message {{
            color: #4a5568;
            font-size: 1.1rem;
            line-height: 1.8;
            margin-bottom: 40px;
        }}
        
        .explore-btn {{
            display: inline-flex;
            align-items: center;
            gap: 10px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 16px 40px;
            border-radius: 50px;
            font-size: 1.1rem;
            font-weight: 600;
            text-decoration: none;
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
            transition: all 0.3s;
        }}
        
        .explore-btn:hover {{
            transform: translateY(-3px);
            box-shadow: 0 15px 40px rgba(102, 126, 234, 0.5);
        }}
        
        .explore-btn svg {{
            width: 20px;
            height: 20px;
            fill: white;
        }}
        
        /* Footer */
        .site-footer {{
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            color: #e2e8f0;
            padding: 60px 0 30px;
            margin-top: 80px;
        }}
        
        .footer-content {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 0 2rem;
        }}
        
        .footer-grid {{
            display: grid;
            grid-template-columns: 2fr 1fr 1fr 1fr;
            gap: 3rem;
            margin-bottom: 40px;
        }}
        
        .footer-brand {{
            max-width: 350px;
        }}
        
        .footer-logo {{
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 20px;
        }}
        
        .footer-logo-icon {{
            width: 50px;
            height: 50px;
            border-radius: 14px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            overflow: hidden;
        }}
        
        .footer-logo-icon img {{
            width: 100%;
            height: 100%;
            object-fit: cover;
            border-radius: 14px;
        }}
        
        .footer-logo-text {{
            font-size: 1.8rem;
            font-weight: 800;
            background: linear-gradient(135deg, #667eea 0%, #a855f7 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        
        .footer-desc {{
            color: #94a3b8;
            line-height: 1.8;
            font-size: 0.95rem;
        }}
        
        .footer-section h4 {{
            color: white;
            font-size: 1.1rem;
            font-weight: 700;
            margin-bottom: 20px;
            position: relative;
            padding-bottom: 10px;
        }}
        
        .footer-section h4::after {{
            content: '';
            position: absolute;
            bottom: 0;
            left: 0;
            width: 40px;
            height: 3px;
            background: linear-gradient(90deg, #667eea, #a855f7);
            border-radius: 2px;
        }}
        
        .footer-links {{
            list-style: none;
        }}
        
        .footer-links li {{
            margin-bottom: 12px;
        }}
        
        .footer-links a {{
            color: #94a3b8;
            text-decoration: none;
            transition: all 0.3s;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        
        .footer-links a:hover {{
            color: #a855f7;
            transform: translateX(5px);
        }}
        
        .footer-bottom {{
            border-top: 1px solid rgba(255, 255, 255, 0.1);
            padding-top: 30px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 20px;
        }}
        
        .footer-bottom p {{
            color: #64748b;
            font-size: 0.9rem;
        }}
        
        .footer-bottom a {{
            color: #a855f7;
            text-decoration: none;
        }}
        
        .social-links {{
            display: flex;
            gap: 15px;
        }}
        
        .social-link {{
            width: 40px;
            height: 40px;
            border-radius: 10px;
            background: rgba(255, 255, 255, 0.05);
            display: flex;
            align-items: center;
            justify-content: center;
            color: #94a3b8;
            text-decoration: none;
            transition: all 0.3s;
        }}
        
        .social-link:hover {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            transform: translateY(-3px);
        }}
        
        /* Responsive */
        @media (max-width: 968px) {{
            .nav-menu {{
                display: none;
            }}
            
            .footer-grid {{
                grid-template-columns: 1fr 1fr;
            }}
            
            .progress-title {{
                font-size: 2rem;
            }}
        }}
        
        @media (max-width: 600px) {{
            .header-content {{
                padding: 1rem;
            }}
            
            .progress-container {{
                padding: 40px 20px;
            }}
            
            .progress-title {{
                font-size: 1.6rem;
            }}
            
            .footer-grid {{
                grid-template-columns: 1fr;
            }}
            
            .footer-bottom {{
                flex-direction: column;
                text-align: center;
            }}
        }}
    </style>
</head>
<body>
    <!-- Header -->
    <header class="site-header">
        <div class="header-content">
            <a href="../../index.html" class="logo">
                <div class="logo-icon">
                    <img src="../../images/logo.webp" alt="ShramTools Logo">
                </div>
                <div class="logo-text">
                    <span class="logo-main">ShramTools</span>
                    <span class="logo-sub">By Shram Kavach</span>
                </div>
            </a>
            <nav class="nav-menu">
                <a href="../../index.html" class="nav-link">Home</a>
                <a href="../../index.html#financial" class="nav-link">Financial</a>
                <a href="../../index.html#health" class="nav-link">Health</a>
                <a href="../../index.html#math" class="nav-link">Math</a>
                <a href="../../about-us.html" class="nav-link">About</a>
                <a href="../../index.html" class="nav-link nav-link-primary">All Tools</a>
            </nav>
        </div>
    </header>

    <!-- Main Content -->
    <main class="main-content">
        <div class="progress-container">
            <div class="progress-icon">
                <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z"/>
                </svg>
            </div>
            
            <h1 class="progress-title">{tool_name}</h1>
            
            <div class="category-badge">{category_display}</div>
            
            <div class="progress-badge">
                <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z"/>
                </svg>
                Under Development
            </div>
            
            <p class="progress-subtitle">Coming Soon!</p>
            
            <p class="progress-message">
                We're working hard to bring you an amazing <strong>{tool_name}</strong> tool. 
                Our team is crafting a feature-rich, user-friendly experience that will help you 
                achieve accurate results with ease. Stay tuned!
            </p>
            
            <a href="../../index.html" class="explore-btn">
                <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z"/>
                </svg>
                Explore Other Tools
            </a>
        </div>
    </main>

    <!-- Footer -->
    <footer class="site-footer">
        <div class="footer-content">
            <div class="footer-grid">
                <div class="footer-brand">
                    <div class="footer-logo">
                        <div class="footer-logo-icon">
                            <img src="../../images/logo.webp" alt="ShramTools Logo">
                        </div>
                        <span class="footer-logo-text">ShramTools</span>
                    </div>
                    <p class="footer-desc">
                        Your trusted destination for 250+ free online calculators and tools. 
                        From financial planning to health tracking, we've got you covered.
                    </p>
                </div>
                
                <div class="footer-section">
                    <h4>Quick Links</h4>
                    <ul class="footer-links">
                        <li><a href="../../index.html">Home</a></li>
                        <li><a href="../../index.html#financial">Financial Tools</a></li>
                        <li><a href="../../index.html#health">Health Tools</a></li>
                        <li><a href="../../index.html#math">Math Tools</a></li>
                    </ul>
                </div>
                
                <div class="footer-section">
                    <h4>More Tools</h4>
                    <ul class="footer-links">
                        <li><a href="../../index.html#text">Text Tools</a></li>
                        <li><a href="../../index.html#image">Image Tools</a></li>
                        <li><a href="../../index.html#student">Student Tools</a></li>
                        <li><a href="../../index.html#other">Other Tools</a></li>
                    </ul>
                </div>
                
                <div class="footer-section">
                    <h4>Company</h4>
                    <ul class="footer-links">
                        <li><a href="../../about-us.html">About Us</a></li>
                        <li><a href="../../privacy-policy.html">Privacy Policy</a></li>
                        <li><a href="../../terms-of-service.html">Terms of Service</a></li>
                        <li><a href="../../contact.html">Contact</a></li>
                    </ul>
                </div>
            </div>
            
            <div class="footer-bottom">
                <p>&copy; 2025 ShramTools by <a href="https://shramkavach.com" target="_blank">Shram Kavach</a>. All rights reserved.</p>
                <div class="social-links">
                    <a href="#" class="social-link" aria-label="Twitter">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
                            <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/>
                        </svg>
                    </a>
                    <a href="#" class="social-link" aria-label="GitHub">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
                            <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
                        </svg>
                    </a>
                    <a href="#" class="social-link" aria-label="LinkedIn">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
                            <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
                        </svg>
                    </a>
                </div>
            </div>
        </div>
    </footer>
</body>
</html>'''

def generate_sitemap_entry(category, filename, tool_name):
    """Generate sitemap entry for a tool"""
    return f'''    <url>
        <loc>https://shramtools.shramkavach.com/tools/{category}/{filename}</loc>
        <lastmod>2026-01-08</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.7</priority>
    </url>'''

def generate_tool_route(tool_name, category, filename):
    """Generate JavaScript route entry"""
    return f"        '{tool_name}': 'tools/{category}/{filename}'"

def main():
    tool_count = 0
    sitemap_entries = []
    tool_routes = []
    
    # Create directories and files
    for category, tools in TOOLS.items():
        category_dir = os.path.join(TOOLS_DIR, category)
        os.makedirs(category_dir, exist_ok=True)
        
        for tool_name in tools:
            filename = tool_name_to_filename(tool_name)
            filepath = os.path.join(category_dir, filename)
            
            # Skip if file already exists (like BMI Calculator)
            if os.path.exists(filepath):
                print(f"Skipping (exists): {filepath}")
                continue
            
            # Generate HTML content
            html_content = generate_tool_html(tool_name, category, filename)
            
            # Write file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            tool_count += 1
            print(f"Created: {filepath}")
            
            # Add to sitemap entries
            sitemap_entries.append(generate_sitemap_entry(category, filename, tool_name))
            
            # Add to tool routes
            tool_routes.append(generate_tool_route(tool_name, category, filename))
    
    # Generate sitemap content
    print(f"\n\n=== SITEMAP ENTRIES ({len(sitemap_entries)} tools) ===\n")
    print('\n'.join(sitemap_entries))
    
    # Generate tool routes JavaScript
    print(f"\n\n=== TOOL ROUTES FOR index.html ===\n")
    print("const toolRoutes = {")
    print(',\n'.join(tool_routes))
    print("};")
    
    print(f"\n\nTotal tools created: {tool_count}")
    
    # Write sitemap entries to a file for easy copy
    with open(os.path.join(BASE_DIR, 'sitemap-entries.txt'), 'w') as f:
        f.write('\n'.join(sitemap_entries))
    
    # Write tool routes to a file for easy copy  
    with open(os.path.join(BASE_DIR, 'tool-routes.txt'), 'w') as f:
        f.write("const toolRoutes = {\n")
        f.write(',\n'.join(tool_routes))
        f.write("\n};")

if __name__ == '__main__':
    main()
