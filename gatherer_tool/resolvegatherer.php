<?php
$ip_list=$_GET['ip'];
$vip_port=$_GET['vip_port'];
$output=shell_exec("python ./resolvegatherer.py \"$ip_list\" $vip_port");
echo "<p>$output</p>";
?>
