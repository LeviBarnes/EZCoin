from BlockChain import CBlock
import pickle

def loadBC(filename):
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
   if not isinstance(headBlock, CBlock):
      raise TypeError("Argument 1 to saveBC must be a CBlock")
   if not isinstance(filename, str):
      raise TypeError("Argument 0 to saveBC must be a string")
   myfile = open(filename, "wb")
   pickle.dump(headBlock, myfile)
   myfile.close()
   return


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
   if not err:
      print ("All tests pass")

   
   
   
   

   

