# -*- coding: utf-8 -*-
import scrapy
from coolscrapy.items import CoolscrapyItem
import sys


class HuxiuSpider(scrapy.Spider):
    name = 'huxiu'
    allowed_domains = ['www.huxiu.com']
    start_urls = ['http://www.huxiu.com/']

    def parse(self, response):
        for sel in response.xpath('//div[@class="mob-ctt"]'):
            item = CoolscrapyItem()     #有这个就不用yield了
            item['title'] = sel.xpath('h2/a/text()')[0].extract()
            item['link'] = sel.xpath('h2/a/@href')[0].extract()
            url = response.urljoin(item['link'])
            item['desc'] = sel.xpath('div[@class="mob-sub"]/text()').extract_first()
            # print item['title'] ,item['link'] ,item['desc']
            yield scrapy.Request(url, callback=self.parse_article)  #找到自己想要的链接再进行处理
    def parse_article(self, response):
        detail = response.xpath('//div[@class="article-wrap"]')
        item = CoolscrapyItem()
        item['title'] = detail.xpath('h1/text()').extract_first().strip()
        item['link'] = response.url
        item['posttime'] = detail.xpath(
            '//span[@class="article-time pull-left"]/text()').extract_first()
        print item['title'],item['link'],item['posttime']
        yield item