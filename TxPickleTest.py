import Signatures
from Transactions import Tx

pr1,pu1 = Signatures.generate_keys()
pr2,pu2 = Signatures.generate_keys()

Tx1=Tx()
Tx1.add_input(pu1, 2.4)
Tx1.add_output(pu2,2.34)
Tx1.sign(pr1)
print (Tx1.isvalid())

import pickle
try:
    foo = pickle.dumps(Tx1)
    print ("Successfully pickled Tx1")
except:
    print("Couldn't pickle Tx1")

import json
try:
    bar = json.dumps(Tx1)
    print ("Successfully json serialized Tx1")
except:
    print("Couldn't json serialize Tx1")

from BlockChain import TxBlock

B = TxBlock()
B.addTx(Tx1)

Tx2 = Tx()
Tx2.add_input(pu1, 1)
Tx2.add_output(pu2, 1.4)
Tx2.sign(pr1)
B.addTx(Tx2)

try:
    foo = pickle.dumps(B)
    print ("Successfully pickle serialized block B")
except:
    print("Couldn't pickle serialize a block")
print(B)

