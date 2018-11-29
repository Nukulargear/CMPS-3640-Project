import socket
import sys
import threading
from _thread import *

import time

from base import *

class basicClient(base):
	def __init__(self, name, port):
		base.__init__(self, name, port)
		
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server_address = ('localhost', int(port_num))
		self.sock.connect(self.server_address)
		
		print('Connecting to {} port {}'.format(*self.server_address))
		print('To close the connection, send [shutdown]')

		
	def begin(self):
		
		threading.Thread(target = self.send,args = ()).start()
		threading.Thread(target = self.listenToServer,args = ()).start()
		threading.Thread(target = self.keepAlive,args = ()).start()
		

				
	def listenToServer(self):
		
		while self.close_self_flag:
			data = self.sock.recv(1024).decode()
			if len(data) > 0:
				print('Server Timestamp:', data)
				
		self.sock.close()
		
		
	#keep alive	
	def keepAlive(self):

		
		while self.close_self_flag:
			time.sleep(5)
			string = 'Keep Alive thread'
			self.sock.sendall(string.encode())
		

	
	
	
if __name__ == "__main__":
	while True:
		port_num = input("Port? ")
		try:
			port_num = int(port_num)
			break
		except ValueError:
			pass

	basicClient('',port_num).begin()
