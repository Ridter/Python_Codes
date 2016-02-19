#!/usr/bin/python
#coding:utf-8
import requests
import re
import time
import warnings
import sys
import threading  
import os
from bs4 import BeautifulSoup
reload(sys)  
sys.setdefaultencoding('utf8')
warnings.filterwarnings("ignore")
pagescount = 8800 #总页数
userlinks = []
havedonepage = []
# page 21240
counts = 1 #计数器
done = []
test = []
username = []
jigou=[]
job=[]
phone=[]
email=[]
def getdata(page):
  global counts,username,jigou,job,phone,email
  global userlinks
  urls = "http://xxxxxx.com.cn//oanames.nsf/PeopleByName?OpenView&Start="+str(page)
  headers = {'content-type': 'application/json',
           'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0',
           'Cookie':'tcoa=%u767D%u5A67; LtpaToken=AAECAzU2QzZBMUY5NTZDNzJFOTlDTj0TsNcT5rovT1U9amZnc29hL089ZmF3n/fWy6VhzkyPohmO4UbX0eN01lI='}
  r = requests.get(urls,verify=False,headers=headers)
  html = r.text
  soup = BeautifulSoup(html)
  table = soup.find('table', attrs={'border':'0', 'cellpadding':'2', 'cellspacing':'0'})
  for raws in table.findAll('tr'):
    try:
      username = raws.findAll('td')[0:1][0].findAll('a')[0:1][0].text
      jigou = raws.findAll('td')[1:2][0].text
      job = raws.findAll('td')[2:3][0].text
      phone = raws.findAll('td')[3:4][0].text
      email =  raws.findAll('td')[4:5][0].text
    except:
      pass
    write(username,jigou,job,phone,email)
  print "[*] reading..正在写第"+str(page)+"页"+"第"+str(counts)+"条数据"
  counts = counts+1
  havedonepage.append(page)
  countpage(havedonepage)
  
#将已经读取的页码写入1.txt，过滤已读取页码
def reading():
  global done
  f = open('1.txt','r')
  pages= f.readlines()
  done = []
  for page in pages:
    done.append(page.strip('\n'))

def split(list):
  for j in list:
    if str(j+1) in done:
      print '[*] I have writed !\n'
    else:
      getdata(j+1)
  time.sleep(1)
    

def thread_main(count):
  reading()
  for i in range(0,pagescount,int(count)):
    b = range(i,i+count)
    t = threading.Thread(target=split,args=(b,))   #添加线程  
    t.start()
    #t.join()
  print "current has %d threads" % (threading.activeCount() - 1)

#将数据写入文件
def write(username,jigou,job,phone,email):
  filesname = 'users.txt'
  file_object = open(filesname,'a')
  try:
    file_object.write(username+'\t'+jigou+'\t'+job+'\t'+phone+'\t'+email+'\n')
  except:
    pass
  file_object.close()

#将随机读取的页码存入文件  
def countpage(pages):
  filesname = "havedown.txt"
  file_object = open(filesname, 'w')
  for page in pages:
    file_object.write(str(page)+'\n')
  file_object.close()


def main():
  thread_main(500)

if __name__ == "__main__":
  try:
    main()
  except:
    print 'Error~'





