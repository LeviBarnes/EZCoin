for f in ["Signatures.py",
          "Transactions.py",
          "BlockChain.py",
          "StoreBlockChain.py",
          "Miner.py",
          "TxBlockTest.py",
          "TxPickleTest.py"
          ]:
    print("***** Executing " + f + " ********")
    prog = open(f)
    exec(prog.read())
    print("***********************************")
    print()
