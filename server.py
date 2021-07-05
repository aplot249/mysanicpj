#@author: sareeliu
#@date: 2021/6/21 13:51
import sanic
from sanic.response import empty
from sanic.exceptions import NotFound
from sanic_cors import CORS
from sanic.websocket import WebSocketProtocol
from sanic import Blueprint

from bp_email import bp_email
from bp_vpn import bp_vpn
from bp_vxlink import bp_vxlink
from bp_douyin import bp_douyin
from bp_cableav import bp_cableav
from bp_i159 import bp_159i

app = sanic.Sanic(name="index")
CORS(app)

api = Blueprint.group(bp_email,bp_vpn,bp_vxlink,bp_douyin,bp_cableav,bp_159i,url_prefix='api')
app.blueprint(api)

if __name__ == "__main__":
    app.error_handler.add(NotFound,lambda r, e: empty(status=404))
    app.run(host='127.0.0.1', port=8008,protocol=WebSocketProtocol,auto_reload=True)