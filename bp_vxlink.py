#@author: sareeliu
#@date: 2021/6/30 10:50
from sanic import Blueprint
import pathlib,asyncio,re

from utils.mycos import client
from utils.vxpdf import VXUrl2Pdf

bp_vxlink = Blueprint("bp_vxlink", url_prefix="vxlink")

# 1、pdf转换
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


# api/vxlink/feed
# vxlink提交
@bp_vxlink.websocket('/feed')
async def feed(request, ws):
    vxlink = request.args.get('vx')
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

