#@author: sareeliu
#@date: 2021/7/2 10:24
import requests
from utils.vxpdf import VXUrl2Pdf

response = requests.get("https://mp.weixin.qq.com/s/SH3LBCNFnPuU9x_Q3g0I0Q")
# print(response.text)

vxurl2pdf = VXUrl2Pdf("https://mp.weixin.qq.com/s/SH3LBCNFnPuU9x_Q3g0I0Q")
print(vxurl2pdf.get_title())
print(vxurl2pdf.ws_api.get_article_content("https://mp.weixin.qq.com/s/SH3LBCNFnPuU9x_Q3g0I0Q")['content_html'])