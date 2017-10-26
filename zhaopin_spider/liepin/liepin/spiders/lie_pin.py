# -*- coding: utf-8 -*-
import scrapy
from liepin.industries import industries
from liepin.city import city
from liepin.items import LiepinItem
from scrapy_redis.spiders import RedisSpider

class LiePinSpider(RedisSpider):
    name = 'lie_pin'
    allowed_domains = ['liepin.com']
    redis_key = 'liepin:start_url'

    #行业类别列表
    indusList = industries()

    #城市类别列表
    cityList = city()

    #薪资类别列表
    salaList = ['10$15','15$20','20$30','30$50','50$100','100$999']

    #企业规模类别列表
    sclaList = ['010','020','030','040','050','060','070','080']

    #生成基于 不同行业,城市,薪资,规模的第一页请求
    def parse(self, response):
        base_url = 'https://www.liepin.com/zhaopin/?&fromSearchBtn=2&ckid=3ff03f8bf33c6fa6&d_=&&sfrom=click-pc_homepage-centre_searchbox-search_new&init=-1&dqs=%s&industryType=&&&degradeFlag=0&industries=%s&salary=%s&compscale=%s&&&key=&headckid=868e6dec6ba02432&d_pageSize=40&siTag=1B2M2Y8AsgTpgAmY7PhCfg~HjSmCnkUpSjgS7HPdUS6mw&d_headId=e9694c6e8bfe655bfb1a281091ef8886&d_ckId=f186d69a3499a961e77eb21f0be617b0&d_sfrom=search_fp&d_&curPage=0'
        for indusId in self.indusList:
            for cityId in self.cityList:
                for salaId in self.salaList:
                    for sclaId in self.sclaList:
                        full_url = base_url % (cityId,indusId,salaId,sclaId)
                        yield scrapy.Request(full_url,callback=self.first_parse)

    #提取第一页职位url,如果有下一页,将下一页加入请求
    def first_parse(self, response):
        #职位链接列表
        posi_list = response.xpath('//div[@class="sojob-result "]//div[@class="job-info"]/h3/a/@href').extract()
        if posi_list:
            for posi in posi_list:
                if 'www.liepin' not in posi:
                    posi = 'https://www.liepin.com' + posi
                yield scrapy.Request(posi,callback=self.detail_parse)
            # 第一种:通过寻找下一页链接,循环每一页
            # next_page = response.xpath('//div[@class="sojob-result "]//div[@class="pagerbar"]/a[last()-1]/@href').extract()
            # if next_page and 'javascript:;' not in next_page:
            #     nextPage = 'https://www.liepin.com' + next_page[0]
            #     print 'next:' + nextPage
            #     yield scrapy.Request(nextPage,callback=self.first_parse)

            # 第二种:通过寻找尾页页码,循环此页码生成每一页请求
            last_page = response.xpath('//div[@class="sojob-result "]//div[@class="pagerbar"]/a[last()]/@href').extract()
            if 'javascript:;' not in last_page:
                pageNum = int(last_page[0].split('=').pop())
                for num in range(1,pageNum+1):
                    next_page = response.url.replace('curPage=0','curPage=' + str(num))
                    yield scrapy.Request(next_page,callback=self.second_parse)

    #处理大于1的页码页面
    def second_parse(self,response):
        #职位链接列表
        posi_list = response.xpath('//div[@class="sojob-result "]//div[@class="job-info"]/h3/a/@href').extract()
        if posi_list:
            for posi in posi_list:
                if 'www.liepin' not in posi:
                    posi = 'https://www.liepin.com' + posi
                yield scrapy.Request(posi,callback=self.detail_parse)


    #职位详情页处理
    def detail_parse(self,response):
        panduan = lambda x:x[0] if x else 'unknown'
        job = LiepinItem()
        #如果是'/a/'类型网页
        if '/a/' in response.url:
            #职位名称
            job['name'] = response.xpath('//div[@class="title-info"]/h1/text() | //div[@class="title-info "]/h1/text()').extract()[0]
            #公司名称
            job['co_name'] = response.xpath('//div[@class="title-info"]/h3/text() | //div[@class="title-info "]/h3/text()').extract()[0].strip()
            #区域
            job['area'] = response.xpath('//div[@class="title"]//p[@class="basic-infor"]/span/text()').extract()[0]
            #薪资
            job['salary'] = response.xpath('//div[@class="title"]//p[@class="job-main-title"]/text()').extract()[0].strip()
            #经验
            job['exp'] = response.xpath('//div[@class="resume clearfix"]/span[2]/text()').extract()[0]
            #学历
            job['edu'] = response.xpath('//div[@class="resume clearfix"]/span[1]/text()').extract()[0]
            #招聘人数
            job['num'] = 'unknown'
            #发布时间
            job['time'] = response.xpath('//div[@class="job-title-left"]/p/time/text()').extract()[0].strip()
            #其他要求
            otherqlist = response.xpath('//div[@class="resume clearfix"]/span[position()>2]/text()').extract()
            job['otherq'] = ','.join(otherqlist)
            #福利
            fulis = []
            fuliList = response.xpath('//div[@class="job-main main-message"][3]//ul/li')
            for fuli in fuliList:
                fulis.append(fuli.xpath('./span/text()').extract()[0] + ':' +fuli.xpath('./text()').extract()[0])
            job['welfare'] = ','.join(fulis)
            #职位信息
            infolist = response.xpath('//div[@class="job-main main-message"][1]/div[@class="content content-word"]/text()').extract()
            job['info'] = ' '.join(infolist)
            #上班地址
            job['local'] = 'unknown'
            #公司网址
            job['co_url'] = 'unknown'
            #公司类别
            job['co_type'] = response.xpath('//div[@class="job-main main-message"][2]//ul/li[5]/text()').extract()[0]
        #如果是 '/job/'类型网页
        elif '/job/' in response.url:
            #职位名称
            job['name'] = response.xpath('//div[@class="title-info"]/h1/text()').extract()[0]
            #公司名称
            job['co_name'] = response.xpath('//div[@class="title-info"]/h3/a/text()').extract()[0].strip()
            #区域
            job['area'] = response.xpath('//div[@class="job-item"]//p[@class="basic-infor"]/span/a/text()').extract()[0]
            #薪资
            job['salary'] = response.xpath('//div[@class="job-item"]//p[@class="job-item-title"]//text()').extract()[0].strip()
            #经验
            job['exp'] = response.xpath('//div[@class="job-qualifications"]/span[2]/text()').extract()[0]
            #学历
            job['edu'] = response.xpath('//div[@class="job-qualifications"]/span[1]/text()').extract()[0]
            #招聘人数
            job['num'] = 'unknown'
            #发布时间
            job['time'] = response.xpath('//div[@class="job-title-left"]/p/time/text()').extract()[0].strip()
            #其他要求
            otherqlist = response.xpath('//div[@class="job-qualifications"]/span[position()>2]/text()').extract()
            job['otherq'] = ','.join(otherqlist)
            #福利
            welist = response.xpath('//div[@class="tag-list"]/span/text()').extract()
            job['welfare'] = ','.join(welist)
            #职位信息
            infolist = response.xpath('//div[@class="content content-word"]//text()').extract()
            job['info'] = ' '.join(infolist)
            #上班地址
            job['local'] = response.xpath('//div[@class="company-infor"]//ul[@class="new-compintro"]//li[3]//text()').extract()[0].split('：'.decode('utf8')).pop()
            #公司网址
            job['co_url'] = response.xpath('//div[@class="company-infor"]//div[@class="company-logo"]//p/a/@href').extract()[0]
            #公司类型
            if response.xpath('//ul[@class="new-compintro"]/li[1]/a/text()').extract():
                job['co_type'] = response.xpath('//ul[@class="new-compintro"]/li[1]/a/text()').extract()[0]
            else:
                job['co_type'] = response.xpath('//ul[@class="new-compintro"]/li[1]/text()').extract()[0]
        #如果是'/cjob/'网页
        else:
            #职位名称
            job['name'] = response.xpath('//div[@class="job-title"]/h1/text()').extract()[0]
            #公司名称
            job['co_name'] = response.xpath('//div[@class="job-title"]/h2/text()').extract()[0]
            #区域
            job['area'] = response.xpath('//div[@class="job-main"]/p[@class="job-main-tip"]/span[1]/text()[2]').extract()[0]
            #薪资
            job['salary'] = response.xpath('//div[@class="job-main"]/div[@class="job-main-title"]/strong/text()').extract()[0]
            #经验
            job['exp'] = panduan(response.xpath('//div[@class="job-main"]/p[@class="job-qualifications"]/span[2]/text()').extract())
            #学历
            job['edu'] = panduan(response.xpath('//div[@class="job-main"]/p[@class="job-qualifications"]/span[1]/text()').extract())
            #招聘人数
            job['num'] = 'unknown'
            #发布时间
            job['time'] = response.xpath('//p[@class="job-main-tip"]/span[2]/text()').extract()[0].strip()
            #其他要求
            job['otherq'] = 'unknown'
            #福利
            wellist = panduan(response.xpath('//p[@class="job-labels"]/span/text()').extract())
            job['welfare'] = ','.join(wellist)
            #职位信息
            job['info'] = response.xpath('//div[@class="job-info"]//div[@class="job-info-content"]/text()').extract()[0].strip()
            #上班地址
            job['local'] = response.xpath('//div[@class="side-box right-post-map"]/div[@class="side-content"]/p/text()').extract()[0]
            #公司网址
            job['co_url'] = 'unknown'
            #公司类型
            job['co_type'] = 'unknown'
        yield job
        # #职位名称
        # print job['name']
        # #公司名称
        # print job['co_name']
        # #区域
        # print job['area']
        # #薪资
        # print job['salary']
        # #经验
        # print job['exp']
        # #学历
        # print job['edu']
        # #招聘人数
        # print job['num']
        # #发布时间
        # print job['time']
        # #其他要求
        # print job['otherq']
        # #福利
        # print job['welfare']
        # #职位信息
        # print job['info']
        # #上班地址
        # print job['local']
        # #公司网址
        # print job['co_url']
        # #公司类型
        # print job['co_type']


