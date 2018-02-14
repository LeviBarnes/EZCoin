from BlockChain import TxBlock

if True:
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
   import FileIO
   FileIO.saveKeys("prkey1.dat", pr1)
   FileIO.saveKeys("prkey2.dat", pr2)
   FileIO.saveKeys("prkey3.dat", pr3)
   FileIO.saveKeys("prkey4.dat", pr4)
   FileIO.saveBC("BlockChain.dat", B1)
   

