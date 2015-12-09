#!/usr/bin/env python
#coding:utf-8
import sys
import time
import urllib2
import urllib 
import re
import hashlib
if len(sys.argv) < 2:
  print '\nUsage:'
  print '\t%s --online [hash..] ' % sys.argv[0]
  print '\t%s --offline [hash..] [dictionary..]'  % sys.argv[0]
  sys.exit(1)

def banner():
  print '''
                  ___           ___           ___           ___           ___     
    ___          /  /\         /  /\         /  /\         /  /\         /__/|    
   /  /\        /  /:/        /  /::\       /  /::\       /  /:/        |  |:|    
  /  /:/       /  /:/        /  /:/\:\     /  /:/\:\     /  /:/         |  |:|    
 /__/::\      /  /:/  ___   /  /:/~/:/    /  /:/~/::\   /  /:/  ___   __|  |:|    
 \__\/\:\__  /__/:/  /  /\ /__/:/ /:/___ /__/:/ /:/\:\ /__/:/  /  /\ /__/\_|:|____
    \  \:\/\ \  \:\ /  /:/ \  \:\/:::::/ \  \:\/:/__\/ \  \:\ /  /:/ \  \:\/:::::/
     \__\::/  \  \:\  /:/   \  \::/~~~~   \  \::/       \  \:\  /:/   \  \::/~~~~ 
     /__/:/    \  \:\/:/     \  \:\        \  \:\        \  \:\/:/     \  \:\     
     \__\/      \  \::/       \  \:\        \  \:\        \  \::/       \  \:\    
                 \__\/         \__\/         \__\/         \__\/         \__\/
  
        |-----------------------------------------------|
        | [+] MD5 Hash Cracker (online | offline)       |
        | [+] Home: http://www.isecur1ty.org            |
        | [+] Written by: isecur1ty team members        |
        | [+] Changed by: Ridter                        |
        | [+] Credits: Obzy, Relik and Sas-TerrOrisT    |
        |-----------------------------------------------|
'''

option   = sys.argv[1]
passwd   = sys.argv[2]

