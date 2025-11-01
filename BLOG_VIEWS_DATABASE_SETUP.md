# Blog Views Database Setup Guide

## Overview
This system tracks blog article views using a MySQL database instead of localStorage, providing persistent, cross-device tracking and analytics.

## Database Tables

### 1. `blog_article_views`
Stores the total view count for each article.

| Column | Type | Description |
|--------|------|-------------|
| id | INT | Primary key |
| article_id | VARCHAR(100) | Unique article identifier |
| view_count | INT | Total number of views |
| last_viewed | TIMESTAMP | Last time article was viewed |
| created_at | TIMESTAMP | When record was created |

### 2. `blog_view_history`
Logs each individual view for detailed analytics.

| Column | Type | Description |
|--------|------|-------------|
| id | INT | Primary key |
| article_id | VARCHAR(100) | Article identifier |
| user_ip | VARCHAR(45) | Viewer's IP address |
| user_agent | TEXT | Browser/device info |
| referrer | VARCHAR(500) | Where viewer came from |
| session_id | VARCHAR(100) | Session identifier |
| viewed_at | TIMESTAMP | When view occurred |

## Setup Instructions

### Step 1: Configure Database Connection

Edit `api/db-config.php` and update these values:

```php
define('DB_HOST', 'your-mysql-host.com');     // Your MySQL host
define('DB_NAME', 'your_database_name');       // Your database name
define('DB_USER', 'your_username');            // Your database username
define('DB_PASS', 'your_password');            // Your database password
```

For **XAMPP local development**:
```php
define('DB_HOST', 'localhost');
define('DB_NAME', 'scribbletools_db');
define('DB_USER', 'root');
define('DB_PASS', '');  // Empty for XAMPP default
```

For **Hostinger hosting**:
```php
define('DB_HOST', 'your-hostinger-mysql-host.com');
define('DB_NAME', 'u123456_dbname');
define('DB_USER', 'u123456_user');
define('DB_PASS', 'your-secure-password');
```

### Step 2: Create Database (if needed)

If using XAMPP:
1. Open http://localhost/phpmyadmin
2. Click "New" to create a database
3. Name it `scribbletools_db`
4. Select `utf8mb4_unicode_ci` collation
5. Click "Create"

### Step 3: Run Setup Script

**Option A: Via Browser**
1. Make sure XAMPP/MySQL is running
2. Open: `http://localhost/allinone-tools/api/setup-blog-views-table.php`
3. You should see success messages
4. **Delete the setup file after running** for security

**Option B: Via Terminal**
```bash
cd /Applications/XAMPP/htdocs/allinone-tools
php api/setup-blog-views-table.php
```

### Step 4: Verify Setup

Check that tables were created:
1. Go to phpMyAdmin
2. Select your database
3. You should see:
   - `blog_article_views` (12 articles initialized with 0 views)
   - `blog_view_history` (empty, will fill as views are tracked)
   - `tool_clicks` (existing table)

### Step 5: Test the API

Test retrieving views:
```bash
curl http://localhost/allinone-tools/api/track-blog-views.php
```

Test incrementing a view:
```bash
curl -X POST http://localhost/allinone-tools/api/track-blog-views.php \
  -H "Content-Type: application/json" \
  -d '{"article_id":"text-article"}'
```

## API Endpoints

### GET - Retrieve View Counts

**Get all articles:**
```
GET /api/track-blog-views.php
```

Response:
```json
{
  "success": true,
  "data": [
    {
      "article_id": "text-article",
      "view_count": 42,
      "last_viewed": "2025-11-02 10:30:00"
    },
    ...
  ],
  "total_articles": 12
}
```

**Get specific article:**
```
GET /api/track-blog-views.php?article_id=text-article
```

Response:
```json
{
  "success": true,
  "data": {
    "article_id": "text-article",
    "view_count": 42,
    "last_viewed": "2025-11-02 10:30:00"
  }
}
```

### POST - Increment View Count

```
POST /api/track-blog-views.php
Content-Type: application/json

{
  "article_id": "text-article"
}
```

Response:
```json
{
  "success": true,
  "message": "View count incremented",
  "data": {
    "article_id": "text-article",
    "view_count": 43
  }
}
```

## Frontend Integration

The system automatically works with your existing code:

### blog.html
- Fetches view counts from database on page load
- Increments view count when article is opened
- Falls back to localStorage if API fails

### index.html
- Displays top 3 viewed articles from database
- Updates every 5 seconds
- Shows real-time rankings

## Features

✅ **Persistent Storage** - Views survive browser clearing
✅ **Cross-Device Tracking** - Views counted across all devices
✅ **Real Analytics** - Track IP, user agent, referrer, timestamps
✅ **Automatic Fallback** - Uses localStorage if database unavailable
✅ **Top Articles Display** - Shows top 3 most viewed on homepage
✅ **Scalable** - Can handle thousands of views efficiently

## Article IDs

All 12 blog articles are initialized:

1. `text-article` - Mastering Text Tools
2. `financial-article` - Financial Calculator Guide
3. `health-article` - Health Calculator Guide
4. `math-article` - Math Made Easy
5. `image-article` - Image Processing Tips
6. `student-article` - Student Success Guide
7. `time-article` - Master Time Management
8. `exam-article` - Ace Your Exams
9. `investment-article` - Investment Calculator Guide
10. `fitness-article` - Start Your Fitness Journey
11. `budget-article` - Budget Planning 101
12. `productivity-article` - 10x Your Productivity

## Analytics Queries

Get most viewed articles:
```sql
SELECT article_id, view_count, last_viewed 
FROM blog_article_views 
ORDER BY view_count DESC 
LIMIT 10;
```

Get total views today:
```sql
SELECT COUNT(*) as today_views 
FROM blog_view_history 
WHERE DATE(viewed_at) = CURDATE();
```

Get views by hour:
```sql
SELECT HOUR(viewed_at) as hour, COUNT(*) as views 
FROM blog_view_history 
WHERE DATE(viewed_at) = CURDATE() 
GROUP BY HOUR(viewed_at) 
ORDER BY hour;
```

Get unique visitors (by IP):
```sql
SELECT COUNT(DISTINCT user_ip) as unique_visitors 
FROM blog_view_history 
WHERE DATE(viewed_at) = CURDATE();
```

## Troubleshooting

**Database connection failed:**
- Check credentials in `api/db-config.php`
- Ensure MySQL is running
- Verify database exists

**Tables not created:**
- Check MySQL user has CREATE TABLE permission
- Look at PHP error logs
- Run setup script again

**Views not incrementing:**
- Check browser console for errors
- Verify API endpoint URL is correct
- Test API directly with curl

**Fallback to localStorage:**
- This is normal if database is unavailable
- Check network tab in browser dev tools
- Verify API file path is correct

## Security Notes

1. **Delete setup script** after running: `api/setup-blog-views-table.php`
2. Use **strong database password** in production
3. Consider adding **rate limiting** to prevent spam
4. Enable **HTTPS** for production deployment
5. Never commit `db-config.php` with real credentials to Git

## Production Deployment

When deploying to Hostinger:

1. Upload all files via FTP/File Manager
2. Update `db-config.php` with Hostinger credentials
3. Run setup script once via browser
4. Delete setup script
5. Test API endpoints
6. Monitor via Hostinger MySQL panel

## Support

For issues or questions:
- Check error logs in `/api/error_log`
- Enable PHP error reporting for debugging
- Check MySQL slow query log
- Monitor database size and performance

---

**Last Updated:** November 2, 2025
**Version:** 1.0.0
