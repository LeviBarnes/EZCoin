from Transactions import Tx
from BlockChain import TxBlock
from Comm import Comm
import multiprocessing as mp
from EZCoinSocket import newServerSocket, recvNewObject
import time
myComm = Comm()

sendQueue = mp.Queue()
TxQueue = mp.Queue()
BlockQueue = mp.Queue()

p = mp.Process(target=myComm.loop, args=(TxQueue, BlockQueue, sendQueue,))
Tx1 = Tx()
Tx1.add_input('hgety',123)
Tx2 = Tx()
Tx2.add_input('qteru',456)
sSock = newServerSocket(10002)
p.start()
time.sleep(10)
sendQueue.put(Tx1)

print ("rec'd " + str(recvNewObject(sSock)))
sendQueue.put(Tx2)
sendQueue.put(None)
time.sleep(20)
print ("rec'd " + str(recvNewObject(sSock)))
p.join()


