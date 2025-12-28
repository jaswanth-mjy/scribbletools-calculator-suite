/**
 * @file Reusable script for launching tool applications (Resume Builder, Cover Letter Generator, etc.)
 * Handles path resolution, button states, and popup blocking.
 */

/**
 * Opens a tool application or its samples page in a new tab.
 * @param {HTMLButtonElement} button - The button that was clicked.
 * @param {string} targetType - 'app' to open the main tool, 'samples' to open the samples page.
 * @param {object} config - Configuration for the specific tool.
 * @param {string} config.appName - The display name of the tool (e.g., "Cover Letter Generator").
 * @param {string} config.appFileName - The filename of the tool's main application (e.g., "cover-letter-generator-app.html").
 * @param {string} [config.samplesFileName] - The filename of the tool's samples page.
 */
function launchTool(button, targetType, config) {
    console.log(`🚀 Launching ${config.appName} - Target: ${targetType}`, button);

    if (!button) {
        console.warn('⚠️ Button parameter is null or undefined');
        button = event ? event.target : null;
    }

    const originalText = button ? button.innerHTML : '';
    if (button) {
        try {
            button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Opening...';
            button.disabled = true;
            button.style.opacity = '0.7';
        } catch (domError) {
            console.warn('⚠️ Error updating button appearance:', domError.message);
        }
    }

    // Determine the target file based on the type
    const targetFileName = targetType === 'app' ? config.appFileName : config.samplesFileName;
    if (!targetFileName) {
        console.error(`❌ Configuration error: No filename specified for targetType "${targetType}"`);
        if (button) {
            button.innerHTML = originalText;
            button.disabled = false;
            button.style.opacity = '1';
        }
        return false;
    }

    // --- Path Resolution Logic ---
    const currentPath = window.location.pathname;
    let finalPath;

    const isGitHubPages = window.location.hostname.includes('github.io');
    const repoName = 'scribbletools.shramkavach.com';
    const isStandalone = currentPath.includes('/client/tools/student/career/');

    if (isStandalone) {
        // If viewing the file directly, the target is in the same directory.
        const basePath = currentPath.substring(0, currentPath.lastIndexOf('/') + 1);
        finalPath = basePath + targetFileName;
    } else {
        // If loaded via the main site's router, construct the full path.
        const basePath = isGitHubPages ? `/${repoName}` : '';
        finalPath = `${basePath}/client/tools/student/career/${targetFileName}`;
    }

    console.log(`Resolved path to open: ${finalPath}`);

    // --- Open New Tab ---
    try {
        const newWindow = window.open(finalPath, '_blank', 'noopener,noreferrer');
        if (newWindow) {
            newWindow.focus();
            console.log(`✅ ${config.appName} (${targetType}) opened in new tab`);
        } else {
            console.log('❌ Popup blocked - please allow popups for this site');
            if (button) {
                button.innerHTML = '<i class="fas fa-exclamation-triangle"></i> Popup Blocked';
            }
        }
    } catch (e) {
        console.error(`❌ Failed to open new tab for ${config.appName}:`, e.message);
        if (button) {
            button.innerHTML = '<i class="fas fa-exclamation-circle"></i> Error';
        }
    } finally {
        // Reset button after a delay
        setTimeout(() => {
            if (button) {
                try {
                    button.innerHTML = originalText;
                    button.disabled = false;
                    button.style.opacity = '1';
                } catch (resetError) {
                    console.warn('⚠️ Error resetting button state:', resetError.message);
                }
            }
        }, 2000);
    }

    return false; // Prevent default link behavior
}

/**
 * Initializes the tool landing page by setting up configurations and event listeners.
 * @param {object} config - The configuration object for the tool.
 */
function initializeToolPage(config) {
    document.addEventListener('DOMContentLoaded', function() {
        console.log(`📋 ${config.appName} landing page loaded`);

        // Attach event listeners to buttons
        const appButtons = document.querySelectorAll(`[data-action="launch-app"]`);
        appButtons.forEach(btn => {
            btn.addEventListener('click', () => launchTool(btn, 'app', config));
        });

        if (config.samplesFileName) {
            const samplesButtons = document.querySelectorAll(`[data-action="launch-samples"]`);
            samplesButtons.forEach(btn => {
                btn.addEventListener('click', () => launchTool(btn, 'samples', config));
            });
        }

        // --- Accessibility Check ---
        const currentPath = window.location.pathname;
        const isGitHubPages = window.location.hostname.includes('github.io');
        const repoName = 'scribbletools.shramkavach.com';
        const isStandalone = currentPath.includes('/client/tools/student/career/');
        let appPath;

        if (isStandalone) {
            const basePath = currentPath.substring(0, currentPath.lastIndexOf('/') + 1);
            appPath = basePath + config.appFileName;
        } else {
            const basePath = isGitHubPages ? `/${repoName}` : '';
            appPath = `${basePath}/client/tools/student/career/${config.appFileName}`;
        }

        console.log(`Testing app accessibility at: ${appPath}`);
        fetch(appPath, { method: 'HEAD' })
            .then(response => {
                if (!response.ok) {
                    console.warn(`❌ ${config.appName} app not found at: ${appPath} (Status: ${response.status})`);
                    const buttons = document.querySelectorAll('[data-action]');
                    buttons.forEach(btn => {
                        btn.style.opacity = '0.5';
                        btn.title = `${config.appName} app not found (${response.status})`;
                        btn.disabled = true;
                    });
                } else {
                    console.log(`✅ ${config.appName} app is accessible.`);
                }
            })
            .catch(error => {
                console.error(`❌ Error checking app accessibility for ${config.appName}:`, error.message);
            });
    });
}