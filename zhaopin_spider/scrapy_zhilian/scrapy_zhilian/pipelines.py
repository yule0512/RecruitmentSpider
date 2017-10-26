# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class ScrapyZhilianPipeline(object):
    def process_item(self, item, spider):
        item['spider_name'] = spider.name

        print item['spider_name'],item['name']
        return item
