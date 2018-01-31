from BlockChain import CBlock

def mine(Block):
    for q in range(128*128):
        n = q//128
        m = q%128
        Block.newNonce(bytes([n,m]).decode())
        thisHashZero = Block.computeHash()[0]
        if Block.isvalid():
            print("Found a block!")
            print("Nonce = '" + bytes([n,m]).decode()+"'("+str(n)+", "+str(m)+")")
            break
