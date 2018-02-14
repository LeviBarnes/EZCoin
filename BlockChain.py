from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from Signatures import public_key_to_ssl
from cryptography.hazmat.backends.openssl.rsa import _RSAPublicKey

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
      """
      CBlock.computeHash() -> hash (bytes)

      Computes the SHA-256 hash of the block and returns it
      """
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
   def __init__(self, previousBlock):
      nonce = 'aaaaaaaaaaaaaaaaa'
      super(TxBlock, self).__init__([nonce], previousBlock)
   def addTx(self, tx_in):
      """
      TxBlock.addTx(Tx)

      Adds the given transaction to the block.
      """
      self.data.append(tx_in)
   def newNonce(self, _nonce):
      """
      TxBlock.newNonce(_nonce)

      Replaces the block nonce with the new nonce
      _nonce can be any data that can be cast as a string
      """
      self.data[0] = _nonce
   def isvalid(self,chkhash=None):
      """
      TxBlock.isvalid() -> bool

      Checks the transactions and nonce of the block
      Return True for a valid block
      """
      #TODO Allow miner to take transaction fees
      # sum of *all* inputs from *all* tx's must still be >= sum of
      # *all* outputs - the mining reward
      valid = True
      for tx in self.data[1:]:
         if not tx.isvalid():
            valid = False
      if self.computeHash()[0] != 0:
         valid = False
      if chkhash != None and self.computeHash() != chkhash:
         valid = False
      return valid

   def getBalance(self, public):
      """
      TxBlock.getBalance(public) -> float

      Finds the balance for the given public key accounting to transactions
      in the block plus all ancestor blocks.
      """
      if type(public) == _RSAPublicKey:
         public = public_key_to_ssl(public)
      thisblock = self
      balance = 0
      #print("Getting balance for " + str(public[-15:]))
      while thisblock != None:
         for tx in thisblock.data[1:]:
            for i in tx.inputs:
               #print("Input: " + str(i[1]) + " from " + str(i[0][-15:]))
               if i[0] == public:
                  #print ("Subtracting " + str(i[1]))
                  balance = balance - i[1]
            for o in tx.outputs:
               #print("Input: " + str(o[1]) + " to " + str(o[0][-15:]))
               if o[0] == public:
                 #print ("Adding " + str(o[1]))
                 balance = balance + o[1]
         thisblock = thisblock.previousBlock
      return balance

      
 


if __name__ == "__main__":
   root = CBlock(b"This is the root block", None)
   b1 = CBlock("This is the second block", root) 
   b2 = CBlock(someClass(), b1) 
   b3 = CBlock(445, b2)
   b4 = CBlock("Can we hash a non-string?", b3)

   if b3.previousBlock.previousBlock.computeHash() != b3.previousBlock.previousHash:
      print("ERROR: Bad hashes")
   else:
      print("CBlock Passed.")
      
   import Signatures
   import Transactions

   pr1, pu1 = Signatures.generate_keys()
   pr2, pu2 = Signatures.generate_keys()
   pr3, pu3 = Signatures.generate_keys()
   pr4, pu4 = Signatures.generate_keys()
   
   root = TxBlock(None)

   Tx1 = Transactions.Tx()
   Tx1.add_input(pu1, 1)
   Tx1.add_output(pu2, 1)
   Tx1.sign(pr1)
   root.addTx(Tx1)

   Tx2 = Transactions.Tx()
   Tx2.add_input(pu2, 0.8)
   Tx2.add_output(pu3, 0.75)
   Tx2.sign(pr2)
   root.addTx(Tx2)

   Tx3 = Transactions.Tx()
   Tx3.add_output(pu4, 2.25)
   root.addTx(Tx3)

   B1 = TxBlock(root)

   Tx4 = Transactions.Tx()
   Tx4.add_input(pu4, 1.5)
   Tx4.add_output(pu1,1.35)
   Tx4.sign(pr4)

   Tx5 = Transactions.Tx()
   Tx5.add_input(pu4,2.1)
   Tx5.add_output(pu2,2.0)
   Tx5.sign(pr4)

   Tx6 = Transactions.Tx()
   Tx6.add_input(pu2, 1.05)
   Tx6.add_output(pu3,1.0)
   Tx6.sign(pr2)
   B1.addTx(Tx4)
   B1.addTx(Tx5)
   B1.addTx(Tx6)

   if abs(B1.getBalance(pu4) +1.35) > 0.001:
      print ("ERROR! Wrong balance ("+ str(B1.getBalance(pu4)) +") for pu4")
   else:
      print ("Right balance ("+ str(B1.getBalance(pu4)) +") for pu4")

   if abs(B1.getBalance(pu2) - 1.15) > 0.001:
      print ("ERROR! Wrong balance ("+ str(B1.getBalance(pu2)) +") for pu2")
   else:
      print ("Right balance ("+ str(B1.getBalance(pu2)) +") for pu2")
   
