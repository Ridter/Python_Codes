#!/usr/bin/python
# -*- coding: utf-8 -*-
#############################################################
##                                                         ##
##     ,         ,          @www.guetsec.org               ##
##    /           \         @blog.guetsec.org              ##
##   ((__--,,,--__))                                       ##
##     (_) 0 0 (_)__________________                       ##
##       \  _ /                    |\                      ##
##        o _o  \   GUET Sec Team  | \                     ##
##               \   ____________  |  \                    ##
##                |||         WW |||   *                   ##
##                |||            |||                       ##
##                |||            |||                       ##
##                                                         ##
#############################################################
## @file    pyIpclient.py                                  ##
## @date    2013-11-08                                     ##
## @author  xspyhack@gmail.com                             ##
## @team    GUET Sec                                       ##
## @brief   python implementation of Ipclient              ##
#############################################################

import pygtk
pygtk.require('2.0')
import gtk
import gobject
import glib
import socket
import threading
import struct
import hashlib
import bz2
import tempfile
import sys
import os
from random   import *
from ctypes   import *
from struct   import *
from datetime import *


CONF = {
    'ICON NAME': 'ipclient.ico',
    'SOFTWARE DIR': os.path.dirname(os.path.abspath(sys.argv[0])) + '/',
    'CONFIG FILE NAME' : '.ipclient_config'
}
PROTO = {
    'BANNER': 0x2382,
    'RESV': 0x3ff00000
    }
SERVER = {
    'IP': '172.16.12.11',
    'CONTROL PORT': 5300,
    'REFRESH PORT': 5301
 }
HOST = {
    'CONTROL PORT': 5200,
    'REFRESH PORT': 5201,
    'MAC ADDR'    : '20-6a-8a-54-26-cb' # this is my mac_addr
}
CONTROL_CMD = {
    'CLOCK SYN'            : '\x1e',
    'CLOCK SYN REPLY'      : '\x1f',
    'LOGIN USERID'         : '\x1f',
    'LOGIN USERID REPLY'   : '\x20',
    'LOGIN PASSWORD'       : '\x21',
    'LOGIN PASSWORD REPLY' : '\x22',
    'LOGOUT USERID'        : '\x14',
    'LOGOUT USERID REPLY'  : '\x15',
    'LOGOUT PASSWORD'      : '\x16',
    'LOGOUT PASSWORD REPLY': '\x17'
}
REFRESH_CMD = {
    'REFRESH ONLINE'       : '\x1e',
    'REFRESH ONLINE REPLY' : '\x1f',
    'REFRESH 0A'           : '\x0a', # unkown usage 
    'REFRESH 0A REPLY'     : '\x0b', # unkown usage 
    'REFRESH GET NEWS'           : '\x05',
    'REFRESH GET NEWS REPLY'     : '\x06' 
}
RESULTS = { 
    0x1:  u'your ip needn\'t use ipclient.',
    0xa:  u'your account is expired.',
    0xb:  u'your account is disabled.',
    0x14: u'your account has not enough money.',
    0x15: u'your accont has not available hours in this month.',
    0x16: u'your account has not available flow in this mouth.',
    0x19: u'your account cannot be used in this IP.',
    0x1e: u'your account cannot be used in this time.',
    0x1f: u'please dial later.',
    0x20: u'too many users are using this account now.',
    0x21: u'ipclient cannot be used for your account.',
    0x22: u'please dial later.',
    0x63: u'userid or password error.'
    }
CONTROL_PACKET = {
    'LENGTH' : 300,
    'RESULT' : RESULTS,
    'CMD'    : CONTROL_CMD,
    'FILL BYTE' : 0xff,
    'RANDOM STRING LENGTH' : 0x13 
}
REFRESH_PACKET = {
    'LENGTH' : 500,
    'CMD'    : REFRESH_CMD,
    'FILL BYTE' : 0xff,
    'RANDOM STRING LENGTH' : 0x29
}
TIME = {
    'SOCK TIMEOUT' : 3,
    'TIMEOUT FOR RE LOGIN' : 80,
    'REFRESH ONLINE INTERVAL': 15 * 1000
}
MSG = {
    'TIMEOUT' : u'连接服务器失败',
    'INVALID PACKET' : u'接收到错误的数据包',
    'AUTOLOGIN FAIL' : u'自动登录失败',
    'SUCCESS' : u''
}

