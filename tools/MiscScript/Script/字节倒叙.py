f = open('zip', 'rb').read()
res = open('1.zip', 'wb')
res.write(f[::-1])