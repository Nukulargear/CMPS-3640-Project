import socket
import sys
import threading

close_client_flag = 1

class sendThread (threading.Thread):
	def __init__(self, socket):
		threading.Thread.__init__(self)
		self.socket = socket
		
	def run(self):
		send()
		
class receiveThread (threading.Thread):
	def __init__(self, socket):
		threading.Thread.__init__(self)
		self.socket = socket
		
	def run(self):
		listen()
		

def send():
	global close_client_flag
	try:
		while close_client_flag:
			message = (input(""))
			print('Sending {!r}'.format(message))
			sock.sendall(message.encode())
			
			if message == 'shutdown':
				close_client_flag = 0
				break
	finally:
		print('Closing Client')
	
		
		
def listen():
	global close_client_flag
	
	while close_client_flag:
		data = sock.recv(1024).decode()
		if len(data) > 0:
			print('Server Timestamp:', data)
			
	sock.close()
	



		


#Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 10000)
print('Connecting to {} port {}'.format(*server_address))
print('To close the connection, send [shutdown]')
sock.connect(server_address)



t1 = sendThread(sock)
t2 = receiveThread(sock)
t1.start()
t2.start()
t1.join()
t2.join()
