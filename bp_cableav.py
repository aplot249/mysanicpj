#@author: sareeliu
#@date: 2021/7/4 18:55
from lxml import etree
from sanic.response import json as sjson
from sanic import Blueprint
import aiohttp,asyncio,re,json

bp_cableav = Blueprint(url_prefix='cableav',name='bp_cableav')


async def item(title,link,res_list):
    async with aiohttp.ClientSession() as session:
        response = await session.get(link)
        res = await response.text()
        vidorev_jav_js_object = re.search("var vidorev_jav_js_object = (.*?);",res).group(1)
        vidorev_jav_js_object_json = json.loads(vidorev_jav_js_object)
        d1 = vidorev_jav_js_object_json['single_media_sources']
        d2 = vidorev_jav_js_object_json['single_media_vod_metadata']
        d1.insert(0,d2)
        d1.insert(0,{"title":title})
        # print(d1)
        res_list.append(d1)


@bp_cableav.get('/<tag>/')
async def parsepage(request,tag):
    async with aiohttp.ClientSession() as session:
        baseUrlList = {
             "chinese-live-porn":"https://cableav.tv/category/chinese-live-porn",   # 中国主播
             "korean-live-porn":"https://cableav.tv/category/korean-live-porn" ,    # 韩国主播
             "selfie-porn":"https://cableav.tv/category/selfie-porn" ,              # 自拍流出
             "private-show-porn":"https://cableav.tv/category/private-show-porn",   # 主播福利
             "kol-selfie-porn":"https://cableav.tv/category/kol-selfie-porn",       # 网红福利
             "master-91porn":"https://cableav.tv/category/master-91porn" ,          # 91大神
             "chinese-av-porn":"https://cableav.tv/category/chinese-av-porn",       # 国产AV
             "jav-4k":"https://cableav.tv/category/jav-4k",
        }
        # print(request.args)
        page = request.args.get("page")
        response = await session.get(f"{baseUrlList[tag]}/page/{page}/")
        res = await response.text()
        tree = etree.HTML(res)
        divs = tree.xpath('//article/div/div[@class="blog-pic"]/div')
        list,res_list = [],[]
        for div in divs:
            link = div.xpath("./a/@href")[0]
            title = div.xpath("./a/@title")[0].replace(" ",'')
            list.append(item(title,link,res_list))
        await asyncio.gather(*list)
        return sjson(res_list)
