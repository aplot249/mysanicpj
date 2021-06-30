#@author: sareeliu
#@date: 2021/6/21 13:51
import sanic,re,pathlib
from sanic.response import json,empty
from sanic.exceptions import NotFound
from sanic_cors import CORS
from sanic.websocket import WebSocketProtocol
import asyncio,aiohttp
from lxml import etree
from mycos import client
from vxpdf import VXUrl2Pdf
from async_sendemail import send_email

app = sanic.Sanic(name="index")
CORS(app)

def task_handle(vxlink):
    vxpdf = VXUrl2Pdf(url=vxlink)
    vxpdf.makepdf()
    try:
        Bucket = 'vxfile'
        LocalFilePath = vxpdf.abs_pdfname
        Key = pathlib.Path(LocalFilePath).name
        print(LocalFilePath,Key)
        res = client.put_object_from_local_file( Bucket, LocalFilePath, Key)
        print(res)
        return {'status':'success',"name":vxpdf.title}
    except:
        return {'status':'fail',"name":vxpdf.title}

@app.websocket('/feed')
async def feed(request, ws):
    vxlink = request.args['vx'][0]
    print("vxlink为"+str(vxlink))
    try:
        re.match('https://mp.weixin.qq.com/s/(\w+)',vxlink).group()
    except:
        await ws.send("下载失败【链接错误】")
        return False
    # data = await ws.recv()
    # print('收到数据: ' + data)
    await ws.send("提交成功,开始下载...")
    loop = asyncio.get_event_loop()
    # requests模块默认不支持异步操作，所以就使用线程池来配合实现了。
    future = loop.run_in_executor(None, task_handle, vxlink)
    response = await future
    if response['status'] == 'success':
        await ws.send("下载成功【"+str(response['name'])+"】")
    else:
        await ws.send("下载失败【"+str(response['name'])+"】")

@app.get("/vpnsoftware")
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

@app.post('/email')
async def email(request):
    toemail = request.form['toemail'][0]
    title = request.form['title'][0]
    content = request.form['content'][0]
    print(toemail,title,content)
    app.add_task(send_email(toemail,title,content))
    return json(request.form)

@app.get('/expire')
async def expire(request):
    async with aiohttp.ClientSession() as session:
        response = await session.get("https://chuanyun101.com/jhsfq/check_expired/")
        res =await response.text()
        print(res)
        import json as myjson
        res_dict = myjson.loads(res)
        for item in res_dict['expired']:
            toemail = item['email']
            title = '穿云101账号已经到期'
            content = '您在网站 http://chuanyun101.com 的外网账号已经到期，如需继续使用，请联系管理员续费。'
            app.add_task(send_email(toemail, title, content))
            asyncio.sleep(30)
        for item in res_dict["will_expired"]:
            toemail = item['email']
            title = '穿云101账号将要到期'
            content = '您在网站 http://chuanyun101.com 的外网账号还有%s天期限，到期将不能使用，请及时续费。' % item['remaining_days']
            app.add_task(send_email(toemail, title, content))
            asyncio.sleep(30)
        return json(res)


if __name__ == "__main__":
    app.error_handler.add(NotFound,lambda r, e: empty(status=404))
    app.run(host='127.0.0.1', port=8008,protocol=WebSocketProtocol,auto_reload=True)