#@author: sareeliu
#@date: 2021/7/2 10:24
import requests,re,aiohttp,asyncio
from requests_toolbelt import MultipartEncoder

# headers = {
#     "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36",
#     "referer": "https://3g.gljlw.com/diy/douyin.php"
# }
# url = "https://3g.gljlw.com/diy/ttxs_dy2.php?url=https%3A//v.douyin.com/eWMkRT9/&r=011715320318362199&s=bbf3165ccbd383d6587fefdbfffb8844"
#
# html = requests.get(url,headers=headers)
# # print(html.text)
# img = re.search('视频截图:\<br/\>\<img src=\"(?P<img>.*?)" width', html.text).groupdict('img')
# link = re.search('location.replace\(\"(?P<link>.*?)\"\)', html.text).groupdict('link')
# print(img,link)
import time

# data = {
#     "title":"标题10",
#     "link":"http://baidu.com/",
#     "img":"www，chuayun101fd"
# }
# res = requests.post("http://127.0.0.1:8000/video/",data=data)
# print(res.json())

# m = MultipartEncoder(
#     fields={
#         "title":"标题10",
#         "link":"http://baidu.com/"+str(time.time()),
# 、        'img': ('6.jpg', open('./6.jpg', 'rb'),"jpg"),
# })

# r = requests.post('http://127.0.0.1:8000/video/', data=m, headers={'Content-Type': m.content_type})
# print(r.json())

# headers = {
#     "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36",
# }
# res = requests.get("https://v.douyin.com/e418Xn4/",headers=headers)
#
# print(res.text)

# url = "https://v29.douyinvod.com/b7032067278a321e844b5eb059286dd5/60f9fa2e/video/tos/cn/tos-cn-ve-15/7690595b660b49e395594d649469d55e/?a=1128&amp;br=629&amp;bt=629&amp;btag=4&amp;cd=0%7C0%7C0&amp;ch=0&amp;cr=0&amp;cs=0&amp;cv=1&amp;dr=0&amp;ds=3&amp;er=&amp;ft=fjLApiHH_MZi85gkag31r5CYj9-w&amp;l=2021072306071601021216002830470BC4&amp;lr=&amp;mime_type=video_mp4&amp;net=0&amp;pl=0&amp;qs=0&amp;rc=ajdxdmpuOTc6NjMzNGkzM0ApNTw2aGc7NzxnNzw8OmZnZGcpaGRqbGRoaGRmMl5vM2hzNC5eYC0tZC1hc3MyNDQtX2ExLjIxLWE1MjJiOmNwb2wrbStqdDo%3D&amp;vl=&amp;vr="
#
# html = requests.get(url)
# html.content

headers = {
    "Referer": "https://www.douyin.com/",
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1"
}

share_link = "https://v.douyin.com/e418Xn4/"
# session = requests.session()
# response = session.get(share_link)
# response.encoding = response.apparent_encoding
# print(response.text)
async def get_title(share_link):
    async with aiohttp.ClientSession() as session:
        response = await session.get(share_link)
        res = await response.text()
        print(res)
        title = re.search('<title data-react-helmet="true"> (?P<title>.*?) - 抖音</title>',res).groupdict()['title']
        title = re.sub('\s||#','',title)
        print(title)

asyncio.get_event_loop().run_until_complete(get_title(share_link))