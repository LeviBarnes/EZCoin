# socket_echo_client.py
import socket
import sys
import pickle
from BlockChain import TxBlock
import Signatures
from Transactions import Tx
from Miner import mine

class EasyCoinManifest:
    def __init__(self, obj):
        self.kind = type(obj)
        self.sz = len(pickle.dumps(obj))

#Makes some blocks, then sends them via socket
pr1,pu1 = Signatures.generate_keys()
pr2,pu2 = Signatures.generate_keys()
pr3,pu3 = Signatures.generate_keys()
pr4,pu4 = Signatures.generate_keys()

Tx1 = Tx()
Tx1.add_input(pu1,3)
Tx1.add_output(pu2,2.8)
Tx1.add_output(pu4,0.2)
Tx1.sign(pr1)

B1 = TxBlock()
B1.addTx(Tx1)

Tx2 = Tx()
Tx2.add_input(pu1,3)
Tx2.add_output(pu2,2.8)
Tx2.add_output(pu4,0.2)
Tx2.sign(pr1)

B2 = TxBlock()
B2.addTx(Tx2)

Tx3 = Tx()
Tx3.add_input(pu3,0.2)
Tx3.add_input(pu4,0.2)
Tx3.add_output(pu2,0.4)
Tx3.sign(pr3)
B2.addTx(Tx3)

Tx4 = Tx()
Tx4.add_input(pu1,0.4)
Tx4.add_output(pu2,0.4)
Tx4.sign(pr1)

B3 = TxBlock()
B3.addTx(Tx4)

for B in [B1,B2,B3]:
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    server_address = ('localhost', 10000)
    print('connecting to {} port {}'.format(*server_address))
    sock.connect(server_address)

    #Mine for a valid nonce
    mine(B)
    try:

        # Send manifest
        message = pickle.dumps(EasyCoinManifest(B))
        print('sending {!r}',format(message))
        sock.sendall(message)

        # Recv acknowledgement
        data = sock.recv(8)
        if data != b"ACK_MFST":
            raise RuntimeError("No acknowledgement from server")
        # Send data
        message = pickle.dumps(B)
        print('sending {!r}'.format(message))
        sock.sendall(message)

        data = sock.recv(8)
        if data != b"ACK_MMSG":
            raise RuntimeError("No acknowledgment from server")

#        # Look for the response
#        amount_received = 0
#        amount_expected = len(message)

#        while amount_received < amount_expected:
#            data = sock.recv(4)
#            amount_received += len(data)
#            print('received {!r}'.format(data))

    finally:
        print('closing socket')
        sock.close()
