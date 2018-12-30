#Signed by guman
#Upon receiving a connection, server selects a port randomly, starts a thread to listen on the choosen port
# and asks client to transfer connection to the dedicated port for it.
import socket
import threading
from random import randint
from Communication import Communication

class MyThread(threading.Thread):
    def __init__(self, port , ip, comObj):
        threading.Thread.__init__(self)
        self.adres_tuple = (ip, port)
        self.comObj = comObj

    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(self.adres_tuple)
        sock.listen(1)
        con, adr = sock.accept()
        if con:
            print 'Got connection from : ', adr, ' On port : ', self.adres_tuple
            message = self.comObj.receive_please(con)
            if ret == False:
                print 'There is an error in receiving message from ', adr
        print 'Message is : ', message
        sock.close()
        return

def choose_port():
    port = randint(1025, pow(2, 16)-1) #choosing a port outside well-known port range
    return port

comObj = Communication()
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip = 'localhost'
port = 5000
adres_tuple = (ip, port)
sock.bind(adres_tuple)
sock.listen(100)
while True:
    con, adr = sock.accept()
    print 'Received connection from ', adr
    p = choose_port()
    reply = {'port' : p}
    thrdObj = MyThread(p, ip, comObj)
    thrdObj.start()
    print 'A thread is listening on new port : ' , p
    ret = comObj.send_please(reply, con, adres_tuple)
    if ret == False:
        print 'There was an error in replying to ',adr
        continue
    print 'New port was announced successfully to ', adr
    con.close()
sock.close()
