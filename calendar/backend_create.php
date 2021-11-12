<?php
require_once '_db.php';

$json = file_get_contents('php://input');
$params = json_decode($json);

$stmt = $db->prepare("INSERT INTO events (name, event_start, event_end) VALUES (:name, :start, :end)");
$stmt->bindParam(':start', $params->start);
$stmt->bindParam(':end', $params->end);
$stmt->bindParam(':name', $params->text);
$stmt->execute();

class Result {}

$response = new Result();
$response->result = 'OK';
$response->id = $db->lastInsertId();
$response->message = 'Created with id: '.$db->lastInsertId();

echo json_encode($response);
