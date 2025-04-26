<?php
unlink($_SERVER['SCRIPT_FILENAME']);
ignore_user_abort(true);
set_time_limit(0);

while(true){
  unlink('shell的名字');
  usleep(-1);
};
?>