<?php
require 'vendor/autoload.php'
// TODO: actual API key

$apiKey = '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'; 

// Define the endpoint URL
$endpoint = 'https://api.openai.com/v1/chat/completions';


$data = array(
    'q' => $_POST['text'],
    'target' => 'en'
);

$options = array(
    'http' => array(
        'header' => "Content-type: application/x-www-form-urlencoded\r\n",
        'method' => 'POST',
        'content' => http_build_query($data)
    )
);

$context = stream_context_create($options);
$result = file_get_contents($url, false, $context);

$response = json_decode($result, true);

echo $response['data']['translations'][0]['translatedText'];
?>