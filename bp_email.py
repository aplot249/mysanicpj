#@author: sareeliu
#@date: 2021/6/30 10:53
import aiohttp,asyncio
from sanic.response import json
from sanic import Blueprint
from utils.async_sendemail import send_email
from sanic import Sanic
import json as myjson

bp_email = Blueprint("bp_email", url_prefix="email")

# api/email/register
# 3、发送注册邮件
@bp_email.post('/register')
async def register_email(request):
    toemail = request.form['toemail'][0]
    title = request.form['title'][0]
    content = request.form['content'][0]
    print(toemail,title,content)
    app = Sanic.get_app()
    app.add_task(send_email(toemail,title,content))
    return json(request.form)

# 发送账号过期邮件
async def send_expire_email(res_dict):
    for item in res_dict['expired']:
        toemail = item['email']
        title = '穿云101账号已经到期'
        content = '您在网站 http://chuanyun101.com 的外网账号已经到期，如需继续使用，请联系管理员续费。'
        app = Sanic.get_app()
        app.add_task(send_email(toemail, title, content))
        await asyncio.sleep(61)
    for item in res_dict["will_expired"]:
        toemail = item['email']
        title = '穿云101账号将要到期'
        content = '您在网站 http://chuanyun101.com 的外网账号还有%s天期限，到期将不能使用，请及时续费。' % item['remaining_days']
        app = Sanic.get_app()
        app.add_task(send_email(toemail, title, content))
        await asyncio.sleep(61)

# api/email/expire
# 获取账号过期数据
@bp_email.get('/expire')
async def expire_email(request):
    async with aiohttp.ClientSession() as session:
        response = await session.get("https://chuanyun101.com/jhsfq/check_expired/")
        res = await response.text()
        print(res)
        res_dict = myjson.loads(res)
        app = Sanic.get_app()
        app.add_task(send_expire_email(res_dict))
        return json(res)
