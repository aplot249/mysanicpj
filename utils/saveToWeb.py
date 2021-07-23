#@author: sareeliu
#@date: 2021/7/22 21:30
import requests,pathlib
from requests_toolbelt import MultipartEncoder

def down_img_and_save_to_web(title,img,link):
    imgcontent = requests.get(img)
    img_save_path = 'douyin/img/'+title+"."+str(img).split('.')[-1]
    with open(img_save_path,'wb') as f:
        f.write(imgcontent.content)
        f.flush()

    m = MultipartEncoder(
        fields={
            "title":title,
            "link":link,
            'img': (title+'.'+str(img).split('.')[-1], open(img_save_path, 'rb'),"jpg"),
    })
    r = requests.post('http://django.chuanyun101.com/video/', data=m, headers={'Content-Type': m.content_type})
    print(r.json())