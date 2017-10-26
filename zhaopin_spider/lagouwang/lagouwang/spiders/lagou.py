# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from lagouwang.items import LagouwangItem
from scrapy_redis.spiders import RedisCrawlSpider


class LagouSpider(RedisCrawlSpider):
    name = 'lagou'
    redis_key = 'lagou:start_urls'
    allowed_domains = ['lagou.com']
    # start_urls = ['https://www.lagou.com']

    rules = (
        Rule(LinkExtractor(allow=("zhaopin/.*",)),follow=True,),
        Rule(LinkExtractor(allow=("gongsi/j\d+.html",)),follow=True),
        Rule(LinkExtractor(allow=r'jobs/\d+.html'), callback='parse_item', follow=True),
    )


    def parse_item(self, response):
        item = LagouwangItem()
        htmls = response.body
        if '已下线' not in htmls:
            # 公司名称
            co_name = response.xpath("//div[@class='company']/text()").extract()[0].encode('utf-8')
            # 职位名称
            name = response.xpath("//div[@class='job-name']/span/text()").extract()[0].encode('utf-8')
            # 薪资
            salary = response.xpath("//dd[@class='job_request']//span[1]/text()").extract()[0].encode('utf-8')
            # 区域
            area = response.xpath("//dd[@class='job_request']//span[2]/text()").extract()[0].encode('utf-8').replace('/','')
            # 工作年限
            exp = response.xpath("//dd[@class='job_request']//span[3]/text()").extract()[0].encode('utf-8').replace('/','')
            # 学历
            edu = response.xpath("//dd[@class='job_request']//span[4]/text()").extract()[0].encode('utf-8').replace('/','')
            # 发布时间
            time = response.xpath("//p[@class='publish_time']/text()").extract()[0].split(' ')[0]
            time = self.getVal(time)
            # 职位描述
            info = response.xpath("//dd[@class='job_bt']//p/text()").extract()
            info = self.getVal(info)
            if info != '':
                info =   '\n'.join(info).encode('utf-8')

            # 工作地点
            local = ','.join(response.xpath("//div[@class='work_addr']/a/text()").extract()[:-1]).encode('utf-8')
            # 公司福利
            welfare = response.xpath('//dd[@class="job-advantage"]//p/text()').extract()[0].encode('utf-8')
            # 公司网址
            co_url = response.xpath('//dl[@id="job_company"]//li/a/@href').extract()[0].encode('utf-8')
            # 招聘人数
            num = '0'
            # 公司类别
            co_type = response.xpath('//dl[@id="job_company"]//li[1]/text()').extract()[1].encode('utf-8')
            print name,co_name,area,salary,exp,edu,num,time,welfare,info,local,co_url,co_type
            item['name'] = name
            item['co_name'] = co_name
            item['area'] = area
            item['salary'] = salary
            item['exp'] = exp
            item['edu'] = edu
            item['num'] = num
            item['time'] = time
            item['welfare'] = welfare
            item['info'] = info
            item['local'] = local
            item['co_url'] = co_url
            item['co_type'] = co_type


            yield item
            print item

    def getVal(self,data):
            return data if data else ''