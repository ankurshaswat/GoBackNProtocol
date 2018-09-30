# import socket
# import time

# from threading import *


# def send_message(str):
#     s.send(str.encode())
#     # data = ''
#     # data = s.recv(1024).decode()
#     # print (data)

# print("START")

# # Initialize host and port
# host = "10.0.0.1"
# port = 8000
# print (host)
# print (port)

# # Initialize window variables
# nextSeqNum = 1
# nextAckExpected = 1
# windowSize = 7
# lastPacket = 100
# lastAckReceived=-1

# # Create Client Socket
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# # s.settimeout(0.1)

# print("Trying to connect with server")


# # Connect Socket to server
# s.connect((host, port))

# print("Connection established with server")

# done = False

# while not done:
#     if(nextSeqNum < nextAckExpected + windowSize)and nextSeqNum <= lastPacket and not done:

#         # Create Packet (Data is Packet Number here)
#         pkt = str(nextSeqNum) + ',' + 'Custom Data Here'

#         # Send Packet
#         send_message(pkt)

#         print("Packet sent to server")

#         # Increment nextSeqNum
#         nextSeqNum = nextSeqNum + 1

#     try:
#         packet = s.recvfrom(1024).decode().split(',')

#         print('Client received- '+str(packet))
#         if packet[0] == nextAckExpected:
#             nextAckExpected += 1
#             lastAckReceived = time.time()
#             if packet[0] == lastPacket:
#                 done = True

#     except:
#         if(time.time() - lastAckReceived > 0.1):
#             for i in range(windowSize):
#                 pkt = str(i+nextAckExpected) + ',' + 'Custom Data Here'
#                 send_message(pkt)

# # send_message("hello there!")
# # print('server sent:', s.recv(1024).decode())
# s.close()



import socket
import time
from threading import *
def send_message(str):
   s.send(str.encode()) 
#    data = ''
#    data = s.recv(1024).decode()
#    print (data)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(1)
host = "10.0.0.1"
port = 8000
print (host)
print (port)
s.connect((host,port))

done = False

# Initialize window variables
nextSeqNum = 1
nextAckExpected = 1
windowSize = 7
lastPacket = 100
lastAckReceived=-1


while not done:
    if(nextSeqNum < nextAckExpected + windowSize)and nextSeqNum <= lastPacket and not done:

        # Create Packet (Data is Packet Number here)
        pkt = str(nextSeqNum) + ',' + 'Custom Data Here'

        # Send Packet
        send_message(pkt)
        print("Packet sent to server")

        packet = s.recv(1024).decode().split(',')
        print('Client received- '+str(packet))
      

        # Increment nextSeqNum
        nextSeqNum = nextSeqNum + 1

        time.sleep(1)

    # try:
    #     packet = s.recv(1024).decode().split(',')

    #     print('Client received- '+str(packet))
    #     if packet[0] == nextAckExpected:
    #         nextAckExpected += 1
    #         lastAckReceived = time.time()
    #         if packet[0] == lastPacket:
    #             done = True

    # except:
    #     if(time.time() - lastAckReceived > 0.1):
    #         for i in range(windowSize):
    #             pkt = str(i+nextAckExpected) + ',' + 'Custom Data Here'
    #             send_message(pkt)


send_message("hello there!")
print('server sent:', s.recv(1024).decode())
s.close() 
  
