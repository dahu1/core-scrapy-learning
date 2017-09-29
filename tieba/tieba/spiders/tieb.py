# -*- coding: utf-8 -*-
import scrapy
import sys, os,json,re
from scrapy import Request
from tieba.items import TiebaItem
from scrapy_splash import SplashRequest

reload(sys)
sys.setdefaultencoding("utf-8")


class TiebSpider(scrapy.Spider):
    name = 'tieb'
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
                yield Request(response.urljoin(link), callback=self.comment_parse, meta={'item': item})
                link = item['_id'].split('/')[-1]
                yield Request('https://tieba.baidu.com/p/totalComment?t=1506043640283&tid=%s&fid=13785031&pn=1&see_lz=0'% link,callback=self.sub_comment_parse, meta={'item': item})
                # yield SplashRequest(response.urljoin(link), callback=self.comment_parse, meta={'item': item},args={'wait': '0.2'})
            # item['_id']=item['title']
            print item['title']
            for key in item:
                item[key] = item[key] if item[key] else "nothing"
            # yield item
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
            item["comment"]['reply%s' % index]['post_id'] = i.xpath(
                './@data-field').extract_first()
            data_field = json.loads(i.xpath('./@data-field').extract_first())
            item["comment"]['reply%s' % index]['post_id']=data_field['content']['post_id']
            index += 1
        item['panduan']='1'
        # print '!!comment_parse'
        # for key in item:
        #     print key
        yield item  #attention!
        # return item

    def sub_comment_parse(self, response):
        item = response.meta['item']
        comment_item=dict()
        data = json.loads(response.body)
        for key in data['data']['comment_list']:
            print key
            j=1
            comment_item[key]=dict()
            for i in data['data']['comment_list'][key]['comment_info']:
                a=re.sub('\<.*\>', '', i['content'])
                print a, i['username']
                comment_item[key]["%s"%j]=a+">>>"+i['username']
                j+=1


        item["comment_item"]=dict()
        item['comment_item']=comment_item
        item['panduan'] = '2'
        # return item
        # print '!!!sub_comment_parse'
        # for key in item:
        #     print key
        yield item
