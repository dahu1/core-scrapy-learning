# -*- coding: utf-8 -*-
import scrapy
from coolscrapy.items import CoolscrapyItem
import urllib
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

class HuxiuSpider(scrapy.Spider):
    name = 'huxiu'
    allowed_domains = ['www.huxiu.com']
    start_urls = ['http://www.huxiu.com/']

    def parse(self, response):
        index=0
        for sel in response.xpath('//div[@class="mob-ctt"]'):
            index+=1
            item = CoolscrapyItem()     #有这个就不用yield了
            item['title'] = sel.xpath('h2/a/text()').extract_first()
            item['link'] = sel.xpath('h2/a/@href').extract_first()
            url = response.urljoin(item['link'])
            item['_id']=item['title']   #注意item需要保持唯一不变,设法在加入的item找到唯一不变的值,如网页,标题等,如果不指定,系统会自带,但是重复插入还是会插进去
            # src=sel.xpath('../div[@class="mod-thumb "]/a/img/@data-original').extract_first()
            # src=src if src else sel.xpath('../a[@class="transition"]/div[@class="mod-thumb "]/img/@data-original').extract_first()  #虎嗅网推送部分的图片
            # src=src.split('?')[0]   #观察图片代码,大图保存
            item['desc'] = sel.xpath('div[@class="mob-sub"]/text()').extract_first()
            for key in item:
                item[key]=item[key] if item[key] else "nothing"
            print item['title'] ,item['link'] ,item['desc']
            yield item
            # print item['title']
            # urllib.urlretrieve(src,'%s.jpg'%index)
            # yield scrapy.Request(url, callback=self.parse_article)  #找到自己想要的链接再进行处理
    def parse_article(self, response):
        detail = response.xpath('//div[@class="article-wrap"]')
        item = CoolscrapyItem()
        item['title'] = detail.xpath('h1/text()').extract_first().strip()
        item['link'] = response.url
        item['posttime'] = detail.xpath(
            '//span[@class="article-time pull-left"]/text()').extract_first()
        print item['title'],item['link'],item['posttime']
        yield item