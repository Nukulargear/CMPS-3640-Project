from base import * 

# Things to do:
# GUI integration
# sharing of global client list
#

# command list:
# scan - scans all ports in the local network
# connect {port} - connects to a specific sever port
# sbroadcast {message} - server broadcast message
# cbroadcast {message} - client broadcast message
# serverlist - shows all connect servers
# clientlist - shows all connected clients
# shutdown

#server port range
min_port_range = 8080
max_port_range = 8090

temporary_con =  ['servername','send_port','listen_port', 00000]

def connectDatabase():

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



class Server(base):
	def __init__(self, name, port, server_name):
		base.__init__(self, name, port, 'server')

		self.own_server_name = server_name #inconsistency for now
		self.server_name = 'server/' + server_name
		print(self.server_name)
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.sock.bind((self.name, self.port))
		
		#list for clients
		self.client_list = []
		#dictionary for server
		self.server_list = {}
		
		
		#local client list to be combined with global 
		self.local_client_list = []
		
		#global client list
		self.global_client_list = []
		
		#temporary container for connection information
		self.temporary_connection  = temporary_con

		#network flags
		self.server_write_flag = 0
		self.other_server_write_flag = 0 #if it is 1, then current server cannot send its curren client list.
		
		
		
	def begin(self):
		threading.Thread(target = self.connectionManager,args = ()).start()
		threading.Thread(target = self.autoPortConnect,args = ()).start()
		self.userInput()
		
	def connectionManager(self):
		self.sock.listen(5)
	
		while self.close_self_flag:
			
			connection, address = self.sock.accept()
		
			connection_command_value = None
			connection_command = None
		
			#receive intitial name
			try:
				
				connection_info = connection.recv(self.size).decode('utf-8')
				connection_info = connection_info.split("/")
		
				
				try:
					connection_command_value = connection_info[3]	
				except:
					pass
				
				try:
					connection_command = connection_info[2]	
				except:
					pass
					
			
				connection_name = connection_info[1]
				connection_type = connection_info[0]
			
		
				#connection.settimeout(60)
				
				if connection_type == 'client':
					self.client_list.append([connection, connection_name])
					self.global_client_list.append(connection_name)
				
					
					
					threading.Thread(target = self.listenToClient,args = (connection, address, connection_name)).start()
					print('Client connection received:', connection_name, connection, address)
					
					#inform all the servers that this server wants to update the global list
					
					self.server_write_flag = 1
					
					#print(bool(self.server_write_flag),  not self.other_server_write_flag)
				
							
				if connection_type == 'server':
		
					if connection_name not in self.server_list:

						threading.Thread(target = self.listenToServer,args = (connection, address, connection_name)).start()
						print('Server connection received:', connection_name, connection, address)
						
						#now connect to the server as well to make it a two way connection
						
						self.temporary_connection[0] = connection_name 						
						self.temporary_connection[2] = connection 
						
						if connection_command == 'connect':
							threading.Thread(target = self.connectToServer,args = (int(connection_command_value), 'end_handshake')).start()
						else:
							self.server_list[self.temporary_connection[0]] = (self.temporary_connection[1], self.temporary_connection[2], self.temporary_connection[3])
							self.temporary_connection  = temporary_con
			except:
				#ignore messages that do not comply with the / protocol
				pass
			

		
			
	def listenToClient(self, client, address, client_name):
		
		while self.close_self_flag:
			try:
				data = client.recv(self.size).decode('utf-8')
				
				if data:
					# Set the response to echo back the recieved data 
					print(client_name, ':', data)
			
					# propagating message to other servers
					message = 'client/' + str(client_name) + '/' + str(data)
					#print('Sending Message to Servers:', message)
					for socket in self.server_list.values():
						socket[0].sendall(message.encode())
						
					message = str(client_name) + ': ' + str(data)
					#print('Sending to local clients:', message)					
					for send_client in self.client_list:
						send_client[0].send(message.encode())
					
				else:
					raise error(client_name, 'has disconnected')
			except:
			
			
				self.client_list.remove([client, client_name])
				self.global_client_list.remove(client_name)
				
				client.close()
				return False
		

		client.close()
	
	def listenToServer(self, server, address, server_name):
					
		while self.close_self_flag:
		
			message_source = None
			message_type_source = None
			message_content = None
		
			try:
				data = server.recv(self.size).decode('utf-8')
				
			
				
				if data:
					try:
						message_data = data.split("/")
						message_source = message_data[0]
						message_type_source = message_data[1]
						message_content = message_data[2]
					except:
						pass
						
					#used for server communiation
					if message_type_source == 'update':

						print(server_name, 'is now', message_content)
						self.other_server_write_flag = 1
						
						print(self.own_server_name, 'is now locked')
						
						message = 'server/lock/' + str(self.own_server_name) + ' is now locked'
						
						for socket in self.server_list.values():
							socket[0].sendall(message.encode())
						
						
						#update global client list	
						#send global client list
						print(self.own_server_name, 'has now finished updating the global client list.')
						self.other_server_write_flag = 0
						
							
						message = 'server/unlock/' + str(self.own_server_name) + ' is now unlocked' 
						
						for socket in self.server_list.values():
							socket[0].sendall(message.encode())
							
					elif message_type_source == 'unlock':
						print(message_content)
						self.other_server_write_flag = 0
						
						
						
					elif message_type_source == 'lock':
					
						print(message_content)
						self.other_server_write_flag = 1
						
					
					elif message_source == 'client':
						
						message = str(message_type_source) + ': ' + str(message_content)
						
						for client in self.client_list:
							client[0].send(message.encode())
					
					else:
						print(server_name, ':', data)
					
				else:
					raise error(server_name, 'has disconnected')
			except:
				print('Failure Occured')
				self.server_list.pop(server_name)
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
				threading.Thread(target = self.connectToServer,args = (port, 'initial_handshake')).start()
				
				
			elif parsed_message[0] == 'cbroadcast':
				for client in self.client_list:
					client[0].send(parsed_message[1].encode())
					
			elif parsed_message[0] == 'sbroadcast':
				for socket in self.server_list.values():
					socket[0].sendall(parsed_message[1].encode())
					
						
			elif parsed_message[0] == 'clientlist':
				print ('\nClient list:')
				for client in self.client_list:
					print(client[0], client[1])
					
			elif parsed_message[0] == 'serverlist':

				#print (self.server_list)
				for servername, connection_info, in self.server_list.items():
					print(servername, connection_info[2])
		
			
	def portScanner(self):
	

		try:
			for port in range(min_port_range,max_port_range):
				if(port != self.port):
					sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			
					result = sock.connect_ex(('localhost', port))
					
					if result == 0:
						
						print ("Port {", format(port), "]:  Open")
						#sock.sendall(self.server_name.encode())
						
						
						
						
						sock.close()

		except KeyboardInterrupt:
			print ("You pressed Ctrl+C")
			sys.exit()

		except socket.gaierror:
			print ('Hostname could not be resolved. Exiting')


		except socket.error:
			print ("Couldn't connect to server")
		
				
	def autoPortConnect(self):
		time.sleep(5)
		while self.close_self_flag:

			try:
				for port in range(min_port_range,max_port_range):
					if(port != self.port):
						connected_server_ports = []
						for servername, connection_info, in self.server_list.items():
							
							connected_server_ports.append(connection_info[2])
							
						sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				
						result = sock.connect_ex(('localhost', port))
						
						sock.close()
						if result == 0 and port not in connected_server_ports:

							#print ("Port {", format(port), "]:  Connecting")
							threading.Thread(target = self.connectToServer,args = (port, 'initial_handshake')).start()
					
									
									
			except socket.error:
				print ("Couldn't ping server.")
				
			time.sleep(5)
			
	def connectToServer(self, port, handshake_flag):
	

		try:
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			result = sock.connect(('localhost', port))
			
			
			
			if handshake_flag == 'initial_handshake':
			
				message = str(self.server_name) + '/connect/' + str(self.port) 
			
				
			else:
				message = self.server_name
				
				
			self.temporary_connection[1] = sock
			self.temporary_connection[3] = sock.getpeername()[1] 			
			
			if handshake_flag == 'end_handshake':
				self.server_list[self.temporary_connection[0]] = (self.temporary_connection[1], self.temporary_connection[2], self.temporary_connection[3])
				self.temporary_connection  = temporary_con
			
			
		
			sock.sendall(message.encode())
			
			print('Establishing connection with', sock)
			
			#handler for consistency changes
			while self.close_self_flag:
				time.sleep(self.sleep_timer)
				
				
				'''
				Start Here for Mutual Exclusion
				'''
				
				
				if  self.server_write_flag and not self.other_server_write_flag :
					message = str('server/update/requesting to lock.') 
					sock.sendall(message.encode())
					
					
					self.server_write_flag = 0
					
					
					
			'''
			add remove socket entry for server dict?
			'''
			
	
	
	
		except KeyboardInterrupt:
			print ("You pressed Ctrl+C")
			sys.exit()

		except socket.gaierror:
			print ('Hostname could not be resolved. Exiting')
			

		except socket.error:
			print ("Couldn't connect to:", sock)
			
	
if __name__ == "__main__":
	
	while True:
		port_num = input("Port? ")
		try:
			port_num = int(port_num)
			break
		except ValueError:
			pass
	
	
	Server('localhost', port_num, 'server' + str(random.randint(1,101))).begin()