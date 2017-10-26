# -*- coding: utf-8 -*-

# Scrapy settings for lagouwang project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'lagouwang'

SPIDER_MODULES = ['lagouwang.spiders']
NEWSPIDER_MODULE = 'lagouwang.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'truelove (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 10

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 0.3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 100
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language':'zh-CN,zh;q=0.8',
    'Cache-Control':'max-age=0',
    'Connection':'keep-alive',
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
    'Cookie':'LGUID=20171011200319-2bee2600-ae7c-11e7-94b3-5254005c3644; user_trace_token=20171011200323-11be00ff-f82b-4fc7-904e-0165469ba3eb; index_location_city=%E5%8C%97%E4%BA%AC; SEARCH_ID=6db5d2eba4d342faba6fab5b7ee00773; JSESSIONID=ABAAABAABEEAAJA89E72E802C2942257D0BB634F77BDB43; ab_test_random_num=0; X_HTTP_TOKEN=870c4f1f69dc047fd39768b32ecd275b; _ga=GA1.2.1147005544.1507723387; _gid=GA1.2.863770894.1508487710; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1508143069,1508487709,1508564738,1508639203; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1508641049; LGSID=20171022102652-775b1499-b6d0-11e7-95f4-5254005c3644; LGRID=20171022105729-bdf3bdb7-b6d4-11e7-95f4-5254005c3644; _putrc=6D41DA4A03DDBD36; login=true; unick=%E7%8E%8B%E8%B6%85%E5%87%A1; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=0',
}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'truelove.middlewares.TrueloveSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'truelove.middlewares.MyCustomDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html

ITEM_PIPELINES = {
    #'lagouwang.pipelines.LagouwangPipeline': 1,
    'scrapy_redis.pipelines.RedisPipeline': 999,  # 数据统一存到redis服务器上的 管道文件
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

USER_AGENS = [
    'Mozilla/5.0 (compatible; WOW64; MSIE 10.0; Windows NT 6.2)',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A334 Safari/7534.48.3'
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows Phone OS 7.0; Trident/3.1; IEMobile/7.0; LG; GW910)'
    'Mozilla/5.0 (iPhone; CPU iPhone OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A334 Safari/7534.48.3'
]
'''
#mysql连接属性
MYHOST = '192.168.2.120'
# MYUSER = 'centos4'
MYUSER = 'root'
MYPASSWORD = '123456'
MYDB = 'zhilian'
'''
# ---------------------------------scrapy-redis-----------------------------------
# url 过滤 用scrapy_redis
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"

# 调度器改成 scrapy-redis 调度器
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
# 可以暂停
SCHEDULER_PERSIST = True

# 请求队列模式
SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderPriorityQueue" # 优先级
# SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderQueue"  # 队列
# SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderStack"  # 栈  先进后出

# LOG_LEVEL = 'DEBUG'
# redis服务器的 ip地址和端口号
#REDIS_HOST = '192.168.6.6'
REDIS_HOST = '192.168.2.120'
#REDIS_HOST = '10.11.9.128'
#REDIS_HOST = '192.168.2.218'
REDIS_PORT = 6379

# 定义redis连接信息，如果定义redis_url 则redis_host 不生效
REDIS_URL = 'redis://:@192.168.2.120:6379/1'    # 最后2 是指定数据库索引
#rediscli = redis.StrictRedis(host='192.168.6.6', port=6379, db=2, password='123')
