from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

class someClass:
   def __init__(self):
      self.foo = [1,2,3]
      self.bar = "Some message"
   def __bytes__(self):
      outbytes=bytes(0)
      for i in self.foo:
         outbytes = outbytes + bytes(str(i),'utf-8')
      outbytes = outbytes + bytes(self.bar,'utf-8')
      return outbytes
class CBlock:
   data = None
   previousHash = None
   previousBlock = None
   def computeHash(self):
      digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
      #TODO bytes only works for strings?
      thedata = self.data
      thedata = bytes(str(thedata),'utf-8')
      digest.update(thedata)
      return digest.finalize()

   def __init__(self, _data, previousBlock):
      self.data = _data
      if previousBlock != None:
         self.previousHash = previousBlock.computeHash()
      self.previousBlock = previousBlock

class TxBlock(CBlock):
   def __init__(self, previousBlock=None):
      nonce = 'aaaaaaaaaaaaaaaaa'
      self.data = [nonce]
      if previousBlock != None:
         self.previousHash = previousBlock.computeHash()
      self.previousBlock = previousBlock
   def addTx(self, tx_in):
      self.data.append(tx_in)
   def newNonce(self, _nonce):
      self.data[0] = _nonce
   def isvalid(self, check_hash=None):
      valid = True
      for tx in self.data[1:]:
         if not tx.isvalid():
            valid = False
      if check_hash != None and self.computeHash() != check_hash:
         valid = False
      #One leading zero
      if self.computeHash()[0] != 0:
         valid = False
      return valid

      
 


if __name__ == "__main__":
   root = CBlock(b"This is the root block", None)
   b1 = CBlock("This is the second block", root) 
   b2 = CBlock(someClass(), b1) 
   b3 = CBlock(445, b2)
   b4 = CBlock("Can we hash a non-string?", b3)

   if b3.previousBlock.previousBlock.computeHash() != b3.previousBlock.previousHash:
      print("ERROR: Bad hashes")
   else:
      print("Passed.")

   
