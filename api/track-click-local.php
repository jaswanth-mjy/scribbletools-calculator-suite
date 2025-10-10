<?php
/**
 * Click Tracking API Endpoint - Local Development Version
 * ScribbleTools - Track tool usage statistics locally
 */

header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST, GET, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');

// Handle preflight OPTIONS request
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit();
}

// Use local database configuration
require_once 'db-config-local.php';

function trackClick($toolName, $toolPath, $toolCategory) {
    global $pdo;
    
    try {
        // Get user information (local development friendly)
        $userIP = $_SERVER['REMOTE_ADDR'] ?? '127.0.0.1';
        $userAgent = $_SERVER['HTTP_USER_AGENT'] ?? 'Local Development';
        $referrer = $_SERVER['HTTP_REFERER'] ?? 'http://localhost';
        
        // Check if this tool already has entries
        $checkStmt = $pdo->prepare("SELECT id, click_count FROM tool_clicks WHERE tool_name = ? AND tool_path = ?");
        $checkStmt->execute([$toolName, $toolPath]);
        $existing = $checkStmt->fetch();
        
        if ($existing) {
            // Update existing record
            $updateStmt = $pdo->prepare("
                UPDATE tool_clicks 
                SET click_count = click_count + 1, 
                    user_ip = ?, 
                    user_agent = ?, 
                    referrer = ?,
                    last_updated = CURRENT_TIMESTAMP 
                WHERE id = ?
            ");
            $updateStmt->execute([$userIP, $userAgent, $referrer, $existing['id']]);
            $newCount = $existing['click_count'] + 1;
        } else {
            // Insert new record
            $insertStmt = $pdo->prepare("
                INSERT INTO tool_clicks (tool_name, tool_path, tool_category, click_count, user_ip, user_agent, referrer) 
                VALUES (?, ?, ?, 1, ?, ?, ?)
            ");
            $insertStmt->execute([$toolName, $toolPath, $toolCategory, $userIP, $userAgent, $referrer]);
            $newCount = 1;
        }
        
        // Log for local development
        error_log("LOCAL: Tracked click for $toolName (count: $newCount)");
        
        return [
            'success' => true,
            'tool_name' => $toolName,
            'click_count' => $newCount,
            'message' => 'Click tracked successfully (LOCAL)',
            'environment' => 'local_development'
        ];
    } catch (Exception $e) {
        error_log("LOCAL: Click tracking error: " . $e->getMessage());
        return [
            'success' => false,
            'error' => 'Failed to track click',
            'message' => $e->getMessage(),
            'environment' => 'local_development'
        ];
    }
}

function getClickStats($limit = 20) {
    global $pdo;
    
    try {
        $stmt = $pdo->prepare("
            SELECT tool_name, tool_category, click_count, last_updated 
            FROM tool_clicks 
            ORDER BY click_count DESC 
            LIMIT ?
        ");
        $stmt->execute([$limit]);
        $results = $stmt->fetchAll();
        
        error_log("LOCAL: Retrieved " . count($results) . " tool statistics");
        return $results;
    } catch (Exception $e) {
        error_log("LOCAL: Get stats error: " . $e->getMessage());
        return [];
    }
}

function getCategoryStats() {
    global $pdo;
    
    try {
        $stmt = $pdo->query("
            SELECT tool_category, SUM(click_count) as total_clicks, COUNT(*) as tool_count 
            FROM tool_clicks 
            GROUP BY tool_category 
            ORDER BY total_clicks DESC
        ");
        $results = $stmt->fetchAll();
        
        error_log("LOCAL: Retrieved " . count($results) . " category statistics");
        return $results;
    } catch (Exception $e) {
        error_log("LOCAL: Get category stats error: " . $e->getMessage());
        return [];
    }
}

// Handle different request methods
switch ($_SERVER['REQUEST_METHOD']) {
    case 'POST':
        $input = json_decode(file_get_contents('php://input'), true);
        
        if (!isset($input['tool_name']) || !isset($input['tool_path']) || !isset($input['tool_category'])) {
            http_response_code(400);
            echo json_encode([
                'success' => false,
                'error' => 'Missing required fields: tool_name, tool_path, tool_category',
                'environment' => 'local_development'
            ]);
            exit();
        }
        
        $result = trackClick($input['tool_name'], $input['tool_path'], $input['tool_category']);
        echo json_encode($result);
        break;
        
    case 'GET':
        $action = $_GET['action'] ?? 'stats';
        
        switch ($action) {
            case 'stats':
                $limit = (int)($_GET['limit'] ?? 20);
                $stats = getClickStats($limit);
                echo json_encode([
                    'success' => true,
                    'data' => $stats,
                    'environment' => 'local_development',
                    'count' => count($stats)
                ]);
                break;
                
            case 'categories':
                $categoryStats = getCategoryStats();
                echo json_encode([
                    'success' => true,
                    'data' => $categoryStats,
                    'environment' => 'local_development',
                    'count' => count($categoryStats)
                ]);
                break;
                
            case 'test':
                // Special test endpoint for local development
                echo json_encode([
                    'success' => true,
                    'message' => 'Local API is working!',
                    'environment' => 'local_development',
                    'database_host' => DB_HOST,
                    'database_name' => DB_NAME,
                    'timestamp' => date('Y-m-d H:i:s')
                ]);
                break;
                
            default:
                http_response_code(400);
                echo json_encode([
                    'success' => false,
                    'error' => 'Invalid action',
                    'environment' => 'local_development'
                ]);
        }
        break;
        
    default:
        http_response_code(405);
        echo json_encode([
            'success' => false,
            'error' => 'Method not allowed',
            'environment' => 'local_development'
        ]);
}
?>