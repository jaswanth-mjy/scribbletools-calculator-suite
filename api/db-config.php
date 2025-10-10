<?php
/**
 * Database Configuration for Hostinger
 * ScribbleTools Click Tracking System
 */

// Database credentials for Hostinger
define('DB_HOST', 'your-hostinger-mysql-host.com'); // Replace with your Hostinger MySQL host
define('DB_NAME', 'your_database_name'); // Replace with your database name
define('DB_USER', 'your_username'); // Replace with your database username
define('DB_PASS', 'your_password'); // Replace with your database password

// Create database connection
try {
    $pdo = new PDO("mysql:host=" . DB_HOST . ";dbname=" . DB_NAME . ";charset=utf8mb4", DB_USER, DB_PASS);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    $pdo->setAttribute(PDO::ATTR_DEFAULT_FETCH_MODE, PDO::FETCH_ASSOC);
} catch(PDOException $e) {
    error_log("Database connection failed: " . $e->getMessage());
    die("Database connection failed");
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
)";

try {
    $pdo->exec($createTableSQL);
} catch(PDOException $e) {
    error_log("Table creation failed: " . $e->getMessage());
}
?>