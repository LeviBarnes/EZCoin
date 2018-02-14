#socket_echo_server.py
import socket
import sys
import pickle
from BlockChain import TxBlock
from Transactions import Tx
from EZCoinSocket import EasyCoinManifest, openServerSocket, recvNewObject


def handleTx(newTx, Tx_list):
    Tx_list.append(newTx)

def handleBlock(newBlock, lastBlock):
    newBlock.previousBlock = lastBlock
    if lastBlock != None:
        newBlock.previousHash = newBlock.computeHash()
    lastBlock = newBlock
    return lastBlock
    

Tx_list = []
lastBlock = None
recd = 0
sSocket = newServerSocket()

#Recv 4 objects
for iter in range(4):
    newObj = recvNewObject(sSocket)
    if type(newObj) == Tx:
        handleTx(newObj, Tx_list)
    elif type(newObj) == TxBlock:
        lastBlock = handleBlock(newObj, lastBlock)
    else:
        raise RuntimeError("Object sent is neither transaction nor block.")
        exit()

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
        
