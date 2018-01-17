from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import pickle

class CBlock:
   data = None
   previousHash = None
   previousBlock = None
   def computeHash(self):
      digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
      #TODO bytes only works for strings?
      thedata = self.data
      if type(thedata) == type("Hello"):
         thedata = bytes(thedata, 'utf-8') 
      digest.update(thedata)
      return digest.finalize()

   def __init__(self, _data, previousBlock):
      self.data = _data
      if previousBlock != None:
         self.previousHash = previousBlock.computeHash()
      self.previousBlock = previousBlock
 


if __name__ == "__main__":
   root = CBlock("This is the root block", None)
   b1 = CBlock("This is the second block", root) 
   b2 = CBlock(b"This block has data in bytes", b1) 
   b3 = CBlock(445, b2) 

   myfile = open("blockchain.dat", "wb")
   pickle.dump(b3, myfile)

   
