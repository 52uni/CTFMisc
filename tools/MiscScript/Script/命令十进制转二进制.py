cmd='/flag'

payload=''
for c in cmd:
        payload+=f'\\{bin(int(oct(ord(c))[2:]))[2:]}'

payload+='\\\''


print(payload)