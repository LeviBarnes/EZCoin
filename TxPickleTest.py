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
