# Signed by Guman.
# Licensed under GNU GPL.
# Powered by Python 2.7.
# Digitally sign/verify and send/receive large dictionaries via TCP socket
import sys
import json
import base64
import cryptography.exceptions
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.hazmat.primitives.serialization import load_pem_private_key

class Communication:

    def __init__(self, verbose = True, flag = 'EOMEOM',buf_size = 60):
        self.verbose = verbose
        if buf_size > 56000:
            buf_size = 56000
        self.buf_size = buf_size
        self.flag = flag

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

    def padd_please(self, message):
        try:
            messageLength = len(message)
            paddLength = (self.buf_size - (messageLength + len(self.flag))%self.buf_size)
            message = message + '}'*paddLength
            return message
        except:
            self.error_handler('Communication_:_padd_please' , sys.exc_info())
            return False

    def depadd_please(self, message):
        try:
            message =  message.strip('}') + '}'
            return message
        except:
            self.error_handler('Communication_:_depadd_please', sys.exc_info())
            return False

    def add_flag(self, message):
        try:
            message = message + self.flag
            return message
        except:
            self.error_handler('Communication_:_add_flag_please' , sys.exc_info())
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

    def verify_please(self, payload_contents, path_to_public_key):
        try:
            public_key = self.load_key_please(path_to_public_key, 'pu')
            if public_key == False:
                return False
            #payload_contents = json.loads(payload_contents)
            signature = self.decode_please(payload_contents['signature'])
            if signature == False:
                return False
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

    def sign_please(self, message, private_key_path):
        try:
            private_key = self.load_key_please(private_key_path, 'pr')
            if private_key == False:
                return False
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
            if signature == False:
                return False
            message['signature'] = signature
            return message
        except:
            self.error_handler('Communication_:_sign_please', sys.exc_info())
            return False

    def recv_a_chunk(self, con):
        # Helper function to recv n bytes or return None if EOF is hit
        try:
            data = ''
            while len(data) < self.buf_size:
                packet = con.recv(self.buf_size - len(data))
                data += packet
                if not packet:
                    return data
            return data
        except:
            self.error_handler('Communication_:_recv_a_chunk', sys.exc_info())
            return False

    def send_please(self, message, s, adres_tuple ='' , handshaking = False):
        try:
            message = json.dumps(message)
            message = self.padd_please(message)
            message = self.add_flag(message)
            if message == False:
                return False
            if handshaking: #Handshaking required otherwise connection is established.
                s.connect(adres_tuple) #s is socket object otherwise s is connection
            i = 0
            while (i*self.buf_size) < len(message):
                x = message[i*self.buf_size : (i+1)*self.buf_size]
                s.sendall(x)
                i = i + 1
            return True
        except:
            self.error_handler('Communication_:_send_please', sys.exc_info())
            return False

    def recv_the_rest_chunks(self,con, message):
        try:
            while True:
                nmessage = self.recv_a_chunk(con)
                if nmessage == False:
                    return False
                message = message + nmessage
                if self.flag == message[-len(self.flag):]:
                    break
            return message
        except:
            self.error_handler('Communication_:_receive_other_chunks', sys.exc_info())
            return False

    def receive_please(self, con):
        try:
            message = self.recv_a_chunk(con)
            if message == False:
                return False
            if not(self.flag == message[-len(self.flag):]):
                message = self.recv_the_rest_chunks(con, message)
                if message == False:
                    return False
            message = message.strip(self.flag) #removing flag
            message = self.depadd_please(message)
            message = json.loads(message)
            return message
        except:
            self.error_handler('Communication_:_receive_please', sys.exc_info())
            return False
