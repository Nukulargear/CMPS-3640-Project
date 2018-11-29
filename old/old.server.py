import socket
import sys
import queue
#import psycopg2
import datetime
import threading
from _thread import *

# Database
# Things to do:
# GUI
# Server Promotion
# Keep Alive


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

class ThreadedServer(object):
	def __init__(self, host, port):
		self.host = host
		self.port = port
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.sock.bind((self.host, self.port))
		print('Server is up and running.')

	def listen(self):
		self.sock.listen(5)
		while True:
			client, address = self.sock.accept()
			client.settimeout(60)
			threading.Thread(target = self.listenToClient,args = (client,address)).start()
		
			
	def listenToClient(self, client, address):
		size = 1024
		while True:
			try:
				data = client.recv(size)
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

if __name__ == "__main__":
	while True:
		port_num = input("Port? ")
		try:
			port_num = int(port_num)
			break
		except ValueError:
			pass

	ThreadedServer('',port_num).listen()