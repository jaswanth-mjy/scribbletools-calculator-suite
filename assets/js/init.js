// ScribbleTools Initialization Script - Security Optimized
// This external file helps reduce inline scripts and improve CSP compliance

(function() {
    'use strict';
    
    // Suppress Tailwind CDN production warning
    const originalWarn = console.warn;
    console.warn = function(message) {
        if (typeof message === 'string' && message.includes('cdn.tailwindcss.com should not be used in production')) {
            return; // Suppress this specific warning
        }
        originalWarn.apply(console, arguments);
    };
    
    // Configure Tailwind when it loads
    window.configureTailwind = function() {
        if (typeof tailwind !== 'undefined') {
            tailwind.config = {
                ...tailwind.config,
                corePlugins: {
                    preflight: true,
                }
            };
        }
    };
    
    // Initialize on load
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', window.configureTailwind);
    } else {
        window.configureTailwind();
    }
})();