COPYRIGHT = {
    'SOFTWARE': '@Ipclient for python by guetsec',
    'AUTHOR'  : '@author: xspyhack@guetsec',
    'EMAIL'   : '@email: xspyhack@gmail.com',
    'VERSION' : '@Version: 1.85, GUET'
}
CONFIG_FILE = {    
    'USERID DELTA': - ord('0'),
    'IN CURRENT DIR' : 0x1,
    'IN HOME DIR'    : 0x2,
    
    'FILE IN CURRENT DIR': CONF['SOFTWARE DIR'] + CONF['CONFIG FILE NAME'],
    'FILE IN HOME DIR'   : '~/' + CONF['CONFIG FILE NAME'],
    'NOW FILE IN': 0x1,
    'FILE SAVED' :  u'配置文件已保存'
}
BZ2_ICON = ('BZh91AY&SY\xd8>\xa4\x04\x00\x00\x08\xf4\xdd\xfe\xe4\xc5\x00P@D'   +
            '\x84@\xcc\xc0\xc8\x80\x10@\x08D\x84\x00@@\xcc\xb0\x01z\xda\xad'   +
            '\x98i\xa2MO$\x19\x194\x06\x8fQ\xa3@\xf4\x83S\xc91)\x90F\x98\x00'  +
            '\x11\x93\x08\xc1)\xa0\x94\xc4\xca3Pz\x9a\x19\x01\xa0=D\xed\x9f'   +
            '\xec\xe9\xb3\xdd\xbe<Z\xc7\x847%z\nB\xa7d\x8cP\xab\x92\xa9\x94'   +
            '\xc9\x1a\xd5\x7f=\xb6\xda\xf5\xf7\nH7\x15\xc6U\xc2\x8f8j\x86/'    +
            '\xcc\x11\x90\xe0T\x1b\x19\x83\x10IF\xc1\xe1\x85*@\xaa\xca\x12'    +
            '\xf3\xa2\xb8\xb2\x18\xc1%3\xca{X\x06e\x12\t\x83DH\x92\'\x82d'     +
            '\xb5M\xf9\xcf\xdb\xa7\x04h\x87\xc9\xb6\xc1}M\xfc\xebZ6Q1r\x14S'   +
            '\x9bBgO\xfd\x10\xd2Bx\xff\xfa\x04\xf8z0\x85$a"\xf6\xaaV\xad%\xae' +
            'j\xd8\xdf\xf6\xb8(\x1f\xd1e\xb5\xf8\xbd+"\xf7\x81*\x1b\tv,\xa6'   +
            '\xc1aB2\x077Vuul\xdff.n\xea\xe1y\x92\x02\xa0\xb1\xad\x1aM2\x98p'  +
            '\x85\xf2\xcc\x92R\xc2\xa7\xbd\x81\x89\x8b\xda%t\xba\x86\x13\xbar' +
            '\x95\x8e\xaf\x04e\x9eN\x03[\xb2s\x82\xa6\xe1vV\xc7$\xdb\xd4Z\x9f' +
            'Iy\x7f\x98;s\xd9P\x87\x96@!0\x17u"4$\xc5\xf7V\x94tahur\x19&\x02'  +
            '\xe4\xa4\xca\x06\x94\x01-!\x0f\xee\x86D\x9b\x11\xec]\xc9\x14\xe1B'+
            'C`\xfa\x90\x10' )

## @func   changestr
## @brief  add delta to each char of string
def changestr(string, delta):
    newstring = ''
    for i in range(len(string)):
        newstring += chr( ord(string[i]) + delta )
    return newstring

## @func   my_random
## @brief  return random interger [start, start + delta)
def random_int(n, delta):
    return randint(delta, n + delta - 1)

## @func  pack_string_into
## @brief pack the length of string and string itself into ctypes char 
##        buffer arg0(buf) at arg1(offset), return the all bytes packed.
def pack_string_into(buf, offset, string):
    n = len(string)
    pack_into('<I', buf, offset, n)
    n = len(string)
    for i in range(n):
        buf [offset + 4 + i] = string[i]
    return (n + 4)

## @func   pack_string_from
## @brief  unpack a string(have a leading length of dword) from c_char buffer 
##         buf(arg0) at offset offset(arg1), return the string and the 
##         num of bytes unpacked.
def unpack_string_from(buf, offset):
    length, = unpack_from('<I', buf, offset)
    s = ''    
    for i in range(length):
        s += buf[offset + 4 + i]
    return (s, length + 4)

## @func  random_string
## @brief generate a random string of length arg0
def random_string(length):    
    s = ''
    for i in range(length):
        s += choice('0123456789abcdef')
    return s

## @func  mdstring
## @brief do the md5 encrypt of the string(arg0), then get the hex string
##        of each byte of the encryption string.
def mdstring(string):
    md5ob = hashlib.md5()
    md5ob.update(string)
    return md5ob.hexdigest()
        
## @func  flow_encrypt
## @brief use the key to encrypt the password,
##        this is a flow encryption algorithm.
def flow_encrypt(password, key):
    n = len(password)
    en_pswd = ''
    vkey = key
    for i in range(n):
        c = ord(password[i])
        temp = vkey
        temp = (temp & 0xffff) >> 8
        d = temp & 0xff
        c = d ^ c
        en_pswd += chr(c)
        c = ord(en_pswd[i])
        e = vkey & 0xffff
        e = (e + c) & 0xffff
        e = (e * 0xce6d) & 0xffff
        e = (e + 0x58bf) & 0xffff
        vkey = e        
    return en_pswd

