#socket_echo_server.py
import socket
import sys
import pickle
from BlockChain import TxBlock
from Transactions import Tx
    
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

        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(16)
            #print('received {!r}'.format(data))
            if data:
                #print('sending data back to the client')
                connection.sendall(data)
            else:
                #print('no data from', client_address)
                break
            all_data = all_data + data
        print("Unpickling block " + str(recd))
        newBlock = pickle.loads(all_data)
        newBlock.previousBlock = lastBlock
        if lastBlock != None:
            newBlock.previousHash = newBlock.computeHash()
        lastBlock = newBlock
        recd = recd + 1
        if recd > 2:
            break
    finally:
        pass
print(lastBlock.isvalid())
print(lastBlock.previousBlock.isvalid()) #This block is intentionally invalid
print(lastBlock.previousBlock.previousBlock.isvalid())
# Clean up the connection
        
connection.close()
