# Medical-Translation
What is the goal of this project?
- This project seeks to leverage Microsoft Azure's GPT API in order to power medically compliant translation. This can help improve patient-doctor relationships among patients that do not primarily speak English.

What are the key files in this repository?
- CHOCTranslation.htm contains a modified version of CHOC's website HTML. It contains assets originally found in CHOC's website in addition to new assets. 

- CHOCTranslation.htm has been modified to directly include the translation box's CSS in the HTML as a style block.

- The styles can be separately found in translatorStyles.css.

- Icon assets are found in font-awesome.min.css.

- Countries.js provides a reactive list for the translation box.

- script.js contains functions that handle button events and creates a call to the PHP file.

- translate.php contains the actual API call which then posts the result into the other translation box.

How does this project assure translation quality?
- We use a semantic similarity model to make sure our engineered prompt produces translations close to that of human translation.

How does this project assure medical compliance?
- We use Microsoft Azure's version of the API in order to have control over the data.