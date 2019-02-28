<?php
$vip_port=$_GET['vip_port'];
$state=$_GET['state'];
$output=shell_exec("python ./fetchgathererbyvip_online.py $vip_port $state");
echo "<p>$output</p>";
?>
