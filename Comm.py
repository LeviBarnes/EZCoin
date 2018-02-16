from EZCoinSocket import newClientSocket, newServerSocket
from EZCoinSocket import recvNewObject, sendMessage 
from Transactions import Tx
from BlockChain import TxBlock
from socket import SHUT_RDWR

class Comm:
   def __init__(self):
      self.sSock = newServerSocket()
   def loop(self,newTxQueue, newBlockQueue, outQueue):
      task = None
      while True:
         if not outQueue.empty():
            toSend = outQueue.get()
            if toSend == None:
               return
            self.cSock = newClientSocket(10002)
            if self.cSock != None:
               sendMessage(toSend, self.cSock)
               self.cSock.shutdown(SHUT_RDWR)
               self.cSock.close()
         newObj = recvNewObject(self.sSock)
         if type(newObj) == Tx:
            newTxQueue.put(newObj)
         if type(newObj) == TxBlock:
            newBlockQueue.put(newObj)
   def __del__(self):
      self.sSock.close()
 
         
         
