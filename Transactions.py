import BlockChain
import Signatures
from cryptography.hazmat.backends.openssl.rsa import _RSAPublicKey

class Tx:
    def __init__(self):
        self.inputs = []
        self.outputs = [] #_outputs
        self.reqd_sigs = [] #_reqd_sigs
        self.sigs = [] #_sigs
    def __repr__(self):
        outstr=""
        if self.inputs != None:
            outstr = outstr + "Inputs:\n"
            for i in self.inputs:
                outstr = outstr + "   " + str(i[0]) + " -- " + str(i[1]) + "\n"
        if self.outputs != None:
            outstr = outstr + "Outputs:\n"
            for o in self.outputs:
                outstr = outstr + "   " + str(o[0]) + " -- " + str(o[1]) + "\n"
        if self.reqd_sigs != None:
            outstr = outstr + "Required sigs:\n"
            for r in self.reqd_sigs:
                outstr = outstr + "   " + str(r) + "\n"
        if self.sigs != None:
            outstr = outstr + "Signatures:\n"
            for s in self.sigs:
                outstr = outstr + "   " + str(s) + "\n"
        return outstr
                
    def add_input(self, public, amount):
        """
        add_input(public, amount)

        add one input to the tx. Takes a public addres and an amount
        """
        if type(public) == _RSAPublicKey:
            public = Signatures.public_key_to_ssl(public)
        self.inputs.append((public, amount))
        self.reqd_sigs.append(public)
    def add_output(self,public, amount):
        """
        add_input(public, amount)

        add one input to the tx. Takes a public addres and an amount
        """
        if type(public) == _RSAPublicKey:
            public = Signatures.public_key_to_ssl(public)
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
    def check_amts(self):
        """
        Tx.check_amts() -> bool

        checks that no input or output is negative and that the total
        input is greater than or equal to total output
        """
        amt_in = 0
        amt_out = 0
        for i in self.inputs:
            amt_in  = amt_in + i[1]
            if i[1]< 0:
                return False
        for o in self.outputs:
            amt_out = amt_out + o[1]
            if o[1]< 0:
                return False
        if amt_in >= amt_out:
            return True
        else:
            return False
    def isvalid(self):
        """
        Tx.isvalid() -> bool

        checks both the signatures and the input/output
        amounts
        """
        return self.check_amts() and self.check_sigs()

    
if __name__ == "__main__":
    pr1,pu1 = Signatures.generate_keys()
    pr2,pu2 = Signatures.generate_keys()
    pr3,pu3 = Signatures.generate_keys()

    Tx1 = Tx()
    Tx1.add_input(pu1, 2)
    Tx1.add_output(pu2, 1)
    Tx1.add_output(pu3, 1)
    Tx1.sign(pr1)
    if Tx1.isvalid():
        print ("Tx1 is valid")
    else:
        print ("Tx1 is invalid")

    Tx2 = Tx()
    Tx2.add_input(pu1, 2)
    Tx2.add_output(pu2, 2.6)
    Tx2.sign(pr1)
    if Tx2.isvalid():
        print ("Tx2 is valid")
    else:
        print ("Tx2 is invalid")

    Tx3 = Tx()
    Tx3.add_input(pu1, 2)
    Tx3.add_output(pu2, 1)
    Tx3.add_output(pu3, 1)
    Tx3.add_reqd(pu2)
    Tx3.sign(pr2)
    Tx3.sign(pr1)
    if Tx3.isvalid():
        print ("Tx3 is valid")
    else:
        print ("Tx3 is invalid")
    Tx3.add_output(pu2,1)
    if Tx3.isvalid():
        print ("Tx3(mod) is valid")
    else:
        print ("Tx3(mod) is invalid")
    
