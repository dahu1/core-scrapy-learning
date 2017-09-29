#!/usr/bin/python
#coding=utf-8
#__author__='dahu'
#data=2017-
# 
import re
s1='回复 玉玲兰香 :<img class="BDE_Smiley" width="30" height="30" changedsize="false" src="https://gsp0.baidu.com/5aAHeD3nKhI2p27j8IqW0jdnxx1xbK/tb/editor/images/client/image_emoticon29.png" ><img class="BDE_Smiley" width="30" height="30" changedsize="false" src="https://gsp0.baidu.com/5aAHeD3nKhI2p27j8IqW0jdnxx1xbK/tb/editor/images/client/image_emoticon29.png" >已经在睡了'
s2='走了'
print re.sub('\<.*\>','',s2)

