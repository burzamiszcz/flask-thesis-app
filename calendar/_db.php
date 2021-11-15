<?php

$db_exists = file_exists("daypilot.sqlite");

$db = new PDO('sqlite:daypilot.sqlite');
$db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

if (!$db_exists) {
    //create the database
    $db->exec("CREATE TABLE IF NOT EXISTS events (
                        id INTEGER PRIMARY KEY, 
                        name TEXT, 
                        event_start DATETIME, 
                        event_end DATETIME
                        )");
}

?>
