#!/usr/bin/python
#coding=utf-8
#author=dahu
import json
data={
"desc":"女友不是你想租想租就能租",
"link":"/article/214877.html",
"title":"押金8000元，共享女友门槛不低啊"
}
with open('tmp.json','w') as f:
    json.dump(data,f,ensure_ascii=False)        #指定ensure_ascii
