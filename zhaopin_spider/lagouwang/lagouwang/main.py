from scrapy import cmdline
cmdline.execute('scrapy crawl lagou'.split())

# import os
# os.chdir('spiders')
# cmdline.execute('scrapy runspider lagou.py'.split())