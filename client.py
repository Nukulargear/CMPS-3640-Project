from base import *

class basicClient(base):
	def __init__(self, name, port):
		base.__init__(self, name, port, 'client')
		
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server_address = ('localhost', int(self.port))
		self.sock.connect(self.server_address)
		
		print('Connecting to {} port {}'.format(*self.server_address))
		print('To close the connection, send [shutdown]')

		

		
	def begin(self):
		
		
		threading.Thread(target = self.listenToServer,args = ()).start()
		threading.Thread(target = self.keepAlive,args = ()).start()
		
		self.userInput()
				
	def listenToServer(self):
		
		while self.close_self_flag:
			data = self.sock.recv(1024).decode()
			if len(data) > 0:
				print('Server Timestamp:', data)
				
	
		
	#keep alive	
	def keepAlive(self):

		while self.close_self_flag:
			time.sleep(10)
			string = 'Keep Alive thread'
			self.sock.sendall(string.encode())
		
		
			
	def userInput(self):
		try:
			while self.close_self_flag:
				message = (input(""))
				parsed_message = message.split("/")
				
				#print('Sending {!r}'.format(message))
				if message == 'shutdown':
				
					self.close_self_flag = 0
					self.sock.close()
					sys.exit(0)
				
				elif parsed_message[0] == 'send':
					print(parsed_message[1])
				
				else:	
					self.sock.sendall(message.encode())
				
		
		finally:
			print('Shutting down...')
	

if __name__ == "__main__":
	'''	
	while True:
		port_num = input("Port? ")
		try:
			port_num = int(port_num)
			break
		except ValueError:
			pass
	'''
	basicClient('localhost', 8080).begin()
