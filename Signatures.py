from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
from datetime import date

def generate_keys():
    # generate private/public key pair
    key = rsa.generate_private_key(backend=default_backend(), public_exponent=65537, \
        key_size=2048)

    # get public key in OpenSSH format
    public_key = key.public_key().public_bytes(serialization.Encoding.OpenSSH, \
        serialization.PublicFormat.OpenSSH)

    return key, public_key

def sign(message, private_key):
    if type(message) == type(b"Hello"):
        message = message.decode() 
    signature = private_key.sign(bytes(message, 'utf8'), 
                                 padding.PSS(mgf=padding.MGF1(hashes.SHA256()),
                                             salt_length=padding.PSS.MAX_LENGTH),
                                 hashes.SHA256()                                 )
    return signature


if __name__ == "__main__":
    private_key, public_key = generate_keys()
    # decode to printable strings
    # get private key in PEM container format
    pem = private_key.private_bytes(encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption())

    private_key_str = pem.decode('utf-8')
    public_key_str = public_key.decode('utf-8')

    print('Private key = ') 
    print(private_key_str)
    print('Public key = ')
    print(public_key_str)

    message = ("This message was signed by " + public_key_str + 
               " on " + date.today().strftime("%Y/%m/%d")       )
    print()
    print('Message = ')
    print (message)

    signature = sign(message, private_key)
    signature = sign(b"This message is already bytes", private_key)

    print()
    print('signature = ')
    print (signature)

    
