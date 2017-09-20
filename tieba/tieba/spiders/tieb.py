# -*- coding: utf-8 -*-
import scrapy
import sys, os
from scrapy import Request
from tieba.items import TiebaItem

reload(sys)
sys.setdefaultencoding("utf-8")


class TiebSpider(scrapy.Spider):
    name = 'tieb'
    # allowed_domains = ['tieba.baidu.com']
    start_urls = ['https://tieba.baidu.com/f?kw=%E9%9B%B6%E5%BA%A6%E5%90%9B%E4%B8%8A&ie=utf-8&tp=0']
    index = 1

    def parse(self, response):
        for i in response.xpath('//li[@class=" j_thread_list clearfix"]'):
            item = TiebaItem()  # attention! item的实例化对象一定要在for里面,也就是yield之后必须再实例化一个item
            item['title'] = i.xpath('.//div[@class="threadlist_title pull_left j_th_tit "]/a/text()').extract_first()
            item['author'] = i.xpath('.//a[@class="frs-author-name j_user_card "]/text()').extract_first()
            item['describ'] = i.xpath(
                './/div[@class="threadlist_abs threadlist_abs_onlyline "]/text()').extract_first().strip()
            item['comment_num'] = i.xpath('.//span[@class="threadlist_rep_num center_text"]/text()').extract_first()
            link = i.xpath('.//div[@class="threadlist_title pull_left j_th_tit "]/a/@href').extract_first()
            item['_id'] = response.urljoin(link)
            if link:
                # yield response.follow(response.urljoin(link), self.comment_parse)
                yield Request(response.urljoin(link), callback=self.comment_parse, meta={'item': item})
            # item['_id']=item['title']
            print item['title']
            for key in item:
                item[key] = item[key] if item[key] else "nothing"
            yield item
        self.index += 1
        a = response.xpath(
            '//div[@class="thread_list_bottom clearfix"]//a[@class="next pagination-item "]/text()').extract_first()
        if a:
            print '>>>\n', a, "第%s页" % self.index, '\n>>>'
            # yield {'glap': '>>>' + a + "this is %s page" % self.index}
        #
        next_page_url = response.xpath(
            '//div[@class="thread_list_bottom clearfix"]//a[@class="next pagination-item "]/@href').extract_first()
        if next_page_url != None:
            yield Request(response.urljoin(next_page_url))
            # scrapy.Request(response.urljoin(next_page_url))

    def comment_parse(self, response):
        # 每个帖子的页面,抓取所有人的回复
        item = response.meta['item']
        item["comment"] = dict()
        index = 1
        for i in response.xpath('//div[@class="l_post l_post_bright j_l_post clearfix  "]'):
            item["comment"]['reply%s' % index] = dict()
            item["comment"]['reply%s' % index]['main'] = i.xpath(
                './/div[@class="d_post_content j_d_post_content "]/text()').extract_first().strip()
            item["comment"]['reply%s' % index]['author'] = i.xpath(
                './/a[@alog-group="p_author"]/text()').extract_first()

            link = i.xpath('').extract_first('.//a[@class="lzl_link_unfold"]/text()').extract_first()
            # link='回复(3)'
            if link.endswith(')'):
                src = i.xpath('').extract_first('.//a[@class="lzl_link_unfold"]/@href').extract_first()
                yield Request(response.urljoin(src), callback=self.sub_comment_parse,
                              meta={'item': item, 'index': index})
            # try :
            # index_reply=1
            # item["comment"]['reply%s' % index]['other']=dict()
            # # item["comment"]['reply%s' % index]['other']=i.xpath('.//span[@class="lzl_content_main"]/text()').extract_first()
            # if i.xpath('.//li[@class="lzl_single_post j_lzl_s_p first_no_border"]'):
            #     for j in i.xpath('.//li[@class="lzl_single_post j_lzl_s_p first_no_border"]'):
            #         # item["comment"]['reply%s' % index]['other'][index_reply]=j.xpath('./div[@class="lzl_cnt"]/span[@class="lzl_content_main"]/text()').extract_first()
            #         item["comment"]['reply%s' % index]['other'][index_reply]=index_reply
            #         index_reply += 1
            # else :
            #     item["comment"]['reply%s' % index].pop('other')
            # # except:

            index += 1
        return item

    def sub_comment_parse(self, response):
        item = response.meta['item']
        index = response.meta['index']
        item["comment"]['reply%s' % index]['other'] = response.xpath('.//span[@class="lzl_content_main"]/text()')
        # for i in response.xpath('//"]'):
        return item
