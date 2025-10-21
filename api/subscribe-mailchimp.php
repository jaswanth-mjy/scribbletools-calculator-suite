<?php
// FREE Mailchimp Subscription API
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST');
header('Access-Control-Allow-Headers: Content-Type');

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['error' => 'Method not allowed']);
    exit;
}

$input = json_decode(file_get_contents('php://input'), true);
$email = $input['email'] ?? '';
$tags = $input['tags'] ?? [];
$source = $input['source'] ?? 'website';

if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
    http_response_code(400);
    echo json_encode(['error' => 'Invalid email address']);
    exit;
}

// Mailchimp API Configuration (FREE TIER - 500 contacts, 1000 emails/month)
$mailchimpApiKey = 'YOUR_MAILCHIMP_API_KEY'; // Get free at https://mailchimp.com
$listId = 'YOUR_LIST_ID';
$dataCenter = substr($mailchimpApiKey, strpos($mailchimpApiKey, '-') + 1);
$mailchimpEndpoint = "https://{$dataCenter}.api.mailchimp.com/3.0/lists/{$listId}/members";

$subscriberData = [
    'email_address' => $email,
    'status' => 'subscribed',
    'merge_fields' => [
        'SOURCE' => $source
    ],
    'tags' => $tags
];

$ch = curl_init();
curl_setopt_array($ch, [
    CURLOPT_URL => $mailchimpEndpoint,
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_POST => true,
    CURLOPT_POSTFIELDS => json_encode($subscriberData),
    CURLOPT_HTTPHEADER => [
        'Content-Type: application/json',
        'Authorization: Basic ' . base64_encode('user:' . $mailchimpApiKey)
    ]
]);

$response = curl_exec($ch);
$httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
curl_close($ch);

// Log all subscriptions locally (free backup system)
$logEntry = [
    'email' => $email,
    'timestamp' => date('Y-m-d H:i:s'),
    'service' => 'mailchimp',
    'status' => ($httpCode >= 200 && $httpCode < 300) ? 'success' : 'failed',
    'http_code' => $httpCode,
    'source' => $source,
    'tags' => $tags
];

$logFile = __DIR__ . '/subscription_log.json';
$existingLog = file_exists($logFile) ? json_decode(file_get_contents($logFile), true) : [];
$existingLog[] = $logEntry;
file_put_contents($logFile, json_encode($existingLog, JSON_PRETTY_PRINT));

if ($httpCode >= 200 && $httpCode < 300) {
    echo json_encode([
        'success' => true,
        'message' => 'Successfully subscribed to Mailchimp',
        'service' => 'mailchimp_free'
    ]);
} else {
    $responseData = json_decode($response, true);
    
    // Check if it's a duplicate email (not an error)
    if (isset($responseData['title']) && $responseData['title'] === 'Member Exists') {
        echo json_encode([
            'success' => true,
            'message' => 'Email already subscribed',
            'service' => 'mailchimp_duplicate'
        ]);
    } else {
        echo json_encode([
            'success' => false,
            'message' => 'Subscription failed: ' . ($responseData['detail'] ?? 'Unknown error'),
            'service' => 'mailchimp_error'
        ]);
    }
}
?>