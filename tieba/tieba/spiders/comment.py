# -*- coding: utf-8 -*-
import scrapy
import sys, os,re
from scrapy import Request
from tieba.items import TiebaItem
from scrapy_splash import SplashRequest
import json

reload(sys)
sys.setdefaultencoding("utf-8")


class CommentSpider(scrapy.Spider):
    name = 'comment'
    # allowed_domains = ['tieba.baidu.com']
    start_urls = ['https://tieba.baidu.com/p/totalComment?t=1506043640283&tid=4482525043&fid=13785031&pn=1&see_lz=0']
    index = 1

    def parse(self, response):
        # print 'hehe',response
        data = json.loads(response.body)
        for key in data['data']['comment_list']:
            print key
            for i in data['data']['comment_list'][key]['comment_info']:
                print re.sub('\<.*\>','',i['content']),i['username']
                # if re.search(i['content'],'<.*>'):
                #     print re.sub('\<.*\>','',i['content'])
                #     # print 'find!',i['content']
                # else:
                #     print i['content']

        # print data
            # print 'hehe',i.xpath('.//div[@class="lzl_cnt"]/span[@class="lzl_content_main"]/text()').extract_first()