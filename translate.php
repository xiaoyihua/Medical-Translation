<?php
    require 'vendor/autoload.php';
    $client = OpenAI::client('YOUR_API_KEY');

    if ($_SERVER['REQUEST_METHOD'] === 'POST') {
        $text = $_POST['text'];
        $translateFrom = $_POST['translateFrom'];
        $translateTo = $_POST['translateTo'];

        if (!empty($text)) {
            $apiUrl = 'https://api.openai.com/v1/chat/completions';
            $data = $client->chat()->create([
                'model' => 'gpt-3.5-turbo',
                'messages' => [[
                    'role' => 'system',
                    'content' => "You are a doctor. You speak multiple languages and are specialized in translating medical documents.",
                ],
                [
                    'role' => 'user',
                    'content' => "Translate the following text from $translateFrom to $translateTo: $text",
                 ]],
                 'temperature' => 1,
                 'max_tokens' => 50,
                 'top_p' => 1, 
            ]);

            if ($result !== false) {
                echo $data['choices'][0]['message']['content'];

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