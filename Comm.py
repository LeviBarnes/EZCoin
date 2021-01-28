from EZCoinSocket import newClientSocket, newServerSocket
from EZCoinSocket import recvNewObject, sendMessage 
from Transactions import Tx
from BlockChain import TxBlock
from socket import SHUT_RDWR


class Comm:
   def __init__(self,cSockNum=None):
      self.sSock = newServerSocket()
      self.cSock = None
      peers = []
      self.cSockNum = cSockNum
   def addPeer(new_peer):
      peers.append(new_peer)
   def loop(self, newTxQueue, newBlockQueue, outQueue):
      task = None
      while True:
         if not outQueue.empty():
            toSend = outQueue.get()
            if toSend == None:
               return
            self.sSock.close()
            self.cSock = newClientSocket(self.cSockNum)
            if self.cSock != None:
               try:
                  sendMessage(toSend, self.cSock)
               except:
                  print("Send failed. No one received.")
               self.cSock.shutdown(SHUT_RDWR)
               self.cSock.close()
               self.cSock = None
            self.sSock = newServerSocket()
         newObj = recvNewObject(self.sSock)
         if type(newObj) == Tx:
            newTxQueue.put(newObj)
         if type(newObj) == TxBlock:
            newBlockQueue.put(newObj)
   def __del__(self):
      self.sSock.close()
      if self.cSock != None:
          self.cSock.close()
 
def startComm(TxQueue, BlockQueue, sendQueue, cSockNum=None):
   myComm = Comm(cSockNum)
   myComm.loop(TxQueue, BlockQueue, sendQueue)
   
         
