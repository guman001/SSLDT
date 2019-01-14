#Signed by Guman
#Powered by Python2.7
#Licensed under GNU GPL
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

def gen_key():
    private_key = rsa.generate_private_key(
         public_exponent=65537,
         key_size=2048,
         backend=default_backend()
     )
    return private_key

def save_private_key(pk, filename):
    pem = pk.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )
    with open(filename, 'wb') as pem_out:
        pem_out.write(pem)
    return

def save_public_key(pk , filename):
    pem = pk.public_bytes(
    encoding = serialization.Encoding.PEM,
    format = serialization.PublicFormat.SubjectPublicKeyInfo)
    with open(filename, 'wb') as pem_out:
        pem_out.write(pem)
    return

name = raw_input('Please select a name for key pair ... \n')
pk = gen_key()
save_public_key(pk.public_key() , 'public_' + name )
save_private_key(pk , 'private_' + name)
print 'Here are the keys... ',os.getcwd()
