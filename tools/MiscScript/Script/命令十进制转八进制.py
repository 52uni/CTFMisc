cmd='flag'

payload='$\''
for c in cmd:
        payload+=f'\\{oct(ord(c))[2:]}'

payload+="'"

print(payload)