from base import * 

# Things to do:
# GUI
# Server Promotion
#

# command list:
# scan - scans all ports in the local network
# connect {port} - connects to a specific sever port
# sbroadcast {message} - server broadcast message
# cbroadcast {message} - client broadcast message
# serverlist - shows all connect servers
# clientlist - shows all connected clients
# shutdown

#sockets are listening ports one to many

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
# new class as it was difficult to manage the connections
class serverConnection():
	def __init__(self):
		self.server_name = 'test'
		self.listen_socket = None
		self.send_socket = None

	def __repr__(self): #sorting/debugging
		return str(self.server_name)	


class Server(base):
	def __init__(self, name, port, server_name):
		base.__init__(self, name, port, 'server')

		self.server_name = 'server/' + server_name
		print(self.server_name)
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.sock.bind((self.name, self.port))
		
		
		
		
		self.client_list = []
		#self.server_list = []
		self.server_receive_list = []
		self.server_send_list = []

	def begin(self):
		threading.Thread(target = self.connectionManager,args = ()).start()
		
		self.userInput()
		
	
	
		
	def connectionManager(self):
		self.sock.listen(5)
	
		while self.close_self_flag:
			
			connection, address = self.sock.accept()
		
			
			connection_port = None
	
			#receive intitial name
			try:
				
				connection_info = connection.recv(self.size).decode('utf-8')
				connection_info = connection_info.split("/")
		
		
				try:
					connection_port = connection_info[2]	
				except:
					pass
					
			
				connection_name = connection_info[1]
				connection_type = connection_info[0]
			
		
				#connection.settimeout(60)
				
				if connection_type == 'client':
					self.client_list.append([connection, connection_name])
					threading.Thread(target = self.listenToClient,args = (connection, address, connection_name)).start()
					print('Client connection received:', connection_name, connection, address)
				
							
				if connection_type == 'server':
					if not (any(connection_name in server for server in self.server_receive_list)):
						self.server_receive_list.append([connection, connection_name])
						threading.Thread(target = self.listenToServer,args = (connection, address, connection_name)).start()
						print('Server connection received:', connection_name, connection, address)
						
						#now connect to the server as well to make it a two way connection
						
						if connection_port != None:
							threading.Thread(target = self.connectToServer,args = (int(connection_port), '')).start()
			
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
				self.client_list.remove([client, client_name])
				#self.client_list = [i for i in self.client_list if i[1] != client_name]
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
				self.server_receive_list.remove([server, server_name])
				server.close()
				return False
		
		server.close()
		
			
	def userInput(self):
	
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
				#self.connectToServer(port)
				threading.Thread(target = self.connectToServer,args = (port, 'handshake')).start()
				
				
			elif parsed_message[0] == 'cbroadcast':
				for client in self.client_list:
					client[0].send(parsed_message[1].encode())
					
			elif parsed_message[0] == 'sbroadcast':
				for server in self.server_send_list:
					try:
						server.sendall(parsed_message[1].encode())
					except:
						self.server_send_list.remove(server)
						print('Failed to send message to:', server)
						
			elif parsed_message[0] == 'clientlist':
				print ('\nClient list:')
				for client in self.client_list:
					print(client[0], client[1])
					
			elif parsed_message[0] == 'serverlist':
				print ('\nServer listen list:')
				for server in self.server_receive_list:
					print(server[0])
				print ('\nServer send list:')
				for server in self.server_send_list:
					print(server)
					
			
		

			
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

			
	def connectToServer(self, port, handshake_flag):
	
	#make to thread, and terminate when remote server shuts down
	
		try:
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			result = sock.connect(('localhost', port))
			
			self.server_send_list.append(sock)
			
			if handshake_flag == 'handshake':
				message = str(self.server_name) + '/' + str(self.port) 
				
			else:
				message = self.server_name
				
		
			#print(message)
		
			sock.sendall(message.encode())
			
			print('Establishing connection with', sock)
			
			
			while self.close_self_flag:
				time.sleep(self.sleep_timer)
				string = 'Server keep alive thread'
				sock.sendall(string.encode())
				
			self.server_send_list.remove(sock)		
	
	
	
		except KeyboardInterrupt:
			print ("You pressed Ctrl+C")
			sys.exit()

		except socket.gaierror:
			print ('Hostname could not be resolved. Exiting')
			

		except socket.error:
			self.server_send_list.remove(sock)		
			print ("Couldn't connect to:", sock)
			
	
if __name__ == "__main__":
	
	while True:
		port_num = input("Port? ")
		try:
			port_num = int(port_num)
			break
		except ValueError:
			pass
	
	
	Server('localhost', port_num, 'Server' + str(random.randint(1,101))).begin()