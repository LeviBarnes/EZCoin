import BlockChain
import Signatures

class Tx:
    inputs = []
    outputs = []
    reqd_sigs = []
    sigs = []
    def __init__(self, _inputs=None, _outputs=None, _reqd_sigs=None,
                 _sigs=None):
        if _inputs != None:
            self.inputs = _inputs
        if _inputs != None:
            self.outputs = _outputs
        if _inputs != None:
            self.reqd_sigs = _reqd_sigs
        if _inputs != None:
            self.sigs = _sigs
    def add_input(self, public, amount):
        """
        add_input(public, amount)

        add one input to the tx. Takes a public addres and an amount
        """
        self.inputs.append((public, amount))
        self.reqd_sigs.append(public)
    def add_output(self,public, amount):
        """
        add_input(public, amount)

        add one input to the tx. Takes a public addres and an amount
        """
        self.outputs.append((public, amount))
    def add_reqd(self,public):
        """
        add_reqd(public)

        add one required signature (a public key)
        """
        self.reqd_sigs.append(public)
    def __gather(self):
        """
        __gather() (private) -> str

        gather the data for signing
        """
        thedata = ""
        for i in self.inputs:
            thedata = thedata + str(i[0]) + str(i[1])
        for o in self.outputs:
            thedata = thedata + str(o[0]) + str(o[1])
        for r in self.reqd_sigs:
            thedata = thedata + str(r)
        #The signatures do not go in here so that the tx may be signed
        #in any order
        return thedata
        
    def sign(self,private):
        """
        sign(private)

        sign this transaction with a private key
        """
        #Gather the data
        thedata = self.__gather()
        #Sign it
        self.sigs.append(Signatures.sign(thedata, private))
    def check_sigs(self):
        """
        check_sigs() -> bool

        checks that the transaction is correctly signed
        """
        #No unsigned txs (yet)
        if self.reqd_sigs == None:
            return False
        #Every input address must sign
        for i in self.inputs:
            if not i[0] in self.reqd_sigs:
                return False
        thedata = self.__gather()
        valid = True
        for k in self.reqd_sigs:
            this_valid = False
            for s in self.sigs:
                if Signatures.verify(thedata, s, k):
                    this_valid = True
                    #print ("Signature " + str(s) + " is valid for address "+
                    #       str(k))
                    break
                #print ("Signature " + str(s) + " is not valid for address "+
                #        str(k))
            if this_valid == False:
                valid = False
        return valid

    
if __name__ == "__main__":
    pr1,pu1 = Signatures.generate_keys()
    pr2,pu2 = Signatures.generate_keys()
    pr3,pu3 = Signatures.generate_keys()

    Tx1 = Tx()
    Tx1.add_input(pu1, 2)
    Tx1.add_output(pu2, 1)
    Tx1.add_output(pu3, 1)
    Tx1.sign(pr1)
    if Tx1.check_sigs():
        print ("Tx1 is valid")
    else:
        print ("Tx1 is invalid")
    Tx2 = Tx()
    Tx2.add_input(pu1, 2)
    Tx2.add_output(pu2, 1)
    Tx2.add_output(pu3, 1)
    Tx2.add_reqd(pu2)
    Tx2.sign(pr2)
    Tx2.sign(pr1)
    if Tx2.check_sigs():
        print ("Tx2 is valid")
    else:
        print ("Tx2 is invalid")
    Tx2.add_output(pu3,1)
    if Tx2.check_sigs():
        print ("Tx2(mod) is valid")
    else:
        print ("Tx2(mod) is invalid")
    
    
