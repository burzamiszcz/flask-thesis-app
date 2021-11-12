<?php
require_once '_db.php';

$stmt = $db->prepare("SELECT * FROM events WHERE NOT (event_end <= :start OR event_start >= :end)");
$stmt->bindParam(':start', $_GET['start']);
$stmt->bindParam(':end', $_GET['end']);
$stmt->execute();
$result = $stmt->fetchAll();

class Event {}
$events = array();

foreach($result as $row) {
  $e = new Event();
  $e->id = $row['id'];
  $e->text = $row['name'];
  $e->start = $row['event_start'];
  $e->end = $row['event_end'];
  $events[] = $e;
}

echo json_encode($events);
