from Transactions import Tx
from BlockChain import TxBlock
import Signatures as sig



pr1,pu1 = sig.generate_keys()
pr2,pu2 = sig.generate_keys()
pr3,pu3 = sig.generate_keys()

Block=TxBlock()
Tx1=Tx()
Tx1.add_input(pu1,1)
Tx1.add_output(pu2,0.33)
Tx1.add_output(pu3,0.66)
Tx1.sign(pr1)

Block.addTx(Tx1)

Tx2=Tx()
Tx2.add_input(pu3,2)
Tx2.add_output(pu2,2)
Tx2.sign(pr3)

Block.addTx(Tx2)

for q in range(128*128):
    n = q//128
    m = q%128
    Block.newNonce(bytes([n,m]).decode())
    thisHashZero = Block.computeHash()[0]
    if thisHashZero==0:
        print("Hash leads with zero for nonce " + str(n) + ", " + str(m))
    if Block.isvalid():
        print("Found a block!")
        print("Nonce = '" + bytes([n,m]).decode()+"'("+str(n)+", "+str(m)+")")
        break


