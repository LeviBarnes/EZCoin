#socket_echo_server.py
import socket
import sys
import pickle
from BlockChain import TxBlock
from Transactions import Tx
from EZCoinSocket import EasyCoinManifest, openServerSocket, recvNewBlock

lastBlock = None
recd = 0
sSocket = openServerSocket()

#Recv 3 blocks
for iter in range(3):
    newBlock = recvNewBlock(sSocket)
    newBlock.previousBlock = lastBlock
    if lastBlock != None:
        newBlock.previousHash = newBlock.computeHash()
    lastBlock = newBlock

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
        
