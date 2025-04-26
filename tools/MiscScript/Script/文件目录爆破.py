import requests

url = "http://challenge-1a8b2b19e0c90ecb.sandbox.ctfhub.com:10800/"

li1 = ['web', 'website', 'backup', 'back', 'www', 'wwwroot', 'temp']
li2 = ['tar', 'tar.gz', 'zip', 'rar']
for i in li1:
    for j in li2:
        url_final = url + "/" + i + "." + j
        r = requests.get(url_final)
        print(str(r)+"+"+url_final)
