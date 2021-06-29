#@author: sareeliu
#@date: 2021/6/24 20:45
import aiohttp
import asyncio
import re

async def douyin(share_link):
    async with aiohttp.ClientSession() as session:
        headers = {
            'User-Agent':"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
        }
        response = await session.get(f"https://ouotool.com/dy?url={share_link}",headers=headers)
        res = await response.text()
        # print(res)
        link = re.search('<source src="(?P<link>.*?)"type="video/mp4">',res).group('link')
        print(link)


share_link = "https://v.douyin.com/e418Xn4/"
loop = asyncio.get_event_loop()
loop.run_until_complete(douyin(share_link))
