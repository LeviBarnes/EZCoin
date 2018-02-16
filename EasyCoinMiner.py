# socket_echo_client.py
import sys
from BlockChain import TxBlock
import Signatures
from Transactions import Tx
from Miner import mine
from EZCoinSocket import EasyCoinManifest, newClientSocket, sendMessage 
 

#Makes some blocks, then sends them via socket
pr1,pu1 = Signatures.generate_keys()
pr2,pu2 = Signatures.generate_keys()
pr3,pu3 = Signatures.generate_keys()
pr4,pu4 = Signatures.generate_keys()

#Tx1 is a valid, signed transaction
Tx1 = Tx()
Tx1.add_input(pu1,3)
Tx1.add_output(pu2,2.8)
Tx1.add_output(pu4,0.2)
Tx1.sign(pr1)

#B1 is a valid block. It's root
B1 = TxBlock(None)
B1.addTx(Tx1)

#Tx2 is a valid Tx
Tx2 = Tx()
Tx2.add_input(pu1,3)
Tx2.add_output(pu2,2.8)
Tx2.add_output(pu4,0.2)
Tx2.sign(pr1)

B2 = TxBlock(None)
B2.addTx(Tx2)

#Tx2 is invalid since it's not signed with pr4
Tx3 = Tx()
Tx3.add_input(pu3,0.2)
Tx3.add_input(pu4,0.2)
Tx3.add_output(pu2,0.4)
Tx3.sign(pr3)
#So, B2 is an invalid block
B2.addTx(Tx3)

#Tx4 and B3 are valid
Tx4 = Tx()
Tx4.add_input(pu1,0.4)
Tx4.add_output(pu2,0.4)
Tx4.sign(pr1)

B3 = TxBlock(None)
B3.addTx(Tx4)

cSocket = newClientSocket()
sendMessage(Tx4, cSocket)

for B in [B1,B2,B3]:
    #Mine for a valid nonce
    mine(B)
    try:
        cSocket = newClientSocket()
        sendMessage(B, cSocket)
    finally:
        print('closing socket')
        cSocket.close()
