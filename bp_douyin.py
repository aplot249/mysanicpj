#@author: sareeliu
#@date: 2021/6/24 20:45
import aiohttp, asyncio, re, os, pathlib
from sanic import Blueprint
from sanic.response import text,json
from sanic.app import get_event_loop
from utils.mycos import client

bp_douyin = Blueprint("bp_douyin",url_prefix='douyin')

async def down_upload_video(res_dict):
    async with aiohttp.ClientSession() as session:
        response = await session.get(res_dict['link2'])
        p = pathlib.Path('video')
        if not p.exists():
            p.mkdir()
        absolute_path = p.joinpath(res_dict['title']+'.mp4')
        print(absolute_path.resolve())
        with open(absolute_path.resolve(), 'wb') as fd:
            while True:
                chunk = await response.content.read(512)
                if not chunk:
                    break
                fd.write(chunk)
                fd.flush()
                os.fsync(fd.fileno())
        # #上传
        await get_event_loop().run_in_executor(None, client.put_object_from_local_file, 'video', absolute_path, absolute_path.name)
        url = client.get_object_url('video', absolute_path.name)
        print(url)
        data = {
            'title':res_dict['title'],
            'link':url,
            "img":res_dict['img']
        }
        # resp = await session.post('http://127.0.0.1:8000/video/',data=data)
        resp = await session.post('http://django.chuanyun101.com/video/',data=data)
        jj = await resp.json()
        print(jj)

async def get_title(share_link,res_dict):
    async with aiohttp.ClientSession() as session:
        response = await session.get(share_link)
        res = await response.text()
        title = re.search('<title data-react-helmet="true"> (?P<title>.*?) - 抖音</title>',res).groupdict()['title']
        title = re.sub('\s||#','',title)
        print(title)
        res_dict['title'] = title


# async def jiekou1(share_link,res_dict):
#     async with aiohttp.ClientSession() as session:
#         headers = {
#             'User-Agent':"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
#         }
#         response = await session.get(f"https://ouotool.com/dy?url={share_link}",headers=headers)
#         res = await response.text()
#         # print(res)
#         link = re.search('<source src="(?P<link>.*?)"type="video/mp4">',res).group('link')
#         # print(link)
#         res_dict['link1'] = link

async def jiekou2(share_link,res_dict):
    async with aiohttp.ClientSession() as session:
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36",
            "referer": "https://3g.gljlw.com/diy/douyin.php"
        }
        response = await session.get(f"https://3g.gljlw.com/diy/ttxs_dy2.php?url={share_link}&r=011715320318362199&s=bbf3165ccbd383d6587fefdbfffb8844",headers=headers)
        res = await response.text()
        img = re.search('视频截图:\<br/\>\<img src=\"(?P<img>.*?)" width', res).groupdict()['img']
        link = re.search('location.replace\(\"(?P<link>.*?)\"\)', res).groupdict('link')['link']
        print(img, link)
        res_dict['img']=img
        res_dict['link2'] = link


@bp_douyin.get('link')
async def mylink(request):
    share_link = request.args.get("sharelink")
    if not re.search('^https://v.douyin.com/.*?',share_link):
        return text("分享链接错误")
    res_dict = {}
    await asyncio.gather(*[
        get_title(share_link,res_dict),
        jiekou2(share_link,res_dict),
        # jiekou2(share_link,res_dict)
    ])
    # print(res_dict)
    get_event_loop().create_task(down_upload_video(res_dict))
    return json(res_dict)

