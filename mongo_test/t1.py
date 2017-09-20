#!/usr/bin/python
#coding=utf-8
#__author__='dahu'
#data=2017-
# 
import datetime,time
from pymongo import MongoClient

#连接到数据库
# client = MongoClient('localhost', 27017)
client = MongoClient("127.0.0.1", 27017)

#list all databases
print client.database_names()   #database list

#delete specific database
# client.drop_database('tieba')   #delete
db = client['dahu']            #没有就新建

#list all collection names
print db.collection_names(include_system_collections=False)

#delete specific collection
#db["mycollection"].drop()

post = {
    "author": "dahu",
    "text": "My first blog post!",
    "tags": ["mongodb", "python", "pymongo"],
    "date": time.ctime()}
# posts = client['dahu'].posts

# post_id = posts.insert_one(post).inserted_id  #注意这两句添加的方式
# posts.insert_many([{'i': i} for i in range(10)])
# posts.update_one({'i': 32}, {'$set': {'i': 1}},upsert=True) #更新,
# posts.update_one({'i': 1}, {'$unset': {'fooo': ''}},upsert=True)
# posts.replace_one({'foo': ''},{'food': ''},upsert=True)
# posts.delete_one({'food':''})
# db['mycollection'].insert(post)   #db[XXX] 没有就新建
# print post_id

db.posts.update_one({'i': 1})
