# SSLDT
Sign and Send Large Dictionaries via TCP socket (= SSLDT)

The following needs in a project led me to write this class and share it:
1) Digitally sign a Python dictionary
2) Send a large signed dictionary via TCP socket

Sign and send large dictionary:
import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
address = (<ip : string> , <port : integer>)
sock.connect(assress)
c = Communication() # An object of Communication Class
message = <a large dictionary>
path_to_privatekey = <path to private key of sender>
result = c.send_please(message, path_to_privatekey, sock, address)
if result:
  print 'Successful'
 else:
  print 'Failure'
