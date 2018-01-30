#socket_echo_server.py
import socket
import sys
import pickle
from BlockChain import TxBlock
from Transactions import Tx

class EasyCoinManifest:
    def __init__(self, obj):
        self.kind = type(obj)
        self.sz = len(pickle.dumps(obj))
    
lastBlock = None

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('localhost', 10000)
print('starting up on {} port {}'.format(*server_address))
sock.bind(server_address)

recd = 0
# Listen for incoming connections
sock.listen(1)
while True:
    # Wait for a connection
    print('waiting for a connection')
    connection, client_address = sock.accept()
    all_data = b""
    try:
        print('connection from', client_address)

        manifest_d = connection.recv(100)
        manifest = pickle.loads(manifest_d)
        expected = manifest.sz
        print ("Expecting a " +str(manifest.kind) + " of size " + str(expected))

        connection.send(b"ACK_MFST")
        data_in = 0
        # Receive the data in small chunks and retransmit it
        while data_in < expected:
            data = connection.recv(16)
            #print('received {!r}'.format(data))
            if data:
                #print('sending data back to the client')
                #connection.sendall(data)
                pass
            else:
                #print('no data from', client_address)
                break
            all_data = all_data + data
            data_in = data_in + len(data)
    finally:
        print ("received " + str(data_in) + " characters. Acknowledging...")
        connection.send(b"ACK_MMSG")
        print("Unpickling block ")
        newBlock = pickle.loads(all_data)
        newBlock.previousBlock = lastBlock
        if lastBlock != None:
            newBlock.previousHash = newBlock.computeHash()
        lastBlock = newBlock
        recd = recd + 1
        if recd > 2:
            break
if lastBlock.isvalid():
    print ("Top block is valid.")
else:
    print ("ERROR! Top block is invalid")

if lastBlock.previousBlock.isvalid(): #This block is intentionally invalid
    print ("ERROR! Invalid block marked valid")
else:
    print ("Bad block successfully detected")

if lastBlock.previousBlock.previousBlock.isvalid():
    print ("Root block is valid")
else:
    print ("ERROR! Root block is invalid")
# Clean up the connection
        
connection.close()
