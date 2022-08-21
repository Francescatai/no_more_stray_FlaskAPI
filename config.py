import os
from datetime import timedelta

# 項目根目錄:當前檔案所在的file
BASE_DIR = os.path.dirname(__file__)

# 數據庫配置
DB_USERNAME = 'root'
DB_PASSWORD = 'root'
DB_HOST = 'localhost'
DB_PORT = '3306'
DB_NAME = 'nomorestray'

DB_URI = 'mysql+pymysql://%s:%s@%s:%s/%s?charset=utf8' % (DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)

SQLALCHEMY_DATABASE_URI = DB_URI
# 是否需要跟蹤修改
SQLALCHEMY_TRACK_MODIFICATIONS = False

# btdgaukzxiwjsnsq
# MAIL_USE_TLS：587
# MAIL_USE_SSL：465

# 發送email的服務器配置
MAIL_SERVER = "smtp.gmail.com"
MAIL_PORT = 465
# MAIL_USE_TLS = True
MAIL_USE_SSL = True
MAIL_USERNAME = "evelyndatalearning@gmail.com"
MAIL_PASSWORD = "btdgaukzxiwjsnsq"
MAIL_DEFAULT_SENDER = "evelyndatalearning@gmail.com"

# redis-server.exe redis.windows.conf
# pip install redis
# pip install gevent
# celery -A app.celery worker --loglevel=info -P gevent
# Celery的redis設定
CELERY_BROKER_URL = "redis://127.0.0.1:6379/0"
CELERY_RESULT_BACKEND = "redis://127.0.0.1:6379/0"

# Flask-Caching的設定
CACHE_TYPE = "RedisCache"
CACHE_DEFAULT_TIMEOUT = 300
CACHE_REDIS_HOST = "127.0.0.1"
CACHE_REDIS_PORT = 6379

# csrf token設置
SECRET_KEY = os.urandom(24)

# session.permanent=True的情况下的過期時間
PERMANENT_SESSION_LIFETIME = timedelta(days=7)

# 頭像設定
AVATARS_SAVE_PATH = os.path.join(BASE_DIR, "media", "avatars")

# 每頁展示文章的數量
PER_PAGE_COUNT = 10
