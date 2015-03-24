#!/usr/bin/env python
# -*- coding: gb18030 -*-
from socket import *
import os
import sys
Timeout = 2.0 
def gethost(fileroute):
    hosts=[]
    fileobject = open(fileroute,'r')
    while 1:
        lines = fileobject.readlines()
        if not lines:
            break
        for line in lines:
            hosts.append(line.strip('\n'))
    return hosts

def scanport():
    hosts = gethost(sys.argv[1])
    PORT = int(sys.argv[2])
    fileobject = open("result.txt",'w')
    tcpCliSock = socket(AF_INET,SOCK_STREAM)
    result = ''
    for host in hosts:     
        try:
            tcpCliSock = socket(AF_INET,SOCK_STREAM)
            tcpCliSock.settimeout(Timeout)
            tcpCliSock.connect((host,PORT))
            tcpCliSock.close()
            del tcpCliSock
            print host+" ->"+str(PORT) +"is Open!"
            result = host+'\n'
            fileobject.writelines([result])
        except error:
            print host+' not connect'
            continue
def main():
    filename= sys.argv[0]
    if len(sys.argv)<3:
        print 'usage:  ' + filename + '  iplist.txt port'
    else:
        scanport()
if __name__=='__main__':
    try:
        main()
    except:
        print "Error"
