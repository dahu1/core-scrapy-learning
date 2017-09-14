#!/usr/bin/python
#coding=utf-8
#author=dahu
import pprint,sys
reload(sys)
sys.setdefaultencoding('utf-8')
b='haha'
def file_size(name):
    if name.endswith('g') or name.endswith("G"):
        a=1000*1000*1000
    elif name.endswith('m') or name.endswith("M"):
        a=1000*1000
    elif name.endswith('k') or name.endswith("K"):
        a=1000
    else:a=10

    # b='lele'
    print b
    return float(name[:-1])*a

if __name__ == '__main__':
    print file_size("150")
    a=['hehe','haha']
    print sum([len(i) for i in a])
    a=['我爱你','hello']
    print len("我爱你")