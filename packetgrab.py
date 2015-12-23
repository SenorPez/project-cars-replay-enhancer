import datetime
import os
import socket
import sys

# Create a new UDP socket.
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
server_address = ("", 5606)
print >> sys.stderr, 'Starting listener on port %s' % server_address[1]
sock.bind(server_address)

i = 0;
directory = "packetdata-"+datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
if not os.path.exists(directory):
	os.makedirs(directory)
while True:
	data, address = sock.recvfrom(65565)
	print >> sys.stderr, 'Writing packet #%s' % i
	f = open('./'+directory+'/pdata'+str(i), 'w')
	f.write(data)
	f.close()
	i+=1
