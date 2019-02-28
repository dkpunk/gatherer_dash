<?php
$vip_port=$_GET['vip_port'];
$output=shell_exec("python ./fetchgathererbyvip.py $vip_port");
echo "<p>$output</p>";
?>
