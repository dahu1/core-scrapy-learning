# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import os
import pymongo
import time
from pymongo import MongoClient
# import codecs

class CoolscrapyPipeline(object):
    def __init__(self):
        self.file = 'data_cn1.json'
        os.system("rm %s"%self.file)
    def process_item(self, item, spider):
        with open(self.file, 'a') as f:
            json.dump(dict(item), f, ensure_ascii=False)
            f.write(',\n')
        return item
    def close_spider(self, spider):
        #爬虫关闭时执行
        os.system("sed -i -e '$s/\(.*\),$/\\1/g' -e '1i [' -e'$a ]' %s"%self.file)
        #转成json格式，下面这个也能转，但不好，原因有二：1、麻烦 2、当json文件很大的时候，下面的很慢
        # with open(self.file,'r') as f:
        #     data=f.read()
        # with open(self.file,'w') as f:
        #     f.write('[\n')
        #     f.write(data[0:-2])
        #     f.write('\n]')
        pass
class CoolPymongoscrapyPipeline(object):
    def open_spider(self,spider):
        # self.client = MongoClient('localhost', 27017)
        self.client = MongoClient('115.159.157.136', 27017)
        self.db = self.client['huxiu']
        # self.db['mycollection'].delete_many({})
        pass
    def process_item(self, item, spider):
        self.db['mycollection'].insert_one(item)    #注意这里是一个个插入,insert_many会报错
        # self.db['mycollection'].update_one(,item)
        pass
    def close_spider(self, spider):
        pass
