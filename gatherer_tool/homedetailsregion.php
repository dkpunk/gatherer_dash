<?php
$dc_name=$_GET['dc_name'];
$output=shell_exec("python ./homedetailsregion.py $dc_name");
echo "$output";
?>
