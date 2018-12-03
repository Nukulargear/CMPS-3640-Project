from base import * 

# Things to do:
# GUI
# Server Promotion
#

# command list:
# scan 
# broadcast {message}
# swarm
# shutdown


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
	def __init__(self, name, port, server_name):
		base.__init__(self, name, port, 'server')

		self.server_name = 'server/' + server_name
		print(self.server_name)
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.sock.bind((self.name, self.port))
		
		
		
		
		self.client_list = []
		self.server_list = []
	

	def begin(self):
		threading.Thread(target = self.connectionManager,args = ()).start()
		
		self.userInput()
		
	
	
		
	def connectionManager(self):
		self.sock.listen(5)
	
		while self.close_self_flag:
			
			connection, address = self.sock.accept()
			
	
			#receive intitial name
			try:
				connection_info = connection.recv(self.size).decode('utf-8')
				connection_info = connection_info.split("/")
				connection_type = connection_info[0]
				connection_name = connection_info[1]
			
				
	
			
				connection.settimeout(60)
				
				if connection_type == 'client':
					self.client_list.append([connection, connection_name])
					threading.Thread(target = self.listenToClient,args = (connection, address, connection_name)).start()
					print('Client:', connection_name, connection, address)
				
							
				if connection_type == 'server':
					if not (any(connection_name in server for server in self.server_list)):
						self.server_list.append([connection, connection_name])
						threading.Thread(target = self.listenToServer,args = (connection, address, connection_name)).start()
						print('Server:', connection_name, connection, address)
			
			except:
				print(connection, ' does not conform to the '/' protocol .')
			

		
			
	def listenToClient(self, client, address, client_name):
		
		
		while self.close_self_flag:
			try:
				data = client.recv(self.size).decode('utf-8')
				
				if data:
					# Set the response to echo back the recieved data 
					print(client_name, 'sent a message:', data)
					string = str(datetime.datetime.now())
					client.send(string.encode())
					
				else:
					raise error(client_name, 'has disconnected')
			except:
				client.close()
				return False
		
		client.close()
		
	def listenToServer(self, server, address, server_name):
					
		while self.close_self_flag:
			try:
				data = server.recv(self.size).decode('utf-8')
				
				if data:
					# Set the response to echo back the recieved data 
					print(server_name, 'sent a message:', data)
					string = str(datetime.datetime.now())
					server.send(string.encode())
					
				else:
					raise error(server_name, 'has disconnected')
			except:
				server.close()
				return False
		
		server.close()
		
			
	def userInput(self):
		try:
			while self.close_self_flag:
				message = (input(""))
				parsed_message = message.split("/")
				
				#print('Sending {!r}'.format(message))
				if parsed_message[0] == 'shutdown':
				
					self.close_self_flag = 0
					
					for client in self.client_list:
						client[0].close()
						
					self.sock.close()
					
					sys.exit(0)
					break

				elif parsed_message[0] == 'scan':
					self.portScanner()
					
				elif parsed_message[0] == 'connect':
					port = int(parsed_message[1])
					self.connectToServer(port)
					#threading.Thread(target = self.connectToServer,args = (port)).start()
					
					
				elif parsed_message[0] == 'cbroadcast':
					for client in self.client_list:
						client[0].send(parsed_message[1].encode())
						
				elif parsed_message[0] == 'sbroadcast':
					for server in self.server_list:
						server[0].send(parsed_message[1].encode())		
				
				elif parsed_message[0] == 'clist':
					print ('Client List:')
					for client in self.client_list:
						print(client[0])
				elif parsed_message[0] == 'slist':
					print ('Server List:')
					for server in self.server_list:
						print(server[0])
				
		
		finally:
			print('Shutting down...')
			
	def portScanner(self):
		try:
			for port in range(8080,8090):
				if(port != self.port):
					sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			
					result = sock.connect_ex(('localhost', port))
					
					if result == 0:
						
						print ("Port {", format(port), "]:  Open")
						sock.sendall(self.server_name.encode())
						
						sock.close()

		except KeyboardInterrupt:
			print ("You pressed Ctrl+C")
			sys.exit()

		except socket.gaierror:
			print ('Hostname could not be resolved. Exiting')
			sys.exit()

		except socket.error:
			print ("Couldn't connect to server")
			sys.exit()

			
	def connectToServer(self, port):
		try:
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

			result = sock.connect(('localhost', port))
			
			# FIX
			# self.server_list.append([connection, connection_name])
			
			sock.sendall(self.server_name.encode())
			
			
	
		except KeyboardInterrupt:
			print ("You pressed Ctrl+C")
			sys.exit()

		except socket.gaierror:
			print ('Hostname could not be resolved. Exiting')
			sys.exit()

		except socket.error:
			print ("Couldn't connect to server")
			sys.exit()
	
if __name__ == "__main__":
	
	while True:
		port_num = input("Port? ")
		try:
			port_num = int(port_num)
			break
		except ValueError:
			pass
	
	
	basicServer('localhost', port_num, 'Server' + str(random.randint(1,101))).begin()