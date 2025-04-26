import requests as re
import time
urls = "http://localhost:55607/getScore.php"
headers1 = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:88.0) Gecko/20100101 Firefox/88.0"}
s = re.Session()
resp = s.get(url = urls,headers = headers1)
for i in range(31):
    resp = s.get(url = urls)
    print(i)
    print('\n\n')
    print(resp.text)
    time.sleep(1)