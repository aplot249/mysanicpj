#@author: sareeliu
#@date: 2021/6/21 14:24

from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client


CONFIG = {
    'SecretId': 'AKIDiCZpsgQORuCG5ey2tc9SpyrV5A6lhltl',      # 替换为用户的 secretId(登录访问管理控制台获取)
    'SecretKey': 'mYCcleJxMVXLn2IKGwdHvJQHuGKNhcHf',      # 替换为用户的 secretKey(登录访问管理控制台获取)
    'Region': 'ap-hongkong',     # 替换为用户的 Region
    'Appid': '1253665887'
}
client = CosS3Client(CosConfig(**CONFIG))
