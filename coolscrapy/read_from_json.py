#!/usr/bin/python
#coding=utf-8
#author=dahu
import json
with open('huxiu.json','r') as f:
    data=json.load(f)
print data[0]['title']
for key in data[0]:
    print '\"%s\":\"%s\",'%(key,data[0][key])
