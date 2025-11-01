<?php
// FREE Brevo (Sendinblue) Subscription API
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
$listIds = $input['listIds'] ?? [1];
$attributes = $input['attributes'] ?? [];

if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
    http_response_code(400);
    echo json_encode(['error' => 'Invalid email address']);
    exit;
}

// Brevo API Configuration (FREE TIER)
$brevoApiKey = 'YOUR_BREVO_API_KEY'; // Get free at https://app.brevo.com/
$brevoEndpoint = 'https://api.brevo.com/v3/contacts';

$data = [
    'email' => $email,
    'listIds' => $listIds,
    'attributes' => $attributes,
    'updateEnabled' => true
];

$ch = curl_init();
curl_setopt_array($ch, [
    CURLOPT_URL => $brevoEndpoint,
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_POST => true,
    CURLOPT_POSTFIELDS => json_encode($data),
    CURLOPT_HTTPHEADER => [
        'Content-Type: application/json',
        'api-key: ' . $brevoApiKey
    ]
]);

$response = curl_exec($ch);
$httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
curl_close($ch);

if ($httpCode >= 200 && $httpCode < 300) {
    // Log subscription locally (free backup)
    $logEntry = [
        'email' => $email,
        'timestamp' => date('Y-m-d H:i:s'),
        'service' => 'brevo',
        'status' => 'success'
    ];
    
    $logFile = __DIR__ . '/subscription_log.json';
    $existingLog = file_exists($logFile) ? json_decode(file_get_contents($logFile), true) : [];
    $existingLog[] = $logEntry;
    file_put_contents($logFile, json_encode($existingLog, JSON_PRETTY_PRINT));
    
    echo json_encode([
        'success' => true,
        'message' => 'Successfully subscribed to Brevo',
        'service' => 'brevo_free'
    ]);
} else {
    // Fallback to local storage
    $logEntry = [
        'email' => $email,
        'timestamp' => date('Y-m-d H:i:s'),
        'service' => 'fallback',
        'status' => 'pending',
        'error' => $response
    ];
    
    $logFile = __DIR__ . '/subscription_log.json';
    $existingLog = file_exists($logFile) ? json_decode(file_get_contents($logFile), true) : [];
    $existingLog[] = $logEntry;
    file_put_contents($logFile, json_encode($existingLog, JSON_PRETTY_PRINT));
    
    echo json_encode([
        'success' => true,
        'message' => 'Subscription saved locally for manual processing',
        'service' => 'fallback'
    ]);
}
?>