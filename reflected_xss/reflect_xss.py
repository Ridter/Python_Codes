#!/usr/bin/env python
#coding=utf-8
import requests
import sys
import time
import re
#global payloads
#payloads=['"><sCript>alert(1)</sCript>','<img src=@ onerror=x>']
jindu=0
def readconf(keyname):
    isFound=0
    try:
        f=open("config","r")
        lines=f.readlines()
        for line in lines:
            if line.startswith(keyname):
                isFound=1
                return line.split('=')[1]
        if isFound==0:
            errorlog("Warn:Can not to read key "+keyname+" from configure file")
            return False
    except:
        errorlog("Warn:can not to read configure file ")
        return False
def errorlog(str):
    str=str+"\n"
    t=time.strftime('%m-%d %H.%M.%S--->',time.localtime(time.time()))
    f=open("error.log","a")
    f.write(t+str)
    f.close()
def findlog(url):
    try:
        f=open("Found","a")
        f.write(url+"\n")
    except:
        errorlog("Fail:open 'Found' file")
    finally:
        f.close()

def main(payload,canshu,checkurl):
        global jindu
	url=checkurl.replace(canshu,canshu+payload)
	#print "checking: "+url
        #TODO timeout,防止ip被屏蔽应该有
        if readconf("sleep"):
            time.sleep(float(readconf("sleep")))
        #可能有Timeout异常
        try:
            a=requests.get(url,timeout=1)
            if a.text.find(payload)!=-1:
                #print "Find!!!!"
                #print url
                #print "-----------------------"
                findlog(url)
            else:
                if jindu%10==0:
                    print time.strftime('%H:%M.%S->',time.localtime(time.time()))+"checking the "+str(jindu)+"th"+" url:"+url
        except:
            errorlog("Fail:request.get "+url)
        jindu=jindu+1
def parse(url):
	#url=http://test.com/test.php?a=1&b=2&c=3
	#canshus=["a=1","c=3"]
        #有可能url是http://test.com这种，没有参数
        #这种情况，返回一个空对象
        try:
	    canshus=url.split("?")[1].split("&")
	    return canshus
        except:
            kong=[]
            return kong
            pass
def readfile(filename):
    #这个global的位置放在上面效果就不一样,不懂为什么
    #global payloads
    try:
        aa=open(filename,"r")
        f=aa.readlines();
        for i in range(0,len(f)):
            #过滤掉\n
            f[i]=f[i].rstrip("\n")
        return f
    except:
        print "Failed to access "+'"'+filename+'" '"file!"
    finally:
        aa.close()
if __name__=="__main__":
	if len(sys.argv)!=1:
            print 'usage:'+sys.argv[0]+" url depth"
	    print 'example:'+sys.argv[0]+'"http://url/test.php?x=1&y=2" 3'
	else:
                #global payloads
                payloads=readfile("keywords.txt")
                urls=readfile("urllist")
                for checkurl in urls:
                        for payload in payloads:
                                for canshu in parse(checkurl):
                                    if len(canshu)!=0:
                                            main(payload,canshu,checkurl)
