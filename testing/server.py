import socket
import time

from threading import Thread

## Create Server Socket and connection
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "10.0.0.1"
port = 8000
print (host)
print (port)
serversocket.bind((host, port))

class client(Thread):
    def __init__(self, socket, address):
        Thread.__init__(self)
        self.sock = socket
        self.addr = address
        
        ## Initialize Variables
        self.expectedSeqNum = 1
        self.AckToSend = 1
        self.lastpktreceived = time.time()	

        self.start()

    def run(self):
        while 1:
            s=self.sock.recv(1024).decode()
            print('Client sent:', s)
            self.sock.send(b'Oi you sent something to me- '+s.encode()) 


    # def run(self):
    #     while 1:
    #         try:
    #             packet = self.sock.recv(1024).decode().split(',')
    #             self.lastpktreceived = time.time()
    #             ## Check Packet against expected Number
    #             if(packet[0] == self.expectedSeqNum):
    #                 print('Received correct', self.expectedSeqNum)

    #                 ## Create ACK
    #                 ackPacket = self.expectedSeqNum + ',' + 'ACK'
                    
    #                 ## Send ACK
    #                 self.sock.send(ackPacket)

    #                 self.expectedSeqNum += 1
    #             else:
    #                 print('Received incorrect ', packet[0])
    #                 ## Create ACK
    #                 ackPacket = self.expectedSeqNum + ',' + 'ACK'
                    
    #                 ## Send ACK
    #                 self.sock.send(ackPacket)

    #             # print('Client sent:', self.sock.recv(1024).decode())
    #             # self.sock.send(b'Oi you sent something to me')
    #         except:
    #             if(time.time() - self.lastpktreceived > 2):
    #                 break

serversocket.listen(5)
print ('server started and listening')
while 1:
    clientsocket, address = serversocket.accept()
    client(clientsocket, address)
