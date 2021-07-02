#@author: sareeliu
#@date: 2021/7/2 10:24
import requests

response = requests.get("https://mp.weixin.qq.com/s/SH3LBCNFnPuU9x_Q3g0I0Q")
print(response.text)