# Signed by Guman.
# Licensed under GNU GPL.
# Powered by Python 2.7.
# Digitally sign/verify and send/receive large dictionaries via TCP socket
import sys
import json
import base64
import cryptography.exceptions
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.hazmat.primitives.serialization import load_pem_private_key

class Communication:

    def __init__(self, verbose = True, buf_size = 56000):
        self.verbose = verbose
        if buf_size > 56000:
            buf_size = 56000
        self.buf_size = buf_size

    def error_handler(self, errorCode, errorMessage):
        if self.verbose:
            print errorCode
            print errorMessage
        return

    def load_key_please(self, filename, type):
        try:
            if type == 'pr': #for private key
                with open(filename, 'rb') as key_file:
                    pemlines = key_file.read()
                private_key = load_pem_private_key(pemlines, None, default_backend())
                return private_key
            else: #for public key
                with open(filename, 'rb') as key_file:
                    pemlines = key_file.read()
                public_key = load_pem_public_key(pemlines,default_backend())
                return public_key
        except:
            self.error_handler('Communication_:_load_key_please' , sys.exc_info())
            return False

    def encode_please(self, data): #Base64 encoder
        try:
            codedData = base64.b64encode(data)
            return codedData
        except:
            self.error_handler('Communication_:_encode_please' , sys.exc_info())
            return False

    def decode_please(self, codedData): #Base64 decoder
        try:
            decodedData = base64.b64decode(codedData + '=' * (-len(codedData) % 4))
            return decodedData
        except:
            self.error_handler('Communication_:_decode_please', sys.exc_info())
            return False

    def verify_please(self, payload_contents, public_key):
        try:
            payload_contents = json.loads(payload_contents)
            signature = self.decode_please(payload_contents['signature'])
            del payload_contents['signature']
            rMessage = payload_contents
            aux = payload_contents.keys()
            aux.sort()
            nmessage = {}
            for key in aux:
                nmessage[key] = payload_contents[key]
            payload_contents = nmessage
            payload_contents = json.dumps(payload_contents)
            payload_contents = bytes(payload_contents.encode('ascii'))
            try:
                public_key.verify(
                    signature,
                    payload_contents,
                    padding.PSS(
                        mgf=padding.MGF1(hashes.SHA256()),
                        salt_length=padding.PSS.MAX_LENGTH,
                    ),
                    hashes.SHA256(),
                )
                return rMessage
            except cryptography.exceptions.InvalidSignature as e:
                self.error_handler('Communication_:_verify_please', 'Signature verification failed!')
                return False
        except:
            self.error_handler('Communication_:_verify_please', sys.exc_info())
            return False

    def sign_please(self, message, private_key):
        try:
            message = json.dumps(message)
            signature = private_key.sign(
                message,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            message = json.loads(message)
            signature = self.encode_please(signature)
            message['signature'] = signature
            message = json.dumps(message)
            return message
        except:
            self.error_handler('Communication_:_sign_please', sys.exc_info())
            return False

    def pad_please(self, message):
        try:
            message = message + '}' * (self.buf_size - len(message))
            return message
        except:
            self.error_handler('Communication_:_pad_please', sys.exc_info())
            return False

    def depad_please(self, message):
        try:
            message = message.strip('}') + '}'
            return message
        except:
            self.error_handler('Communication_:_depad_please', sys.exc_info())
            return False

    def recvall_please(self, sock):
        # Helper function to recv n bytes or return None if EOF is hit
        try:
            data = ''
            while len(data) < self.buf_size:
                packet = sock.recv(self.buf_size - len(data))
                if not packet:
                    return None
                data += packet
            if data[-1] == '}':
                data = self.depad_please(data)
            return data
        except:
            self.error_handler('Communication_:_recvall_please', sys.exc_info())
            return False

    def send_please(self, message, private_key_path, s, adres_tuple, large = True):
        try:
            if large:
                private_key = self.load_key_please(private_key_path , 'pr')
                message = self.sign_please(message, private_key)
                s.connect(adres_tuple)
                i = 0
                while True:
                    x = message[i*self.buf_size : (i+1)*self.buf_size]
                    lx = len(x)
                    if len(x) < self.buf_size: #padding required
                        x = self.pad_please(x)
                    s.sendall(x)
                    if self.buf_size > lx:
                        break
            else:
                private_key = self.load_key_please(private_key_path , 'pr')
                message = self.sign_please(message, private_key)
                s.connect(adres_tuple)
                s.sendall(message)
            return True
        except:
            self.error_handler('Communication_:_send_please', sys.exc_info())
            return False