if option == '--online':
  if len(passwd)  > 32 or 16<len(passwd) <32 or len(passwd)<16: 
    print '\n[*] Error: "%s" doesn\'t seem to be a valid MD5 ' % passwd
  else:
    try:
      banner()
      def navisec():
        site = 'http://md5.navisec.it/'     
        req = urllib2.Request(site)
        try:
          opener = urllib2.urlopen(req)
          data = opener.read()
          match = re.search(r'(<span class="com">//md5.navisec.it/api.php\?token=)(.+[^>])(&amp;type=)', data)
          token = match.group(2)
          para = 'api.php?token=%s&type=md5&hash=%s' % (token,passwd)
          req2 = urllib2.Request(site+para)
          opener2 = urllib2.urlopen(site+para)
          data2 = opener2.read()
          match2 = re.search(r'(PlainText":")(.+[^>])(","Hash)',data2)
          if match: print '[-] site: %s\t\t\tPassword: %s' % (site, match2.group(2))
          else: print '[-] site: %s\t\t\tPassword: Not found' % site
        except urllib2.URLError: print '[+] site: %s \t\t\t\t[+] Error: seems to be down' % site
      navisec()
      
      def cmd5():
        site = 'http://www.cmd5.org/'
        para = urllib.urlencode({'ctl00$ContentPlaceHolder1$TextBoxInput':passwd,'__EVENTTARGET':'','__EVENTARGUMENT':'','__VIEWSTATE':'fnnBgxfmMbWnJaOryFUKnINBXZU0ThgblRLWFCXkRVCyOyqfg2DcpsotDdL1gNvSfPLshOaknZUGi035WQKfTQHQ3Bdv/CiZbX7h4HJgpZAGmdy0R8vu3qYYl3uay1Kp1jHt4wU7cFvusIGNx8kak/nkRNqMNacv/AsCByufj6uMduRO1fyYF8wcA+DUVpA8rfJGzL/Vhn6vDrqgg3kOdzC2IL5ag7rCgdKa413fQrr9hDueXBR1geYvo//ZDtvf1qVpmkxeCo3Fumfa/0TkdDwM6tRqLXIABC7xkOKMdHDuF02xypbYofpyJcvm0Z3B+yvnZOqISlnvvEfoVsbUv79QH00NCNkBcEo63jytQ9c36L/GNuQZHliDKjtgz+trRhRM+PekcmFrYsIrnn+7TqE6JBNlYOxVSsdOOYADVRCT7WIkFVb0pYCEIkT6Y6S+7LVbJDfKWx0eKBz76vhGLIS7COpM5pVq/AED4Qbb6fv6PCOiZh7DSQuu+WaKsJpuEyZX+yQLhHMumP9gvGJbs52o8LY5XBu7J/YgCSlDacihEsl9ozjALTED9lSJ+ErDkSOBYiua9dEG7SEph0ASXBWrjxW6BXJobip4cxxqJ5dWCBzQp1R32DNCMj6qCXfpHdDWsToZxOII03iLOMf15zVrQZ63OOAvKY3egECrYGTzG5Qd6WnjP5+or9qQ8t+Syg/4mHuimxRBUsJ9DeILfqzWzyXVtxMzXHNradjfOxXKoTCdXrQR3OU4rTpwwF6djxpXX33QLhM0TIWZFTQkmoH0OgWd3Ltznfd2jdJ3PC6l2vxn/XUfA+Qb0baR9/qLlbvt4+et6TkW9zTJDS0iXex8d7vvG+MzyrisC7qEZZ+DmF4ucQHIOOE//8JBM2a/fUeK9XOMWW7XcwLjEwiTcQELz2rUeqwh5rmImkg2I1y6jgO8U0AyfBjM2F4Gxy/p+CxlUCwfMyN73k0zyDKD9IGmnu9M4MLJPP+ZRn5LxzCIUoxysa5Pu92SMi/i8Pjix9D67gbANt6mK4jLR+yKM45WmPiuqZRihe49Ul78oXbZHKwPH4Cxzkb2tUTTDZSZbRieXMePUEWCQTBpzN7gL1nxjdte8qSrA8Ci2pCVSq3U6CqVWZgYU5hjCzs7uRN46uYqjYODpCaUppONBIcvbO0Twoblds2dTrMsa1gHyK8g9SYDwIjnZKwfA9dfnFvmCFJWcAzV4OjSKrFqh0XCSvpp8dR9AJYbN1jRpGpNbKTcHsfWwYCAvHQ3jn7410zzKVIOWFfscj3tPr5x9bSnqR0vqMieTR91dLDabXaVrJkIdkYlCt2vsQ5AY1ritH6sekiclg==','__VIEWSTATEGENERATOR':'CA0B0334','ctl00$ContentPlaceHolder1$InputHashType':'md5','ctl00$ContentPlaceHolder1$Button1':'decrypt','ctl00$ContentPlaceHolder1$HiddenField1':'0'})
        req = urllib2.Request(site)
        req.add_header('Proxy-Connection','keep-alive')
        req.add_header('Cache-Control','max-age=0')
        req.add_header('User-Agent','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/39.0.2171.65 Chrome/39.0.2171.65 Safari/537.36')
        req.add_header('Content-Type','application/x-www-form-urlencoded')
        req.add_header('Referer','http://www.cmd5.org/')
        try:
          fd = urllib2.urlopen(req, para)
          data = fd.read()
          match = re.search(r'(<span id="ctl00_ContentPlaceHolder1_LabelAnswer">)(.+[^>])(<br /><br /><a target=_blank)', data)
          match2 = re.search(r'Found\.But this is a payment record\. Hash-type is md5',data)
          if match: print '[-] site: %s\t\t\t\tPassword: %s' % (site, match.group(2))
          if match2: print '[-] site: %s\t\t\t\tPassword: You Can Buy It' % (site)
          else: print '[-] site: %s\t\t\t\tPassword: Not found' % site
        except urllib2.URLError: print '[+] site: %s \t\t\t\t[+] Error: seems to be down' % site
      cmd5()      
      
      def blackbap():
        site = 'http://cracker.blackbap.org/'
        rest = '?do=search&language=en'
        para = urllib.urlencode({'md5':passwd,'isajax':'1'}) 
        req  = urllib2.Request(site+rest)
        try:
          fd   = urllib2.urlopen(req, para)
          data = fd.read()
          match= re.search(r'(<p>Password <strong>)(.+[^>])(</strong></p)', data)
          if match: print '[-] site: %s\t\t\tPassword: %s' % (site, match.group(2))
          else: print '[-] site: %s\t\t\tPassword: Not found' % site
        except urllib2.URLError:  print '[+] site: %s \t\t\t[+] Error: seems to be down' % site
      blackbap()    
      
      def myaddr():
        site = 'http://md5.my-addr.com/'
        rest = 'md5_decrypt-md5_cracker_online/md5_decoder_tool.php'
        para = urllib.urlencode({'md5':passwd})
        req  = urllib2.Request(site+rest)
        try:
          fd   = urllib2.urlopen(req, para)
          data = fd.read()
          match= re.search(r'(Hashed string</span>: )(\w+.\w+)', data)
          if match: print '[-] site: %s\t\t\tPassword: %s' % (site, match.group(2))
          else: print '[-] site: %s\t\t\tPassword: Not found' % site
        except urllib2.URLError:  print '[+] site: %s \t\t\t[+] Error: seems to be down' % site
      myaddr()

      def victorov():
        try:
          site = 'http://www.victorov.su/'
          para = 'md5/?md5e=&md5d=%s' % passwd
          req  = urllib2.Request(site+para)
          req.add_header
          opener = urllib2.urlopen(req)
          data = opener.read()
          match = re.search(r'(<b>)(.+[^>])(</b>)', data)
          if match: print '[-] site: %s\t\t\tPassword: %s' % (site, match.group(2))
          else: print '[-] site: %s\t\t\tPassword: Not found' % site
        except urllib2.URLError:  print '[+] site: %s \t\t\t[+] Error: seems to be down' % site
      victorov()
      
      
      def passcracking():
        site = 'http://passcracking.com/'
        rest = 'index.php'
        para = urllib.urlencode({'datafromuser':passwd})
        req = urllib2.Request(site+rest)
        try:
          fd = urllib2.urlopen(req, para)
          data = fd.read()
          match = re.search(r"(<td bgcolor=#FF0000>)(.+[^<])(</td><td>)", data)
          if match: print '[-] site: %s\t\t\tPassword: %s' % (site, match.group(2))
          else: print '[-] site: %s\t\t\tPassword: Not found' % site
        except urllib2.URLError: print '[+] site: %s \t\t\t[+] Error: seems to be down' % site
      passcracking()

      def md5pass():
        site = 'http://www.md5pass.info/'
        para = urllib.urlencode({'hash':passwd, 'get_pass':'Get+Pass'})
        req = urllib2.Request(site)
        try:
          fd = urllib2.urlopen(req, para)
          data = fd.read()
          match = re.search(r'(Password - <b>)(\w+)', data)
          if match: print '[-] site: %s\t\t\tPassword: %s' % (site, match.group(2))
          else: print '[-] site: %s\t\t\tPassword: Not found' % site
        except urllib2.URLError: print '[+] site: %s \t\t\t[+] Error: seems to be down' % site
      md5pass()

      def md5decryption():
        site = 'http://md5decryption.com/'
        para = urllib.urlencode({'hash':passwd,'submit':'Decrypt+It!'})
        req = urllib2.Request(site)
        try:
          fd = urllib2.urlopen(req, para)
          data = fd.read()
          match = re.search(r'(Decrypted Text: </b>)(.+[^>])(</font><br/><center>)', data)
          if match: print '[-] site: %s\t\t\tPassword: %s' % (site, match.group(2))
          else: print '[-] site: %s\t\t\tPassword: Not found' % site
        except urllib2.URLError: print '[+] site: %s \t\t\t[+] Error: seems to be down' % site
      md5decryption()

      def hashkiller():
        site = 'http://opencrack.hashkiller.com/'
        para = urllib.urlencode({'oc_check_md5':passwd,'oc_submit':'Search+MD5'})
        req = urllib2.Request(site)
        try:
          fd = urllib2.urlopen(req, para)
          data = fd.read()
          match = re.search(r'(<div class="result">)(\w+)(:)(\w+.\w+)', data)
          if match:
            print '[-] site: %s\t\t\tPassword: %s' % (site.replace('http://', ''), match.group(4).replace('<br',''))
          else: print '[-] site: %s\t\t\tPassword: Not found' % site.replace('http://', '')
        except urllib2.URLError: print '[+] site: %s \t\t\t[+] Error: seems to be down' % site
      hashkiller()

      def cloudcracker():
        site = 'http://www.netmd5crack.com/'
        para = 'cgi-bin/Crack.py?InputHash=%s' % passwd
        try:
          req = urllib.urlopen(site+para)
          data = req.read()
          match = re.search(r'<tr><td class="border">[^<]+</td><td class="border">\
          (?P<hash>[^>]+)</td></tr></tbody></table>', data)
          if match: print '[-] site: %s\t\t\tPassword: %s' % (site, match.group(hash))
          else: print '[-] site: %s\t\t\tPassword: Not found' % site
        except urllib2.URLError: print '[+] site: %s \t\t\t[+] Error: seems to be down' % site
      cloudcracker()
      
      def cloudcracker():
        site = 'http://www.cloudcracker.net/'
        para = urllib.urlencode({'inputbox':passwd, 'submit':'Crack+MD5+Hash!'})
        req = urllib2.Request(site)
        try:
          fd = urllib2.urlopen(req, para)
          data = fd.read()
          match = re.search(r'(this.select)(....)(\w+=")(\w+.\w+)', data)
          if match: print '[-] site: %s\t\t\tPassword: %s\n' % (site, match.group(4))
          else: print '[-] site: %s\t\t\tPassword: Not found\n' % site
        except urllib2.URLError: print '[+] site: %s \t\t\t[+] Error: seems to be down' % site
      cloudcracker()
    except KeyboardInterrupt: print '\nTerminated by user ...'
    
elif option == '--offline':
  banner()
  try:
    def offline():
      print '[+] This opertaion will take some time, be patient ...' 
      dictionary = sys.argv[3]
      dic = {}
      shooter = 0
      try:
        f = open(dictionary, 'rb')
        start = time.time()
        for line in f:
          line = line.rstrip()
          dic[line] = hashlib.md5(line).hexdigest()
        for k in dic.keys(): 
          if passwd in dic[k]:
            stop = time.time()
            global spent
            spent = stop - start
            print '\n[-] Hash: %s\t\tData: %s\t\tTime: %.f seconds' % (dic[k], k, spent)
            shooter += 1
        if shooter == 0:  print "\n[*]Password not found in [%s] try the online cracker\n" % dictionary
        f.close()
      except IOError: print '\n[*] Erorr: %s doesn\'t exsit \n' % dictionary
    offline()
  except KeyboardInterrupt: print '\nTerminated by user ...'
  
else: pass 