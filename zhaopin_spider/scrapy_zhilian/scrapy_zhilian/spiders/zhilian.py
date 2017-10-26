# -*- coding: utf-8 -*-
import scrapy
import re
import time
import hashlib
from scrapy_zhilian.items import ScrapyZhilianItem
from scrapy_redis.spiders import RedisSpider
# 导入redis包

#class ZhilianSpider(scrapy.Spider):
class ZhilianSpider(RedisSpider):
    name = 'zhilian'
    redis_key = 'zhilian:start_urls'
    allowed_domains = ['zhaopin.com']
    # start_urls = ['http://sou.zhaopin.com/']
    headers = {
        # 'Host': 'jobs.zhaopin.com',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8',
    }
    # 分布式爬虫 使用parse
    def parse(self,response):
        # start_url = "http://sou.zhaopin.com/jobs/searchresult.ashx"
        # 起始请求获取相应检索条件
        start_url = "http://sou.zhaopin.com/assets/javascript/basedata.js?v=20170823"
        yield scrapy.Request(url=start_url,callback=self.parse_start,headers=self.headers)

    '''
    http://sou.zhaopin.com/jobs/searchresult.ashx?jl=城市&isadv=0&ct=公司性质&isfilter=1&p=1&et=职位类型&el=学历
    页数：p
    职位类型et：不限：et=-1
                全职：et=2
                兼职：et=1
                实习：et=4
                校园：et=5
    公司性质：ct ：-1 到 16
    学历：el   ：-1，-2，1，3,4,5,7,8
    '''
    # 解析城市等信息接口，组装完整的搜索url
    def parse_start(self, response):
        # 获取城市
        # print response.body
        info = response.body
        # print info

        # 第一次 获取 var dCity 后面的城市信息 ID+城市
        pattern = re.compile(r"var dCity = '(.*?)0@';")
        city_info = pattern.findall(info)
        city_info2 = city_info[0].decode("utf-8")
        # 第二次获取中文字段的城市(unicode格式)
        chn = re.compile(ur'[\u4e00-\u9fa5]+')
        city_list = chn.findall(city_info2)
        citys = []
        for city in city_list:
            city = city.encode("utf-8")
            citys.append(city)
        # 排除掉的省
        sheng= ['全国','广东','湖北','陕西','四川','辽宁','吉林','江苏','山东','浙江','广西','安徽','河北','山西','内蒙','黑龙江','福建','江西','河南','湖南','海南','贵州','云南','西藏','甘肃','青海','宁夏','新疆']
        s = set(sheng)
        citys = set(citys)
        # 存 放城市 ,对称差集更新操作
        citys.symmetric_difference_update(s)
        # 最终获取筛选出来的城市
        city_list = list(citys)
        # print city_list
        # 公司性质
        companyNO_ct = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
        # 学历
        educationNO_el = [-1,1,3,4,5,7,8]
        # 职位类型
        positioinNO_et = [1,2,4,5]
        base_url = "http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%s&isadv=0&ct=%s&isfilter=1&et=%s&el=%s"
        i = 0
        for city in city_list:
            for ct in companyNO_ct:
                for et in positioinNO_et:
                    for el in educationNO_el:
                        # # 翻页
                        # for page in range(1,91):
                            #print city+"  下面的:"+"公司类型"+str(ct)+"学历"+str(el)+"职位类型"+str(et)
                            #full_url = base_url % (city,str(ct),str(page),str(et),str(el))
                        full_url = base_url % (city,str(ct),str(et),str(el))
                        i+=1
                        #print i,full_url
                        yield scrapy.Request(full_url, callback=self.parse_list, headers=self.headers, priority=1)

    # 解析列表
    def parse_list(self,response):
        print '根据条件 进入列表页 首页',"response_url:",response.url
        # 获取当前招聘详情的url列表
        recruit_url = response.xpath('//div[@class="newlist_list_content"]//td[@class="zwmc"]//a/@href').extract()
        for url in recruit_url:
            # 筛选排除校园招聘 的url
            if 'jobs.zhaopin.com' in url:
                # print '详情招聘页链接:',url
                # 请求详情页信息
                yield scrapy.Request(url,callback=self.parse_detail,headers=self.headers, priority=2)
        # 获取下一页是否存在url
        next_page = response.xpath('//div[@class="pagesDown"]//li/a[@class="next-page"]/@href').extract()
        # 有下一页分页，再次请求当前parse_list方法请求，再次解析（递归，知道 没有下一页为止）
        if next_page:
            print "下一页url：",next_page[0]
            yield scrapy.Request(next_page[0],callback=self.parse_list,headers=self.headers)
    # 详情页解析
    def parse_detail(self,response):
        print '进入详情解析页'
        item = ScrapyZhilianItem()
        #html = response.body.decode('utf-8')
        #print html
        name = response.xpath('//div[@class="bread_crumbs"]//a[3]/strong/text()')[0].extract().encode('utf-8')
        # 公司福利
        welfare_list = response.xpath('//div[@class="fixed-inner-box"]//span/text()').extract()
        welfare = " ".join(welfare_list).encode("utf-8")

        left_info = response.xpath('//div[@class="terminalpage-left"]')
        for i in left_info:
            salary = i.xpath('.//ul/li[1]/strong/text()')[0].extract().encode('utf-8') # 薪资

            area_city = i.xpath('./ul/li[2]/strong/a/text()').extract()[0].encode('utf-8') # 工作区域_市
            area_qu = i.xpath('./ul/li[2]/strong/text()').extract() # 工作区域_区
            area_qu = self.getVal(area_qu)
            if area_qu !="":
                area_qu = area_qu[0].encode("utf-8")
            area = area_city+area_qu   # 完整的工作区域

            exp = i.xpath('.//ul/li[5]/strong/text()')[0].extract().encode('utf-8') # 经验
            edu = i.xpath('.//ul/li[6]/strong/text()')[0].extract().encode('utf-8') # 学历
            num = i.xpath('.//ul/li[7]/strong/text()')[0].extract().encode('utf-8') # 人数
            time = i.xpath('.//ul/li[3]/strong/span/text()')[0].extract().encode('utf-8') # 发布日期：

        local = response.xpath('//div[@class="tab-inner-cont"]//h2/text()')[0].extract().encode('utf-8') # 工作地点 去换行
        local = local.replace('\n','').strip()

        info = response.xpath('//div[@class="tab-inner-cont"]//p/text()').extract()
        # info = '\n'.join(info).encode('utf-8').replace('\n','').strip()  #转了utf-8
        info = '\n'.join(info).replace('\n','').strip()
        print info
        co_name = response.xpath('//div[@class="terminalpage-right"]//p[@class="company-name-t"]//a/text()')[0].extract().encode('utf-8') # 公司名称
        co_type = response.xpath('//div[@class="terminalpage-right"]//ul/li[2]/strong/text()')[0].extract().encode('utf-8') # 公司类别(公司性质)
        '''
        li_count = response.xpath('//div[@class="terminalpage-right"]//ul/li')[0].extract()
        # co_url = response.xpath('//div[@class="terminalpage-right"]//div[@class="company-box"]//ul/li[4]/strong/a/@href').extract()[0]
        # 有五个li，有网址
        co_url = ""
        i = len(li_count)
        if i == 5:
            # print response.body.decode('utf-8')
            # 公司链接 href为空
            co_url = response.xpath('//ul[@class="terminal-ul clearfix terminal-company mt20"]/li[4]/strong/a/text()')[0].extract()
        else:
            co_url = "该公司没有网站"
        '''
        co_url = response.xpath('//div[@class="terminalpage-right"]//p[@class="company-name-t"]//a/@href')[0].extract().encode('utf-8') # 该公司在智联上的介绍url
        # print co_url
        # 封装item
        item['name'] = name
        item['welfare'] = welfare
        item['salary'] = salary
        item['area'] = area
        item['exp'] = exp
        item['edu'] = edu
        item['num'] = num
        item['time'] = time
        item['local'] = local
        item['info'] = info
        item['co_name'] = co_name
        item['co_type'] = co_type
        item['co_url'] = self.md5(co_url)

        return item

    def getVal(self,data):
        return data if data else ''
    def md5(self,data):
        m = hashlib.md5()
        m.update(data)
        return m.hexdigest()