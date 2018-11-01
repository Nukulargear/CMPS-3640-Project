import socket
import sys
#import psycopg2
import datetime
from threading import *

# Database
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

class client(Thread):
	def __init__(self, socket, address):
		Thread.__init__(self)
		self.sock = socket
		self.addr = address
		self.close_client_flag = 1
		self.start()
		print('Connection Confirmation', client_address)

	def run(self):
		while self.close_client_flag:
			data = client_socket.recv(1024).decode()
			if data == 'shutdown':
				print('Closing Client...')
				self.close_client_flag = 0
				self.sock.close()
				break
				
			print('Client Message:', data)
			string = str(datetime.datetime.now())
			self.sock.send(string.encode())

		

#Create a TCP/IP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Connect the socket to the port where the client will send and listen
server_address = ('localhost', 10000)
#different way of printing
print('Setting up Server on {} port {}'.format(*server_address))

server_socket.bind(server_address)

server_socket.listen(1)

serverCloseFlag = 1

while serverCloseFlag:
	# Wait for a connection)
	client_socket, client_address = server_socket.accept()
	client(client_socket, client_address)
