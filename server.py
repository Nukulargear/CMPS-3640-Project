import socket
import sys

#Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Connect the socket to the port where the client will send and listen
server_address = ('localhost', 10000)
#different way of printing
print('starting up on {} port {}'.format(*server_address))

sock.bind(server_address)

sock.listen(1)

serverCloseFlag = 1

while serverCloseFlag:
	# Wait for a connection
	print('waiting for a connection')
	connection, client_address = sock.accept()
	try:
		print('connection from', client_address)

		# Receive the data in small chunks and retransmit it
		while True:
			#amount of bytes sent per message
			data = connection.recv(100)
	
			
			if data:
						
				if data == b'shutdown':
					print('Closing Server...')
					serverCloseFlag = 0
					
				print('received {!r}'.format(data))
				print('sending data back to the client')
				connection.sendall(data)
			else:
				print('no data from', client_address)
				break
	
	#always executed before leaving the try statement
	finally:
		# Clean up the connection
		connection.close()