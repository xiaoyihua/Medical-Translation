<?php
    require 'vendor/autoload.php';
    $client = OpenAI::client('YOUR_API_KEY');

    if ($_SERVER['REQUEST_METHOD'] === 'POST') {
        $text = $_POST['text'];
        $translateFrom = $_POST['translateFrom'];
        $translateTo = $_POST['translateTo'];

        if (!empty($text)) {
            $apiUrl = 'https://api.openai.com/v1/chat/completions';
            $data = [
                'text' => $text,
                'translateFrom' => $translateFrom,
                'translateTo' => $translateTo
            ];

            $options = [
                'http' => [
                    'header'  => "Content-type: application/x-www-form-urlencoded\r\n",
                    'method'  => 'POST',
                    'content' => http_build_query($data)
                ]
            ];

            $context  = stream_context_create($options);
            $result = file_get_contents($apiUrl, false, $context);

            if ($result !== false) {
                $responseData = json_decode($result, true);
                $translatedText = $responseData['responseData']['translatedText'];

                echo $translatedText;
            } else {
                echo 'Error: Unable to make API call.';
            }
        } else {
            echo 'Error: Text field is empty.';
        }
    } else {
        echo 'Error: Invalid request method.';
    }
?>