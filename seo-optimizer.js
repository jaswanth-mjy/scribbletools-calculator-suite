#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

// SEO templates for different tool categories
const seoTemplates = {
    text: {
        titleSuffix: 'Free Text Tool - ScribbleTools',
        descriptionTemplate: 'Free online {toolName} tool. Process text quickly and efficiently with our professional text utilities. No registration required.',
        keywords: 'text tool, text processing, text utilities, online text tool, free text converter'
    },
    math: {
        titleSuffix: 'Free Math Calculator - ScribbleTools',
        descriptionTemplate: 'Free online {toolName} calculator. Solve mathematical problems quickly and accurately with our professional calculators.',
        keywords: 'calculator, math calculator, online calculator, free calculator, mathematical tool'
    },
    financial: {
        titleSuffix: 'Free Financial Calculator - ScribbleTools',
        descriptionTemplate: 'Free {toolName} calculator. Calculate financial metrics, payments, and planning with our professional financial tools.',
        keywords: 'financial calculator, finance tool, money calculator, investment calculator, loan calculator'
    },
    health: {
        titleSuffix: 'Free Health Calculator - ScribbleTools',
        descriptionTemplate: 'Free {toolName} calculator. Calculate health metrics, BMI, calories, and wellness indicators with our professional health tools.',
        keywords: 'health calculator, BMI calculator, fitness calculator, wellness tool, health metrics'
    },
    image: {
        titleSuffix: 'Free Image Tool - ScribbleTools', 
        descriptionTemplate: 'Free online {toolName} tool. Process, convert, and edit images with our professional image utilities.',
        keywords: 'image tool, photo editor, image converter, online image tool, picture tool'
    },
    student: {
        titleSuffix: 'Free Student Calculator - ScribbleTools',
        descriptionTemplate: 'Free {toolName} calculator for students. Calculate grades, GPA, and academic metrics with our educational tools.',
        keywords: 'student calculator, GPA calculator, grade calculator, academic tool, education calculator'
    }
};

// Generate SEO-optimized HTML head section
function generateSEOHead(toolName, category, toolPath) {
    const template = seoTemplates[category] || seoTemplates.text;
    const formattedToolName = toolName.split('-').map(word => 
        word.charAt(0).toUpperCase() + word.slice(1)
    ).join(' ');
    
    const title = `${formattedToolName} - ${template.titleSuffix}`;
    const description = template.descriptionTemplate.replace('{toolName}', formattedToolName);
    const canonicalUrl = `https://scribbletools.com/${toolPath}`;
    
    return `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${title}</title>
    <meta name="description" content="${description}">
    <meta name="keywords" content="${template.keywords}, ${formattedToolName.toLowerCase()}">
    <meta name="author" content="ScribbleTools Team">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="${canonicalUrl}">
    <meta name="theme-color" content="#D9534F">
    
    <!-- Open Graph / Facebook -->
    <meta property="og:type" content="website">
    <meta property="og:url" content="${canonicalUrl}">
    <meta property="og:title" content="${title}">
    <meta property="og:description" content="${description}">
    <meta property="og:image" content="https://scribbletools.com/assets/og-image.svg">
    <meta property="og:site_name" content="ScribbleTools">
    
    <!-- Twitter -->
    <meta property="twitter:card" content="summary_large_image">
    <meta property="twitter:url" content="${canonicalUrl}">
    <meta property="twitter:title" content="${title}">
    <meta property="twitter:description" content="${description}">
    <meta property="twitter:image" content="https://scribbletools.com/assets/og-image.svg">
    <meta property="twitter:site" content="@scribbletools">
    
    <!-- JSON-LD Structured Data -->
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "WebApplication",
      "name": "${formattedToolName}",
      "url": "${canonicalUrl}",
      "description": "${description}",
      "applicationCategory": "UtilityApplication",
      "operatingSystem": "Any",
      "offers": {
        "@type": "Offer",
        "price": "0",
        "priceCurrency": "USD"
      },
      "publisher": {
        "@type": "Organization",
        "name": "ScribbleTools",
        "url": "https://scribbletools.com"
      }
    }
    </script>
    
    <!-- Additional SEO Meta Tags -->
    <meta name="application-name" content="ScribbleTools">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="default">
    <meta name="apple-mobile-web-app-title" content="${formattedToolName}">
    <meta name="format-detection" content="telephone=no">
    <meta name="mobile-web-app-capable" content="yes">
    <meta name="theme-color" content="#D9534F">
    
    <!-- Preconnect for Performance -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://cdn.tailwindcss.com">
    
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    
    <style>
        /* Common tool styles */
        body { font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; }
        .tool-container { max-width: 1200px; margin: 0 auto; padding: 1rem; }
        .tool-header { text-align: center; margin-bottom: 2rem; }
        .tool-title { font-size: 2rem; font-weight: bold; color: #D9534F; margin-bottom: 0.5rem; }
        .tool-description { color: #666; font-size: 1.1rem; line-height: 1.6; }
    </style>
</head>`;
}

// Add SEO-friendly content structure
function addSEOContent(toolName, category) {
    const formattedToolName = toolName.split('-').map(word => 
        word.charAt(0).toUpperCase() + word.slice(1)
    ).join(' ');
    
    return `
<body class="bg-gray-50">
    <div class="tool-container">
        <header class="tool-header">
            <h1 class="tool-title">${formattedToolName}</h1>
            <p class="tool-description">Professional ${formattedToolName.toLowerCase()} tool for quick and accurate calculations. Free to use, no registration required.</p>
        </header>
        
        <main class="bg-white rounded-lg shadow-lg p-6">
            <!-- Tool content will be inserted here -->
`;
}

console.log('SEO Optimizer for ScribbleTools');
console.log('This script will add comprehensive SEO optimization to all tools.');
console.log('Use this as a template for manual optimization of individual tools.');

module.exports = { generateSEOHead, addSEOContent, seoTemplates };