## @brief get all chars in c_char buffer into a string
def c_char_buf_2_string(buf, length = 0):
    s = ''
    length = (length, len(buf)) [ length is 0 ]
    for i in range(length):
        s += buf[i]
    return s


## CMD packet format 
# +----------------------+-----------------------+-------------------------+-----------------------+
# | (2) Banner(0x2382)   | (1) Command           | (4) Result              | (4) unused_1(const:0) |
# | (4) Len1             | (Len1) Str_1/userid   | (4) Len2                | (Len2) Str_2/passwd   |
# | (4) Len3             | (Len3) Str_3/mac addr | (4) Key                 | (4) unused_2(const:0) |
# | (4) resv(0x3ff00000) | (4) Len4              | (Len4) Str_4/result msg |                       |
# +----------------------+-----------------------+-------------------------+-----------------------+
class CmdPacket:
    def __init__(self, userid, password):
        self.userid   = userid;
        self.password = password;
        self.key      = 0;
        self.en_key   = 0;
        self.packet_units = { 'banner': PROTO['BANNER'], 
                              'resv'  : PROTO['RESV'],
                              'unused_1': 0, 
                              'unused_2': 0 }

    def get_key(self):
        return self.key

    def get_login_userid_packet(self):
        self._set_packet_units(CONTROL_PACKET['CMD']['LOGIN USERID'],
                               0,
                               changestr(self.userid, -10),
                               self._get_a_random_string(),
                               'a',
                               'b',
                               self._get_a_random_interger()
                               )
        return self._fill_packet()

    def check_login_userid_reply(self, packet):
        res = self._is_packet_valid(packet, 
                                    CONTROL_PACKET['CMD']['LOGIN USERID REPLY'])        
        if res is True:
            self.key = self._get_key(packet) - 3344 # 0x0d10 == 3344
        return res

    def get_login_password_packet(self):
        self._set_packet_units(CONTROL_PACKET['CMD']['LOGIN PASSWORD'],
                               0,
                               self._get_a_random_string(),
                               self._get_login_encrypt_password(),
                               HOST['MAC ADDR'],
                               'b',
                               self._get_a_random_interger()
                               )
        return self._fill_packet()

    def check_login_password_reply(self, packet):
        res = self._is_packet_valid(packet, 
                                    CONTROL_PACKET['CMD']['LOGIN PASSWORD REPLY'])
        if res is False:
            return (False, MSG['INVALID PACKET'])
        else:
            reply_msg = ''
            result = self._get_result_from_reply(packet)
            if result is not 0:
                res = False
                reply_msg += CONTROL_PACKET['RESULT'][result] + '\n'
            else:
                res = True
            reply_msg += self._get_str4_from_reply(packet).decode('gbk')
            return (res, reply_msg)

    def get_logout_userid_packet(self):                                   
        self._set_packet_units(CONTROL_PACKET['CMD']['LOGOUT USERID'],
                               0,
                               changestr(self.userid, -15),
                               self._get_a_random_string(),
                               COPYRIGHT['EMAIL'],
                               COPYRIGHT['VERSION'],
                               self._get_a_random_interger()
                               )
        return self._fill_packet()

    def check_logout_userid_reply(self, packet):
        res = self._is_packet_valid(packet, 
                                    CONTROL_PACKET['CMD']['LOGOUT USERID REPLY'])        
        if res is True:
            self.en_key = self._get_key(packet) - 0x2382
        return res

    def get_logout_password_packet(self):
        self._set_packet_units(CONTROL_PACKET['CMD']['LOGOUT PASSWORD'],
                               0,
                               self._get_a_random_string(),
                               flow_encrypt(self.password, self.en_key),
                               HOST['MAC ADDR'],
                               COPYRIGHT['VERSION'],
                               (self.en_key % 10000) * 2 + len(self.password)
                               )
        return self._fill_packet()

    def check_logout_password_reply(self, packet):
        res = self._is_packet_valid(packet,
                                    CONTROL_PACKET['CMD']['LOGOUT PASSWORD REPLY'])
        if res is False:
            return (False, MSG['INVALID PACKET'])
        else:
            reply_msg =  self._get_str4_from_reply(packet).decode('gbk')
            return (True, reply_msg)

    def _set_packet_units(self, cmd, result, str1, str2, str3, str4, key):
        self.packet_units['cmd']    = cmd
        self.packet_units['result'] = result
        self.packet_units['str1']   = str1
        self.packet_units['str2']   = str2
        self.packet_units['str3']   = str3
        self.packet_units['str4']   = str4
        self.packet_units['key']    = key

    def _get_str4_from_reply(self, packet):
        buf = create_string_buffer(packet, CONTROL_PACKET['LENGTH'])
        offset = calcsize('<HB II')
        for i in range(3):            
            strn, length = unpack_string_from(buf, offset)
            offset += length
        offset += calcsize('<III')
        str4, length = unpack_string_from(buf, offset)
        return str4

    def _get_result_from_reply(self, packet):
        buf = create_string_buffer(packet, CONTROL_PACKET['LENGTH'])
        result, = unpack_from('<I', buf, calcsize('<HB') )
        return result

    def _get_login_encrypt_password(self):
        en_pswd = repr(self.key) + self.password
        en_pswd = mdstring(en_pswd)
        en_pswd = (en_pswd[:5]).upper() + self.userid
        en_pswd = mdstring(en_pswd)
        en_pswd = (en_pswd.upper())[:30]
        return en_pswd

    def _is_packet_valid(self, packet, command):
        buf = create_string_buffer(packet, CONTROL_PACKET['LENGTH'])
        banner, cmd = unpack_from('<HB', buf, 0)
        if banner != PROTO['BANNER'] or cmd != ord(command):
            return False
        else: 
            return True

    def _get_key(self, packet):
        buf = create_string_buffer(packet, CONTROL_PACKET['LENGTH'])
        offset = calcsize('<HB II')
        for i in range(3):
            strn, length = unpack_string_from(buf, offset)
            offset += length
        key, = unpack_from('<I', buf, offset)
        return key

    def _fill_packet(self):
        DATA = self.packet_units
        buf = create_string_buffer( CONTROL_PACKET['LENGTH'] )
        memset(buf, CONTROL_PACKET['FILL BYTE'], CONTROL_PACKET['LENGTH'])
        pack_into('<HBII', buf, 0,
                  DATA['banner'],
                  ord(DATA['cmd']),
                  DATA['result'],
                  DATA['unused_1']
                  )
        offset = calcsize('<HBII')
        n = pack_string_into(buf, offset, DATA['str1'])
        offset += n
        n = pack_string_into(buf, offset, DATA['str2'])
        offset += n
        n = pack_string_into(buf, offset, DATA['str3'])
        offset += n
        pack_into('<III', buf, offset,
                  DATA['key'],
                  DATA['unused_2'],
                  DATA['resv']
                  )
        offset += calcsize('<III')
        pack_string_into(buf, offset, DATA['str4'])
        return c_char_buf_2_string(buf)

    def _get_a_random_interger(self):
        return random_int(88888888, 11111111)

    def _get_a_random_string(self):
        return random_string(CONTROL_PACKET['RANDOM STRING LENGTH'])


