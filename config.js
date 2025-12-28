// ScribbleTools Configuration
// This file contains global configuration settings

window.CONFIG = {
    // Site Information
    siteName: 'ScribbleTools',
    siteUrl: 'https://scribbletools.shramkavach.com',
    version: '2.0.0',
    
    // Feature Flags
    features: {
        analytics: true,
        clickTracking: true,
        serviceWorker: false
    },
    
    // API Configuration
    api: {
        baseUrl: '/api',
        endpoints: {
            trackClick: '/track-click.php',
            trackBlogView: '/track-blog-views.php',
            subscribe: '/subscribe-brevo.php'
        }
    },
    
    // Analytics
    analytics: {
        googleAnalyticsId: 'GA_MEASUREMENT_ID',
        trackPageViews: true,
        trackEvents: true
    }
};
