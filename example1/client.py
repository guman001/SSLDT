#signed by guman
import socket
from Communication import Communication

comObj = Communication()
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip = 'localhost'
port = 5000
adres_tuple = (ip, port)
sock.connect(adres_tuple)
print 'Connected to the following host: ', adres_tuple
message = comObj.receive_please(sock)
nport = message["port"]
print 'Received port is : ', nport
nadres_tuple = (ip, nport)
sock.close()
message = {'Test':'OK'}
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Sending message to remote host...'
comObj.send_please(message, sock, nadres_tuple, True)
print 'Message is sent.'
sock.close()