## Refresh packet
# +--------------------+---------------------+--------------+--------------+-----------+
# | (2) Banner(0x2382) | (1) Command         | (8) Key      | (8) Flow     | (8) Money |
# | (4) Len1           | (Len1) Str_1/userid | (4) Len2     | (Len2) Str_2 | (4) Len3  |
# | (Len3) Msg         | (4) Len4            | (Len4) Str_4 |              |           |
# +--------------------+---------------------+--------------+--------------+-----------+

class RefreshPacket:
    def __init__(self, userid, password, key = 0):
        self.refresh_key = key + 1500
        self.userid   = userid
        self.password = password
        self.packet_units = { 'banner': PROTO['BANNER'] }
        self.flow  = 0.0
        self.money = 0.0

    def set_key(self, key):
        self.refresh_key = key + 1500

    def get_refresh_get_news_packet(self):        
        self._set_packet_units(REFRESH_PACKET['CMD']['REFRESH GET NEWS'],           
                               self._get_random_interger(),
                               self._get_random_double(),
                               self._get_random_double(),
                               COPYRIGHT['SOFTWARE'],
                               COPYRIGHT['AUTHOR'],
                               self._get_random_string(),
                               COPYRIGHT['VERSION']
                               )
        return self._fill_packet()

    def check_refresh_get_news_reply(self, packet):
        res = self._is_packet_valid(packet,
                                    REFRESH_PACKET['CMD']['REFRESH GET NEWS REPLY'])
        if res is False:            
            return (False, MSG['INVALID PACKET'])
        else:
            str_news = self._get_str(packet, 3).decode('gbk')            
            str_ip   = self._get_str(packet, 4)
            return (True, (str_news, str_ip))

    def get_refresh_0a_packet(self):
        self._set_packet_units(REFRESH_PACKET['CMD']['REFRESH 0A'],
                               self._get_random_interger(),
                               self._get_random_double(),
                               self._get_random_double(),
                               COPYRIGHT['SOFTWARE'],
                               COPYRIGHT['AUTHOR'],
                               self._get_random_string(),
                               COPYRIGHT['VERSION']
                               )
        return self._fill_packet()

    def check_refresh_0a_reply(self, packet):
        return self._is_packet_valid(packet,
                                     REFRESH_PACKET['CMD']['REFRESH 0A REPLY'])
 
    def get_refresh_online_packet(self):       
        self._set_packet_units(REFRESH_PACKET['CMD']['REFRESH ONLINE'],
                               self.refresh_key,
                               self._get_random_double(),
                               self._get_random_double(),
                               self.userid,
                               COPYRIGHT['AUTHOR'],
                               (u'今天天气真好').encode('gb2312'),
                               COPYRIGHT['VERSION']
                               )                               
        return self._fill_packet()
  
    def check_refresh_online_reply(self, packet):
        res = self._is_packet_valid(packet, 
                                    REFRESH_PACKET['CMD']['REFRESH ONLINE REPLY'])
        if res is False:
            return False
        else:
            self.flow  = self._get_double_from_packet_at(packet, calcsize('<HBQ' ))
            self.money = self._get_double_from_packet_at(packet, calcsize('<HBQd'))
            return True

    def get_flow_money_string(self):        
        str_flow  = u'流量: {0:.2f}KB' 
        str_money = u'剩余金额: {0:.2f}元'
        str_flow  = str_flow.format(self.flow / 1024.0)
        str_money = str_money.format(self.money)        
        return (str_flow, str_money)

    def _set_packet_units(self, cmd, key, flow, money, str1, str2, str3, str4):
        self.packet_units['cmd']   = cmd
        self.packet_units['key']   = key
        self.packet_units['flow']  = flow
        self.packet_units['money'] = money
        self.packet_units['str1']  = str1
        self.packet_units['str2']  = str2
        self.packet_units['str3']  = str3
        self.packet_units['str4']  = str4

    def _fill_packet(self):
        buf = create_string_buffer( REFRESH_PACKET['LENGTH'] )
        memset(buf, REFRESH_PACKET['FILL BYTE'], REFRESH_PACKET['LENGTH'])
        DATA = self.packet_units        
        pack_into('<HB Qdd', buf, 0,
                  DATA['banner'],
                  ord(DATA['cmd']),
                  DATA['key'],
                  DATA['flow'],
                  DATA['money']
                  )
        offset = calcsize('<HB Qdd')
        n = pack_string_into(buf, offset, DATA['str1'])
        offset += n
        n = pack_string_into(buf, offset, DATA['str2'])
        offset += n
        n = pack_string_into(buf, offset, DATA['str3'])
        offset += n
        n = pack_string_into(buf, offset, DATA['str4'])
        return c_char_buf_2_string(buf)

    def _is_packet_valid(self, packet, command):
        buf = create_string_buffer(packet, REFRESH_PACKET['LENGTH'])
        banner, cmd = unpack_from('<HB', buf, 0)
        if banner ==  PROTO['BANNER'] and cmd == ord(command):
            return True
        else: 
            return False

    def _get_double_from_packet_at(self, packet, offset):
        buf = create_string_buffer(packet, REFRESH_PACKET['LENGTH'])
        db_v, = unpack_from('<d', buf, offset)
        return db_v

    def _get_str(self, packet, n_of_str):
        buf = create_string_buffer(packet, REFRESH_PACKET['LENGTH'])
        offset = calcsize('<HB Qdd')
        for i in range(n_of_str):
            strn, n = unpack_string_from(buf, offset)
            offset += n
        return strn

    def _get_random_interger(self):
        return random_int(888888, 111111)
     
    def _get_random_double(self):
        db_ran = c_double( self._get_random_interger() )
        return db_ran.value

    def _get_random_string(self):
        return random_string(REFRESH_PACKET['RANDOM STRING LENGTH'])


