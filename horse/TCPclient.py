# -*- coding: utf-8 -*- 
import socket
 
# 目标地址IP/URL及端口
target_host = "127.0.0.1"
target_port = 9999
 
# 创建一个socket对象
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
 
# 连接主机
client.connect((target_host,target_port))
 
# 发送数据
client.send("GET / HTTP/1.1\r\nHOST:127.0.0.1\r\n\r\n")
 
# 接收响应
response = client.recv(4096)
 
print response