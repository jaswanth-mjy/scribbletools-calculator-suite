// ScribbleTools Configuration
// Update these values for your deployment

const SCRIBBLETOOLS_CONFIG = {
    // Analytics Configuration
    analytics: {
        googleAnalyticsId: 'GA_MEASUREMENT_ID', // Replace with your GA4 Measurement ID
        enableErrorTracking: true,
        enablePerformanceTracking: true,
        enableCalculatorTracking: true
    },
    
    // Site Configuration
    site: {
        name: 'ScribbleTools',
        domain: 'scribbletools.com', // Replace with your domain
        description: 'ScribbleTools is the professional, ad-free toolbox for math, text, finance, health, and more.',
        keywords: 'online calculator, math calculator, area calculator, volume calculator, text tools, financial calculator, health calculator',
        author: 'ScribbleTools Team'
    },
    
    // Social Media Configuration
    social: {
        twitter: '@scribbletools',
        ogImage: 'https://scribbletools.com/assets/og-image.png',
        twitterImage: 'https://scribbletools.com/assets/og-image.png'
    },
    
    // Error Monitoring Configuration
    errorMonitoring: {
        enableGlobalErrorTracking: true,
        enableUnhandledRejectionTracking: true,
        logToConsole: true,
        logToAnalytics: true,
        logToServer: false, // Set to true if you have an error logging endpoint
        serverEndpoint: '/api/log-error' // Your error logging endpoint
    },
    
    // Performance Configuration
    performance: {
        trackPageLoad: true,
        trackUserTiming: true,
        trackNavigationTiming: true
    },
    
    // Feature Flags
    features: {
        communityChat: true,
        toolSuggestions: true,
        offlineMode: false, // Future feature
        darkMode: false, // Future feature
        userAccounts: false // Future feature
    },
    
    // Tool Categories Configuration
    toolCategories: {
        math: { icon: '🔢', color: '#D9534F' },
        text: { icon: '📝', color: '#5CB85C' },
        financial: { icon: '💰', color: '#F0AD4E' },
        health: { icon: '🏥', color: '#5BC0DE' },
        image: { icon: '🖼️', color: '#9B59B6' },
        utility: { icon: '🔧', color: '#34495E' }
    }
};

// Apply configuration to global objects
if (typeof window !== 'undefined') {
    window.SCRIBBLETOOLS_CONFIG = SCRIBBLETOOLS_CONFIG;
}
