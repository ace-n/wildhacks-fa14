<?
header('Content-Type: application/json; charset=utf-8');
include 'google-translate-php.php';

/* Check for a valid query from client. */
if(!isset($_GET['word']) || !isset($_GET['langTo']) || !isset($_GET['langFrom'])) {
	echo '-2';
	die();
}

$word = $_GET['word'];
$langTo   = $_GET['langTo'];
$langFrom = $_GET['langFrom'];

  /* Translate */
$result = translateSimple($langFrom, $langTo, $word);

if($result == NULL) {
    echo "-1";
    die();
}

  /* Echo the result to the client */
print "{\"text\":\"$result\"}";

function translateSimple($langFrom, $langTo, $word) {
	if ($langFrom == $langTo) {
		return $word;
	}
    $tr = new GoogleTranslate($langFrom, $langTo);
    $transArray = $tr->translateArray($word);
    $transArray = json_decode($transArray, true);
    if (isset($transArray) && isset($transArray[0]) && isset($transArray[0][0])){
        return $transArray[0][0][0];
    }
	else {
        return NULL;
    }
}
?>
