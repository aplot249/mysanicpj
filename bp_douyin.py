#@author: sareeliu
#@date: 2021/6/24 20:45
import aiohttp
import re
from sanic import Blueprint
from sanic.response import text

bp_douyin = Blueprint("bp_douyin",url_prefix='douyin')

@bp_douyin.get('link')
async def mylink(request):
    share_link = request.args.get("sharelink")
    # print(share_link)
    if not re.search('^https://v.douyin.com/.*?',share_link):
        return text("分享链接错误")
    # share_link = "https://v.douyin.com/e418Xn4/"
    async with aiohttp.ClientSession() as session:
        headers = {
            'User-Agent':"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
        }
        response = await session.get(f"https://ouotool.com/dy?url={share_link}",headers=headers)
        res = await response.text()
        # print(res)
        link = re.search('<source src="(?P<link>.*?)"type="video/mp4">',res).group('link')
        # print(link)
        return text(link)

# share_link = "https://v.douyin.com/e418Xn4/"
# loop = asyncio.get_event_loop()
# loop.run_until_complete(dylink(share_link))
