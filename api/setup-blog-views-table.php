<?php
/**
 * Database Setup Script for Blog Article Views
 * Run this script once to create the blog_article_views table
 */

require_once 'db-config.php';

// Create blog article views table
$createBlogViewsTable = "
CREATE TABLE IF NOT EXISTS blog_article_views (
    id INT AUTO_INCREMENT PRIMARY KEY,
    article_id VARCHAR(100) NOT NULL,
    view_count INT DEFAULT 0,
    last_viewed TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_article (article_id),
    INDEX idx_view_count (view_count),
    INDEX idx_article_id (article_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
";

// Create view history table for detailed tracking
$createViewHistoryTable = "
CREATE TABLE IF NOT EXISTS blog_view_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    article_id VARCHAR(100) NOT NULL,
    user_ip VARCHAR(45),
    user_agent TEXT,
    referrer VARCHAR(500),
    session_id VARCHAR(100),
    viewed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_article_id (article_id),
    INDEX idx_viewed_at (viewed_at),
    INDEX idx_session_id (session_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
";

try {
    // Create blog views table
    $pdo->exec($createBlogViewsTable);
    echo "✅ Table 'blog_article_views' created successfully!<br>";
    
    // Create view history table
    $pdo->exec($createViewHistoryTable);
    echo "✅ Table 'blog_view_history' created successfully!<br>";
    
    // Insert initial data for all 12 articles
    $articles = [
        'text-article',
        'financial-article',
        'health-article',
        'math-article',
        'image-article',
        'student-article',
        'time-article',
        'exam-article',
        'investment-article',
        'fitness-article',
        'budget-article',
        'productivity-article'
    ];
    
    $insertSQL = "INSERT IGNORE INTO blog_article_views (article_id, view_count) VALUES (?, 0)";
    $stmt = $pdo->prepare($insertSQL);
    
    foreach ($articles as $articleId) {
        $stmt->execute([$articleId]);
    }
    
    echo "✅ Initialized all 12 blog articles with 0 views!<br>";
    echo "<br><strong>Database setup completed successfully!</strong><br>";
    echo "<br>You can now delete this file for security.";
    
} catch(PDOException $e) {
    echo "❌ Error: " . $e->getMessage();
    error_log("Blog views table creation failed: " . $e->getMessage());
}
?>
