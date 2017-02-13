"""
Captures UDP telemetry packets for use by the Project CARS Replay
Enhancer. Run on the network to which Project CARS is broadcasting

Writes the packets to a directory named "packetdata" with an
appended timestamp. Each packet is named "pdata" with an appended
sequence number.

Stop telemetry packet capture by hitting CTRL+C.
"""
import datetime
import os
import socket


def main():
    # Create a new UDP socket.
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind the socket to the port
    server_address = ("", 5606)
    print("Starting listener on port {}".format(server_address[1]))
    udp_socket.bind(server_address)

    i = 0
    directory_name = "packetdata-"+datetime.datetime.now().strftime(
        "%Y%m%d-%H%M%S")
    try:
        if not os.path.exists(directory_name):
            os.makedirs(directory_name)
        while True:
            data, _ = udp_socket.recvfrom(65565)
            print("Writing packet {}".format(i))
            file = open('./'+directory_name+'/pdata'+str(i), 'wb')
            file.write(data)
            file.close()
            i += 1

    except KeyboardInterrupt:
        print("Closing listener on port {}".format(server_address[1]))

    finally:
        if i == 0:
            os.rmdir(directory_name)

if __name__ == '__main__':
    main()
