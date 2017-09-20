# -*- coding: utf-8 -*-
import scrapy
import sys, os
from scrapy import Request
from tieba.items import TiebaItem

reload(sys)
sys.setdefaultencoding("utf-8")


class CommentSpider(scrapy.Spider):
    name = 'comment'
    # allowed_domains = ['tieba.baidu.com']
    start_urls = ['http://tieba.baidu.com/p/4859820256']
    index = 1

    def parse(self, response):
        for i in response.xpath('//div[@class="l_post j_l_post l_post_bright  "]'):
            # if i.xpath('.//li[@class="lzl_single_post j_lzl_s_p first_no_border"]/div[@class="lzl_cnt"]'):
            # if i.xpath('.//div[@class="lzl_cnt"]/a/text()').extract_first():
            #     print "OK"
            # else:
            #     print "NG"
            print 'hehe',i.xpath('.//li[@class="lzl_single_post j_lzl_s_p first_no_border"]/@data-field').extract_first()