class Ipclient:
    def __init__(self):
        self.is_init_sock = False

    def init_sock(self, userid, password):
        self.is_init_sock = True
        self.cmd_packet     = CmdPacket(userid, password)
        self.refresh_packet = RefreshPacket(userid, password)
        self.cmd_sock     = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.refresh_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.cmd_sock.settimeout(TIME['SOCK TIMEOUT'])
        self.refresh_sock.settimeout(TIME['SOCK TIMEOUT'])
        self.cmd_sock.bind( ('0.0.0.0', HOST['CONTROL PORT']) )        
        self.refresh_sock.bind( ('0.0.0.0', HOST['REFRESH PORT']) )
        self.cmd_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.refresh_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.last_refresh_online_dtime = datetime(1988,11,6)

    def close_sock(self):
        if self.is_init_sock is True:            
            self.cmd_sock.close()
            self.refresh_sock.close()

    def get_news(self):
        packet = self.refresh_packet.get_refresh_get_news_packet()
        try:
            self.refresh_sock.sendto(packet, 
                                     (SERVER['IP'], SERVER['REFRESH PORT']))        
            packet = self.refresh_sock.recv(REFRESH_PACKET['LENGTH'])            
        except socket.timeout as ex:            
            return (False, MSG['TIMEOUT'])
        except socket.error as ex:
            return (False, ex.strerror)
        res, t = self.refresh_packet.check_refresh_get_news_reply(packet)
        if res is False:
            return (res, t)
        else:
            str_news, str_ip = t
            return (True, (str_news, str_ip))

    def login(self):
        packet = self.cmd_packet.get_login_userid_packet()
        try:
            self.cmd_sock.sendto(packet, (SERVER['IP'], SERVER['CONTROL PORT']))    
            packet = self.cmd_sock.recv(CONTROL_PACKET['LENGTH'])
        except socket.timeout:             
            return (False, MSG['TIMEOUT'])
        except socket.error as ex:
            return (False, ex.strerror)
        res = self.cmd_packet.check_login_userid_reply(packet)
        if res is False:
            return (False , MSG['INVALID PACKET'])
        packet = self.cmd_packet.get_login_password_packet()
        try:
            self.cmd_sock.sendto(packet, (SERVER['IP'], SERVER['CONTROL PORT']))
            packet = self.cmd_sock.recv(CONTROL_PACKET['LENGTH'])
        except socket.timeout:            
            return (False, MSG['TIMEOUT'])
        except socket.error as ex:
            return (False, ex.strerror)
        res, reply_msg = self.cmd_packet.check_login_password_reply(packet)
        if res is True:
            self.refresh_packet.set_key( self.cmd_packet.get_key() )
        return (res, reply_msg)

    def logout(self):
        packet = self.cmd_packet.get_logout_userid_packet()
        try:
            self.cmd_sock.sendto(packet, (SERVER['IP'], SERVER['CONTROL PORT']))
            packet = self.cmd_sock.recv(CONTROL_PACKET['LENGTH'])
        except socket.timeout:
            return (False, MSG['TIMEOUT'])
        except socket.error as ex:
            return (False, ex.strerror)
        res = self.cmd_packet.check_logout_userid_reply(packet)
        if res is False:
            return (False, MSG['INVALID PACKET'])
        packet = self.cmd_packet.get_logout_password_packet()
        try:
            self.cmd_sock.sendto(packet, (SERVER['IP'], SERVER['CONTROL PORT']))
            packet = self.cmd_sock.recv(CONTROL_PACKET['LENGTH'])
        except socket.timeout:
            return (False, MSG['TIMEOUT'])
        except socket.error as ex:
            return (False, ex.strerror)
        res, reply_msg = self.cmd_packet.check_logout_password_reply(packet)
        return (res, reply_msg)

    def refresh_0A(self):
        packet = self.refresh_packet.get_refresh_0a_packet()
        try:
            self.refresh_sock.sendto(packet, (SERVER['IP'], SERVER['REFRESH PORT']))
            packet = self.refresh_sock.recv(REFRESH_PACKET['LENGTH'])
        except socket.timeout:
            return (False, MSG['TIMEOUT'])
        except socket.error as ex:
            return (False, ex.strerror)
        res = self.refresh_packet.check_refresh_0a_reply(packet)
        if res is False:
            return (False, MSG['INVALID PACKET'])
        else:
            self.last_refresh_online_dtime = datetime.now()
            return (True, '')

    def refresh_online(self):
        packet = self.refresh_packet.get_refresh_online_packet()
        try:
            self.refresh_sock.sendto(packet, (SERVER['IP'], SERVER['REFRESH PORT']))
            packet = self.refresh_sock.recv(REFRESH_PACKET['LENGTH'])
        except socket.timeout:
            return (False, MSG['TIMEOUT'])
        except socket.error as ex:
            return (False, ex.strerror)
        res = self.refresh_packet.check_refresh_online_reply(packet)
        if res is False:
            return (False, MSG['INVALID'])
        else:
            self.last_refresh_online_dtime = datetime.now()
            return (True, self.refresh_packet.get_flow_money_string() )


