#@author: sareeliu
#@date: 2021/6/30 10:52
import aiohttp
from lxml import etree
from sanic.response import json
from sanic import Blueprint

bp_vpn = Blueprint("bp_vpn", url_prefix="vpn")

#/2、获取vpn下载链接
@bp_vpn.get("/software")
async def vpnsoftware(request):
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
    }
    json_content = []
    async with aiohttp.ClientSession() as session:
        response = await session.get("https://www.catpaws2011.com/docs/?p=420",headers=headers)
        res = await response.text()
        # print(res)
        tree = etree.HTML(res)
        ps = tree.xpath("//p[contains(text(),'下载地址')]")
        for p in ps:
            content = p.xpath("./text()")[0]
            href = p.xpath("./a/@href")[0]
            json_content.append({"content":content,"href":href})
    return json(json_content)


