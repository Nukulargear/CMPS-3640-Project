class base(object):

	def __init__(self, name, port):
		self.name = name
		self.port = port
		self.close_self_flag = 1
		
	def send(self):
		try:
			while self.close_self_flag:
				message = (input(""))
				#print('Sending {!r}'.format(message))
				self.sock.sendall(message.encode())
				
				if message == 'shutdown':
					self.close_self_flag = 0
					break
		finally:
			print('Closing Self')