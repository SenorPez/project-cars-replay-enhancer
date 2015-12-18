import socket
import sys

# Create a new UDP socket.
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
server_address = ("", 5606)
print >> sys.stderr, 'Starting listener on port %s' % server_address[1]
sock.bind(server_address)

i = 0;
while True:
	data, address = sock.recvfrom(65565)
	print >> sys.stderr, 'Writing packet #%s' % i
	f = open('./packetdata/pdata'+str(i), 'w')
	f.write(data)
	f.close()
	i+=1
