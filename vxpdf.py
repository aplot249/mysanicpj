#@author: sareeliu
#@date: 2021/3/22 17:09
import os,requests,re
import pdfkit,wechatsogou


class VXUrl2Pdf:

    def __init__(self,url):
        self.title = ''
        self.abs_pdfname = ''
        self.ws_api = wechatsogou.WechatSogouAPI()  #captcha_break_time=3
        self.url = url

    def get_title(self):
        html = requests.get(self.url)
        self.title = re.search('<meta property="og:title" content="(.*?)" />', html.text[:3000]).group(1)
        return self.title

    def get_abs_pdfname(self):
        dir_abs = r"微信公众号文章"
        if not os.path.exists(dir_abs):
            os.mkdir(dir_abs)
        self.abs_pdfname = os.path.join(dir_abs, self.title)+".pdf"
        return self.abs_pdfname

    def get_content(self):
        try:
            content_info = self.ws_api.get_article_content(self.url)['content_html']
            html = f'''
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <title>{self.title}</title>
            </head>
            <body>
            <h2 style="text-align: center;font-weight: 400;">{self.title}</h2>
            {content_info}
            </body>
            </html>
            '''
            return html
        except:
            return None

    def makepdf(self):
        self.get_title()
        self.get_abs_pdfname()
        pdfkit.from_string(self.get_content(), self.abs_pdfname)


if __name__ == '__main__':
    vxpdf = VXUrl2Pdf(url='')
    vxpdf.makepdf()
