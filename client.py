import socket
import sys

#Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 10000)
print('connecting to {} port {}'.format(*server_address))
print('To close the server, send [shutdown]')
sock.connect(server_address)

try:
	# Send data
	#message = b'This is the message.  It will be repeated.'	
	message = (input("Please enter your message: "))
	
	print('sending {!r}'.format(message))
	sock.sendall(message.encode())
	# Look for the response
	amount_received = 0
	amount_expected = len(message)
	
	while amount_received < amount_expected:
		#amount of bytes sent
		data = sock.recv(100)
		amount_received += len(data)
		print('received {!r}'.format(data))
		
finally:
	print('closing socket')
	sock.close()