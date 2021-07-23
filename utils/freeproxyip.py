#@author: sareeliu
#@date: 2021/7/19 14:38
import requests

dd = {'http': "http://45.11.92.243:8888"}
# print(dd)
jjj = requests.get(url="http://ip-api.com/json", proxies=dd)
print(dd, jjj.json())

