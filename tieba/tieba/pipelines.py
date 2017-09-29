# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
import time
from pymongo import MongoClient
import json
import os

class TiebaPipeline(object):
    def open_spider(self,spider):
        self.client = MongoClient('localhost', 27017)
        # self.client = MongoClient('115.159.157.136', 27017)
        self.db = self.client['tieba']
        self.db["零度君上"].drop()
        # self.db['零度君上'].delete_many({})
        pass
    def process_item(self, item, spider):
        # self.db['零度君上'].insert_one(dict(item))    #注意这里是一个个插入,insert_many会报错
        # with open('new_item','a')as f:
        #     f.write("new item!"+'\n')
        #     for key in item:
        #         f.write(key+' ')
        dbname='零度君上'
        if self.db[dbname].find({"_id":item['_id']}).count():
            if item['panduan'] == '1':
                self.db[dbname].update_one({'_id': item['_id']}, {"$set":{"comment":item['comment']}}, upsert=True)
            elif item['panduan'] == '2':
                self.db[dbname].update_one({'_id': item['_id']}, {"$set":{"comment_item":item['comment_item']}}, upsert=True)
            pass
        else:
            self.db[dbname].update_one({'_id': item['_id']}, {"$set": item}, upsert=True)
        pass
    def close_spider(self, spider):
        pass
class TiebaPipelineJson(object):
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