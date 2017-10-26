from scrapy import cmdline
# cmdline.execute('scrapy crawl zhilian'.split())

import os
os.chdir('./spiders')
cmdline.execute('scarpy runspider zhilian.py'.split())