# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TiebaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    link = scrapy.Field()
    _id = scrapy.Field()
    author = scrapy.Field()
    describ = scrapy.Field()
    comment = scrapy.Field()
    comment_num = scrapy.Field()
    panduan = scrapy.Field()
    comment_item= scrapy.Field()

    pass
