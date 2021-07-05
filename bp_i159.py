#@author: sareeliu
#@date: 2021/7/5 0:31
from sanic import Blueprint
from sanic.response import json
from lxml import etree
import asyncio,re,aiohttp

bp_159i = Blueprint(url_prefix="159i",name="bp_159i")

async def parselink(href,title,res):
    async with aiohttp.ClientSession() as session:
        response = await session.get(href)
        html = await response.text()
        tree = etree.HTML(html)
        src = tree.xpath('//p/iframe/@src')[0]
        headers = {"Referer":href}
        response2 = await session.get(src,headers=headers)
        html2 = await response2.text()
        # print(html2)
        m3u8 = re.search('source: "(.*?)",',html2).group(1)
        img = "https:"+re.search('poster: "(.*?)",',html2).group(1)
        # print(m3u8)
        res.append({"title":title,"img":img,"m3u8":m3u8})


@bp_159i.get('/')
async def parse(request):
    async with aiohttp.ClientSession() as session:
        page = request.args.get("page")
        response = await session.get(f"https://159i.com/video/page/{page}/")
        html = await response.text()
        # print(html)
        res,list = [],[]
        tree = etree.HTML(html)
        alinks = tree.xpath('//div[@class="info"]/h2/a')
        for link in alinks:
            href = link.xpath('./@href')[0]
            title = link.xpath('./text()')[0].replace(" ",'')
            list.append(parselink(href,title,res))
        await asyncio.gather(*list)
        return json(res)
