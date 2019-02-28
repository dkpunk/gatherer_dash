<?php
$ip=$_GET['ip'];
$output=shell_exec("python ./getchecks.py $ip");
echo "<p>$output</p>";
?>
