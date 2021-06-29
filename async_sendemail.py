#@author: sareeliu
#@date: 2021/6/29 10:37
import aiohttp,asyncio

async def send_email(toemail,title,content):
    async with aiohttp.ClientSession() as session:
        authority_list = [
                        ('email101', 'js1LkBog8OfQ87as'),   #jiche
                        ('iemail', '6aaacf44d3dcef0951e3013390b8e985'), #kuiying
                        ('expire', 's0LtARyPryp607fL'),     #3232584441
                    ]
        for item in authority_list:
            data = {
                "apiUser": item[0],    # 使用api_user和api_key进行验证
                "apiKey": item[1],
                "to": toemail,            # 收件人地址, 用正确邮件地址替代, 多个地址用';'分隔
                "from": "email@chuanyun101.com",   # 发信人, 用正确邮件地址替代
                "fromName": "chuanyun101.com",
                "subject": title,
                "html": content
            }
            response = await session.post("http://api.sendcloud.net/apiv2/mail/send",data=data)
            res = await response.json()
            print(res['message'])
            if res['message'] == "请求成功":
                break


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(send_email("1010351486@qq.com", "这是标题", "这是我的内容"))