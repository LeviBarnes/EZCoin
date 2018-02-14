from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
from datetime import date
from cryptography import exceptions as crexceptions
from cryptography.hazmat.primitives.serialization import load_ssh_public_key

def generate_keys():
    """
    Signatures.generate_keys()

    returns a 2048-bit RSA private key and public key pair
    """
    # generate private/public key pair
    key = rsa.generate_private_key(backend=default_backend(), public_exponent=65537, \
        key_size=2048)

    # get public key in OpenSSH format
    public_key = key.public_key();
    #TODO push this serialization back into generate_keys()
    #Need to figure a way to deserialize to get a viable _RSAPUblicKey type 
    #from the public_bytes
    #public_key = public_key.public_bytes(serialization.Encoding.OpenSSH, 
    #    serialization.PublicFormat.OpenSSH).decode('utf-8')

    return key, public_key

def sign(message, private_key):
    """ 
    Signatures.sign(message, private_key)
    
    signs the provided message using the private key using SHA256 and returns
    the signature.  'message' can be bytes or a string. Obtain an approriate
    private key by calling Signatures.generate_keys()
    """
    if type(message) == type(b"Hello"):
        message = message.decode() 
    signature = private_key.sign(bytes(message, 'utf-8'), 
                                 padding.PSS(mgf=padding.MGF1(hashes.SHA256()),
                                             salt_length=padding.PSS.MAX_LENGTH),
                                 hashes.SHA256()                                 )
    return signature

def verify(message, signature, public_key):
    """ 
    Signatures.verify(message, signature, private_key)
    
    Verifies that the provided signature corresponds to the given message and
    private key. Hashes using SHA256. 'message' can be bytes or a string. Obtain 
    an approriate private key by calling Signatures.generate_keys() and use
    Signatures.sign() to sign a message
    """
    if type(message) == type(b"Hello"):
        message = message.decode() 
    if type(public_key) == type("Hello"):
        public_key = load_ssh_public_key(bytes(public_key,'utf-8'), default_backend())
    if type(public_key) == type(b"Hello"):
        public_key = load_ssh_public_key(public_key, default_backend())
    try:
        public_key.verify(signature, bytes(message, 'utf-8'), 
                          padding.PSS(mgf=padding.MGF1(hashes.SHA256()),
                                      salt_length=padding.PSS.MAX_LENGTH),
                          hashes.SHA256()                                 ) 
        return True
    except crexceptions.InvalidSignature:
        return False

def public_key_to_ssl(public_key):
    """ 
    Signatures.public_key_to_ssl(public_key)
    
    Return an OpenSSL string expressing the given _RSAPublicKey
    """
    return public_key.public_bytes(serialization.Encoding.OpenSSH, 
        serialization.PublicFormat.OpenSSH).decode('utf-8')

def private_key_to_pem(private_key, passwd = None):
    """
    Signatures.private_key_to_pem(private, password=None)

    Returns the PEM for the given private key
    """
    if passwd != None:
        algo = serialization.BestAvailableEncryption(bytes(str(passwd),'utf-8'))
    else:
        algo = serialization.NoEncryption()
    
    return private_key.private_bytes(encoding = serialization.Encoding.PEM,
                                     format = serialization.PrivateFormat.TraditionalOpenSSL,
                                     encryption_algorithm = algo)

def pem_to_private_key(pem_in, passwd = None):
    """
    Signatures.pem_to_private_key(pem, passwd = None)

    Extract the _RSAPrivateKey instance from a PEM
    """
    if passwd != None:
        passwd = bytes(str(passwd),'utf-8')
    return serialization.load_pem_private_key(pem_in,
                                              passwd,
                                              default_backend())


#This section will only run if Signatures is invoked directly from the
#command line. i.e.
#   > python3 Signatures.py
#When the Signatures module is imported from another python file (i.e.
#   import Signatures
#this code is ignored
if __name__ == "__main__":
    private_key, public_key = generate_keys()
    # get private key in PEM container format
    pem = private_key_to_pem(private_key, b"H%r77y")

    private_key_str = pem.decode('utf-8')
    public_key_str = public_key_to_ssl(public_key)

    print('Private key = ') 
    print(private_key_str)
    print('Public key = ')
    print(public_key_str)

    message = ("This message was signed by " + public_key_str + 
               " on " + date.today().strftime("%Y/%m/%d")       )
    print()
    print('Message = ')
    print (message)

    private_key = pem_to_private_key(bytes(private_key_str,'utf-8'),b"H%r77y")
    signature = sign(message, private_key)

    print()
    print('signature = ')
    print (signature)

    print()
    if verify(message, signature, public_key):
        print("String message verified")
    else:
        print("Verification of string message FAILED")

    #This time, pass the public key as an OpenSSL string
    if verify(message, signature, public_key_str):
        print("String message verified using OpenSSL string")
    else:
        print("Verification of string message FAILED using OpenSSL string")

    signature = sign(b"This message is already bytes", private_key)
    if (verify(b"This message is already bytes", signature, public_key)):
        print("Bytes message verified")
    else:
        print("Verification of bytes message FAILED")


    