class pyGIpclient(Ipclient):
    def delete_event_callback(self, widget, event, data = None):        
        return False

    def destroy_callback(self, widget, data = None):
        self.btn_exit_clicked(None, None)

    def create_gui(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_border_width(15)
        self.window.set_default_size(380, 130)
        self.window.set_position(gtk.WIN_POS_CENTER)
        self.window.set_title('pyIpclient by:xspyhack@guetsec')
        self.window.set_keep_above(True)
        self.window.set_resizable(False)
        self.window.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color('#CCCCCC'))
        self.window.connect('delete_event',
                            self.delete_event_callback, self.window)    
        self.window.connect('destroy', self.destroy_callback)
        vbox = gtk.VBox(False, 10)
        self.window.add(vbox)
        hbox_msg   = gtk.HBox(False, 0)
        hbox_usage = gtk.HBox(False, 0)
        hbox_input = gtk.HBox(False, 0)
        hbox_btns  = gtk.HBox(False, 0)
        separator  = gtk.HSeparator()        
        vbox.pack_start(hbox_msg,   False, False, 0)
        vbox.pack_start(hbox_usage, False, False, 0)
        vbox.pack_start(hbox_input, False, False, 0)
        vbox.pack_start(separator,  False, False, 0)
        vbox.pack_start(hbox_btns,  False, False, 0)                
        self.label_msg   = gtk.Label(u'新闻')
        self.label_ip    = gtk.Label('255.255.255.255')
        self.label_flow  = gtk.Label(u' 流量: 0.00KB')
        self.label_money = gtk.Label(u' 剩余金额: 0.00元')       
        self.label_guetsec = gtk.Label('GUET Sec')
        label_user  = gtk.Label(u' 用户:')
        label_pswd  = gtk.Label(u' 密码:')
        self.entry_user  = gtk.Entry(max = 15)        
        self.entry_pswd  = gtk.Entry(max = 20)
        self.entry_pswd.set_visibility(False)
        self.btn_remember   = gtk.CheckButton(u'记住用户', False)
        self.btn_autologin  = gtk.CheckButton(u'自动登录', False)                
        self.btn_remember.connect ('clicked', self.btn_togg_clicked)
        self.btn_autologin.connect('clicked', self.btn_togg_clicked)        
        btn_open = gtk.Button(u' 开放 ')
        btn_stop = gtk.Button(u' 停止 ')
        btn_hide = gtk.Button(u' 隐藏 ')
        btn_exit = gtk.Button(u' 退出 ')        
        btn_open.connect('clicked', self.btn_open_clicked)
        btn_stop.connect('clicked', self.btn_stop_clicked)
        btn_hide.connect('clicked', self.btn_hide_clicked)
        btn_exit.connect('clicked', self.btn_exit_clicked)
        hbox_msg.pack_start(self.label_msg, True, True, 10)
        hbox_msg.pack_start(self.label_ip,  True, True, 10)
        hbox_usage.pack_start(self.label_flow, True, True, 10)
        hbox_usage.pack_start(self.label_guetsec, False, False, 0)
        hbox_usage.pack_start(self.label_money,True, True, 0)
        hbox_input.pack_start(label_user, False, False, 0)
        hbox_input.pack_start(self.entry_user, False, False, 10)
        hbox_input.pack_start(label_pswd, False, False, 10)
        hbox_input.pack_start(self.entry_pswd, False, False, 5)
        hbox_btns.pack_end(btn_exit, False, False, 5)
        hbox_btns.pack_end(btn_hide, False, False, 5)
        hbox_btns.pack_end(btn_stop, False, False, 5)
        hbox_btns.pack_end(btn_open, False, False, 5)
        hbox_btns.pack_end(self.btn_remember,  False, False, 5)
        hbox_btns.pack_end(self.btn_autologin, False, False, 5)
        icon_path = CONF['SOFTWARE DIR'] + CONF['ICON NAME']
        try:            
            # self.create_icon_file()
            self.window.set_icon_from_file(icon_path)
            self.statusicon = gtk.status_icon_new_from_file(icon_path)
        except glib.GError:            
            self.statusicon = gtk.status_icon_new_from_stock(gtk.STOCK_GO_FORWARD)
        finally:
            self.statusicon.connect('activate',self.trayicon_activate)            
            self.statusicon.set_tooltip(COPYRIGHT['SOFTWARE'])
       
    def __init__(self):
        self.is_login = False        
        self.create_gui()
        self.set_up_refresh_online_timer()
        self.show_news()
        self.search_config_file_to_init()
        self.window.show_all()        
        gtk.main()

    def search_config_file_to_init(self):
        self.conf = ConfigFile()
        if os.path.exists( CONFIG_FILE['FILE IN CURRENT DIR'] ):
            res, msg = self.conf.read_file(CONFIG_FILE['IN CURRENT DIR'])
        else:
            res, msg = self.conf.read_file(CONFIG_FILE['IN HOME DIR'])
        if res is True:
            bSaved_user, bAuto_login, userid, password = self.conf.get_content()
            if bSaved_user is True:
                self.btn_remember.set_active(True)
                self.entry_user.set_text(userid)
                self.entry_pswd.set_text(password)      
            if bAuto_login is True:
                self.btn_autologin.set_active(True)
                self.btn_open_clicked(None)
                if self.is_login is True:                    
                    self.window.hide()                    
                else:
                    self.label_msg.set_text(MSG['AUTOLOGIN FAIL'])

    def create_icon_file(self):
        icon_path = CONF['SOFTWARE DIR'] + CONF['ICON NAME']
        if os.path.exists(icon_path) is False:
            try:
                f_content = bz2.decompress(BZ2_ICON)
                f = open(icon_path, 'w')
                f.write(f_content)
                f.close
            except IOError as ex:
                self.label_msg.set_text(ex.strerror)

    def show_news(self):
        self.init_sock('', '')
        res , t = self.get_news()
        if res is False:
            self.label_msg.set_text(t)
        else:
            str_news, str_ip = t
            self.label_msg.set_text(str_news)
            self.label_ip.set_text(str_ip)

    def set_up_refresh_online_timer(self):
        self.timer_id = gobject.timeout_add(TIME['REFRESH ONLINE INTERVAL'],
                                            self.refresh_online_interval )

    def remove_refresh_online_timer(self):
        gobject.source_remove(self.timer_id)
        self.timer_id = None

    def refresh_online_interval(self):
        if self.timer_id is None:
            return False        
        if self.is_login is False:            
            return True
        res, t = self.refresh_online()
        if res is False:
            self.label_msg.set_text(t)
            delta = datetime.now() - self.last_refresh_online_dtime
            timeout_seconds = delta.total_seconds()
            if timeout_seconds < TIME['TIMEOUT FOR RE LOGIN']:            
                pass
            else:
                self.is_login = False
                self.close_sock()
                self.btn_open_clicked(None, None)                
        else:
            str_flow, str_money = t
            self.label_flow.set_text(str_flow)
            self.label_money.set_text(str_money)
        return True

    def btn_open_clicked(self, widget, data = None):
        if self.is_login is True:
            return 
        userid   = self.entry_user.get_text()
        password = self.entry_pswd.get_text()
        if len(userid) < 5 and len(password) < 5:            
            return
        self.close_sock()
        self.init_sock(userid, password)        
        res, reply_msg = self.login()
        self.label_msg.set_text(reply_msg)
        if res is False:
            return 
        res, msg = self.refresh_0A()
        if res is False:
            self.label_msg.set_text(msg)
            return
        res, t = self.refresh_online()
        if res is False:
            self.label_msg.set_text(t)
            return
        str_flow, str_money = t
        self.label_flow.set_text(str_flow)
        self.label_money.set_text(str_money)
        self.is_login = True

    def btn_stop_clicked(self, widget, data = None):
        if self.is_login is False:
            return 
        self.is_login = False
        res, reply_msg = self.logout()
        self.label_msg.set_text(reply_msg)
        if res is False:
            self.is_login = True
            return 
        else:
            self.close_sock()
            return

    def btn_hide_clicked(self, widget, data = None):
        self.window.hide()

    def btn_exit_clicked(self, widget, data = None):
        if self.is_login is True:
            self.btn_stop_clicked(None, None)
            self.close_sock()
        self.remove_refresh_online_timer()
        gtk.main_quit()

    def btn_togg_clicked(self, widget, data = None):        
        self.conf.set_content( self.btn_remember.get_active(),
                               self.btn_autologin.get_active(),
                               self.entry_user.get_text(),
                               self.entry_pswd.get_text() 
                               )            
        res, msg = self.conf.save_file(CONFIG_FILE['NOW FILE IN'])
        self.label_msg.set_text((msg, CONFIG_FILE['FILE SAVED'])[res is True])

    def trayicon_activate(self, widget):
        self.window.present() 


