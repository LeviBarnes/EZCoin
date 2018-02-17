from Transactions import Tx
from BlockChain import TxBlock
from Comm import startComm
import multiprocessing as mp
from EZCoinSocket import newServerSocket, recvNewObject
import time

if __name__ == '__main__':
    
    sendQueue = mp.Queue()
    TxQueue = mp.Queue()
    BlockQueue = mp.Queue()

    Tx1 = Tx()
    Tx1.add_input('hgety',123)
    sendQueue.put(Tx1)
    Tx2 = Tx()
    Tx2.add_input('qteru',456)
    sendQueue.put(Tx2)
    time.sleep(2)
    p = mp.Process(target=startComm, args=(TxQueue, BlockQueue, sendQueue,10017,))
    p.start()
    sSock = newServerSocket(10017)


    print ("rec'd " + str(recvNewObject(sSock)))
    time.sleep(10)
    print ("rec'd " + str(recvNewObject(sSock)))
    Tx3=Tx()
    Tx3.add_reqd('ahsdyuioywer')
    sendQueue.put(Tx3)
    sendQueue.put(None)
    p.join()
    sSock.close()


