<?php
$apiKey = 'YOUR_API_KEY'; // TODO: replace with your actual API key
$url = 'https://translation.googleapis.com/language/translate/v2?key=' . $apiKey;

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