class ConfigFile:
    def set_content(self, bSaved_user = 0, bAuto_login = 0, userid = '', pswd = ''):
        self.file_head   = PROTO['BANNER']
        self.saved_user  = (0, 1) [bSaved_user is True]
        self.autologin   = (0, 1) [bAuto_login is True]
        self.en_userid   = changestr(userid, CONFIG_FILE['USERID DELTA'] )        
        self.en_password = bz2.compress(pswd)

    def get_content(self):
        return ((False, True) [self.saved_user is 1 ],                
                (False, True) [self.autologin  is 1 ],
                changestr(self.en_userid, - CONFIG_FILE['USERID DELTA']),
                bz2.decompress(self.en_password)
                )

    def _get_content_string(self):
        buf = create_string_buffer(0x100)
        pack_into('<HII', buf, 0, 
                  self.file_head,
                  self.saved_user,
                  self.autologin )
        offset = calcsize('<HII')
        n = pack_string_into(buf, offset, self.en_userid)
        offset += n
        n = pack_string_into(buf, offset, self.en_password)
        offset += n
        length = offset
        return c_char_buf_2_string(buf, length)

    def save_file(self, where):   
        file_path = self._get_file_path(where)
        config_file = ''
        try:
            config_file = open(file_path, 'wb')
            config_file.write(self._get_content_string())            
        except IOError as ex:
            return (False, ex.strerror)
        finally:
            if isinstance(config_file, file):
                config_file.close()
        return (True, MSG['SUCCESS'])

    def read_file(self, where):        
        file_path = self._get_file_path(where)
        config_file = ''
        try:
            config_file = open(file_path, 'rb')
            file_content = config_file.read()
            buf = create_string_buffer(file_content, 100)
            ( self.file_head, 
              self.saved_user, 
              self.autologin ) = unpack_from('<HII', buf, 0)
            offset = calcsize('<HII')
            self.en_userid, n  = unpack_string_from(buf, offset)
            offset += n
            self.en_password, n = unpack_string_from(buf, offset)
            return (True, MSG['SUCCESS'])
        except IOError as ex:
            return (False, ex.strerror)
        finally:
            if isinstance(config_file, file):
                config_file.close()

    def _get_file_path(self, where):
        file_path = (CONFIG_FILE['FILE IN CURRENT DIR'],
                     CONFIG_FILE['FILE IN HOME DIR'])\
            [where is CONFIG_FILE['IN HOME DIR']]
        return file_path


if __name__ == '__main__':
    print "cwd is ", os.getcwd()
    print 'config file path', CONF['SOFTWARE DIR'] + CONF['ICON NAME']
    print 'iconf file path', CONFIG_FILE['FILE IN CURRENT DIR']
    for x in COPYRIGHT:
        print x, COPYRIGHT[x]
    exe = pyGIpclient()








