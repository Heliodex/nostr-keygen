out = open("output.txt", "a", encoding="utf-8")

import socket

# Make a basic socket server that pipes all incoming data to a file

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

port = 7654

# Bind the socket to the port
server_address = ("0.0.0.0", port)
print("starting up on %s port %s" % server_address)
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

while True:
	# Wait for a connection
	print("waiting for a connection")
	connection, client_address = sock.accept()

	try:
		print("connection from", client_address)

		# Receive the data in small chunks and retransmit it
		data = connection.recv(10**4)
		out.write(data.decode("utf-8"))

	except Exception as e:
		print(e)

