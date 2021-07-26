# 并行工作进程数
workers = 2
#自启动
reload = True
# 指定每个工作者的线程数
threads = 2
# 监听内网端口
bind = '0.0.0.0:8008'
# 设置守护进程,将进程交给supervisor管理
daemon = True
# 工作模式协程
worker_class = 'sanic.worker.GunicornWorker'
# 设置最大并发量
worker_connections = 2000
# 设置进程文件目录
pidfile = '/home/mysanicpj/pid.gunicorn'
# 设置访问日志和错误信息日志路
accesslog = '/home/mysanicpj/access.log'
errorlog = '/home/mysanicpj/error.log'
# 设置日志记录水平
# loglevel = 'warning'