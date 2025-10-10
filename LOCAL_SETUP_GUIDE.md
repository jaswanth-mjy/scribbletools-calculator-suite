# Local Development Setup Guide

## Overview
This guide will help you set up the click tracking system locally using XAMPP or WAMP before deploying to Hostinger.

## Prerequisites
- **XAMPP** (recommended) or **WAMP** installed on your system
- Basic knowledge of PHP and MySQL
- Web browser for testing

## Installation Steps

### 1. Download and Install XAMPP

**For Windows:**
1. Download XAMPP from https://www.apachefriends.org/
2. Install XAMPP (choose default installation)
3. Launch XAMPP Control Panel
4. Start **Apache** and **MySQL** services

**For macOS:**
1. Download XAMPP for macOS
2. Install XAMPP in `/Applications/XAMPP/`
3. Launch XAMPP from Applications
4. Start **Apache** and **MySQL** services

### 2. Setup Project Files

1. Copy your project folder to XAMPP's htdocs directory:
   ```
   Windows: C:\xampp\htdocs\allinone-tools\
   macOS: /Applications/XAMPP/htdocs/allinone-tools/
   ```

2. Your project structure should look like:
   ```
   htdocs/allinone-tools/
   ├── index.html
   ├── api/
   │   ├── db-config-local.php
   │   └── track-click-local.php
   ├── client/tools/...
   └── dashboard.html
   ```

### 3. Database Setup

1. Open **phpMyAdmin** in browser: `http://localhost/phpmyadmin`
2. Login (usually no password for local XAMPP)
3. Create a new database named `allinone_tools`
4. The system will automatically create the required table when first accessed

### 4. Configuration

1. Check `api/db-config-local.php` settings:
   ```php
   define('DB_HOST', 'localhost');
   define('DB_NAME', 'allinone_tools');
   define('DB_USER', 'root');
   define('DB_PASS', ''); // Usually empty for XAMPP
   ```

2. If you have a different MySQL setup, update these values accordingly.

### 5. Testing the Setup

1. **Test Database Connection:**
   Visit: `http://localhost/allinone-tools/api/track-click-local.php?action=test`
   
   Expected response:
   ```json
   {
     "success": true,
     "message": "Local API is working!",
     "environment": "local_development",
     "database_host": "localhost",
     "database_name": "allinone_tools",
     "timestamp": "2024-01-XX XX:XX:XX"
   }
   ```

2. **Test Click Tracking:**
   - Open: `http://localhost/allinone-tools/index.html`
   - Click on any tool link
   - Check browser's Network tab to see API calls
   - Visit dashboard: `http://localhost/allinone-tools/dashboard.html`

3. **Test Statistics:**
   Visit: `http://localhost/allinone-tools/api/track-click-local.php?action=stats`

## Development Workflow

### For Local Testing:
1. Use the local URLs:
   - Main site: `http://localhost/allinone-tools/`
   - API: `http://localhost/allinone-tools/api/track-click-local.php`
   - Dashboard: `http://localhost/allinone-tools/dashboard.html`

### Switching to Local Mode:
In your HTML files, you can use environment detection:

```javascript
// Detect if running locally
const isLocal = window.location.hostname === 'localhost' || 
                window.location.hostname === '127.0.0.1';

const API_URL = isLocal 
    ? '/allinone-tools/api/track-click-local.php'
    : '/api/track-click.php';
```

## Troubleshooting

### Common Issues:

1. **"Connection failed" error:**
   - Make sure MySQL is running in XAMPP
   - Check database credentials in `db-config-local.php`
   - Verify database name exists in phpMyAdmin

2. **404 errors on API calls:**
   - Check file paths in browser network tab
   - Ensure files are in correct htdocs directory
   - Verify XAMPP Apache is running

3. **CORS errors:**
   - Should not occur in local development
   - If persistent, check browser console for specific errors

4. **No data showing:**
   - Check if table was created automatically
   - Visit phpMyAdmin to see if `tool_clicks` table exists
   - Look at PHP error logs in XAMPP control panel

### Debugging Tips:

1. **Enable PHP error reporting:**
   Add to top of PHP files:
   ```php
   ini_set('display_errors', 1);
   error_reporting(E_ALL);
   ```

2. **Check XAMPP logs:**
   - Apache logs: `xampp/apache/logs/error.log`
   - MySQL logs: `xampp/mysql/data/mysql_error.log`

3. **Use browser developer tools:**
   - Network tab for API calls
   - Console tab for JavaScript errors

## Database Schema

The system creates this table automatically:

```sql
CREATE TABLE tool_clicks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tool_name VARCHAR(255) NOT NULL,
    tool_path VARCHAR(500) NOT NULL,
    tool_category VARCHAR(100) NOT NULL,
    click_count INT DEFAULT 1,
    user_ip VARCHAR(45),
    user_agent TEXT,
    referrer VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

## Next Steps

1. Test all functionality locally
2. Verify click tracking works
3. Check dashboard displays data correctly
4. Once confirmed working, deploy to Hostinger using the production configuration

---

**Need help?** Check the error logs first, then review the configuration files to ensure all paths and credentials are correct for your local environment.