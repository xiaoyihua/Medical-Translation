<?php

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $sourceText = $_POST['sourceText'];

    // Translate the text using a PHP library or the Google Translate API
    // ...

    // Return the translated text
    echo "<textarea name='translatedText' rows='10' cols='50' readonly>$translatedText</textarea>";
}
?>