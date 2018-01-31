from Transactions import Tx
from BlockChain import TxBlock
import Signatures as sig
from Miner import mine


pr1,pu1 = sig.generate_keys()
pr2,pu2 = sig.generate_keys()
pr3,pu3 = sig.generate_keys()

root=TxBlock()
Tx0=Tx()
Tx0.add_input(pu1,4)
Tx0.add_output(pu2,2)
Tx0.sign(pr1)

Block=TxBlock(root)
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

B2=TxBlock(Block)
Tx3=Tx()
Tx3.add_input(pu2,1)
Tx3.add_output(pu1,1)
Tx3.sign(pr2)
Block.addTx(Tx3)

mine(Block)
if not Block.isvalid():
    print("ERROR: Failed to find a valid nonce.")


if Block.isvalid(B2.previousHash):
    print("ERROR: Modified block hash still matches")
else:
    print("Tamper detected.")

B2.previousHash = Block.computeHash()
if Block.isvalid(B2.previousHash):
    print("Child block generates valid hash.")
else:
    print("ERROR: Child block has wrong hash.")


