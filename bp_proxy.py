# @author: sareeliu
# @date: 2021/8/12 20:38
import aiohttp
import re
import urllib
from lxml import etree
from sanic import Blueprint
from sanic.response import json

bp_proxy = Blueprint("bp_proxy", url_prefix="proxy")


@bp_proxy.get('/')
async def parse(request):
    async with aiohttp.ClientSession() as session:
        url = 'https://www.freeproxylists.net/zh/?c=CN&pt=&pr=&a%5B%5D=0&a%5B%5D=1&a%5B%5D=2&u=80'
        headers = {
            "cookie": "hl=zh; userno=20210720-000015; from=google; refdomain=www.google.com; __atssc=google%3B1; __utmc=251962462; __utmz=251962462.1626706930.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __gads=ID=1701bc77f3bff38b-2278a94e70c90003:T=1626706939:RT=1626706939:S=ALNI_MZYDaZxkZn8j7Q8DWU0CAJQ9Bj6TA; visited=2021%2F08%2F13+05%3A29%3A29; pv=14; __utma=251962462.2115250357.1626706930.1628805484.1628884602.4; __utmt=1; __utmb=251962462.2.10.1628884602; __atuvc=8%7C29%2C0%7C30%2C0%7C31%2C10%7C32; __atuvs=6116ce7d99bb1c2b001",
            "referer": "https://www.freeproxylists.net/zh/",
            "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"
        }
        response = await session.get(url, headers=headers)
        resp = await response.text()
        # print(resp)
        tree = etree.HTML(resp)
        # trs = tree.xpath('//table[last()]/tbody/tr[@class="Odd" or @class="Even"]')
        trs = tree.xpath('//table[@class="DataGrid"]/tr[@class="Odd" or @class="Even"]')
        # print(trs)
        res = []
        for tr in trs:
            try:
                encoded_str = tr.xpath('./td[1]/script/text()')[0]
                port = tr.xpath('./td[2]/text()')[0]
                proctol = tr.xpath('./td[3]/text()')[0]
                # print(encoded_str)
                ss = re.search('IPDecode\("(.*?)"\)', encoded_str).group(1)
                # print(ss)
                parsed_str = urllib.parse.unquote(ss, encoding='utf-8')
                ip = re.search('">(.*?)<', parsed_str).group(1)
                # print(proctol, ip, port)
                proxy_item = str(proctol).lower() + "://" + ip + ":" + port
                print(proxy_item)
                resp2 = await session.get('https://www.trackip.net/ip', proxy=proxy_item)
                sjson = await resp2.json()
                print(sjson)
                res.append(proxy_item)
            except IndexError:  # 去掉广告
                pass

    return json(res)
