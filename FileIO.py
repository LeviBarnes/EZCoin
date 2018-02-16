from BlockChain import CBlock
import pickle
import Signatures

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

def loadBC(filename):
   """
   loadBC(filename)

   Loads a blockchain from the given file
   """
   if not isinstance(filename, str):
      raise TypeError("Argument 0 to loadBC must be a string")
   # TODO support for passing a file object?

   myfile = open(filename, "rb")
   returnval = pickle.load(myfile)

   if not isinstance(returnval, CBlock):
      raise IOError("File " + filename + " does not contain a valid blockchain.")

   myfile.close()
   return returnval

def saveBC(filename, headBlock):
   """
   saveBC(filename, headBlock)

   Saves the block attached to headBlock to the given file
   """
   print (type(headBlock))
   if not isinstance(headBlock, CBlock):
      raise TypeError("Argument 1 to saveBC must be a CBlock")
   if not isinstance(filename, str):
      raise TypeError("Argument 0 to saveBC must be a string")
   myfile = open(filename, "wb")
   pickle.dump(headBlock, myfile)
   myfile.close()
   return

def saveKeys(filename, private, passwd = None):
   """
   saveKeys(filename, private, passwd = None)

   Saves the given private key to the given filename. passwd optional
   """
   pem = Signatures.private_key_to_pem(private, passwd)
   fout = open(filename, 'wb')
   pickle.dump(pem, fout)
   fout.close()
   
def loadKeys(filename, passwd = None):
   """
   loadKeys(filename, passwd = None) -> private, public

   Loads a private key from the given filename. passwd optional
   Also generates a public key. Returns both keys
   """
   fin = open(filename, 'rb')
   pem = pickle.load(fin)   
   private = Signatures.pem_to_private_key(pem, passwd)
   public = private.public_key()
   fin.close()
   return private, public

if __name__ == "__main__":
   import filecmp
   top = loadBC("loadtest_in.dat")

   tmp = top
   nblocks = 1
   err = False
   while tmp.previousBlock != None:
      nblocks = nblocks + 1
      if top.previousBlock.computeHash() != top.previousHash:
         print ("Bad previousHash for block with data " + str(top.data))
         err = True
      tmp = tmp.previousBlock
   if nblocks != 3:
      print ("Expected 3 blocks. Found " + str(nblocks))
      err = True

   if top.previousBlock.previousBlock.data != "This is the root block":
      print ("Wrong data (" + str(top.previousBlock.previousBlock.data) + " in top-2")
      err = True
   onemore = CBlock("Adding this new block", top)
   saveBC("loadtest_out.dat", onemore)

   if filecmp.cmp("loadtest_out.dat", "loadtest_golden.dat"):
      print ("New saved file does not match")
      err = True

   pr1,pu1 = Signatures.generate_keys()
   saveKeys("keysave.dat", pr1, "R$3x&11")
   pr_new, pu_new = loadKeys("keysave.dat", "R$3x&11")
   message = b"Levi was here"
   sig = Signatures.sign(message, pr1)
   if not Signatures.verify(message, sig, pu_new):
      print ("Loaded keys are bad.")
      err = True
   



   if not err:
      print ("All tests pass")


   

