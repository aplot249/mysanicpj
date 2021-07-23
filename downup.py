#@author: sareeliu
#@date: 2021/7/22 21:30
import requests
from requests_toolbelt import MultipartEncoder

m = MultipartEncoder(
    fields={
        "title":"标题10",
        "link":"http://baidu.com/",
        'img': ('6.jpg', open('./6.jpg', 'rb'),"jpg"),
})

r = requests.post('http://127.0.0.1:8000/video/', data=m, headers={'Content-Type': m.content_type})
print(r.json())