#!/usr/bin/python
#coding:utf-8
import requests
import re
import time
import warnings
import sys
import threading  
import os
reload(sys)  
sys.setdefaultencoding('utf8')
warnings.filterwarnings("ignore")
pagescount = 21240
userlinks = []
havedonepage = []
# page 21240
counts = 0 #计数器
done = []
test = []
done1=[17974,17981,1000000000]
def getdata(page,num):
  global counts
  global userlinks
  urls = "https://xxxx.com/index.php?module=CaiWu&type=0&userid=&startdate=&enddate=&page="+str(page)
  headers = {'content-type': 'application/json',
           'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0',
           'Cookie':'cookie'}
  r = requests.get(urls,verify=False,headers=headers)
  data = re.compile(r'<a href="(.*?)" target=')
  html = r.text
  result = data.findall(html)
  print "[*] reading..正在写第"+str(page)+"页"+"第"+str(counts)+"条数据"
  write(result,num)
  havedonepage.append(page)
  countpage(havedonepage)
  counts = counts+1
    
def reading():
  global done
  f = open('1.txt','r')
  pages= f.readlines()
  done = []
  for page in pages:
    done.append(page.strip('\n'))
  print done

def split(list):
  num = list[-1]
  for j in list:
    if str(j) in done:
      print '[*] I have writed !\n'
    else:
      getdata(j,num)
  time.sleep(1)
    

def thread_main(count):
  reading()
  for i in range(0,pagescount,int(count)):
    b = range(i,i+count)
    t = threading.Thread(target=split,args=(b,))   #添加线程  
    t.start()
    #t.join()
  print "current has %d threads" % (threading.activeCount() - 1)

  
def write(result,num):
  filesname = str(num)+'links.txt'
  file_object = open(filesname,'a')
  for url in result:
    file_object.write(url+'\n')
  file_object.close()

def countpage(pages):
  filesname = "havedown.txt"
  file_object = open(filesname, 'w')
  for page in pages:
    file_object.write(str(page)+'\n')
  file_object.close()


def main():
  thread_main(1500)

if __name__ == "__main__":
    try:
        main()
    except:
        print "Error"






