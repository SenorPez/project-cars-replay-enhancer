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
    SOCKET = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    SOCKET.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind the socket to the port
    SERVER_ADDRESS = ("", 5606)
    print("Starting listener on port {}".format(SERVER_ADDRESS[1]))
    SOCKET.bind(SERVER_ADDRESS)

    i = 0
    DIRECTORY = "packetdata-"+datetime.datetime.now().strftime(
        "%Y%m%d-%H%M%S")
    try:
        if not os.path.exists(DIRECTORY):
            os.makedirs(DIRECTORY)
        while True:
            DATA, _ = SOCKET.recvfrom(65565)
            print("Writing packet {}".format(i))
            FILE = open('./'+DIRECTORY+'/pdata'+str(i), 'wb')
            FILE.write(DATA)
            FILE.close()
            i += 1

    except KeyboardInterrupt:
        print("Closing listener on port {}".format(SERVER_ADDRESS[1]))

    finally:
        if i == 0:
            os.rmdir(DIRECTORY)

if __name__ == '__main__':
    main()
