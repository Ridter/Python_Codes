#!/usr/bin/env python
#coding=utf-8
import requests
import re
import string
import sys
import filter
headers={'Connection':'keep-alive',"User-Agent":"Mozilla/5.0 (X11; Linux i686) AppleWebkit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36","Origin":"http://www.oschina.net",'Accept-Encoding':'gzip,deflate,sdch','Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4','X-Requested-With':'XMLHttpRequest','Accept':'application/json,text/javascript,*/*;q=0.01'}
def saveurl(urlset):
    try:
        f=open("urllist","a")
        for url in urlset:
            #unicode字符码写入文件,添加换行
            f.write(url.encode('UTF-8')+"\n")
    #except:
    #    print "Failed to write urllist to file!"
    finally:
        f.close()
def main(requestsurl,depth):
    try:
    #print "%d"%depth
        depth=depth+1
        urlset=parseContent(requests.get(requestsurl,timeout=2,headers=headers).text)
        saveurl(urlset)
        if depth==string.atoi(sys.argv[2]):
            pass
        else:
            for u in urlset:
                main(u,depth)
    except:
        pass
def parseContent(content):
        strlist = re.split('\"',content)
        urlset = set([])
        for strstr in strlist:
            #python正则匹配\时，需要\\\\表示
            #if re.match('http://.*com(/|\w)+', str):
            #这个正则有点简单，只匹配了当前网站
            #if re.match('http://'+domain, str):
            rules="http://"+domain+"[^,^ ^  ^']*"
            #strstr是unicode对象
            result=re.compile(rules).findall(strstr.encode("utf-8"))
            #result是一个数组
            if len(result)==0:
                pass
            else:
                for i in result:
                    urlset.add(i)
        return list(urlset)
if __name__=="__main__":
    if len(sys.argv)!=3:
        print "usage:"+sys.argv[0]+" http://test.com/"+" depth"
        print "example:"+sys.argv[0]+" http://127.0.0.1/a.php?c=1"+" 3"
    else:
        domain=sys.argv[1].split('/')[2]
        #保存最开始的url
        tmp=[]
        tmp.insert(0,sys.argv[1]);
        saveurl(tmp)
        #开始抓取
        main(sys.argv[1],0)
        filter.filter()
