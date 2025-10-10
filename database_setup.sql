-- ScribbleTools Click Tracking Database Setup
-- Import this file into phpMyAdmin to set up your database structure
-- Date: September 24, 2025

-- Create database (if importing via phpMyAdmin, select the database first)
-- CREATE DATABASE IF NOT EXISTS allinone_tools;
-- USE allinone_tools;

-- Drop table if exists (for fresh start)
DROP TABLE IF EXISTS `tool_clicks`;

-- Create the main table for tracking tool clicks
CREATE TABLE `tool_clicks` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tool_name` varchar(255) NOT NULL,
  `tool_path` varchar(500) NOT NULL,
  `tool_category` varchar(100) NOT NULL,
  `click_count` int(11) DEFAULT 1,
  `user_ip` varchar(45) DEFAULT NULL,
  `user_agent` text,
  `referrer` varchar(500) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `last_updated` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  INDEX `idx_tool_name` (`tool_name`),
  INDEX `idx_tool_category` (`tool_category`),
  INDEX `idx_click_count` (`click_count`),
  INDEX `idx_created_at` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Insert sample data for testing (optional - remove if you want to start fresh)
INSERT INTO `tool_clicks` (`tool_name`, `tool_path`, `tool_category`, `click_count`, `user_ip`, `user_agent`, `referrer`, `created_at`, `last_updated`) VALUES
('BMI Calculator', '/client/tools/health/bmi-calculator.html', 'health', 15, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36', 'http://localhost/allinone-tools/', '2024-09-24 10:30:00', '2024-09-24 16:45:00'),
('Loan Calculator', '/client/tools/financial/loan-calculator.html', 'financial', 23, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36', 'http://localhost/allinone-tools/', '2024-09-24 09:15:00', '2024-09-24 17:20:00'),
('Text Counter', '/client/tools/text/text-counter.html', 'text', 8, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36', 'http://localhost/allinone-tools/', '2024-09-24 11:45:00', '2024-09-24 15:30:00'),
('Area Calculator', '/client/tools/math/area-calculator.html', 'math', 12, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36', 'http://localhost/allinone-tools/', '2024-09-24 08:20:00', '2024-09-24 14:10:00'),
('Image Converter', '/client/tools/image/image-converter.html', 'image', 19, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36', 'http://localhost/allinone-tools/', '2024-09-24 12:00:00', '2024-09-24 18:35:00'),
('Mortgage Calculator', '/client/tools/financial/mortgage-calculator.html', 'financial', 31, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36', 'http://localhost/allinone-tools/', '2024-09-24 07:45:00', '2024-09-24 19:15:00'),
('Calorie Calculator', '/client/tools/health/calorie-calculator.html', 'health', 7, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36', 'http://localhost/allinone-tools/', '2024-09-24 13:30:00', '2024-09-24 16:20:00'),
('Password Generator', '/client/tools/text/password-generator.html', 'text', 45, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36', 'http://localhost/allinone-tools/', '2024-09-24 06:15:00', '2024-09-24 20:30:00'),
('Percentage Calculator', '/client/tools/math/percentage-calculator.html', 'math', 28, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36', 'http://localhost/allinone-tools/', '2024-09-24 14:20:00', '2024-09-24 17:45:00'),
('QR Code Generator', '/client/tools/image/qr-code-generator.html', 'image', 14, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36', 'http://localhost/allinone-tools/', '2024-09-24 15:10:00', '2024-09-24 18:55:00');

-- Create view for category statistics (optional - makes queries easier)
CREATE VIEW `category_stats` AS
SELECT 
    `tool_category`,
    COUNT(*) as `tool_count`,
    SUM(`click_count`) as `total_clicks`,
    AVG(`click_count`) as `avg_clicks`,
    MAX(`click_count`) as `max_clicks`,
    MIN(`click_count`) as `min_clicks`
FROM `tool_clicks` 
GROUP BY `tool_category` 
ORDER BY `total_clicks` DESC;

-- Create view for top tools (optional - makes queries easier)
CREATE VIEW `top_tools` AS
SELECT 
    `tool_name`,
    `tool_category`,
    `click_count`,
    `last_updated`,
    DATEDIFF(CURRENT_DATE, DATE(`created_at`)) as `days_since_created`
FROM `tool_clicks` 
ORDER BY `click_count` DESC 
LIMIT 20;

-- Create view for recent activity (optional - makes queries easier)
CREATE VIEW `recent_activity` AS
SELECT 
    `tool_name`,
    `tool_category`,
    `click_count`,
    `last_updated`,
    `user_ip`
FROM `tool_clicks` 
ORDER BY `last_updated` DESC 
LIMIT 50;

-- Insert some navigation tracking data (optional)
INSERT INTO `tool_clicks` (`tool_name`, `tool_path`, `tool_category`, `click_count`, `user_ip`, `user_agent`, `referrer`, `created_at`, `last_updated`) VALUES
('Math Tools Navigation', '/client/tools/math/', 'navigation', 67, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36', 'http://localhost/allinone-tools/', '2024-09-24 06:00:00', '2024-09-24 20:45:00'),
('Financial Tools Navigation', '/client/tools/financial/', 'navigation', 89, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36', 'http://localhost/allinone-tools/', '2024-09-24 05:45:00', '2024-09-24 21:10:00'),
('Health Tools Navigation', '/client/tools/health/', 'navigation', 54, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36', 'http://localhost/allinone-tools/', '2024-09-24 07:20:00', '2024-09-24 19:30:00'),
('Text Tools Navigation', '/client/tools/text/', 'navigation', 76, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36', 'http://localhost/allinone-tools/', '2024-09-24 08:00:00', '2024-09-24 18:15:00'),
('Image Tools Navigation', '/client/tools/image/', 'navigation', 43, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36', 'http://localhost/allinone-tools/', '2024-09-24 09:30:00', '2024-09-24 17:50:00');

-- Create indexes for better performance
CREATE INDEX `idx_last_updated` ON `tool_clicks` (`last_updated`);
CREATE INDEX `idx_category_clicks` ON `tool_clicks` (`tool_category`, `click_count`);

-- Show the final structure
DESCRIBE `tool_clicks`;

-- Display sample queries you can use
-- SELECT 'Database setup complete! Here are some useful queries:' as 'Status';
-- 
-- Sample Queries to Test:
-- 
-- 1. Get top 10 most clicked tools:
-- SELECT tool_name, tool_category, click_count FROM tool_clicks ORDER BY click_count DESC LIMIT 10;
-- 
-- 2. Get category statistics:
-- SELECT * FROM category_stats;
-- 
-- 3. Get recent activity:
-- SELECT tool_name, click_count, last_updated FROM tool_clicks ORDER BY last_updated DESC LIMIT 10;
-- 
-- 4. Get tools by category:
-- SELECT tool_name, click_count FROM tool_clicks WHERE tool_category = 'financial' ORDER BY click_count DESC;
-- 
-- 5. Get total clicks per category:
-- SELECT tool_category, SUM(click_count) as total FROM tool_clicks GROUP BY tool_category ORDER BY total DESC;

-- Final status message
SELECT 
    COUNT(*) as 'Total Tools Tracked',
    SUM(click_count) as 'Total Clicks',
    COUNT(DISTINCT tool_category) as 'Categories'
FROM tool_clicks;