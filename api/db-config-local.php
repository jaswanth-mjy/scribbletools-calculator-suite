<?php
/**
 * Local Development Database Configuration
 * ScribbleTools Click Tracking System - Local Testing
 */

// Local development database credentials (XAMPP/WAMP default)
define('DB_HOST', 'localhost');
define('DB_NAME', 'scribbletools_local'); // You can create this database in phpMyAdmin
define('DB_USER', 'root'); // Default XAMPP/WAMP username
define('DB_PASS', ''); // Default XAMPP/WAMP password (usually empty)

// For production (Hostinger), uncomment and update these:
/*
define('DB_HOST', 'your-hostinger-mysql-host.com');
define('DB_NAME', 'your_production_database');
define('DB_USER', 'your_production_username'); 
define('DB_PASS', 'your_production_password');
*/

// Create database connection
try {
    $pdo = new PDO("mysql:host=" . DB_HOST . ";dbname=" . DB_NAME . ";charset=utf8mb4", DB_USER, DB_PASS);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    $pdo->setAttribute(PDO::ATTR_DEFAULT_FETCH_MODE, PDO::FETCH_ASSOC);
    
    // Log successful connection for local testing
    error_log("Database connected successfully to: " . DB_HOST . "/" . DB_NAME);
} catch(PDOException $e) {
    error_log("Database connection failed: " . $e->getMessage());
    
    // For local development, show more detailed error
    if (DB_HOST === 'localhost') {
        die("Local database connection failed: " . $e->getMessage() . 
            "<br><br>Please ensure:<br>" .
            "1. XAMPP/WAMP is running<br>" .
            "2. MySQL service is started<br>" .
            "3. Database 'scribbletools_local' exists in phpMyAdmin");
    } else {
        die("Database connection failed");
    }
}

// Create table if it doesn't exist
$createTableSQL = "
CREATE TABLE IF NOT EXISTS tool_clicks (
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci";

try {
    $pdo->exec($createTableSQL);
    error_log("Table 'tool_clicks' ready");
} catch(PDOException $e) {
    error_log("Table creation failed: " . $e->getMessage());
}
?>