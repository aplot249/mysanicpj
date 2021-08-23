# @author: sareeliu
# @date: 2021/8/14 17:26
import aiohttp, asyncio
from lxml import etree
import sanic
from sanic.blueprints import Blueprint

bp_ql = Blueprint(url_prefix='ql',name='ql')

@bp_ql.get('/')
async def main(request):
    async with aiohttp.ClientSession() as session:
        url = "http://hnt.gzcqs.com/Query/Jc/DataQueryList.aspx?Jcfa=HUN_BZYH_GROU&Jctype=0&JctypeValue=&State=1&First=2021-07-15&End=2021-08-15&type=1&PrintState=&DJState=&sg="
        headers = {
            "Cookie": "ASP.NET_SessionId=jztzj4tx5trdawljex1nyazz",
            "Referer": "http://hnt.gzcqs.com/Query/Jc/DataQuery.aspx?type=1",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"
        }
        resp = await session.get(url, headers=headers)
        res = await resp.text()
        print(res)


