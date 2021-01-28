# socket_echo_client.py
import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
host = 'localhost'
port=10000
if len(sys.argv) > 1:
    host,port = sys.argv[1].split(':')
    port = int(port)
server_address = (host,port)
print('connecting to {} port {}'.format(*server_address))
sock.connect(server_address)

try:

    # Send data
    #message = b'This is the message.  It will be repeated.'
    message = "Echo this message:"
    print('sending {!r}'.format(message))
    sock.sendall(message)

    # Look for the response
    amount_received = 0
    amount_expected = len(message)

    while amount_received < amount_expected:
        data = sock.recv(16)
        amount_received += len(data)
        print('received {!r}'.format(data))

finally:
    print('closing socket')
    sock.close()
