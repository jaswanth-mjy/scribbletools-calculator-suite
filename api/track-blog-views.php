<?php
/**
 * Blog Article View Tracking API
 * Handles incrementing and retrieving blog article view counts
 */

header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST');
header('Access-Control-Allow-Headers: Content-Type');

require_once 'db-config.php';

// Get request method
$method = $_SERVER['REQUEST_METHOD'];

// Handle preflight OPTIONS request
if ($method === 'OPTIONS') {
    http_response_code(200);
    exit();
}

/**
 * Get client IP address
 */
function getClientIP() {
    $ipaddress = '';
    if (isset($_SERVER['HTTP_CLIENT_IP']))
        $ipaddress = $_SERVER['HTTP_CLIENT_IP'];
    else if(isset($_SERVER['HTTP_X_FORWARDED_FOR']))
        $ipaddress = $_SERVER['HTTP_X_FORWARDED_FOR'];
    else if(isset($_SERVER['HTTP_X_FORWARDED']))
        $ipaddress = $_SERVER['HTTP_X_FORWARDED'];
    else if(isset($_SERVER['HTTP_FORWARDED_FOR']))
        $ipaddress = $_SERVER['HTTP_FORWARDED_FOR'];
    else if(isset($_SERVER['HTTP_FORWARDED']))
        $ipaddress = $_SERVER['HTTP_FORWARDED'];
    else if(isset($_SERVER['REMOTE_ADDR']))
        $ipaddress = $_SERVER['REMOTE_ADDR'];
    else
        $ipaddress = 'UNKNOWN';
    return $ipaddress;
}

/**
 * GET: Retrieve view counts for all articles or specific article
 */
if ($method === 'GET') {
    try {
        $articleId = isset($_GET['article_id']) ? $_GET['article_id'] : null;
        
        if ($articleId) {
            // Get specific article view count
            $stmt = $pdo->prepare("SELECT article_id, view_count, last_viewed FROM blog_article_views WHERE article_id = ?");
            $stmt->execute([$articleId]);
            $result = $stmt->fetch();
            
            if ($result) {
                echo json_encode([
                    'success' => true,
                    'data' => $result
                ]);
            } else {
                echo json_encode([
                    'success' => false,
                    'message' => 'Article not found'
                ]);
            }
        } else {
            // Get all article view counts
            $stmt = $pdo->query("SELECT article_id, view_count, last_viewed FROM blog_article_views ORDER BY view_count DESC");
            $results = $stmt->fetchAll();
            
            echo json_encode([
                'success' => true,
                'data' => $results,
                'total_articles' => count($results)
            ]);
        }
    } catch (PDOException $e) {
        http_response_code(500);
        echo json_encode([
            'success' => false,
            'message' => 'Database error',
            'error' => $e->getMessage()
        ]);
    }
}

/**
 * POST: Increment view count for an article
 */
elseif ($method === 'POST') {
    try {
        // Get POST data
        $input = json_decode(file_get_contents('php://input'), true);
        $articleId = isset($input['article_id']) ? $input['article_id'] : null;
        
        if (!$articleId) {
            http_response_code(400);
            echo json_encode([
                'success' => false,
                'message' => 'article_id is required'
            ]);
            exit();
        }
        
        // Start transaction
        $pdo->beginTransaction();
        
        // Insert or update view count
        $stmt = $pdo->prepare("
            INSERT INTO blog_article_views (article_id, view_count) 
            VALUES (?, 1) 
            ON DUPLICATE KEY UPDATE 
                view_count = view_count + 1,
                last_viewed = CURRENT_TIMESTAMP
        ");
        $stmt->execute([$articleId]);
        
        // Get updated view count
        $stmt = $pdo->prepare("SELECT view_count FROM blog_article_views WHERE article_id = ?");
        $stmt->execute([$articleId]);
        $result = $stmt->fetch();
        $newViewCount = $result['view_count'];
        
        // Log view in history table (optional, for detailed analytics)
        $userIP = getClientIP();
        $userAgent = $_SERVER['HTTP_USER_AGENT'] ?? 'Unknown';
        $referrer = $_SERVER['HTTP_REFERER'] ?? '';
        $sessionId = session_id() ?: uniqid('sess_', true);
        
        $stmt = $pdo->prepare("
            INSERT INTO blog_view_history (article_id, user_ip, user_agent, referrer, session_id) 
            VALUES (?, ?, ?, ?, ?)
        ");
        $stmt->execute([$articleId, $userIP, $userAgent, $referrer, $sessionId]);
        
        // Commit transaction
        $pdo->commit();
        
        echo json_encode([
            'success' => true,
            'message' => 'View count incremented',
            'data' => [
                'article_id' => $articleId,
                'view_count' => $newViewCount
            ]
        ]);
        
    } catch (PDOException $e) {
        $pdo->rollBack();
        http_response_code(500);
        echo json_encode([
            'success' => false,
            'message' => 'Database error',
            'error' => $e->getMessage()
        ]);
    }
}

/**
 * Invalid method
 */
else {
    http_response_code(405);
    echo json_encode([
        'success' => false,
        'message' => 'Method not allowed'
    ]);
}
?>
