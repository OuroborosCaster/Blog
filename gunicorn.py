import os

daemon = True
bind = '0.0.0.0:8000'
pidfile = './gunicorn.pid'
chdir = './'
worker_class = 'uvicorn.workers.UvicornWorker'
workers = 3
threads = 2
worker_connections = 2000
loglevel = 'debug'
log_dir = "logs"

if not os.path.exists(log_dir):
    os.makedirs(log_dir)

accesslog = "./log/gunicorn_access.log"
errorlog = "./log/gunicorn_error.log"
