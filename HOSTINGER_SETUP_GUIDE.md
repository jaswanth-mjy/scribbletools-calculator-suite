# ScribbleTools Click Tracking Setup Guide for Hostinger

## Overview
This system tracks every tool click and stores the data in a MySQL database on Hostinger. It includes:
- Real-time click tracking
- SQL database integration
- Analytics dashboard
- Desktop-optimized marquee message

## Hostinger Setup Instructions

### Step 1: Create MySQL Database
1. Log into your Hostinger control panel
2. Go to **Databases** → **MySQL Databases**
3. Create a new database:
   - Database name: `scribbletools_analytics` (or your preferred name)
   - Username: Create a new user with full privileges
   - Password: Generate a strong password

### Step 2: Configure Database Connection
1. Open `/api/db-config.php`
2. Update these values with your Hostinger database credentials:
```php
define('DB_HOST', 'your-hostinger-mysql-host.com'); // From Hostinger control panel
define('DB_NAME', 'your_database_name'); // Your database name
define('DB_USER', 'your_username'); // Your database username
define('DB_PASS', 'your_password'); // Your database password
```

### Step 3: Upload Files to Hostinger
Upload these files to your Hostinger hosting:
```
/api/db-config.php          → Configure database connection
/api/track-click.php        → API endpoint for tracking clicks
/dashboard.html             → Analytics dashboard
/index.html                 → Updated with tracking system
```

### Step 4: Set File Permissions
Set proper permissions for PHP files:
- `/api/db-config.php` → 644
- `/api/track-click.php` → 644

### Step 5: Database Table Creation
The table will be created automatically when the first API call is made. The table structure:

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
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_tool_name (tool_name),
    INDEX idx_category (tool_category),
    INDEX idx_timestamp (timestamp)
);
```

## Features Implemented

### 1. Desktop Marquee Message
- Shows only on desktop (hidden on mobile)
- Animated scrolling message encouraging desktop use
- Smooth CSS animation with gradient background

### 2. Click Tracking System
- Automatically tracks every tool click
- Captures tool name, category, and usage statistics
- Stores user information (IP, user agent, referrer)
- Incremental click counting per tool

### 3. Analytics Dashboard
- Real-time statistics viewing
- Top tools by clicks
- Category usage breakdown
- Auto-refresh every 30 seconds
- Access at: `https://yourdomain.com/dashboard.html`

### 4. API Endpoints

#### Track Click (POST)
```javascript
POST /api/track-click.php
{
    "tool_name": "Word Counter",
    "tool_path": "client/tools/text/word-counter.html",
    "tool_category": "Text Tools"
}
```

#### Get Statistics (GET)
```javascript
GET /api/track-click.php?action=stats&limit=20
GET /api/track-click.php?action=categories
```

## Testing the Setup

### 1. Test Database Connection
Visit: `https://yourdomain.com/api/track-click.php?action=stats`
- Should return JSON with empty data array if working
- Should show error if database connection fails

### 2. Test Click Tracking
1. Visit your main website
2. Click on any tool
3. Check browser console for: `✅ Click tracked: [Tool Name] (X total clicks)`
4. Visit dashboard to see statistics

### 3. Test Dashboard
Visit: `https://yourdomain.com/dashboard.html`
- Should load without errors
- Should display statistics (even if empty initially)

## Troubleshooting

### Common Issues:

1. **Database Connection Failed**
   - Verify Hostinger database credentials
   - Check if MySQL service is running
   - Ensure database exists

2. **CORS Errors**
   - API includes CORS headers, should work cross-origin
   - If issues persist, check Hostinger's .htaccess settings

3. **404 on API Calls**
   - Ensure `/api/` folder exists in your hosting
   - Check file permissions (644 for PHP files)
   - Verify Hostinger supports PHP (it does)

4. **Dashboard Not Loading**
   - Check browser console for errors
   - Verify API endpoints are accessible
   - Test API directly in browser

### Log Files
- Check Hostinger error logs in control panel
- PHP errors logged to Hostinger's error log
- Browser console shows client-side tracking status

## Security Features
- SQL injection protection using PDO prepared statements
- Input validation and sanitization
- Error logging without exposing sensitive data
- IP address logging for basic analytics

## Performance
- Asynchronous tracking (doesn't block user navigation)
- Fallback to localStorage if server unavailable
- Efficient database queries with indexes
- Minimal impact on site performance

## Maintenance
- Database will grow over time - consider periodic cleanup
- Monitor disk usage in Hostinger control panel
- Regularly backup analytics data
- Update database credentials if changed

---

**Need Help?** Check the browser console for detailed error messages or contact your hosting provider for MySQL-specific issues.