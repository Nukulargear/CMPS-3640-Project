from base import * 

# Database
# Things to do:
# GUI
# Server Promotion
# Identifying Server Address


'''
try:
	connect_str = "dbname='oxysquare' user='pi' host='sharadeos.ddns.net' " + \
				"password='Dol0Rubx'"
	# use our connection values to establish a connection
	conn = psycopg2.connect(connect_str)
	# create a psycopg2 cursor that can execute queries
	cursor = conn.cursor()
	# create a new table with a single column called "name"
	cursor.execute("""SELECT * from test_account""")
	rows = cursor.fetchall()
	print ("\nCurrent Database Entry:")
	
	for row in rows:
		print ("   ", row[0], row[1])
	
except Exception as e:
	print("Failed to Connect to Database Server")
	print(e)

'''

class basicServer(base):
	def __init__(self, name, port):
		base.__init__(self, name, port, 'server')

		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.sock.bind((self.name, self.port))
		
		
		self.client_list = []
		
	

	def begin(self):
		threading.Thread(target = self.clientManager,args = ()).start()
		
		self.userInput()
		
	
	
		
	def clientManager(self):
		self.sock.listen(5)
		
		while self.close_self_flag:
			
			client, address = self.sock.accept()
			
			client.settimeout(60)
			
			self.client_list.append([client, address])
			
			print(client, address)
			
			threading.Thread(target = self.listenToClient,args = (client,address)).start()
			

		
			
	def listenToClient(self, client, address):
		
		
		while self.close_self_flag:
			try:
				data = client.recv(self.size)
				
				if data:
					# Set the response to echo back the recieved data 
					print('Client Message:', data)
					string = str(datetime.datetime.now())
					client.send(string.encode())
					
				else:
					raise error('Client disconnected')
			except:
				client.close()
				return False
		
		client.close()
		
			
	def userInput(self):
		try:
			while self.close_self_flag:
				message = (input(""))
				parsed_message = message.split("/")
				
				#print('Sending {!r}'.format(message))
				if parsed_message[0] == 'shutdown':
				
					self.close_self_flag = 0
					
					for client, address in self.client_list:
						client.close()
						
					self.sock.close()
					
					sys.exit(0)
					break

				elif parsed_message[0] == 'send':
					print(parsed_message[1])
					
				elif parsed_message[0] == 'sendall':
					for client in self.client_list:
						client.send(message[1].encode())
				
				elif parsed_message[0] == 'swarm':
					for client, address in self.client_list:
						print(client)
				
		
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
	basicServer('localhost', 8080).begin()