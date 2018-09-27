import socket
import time

# from threading import *


def send_message(str):
    s.send(str.encode())
    # data = ''
    # data = s.recv(1024).decode()
    # print (data)


# Initialize host and port
host = "10.0.0.1"
port = 8000
print (host)
print (port)

# Initialize window variables
nextSeqNum = 1
nextAckExpected = 1
windowSize = 7
lastPacket = 100
lastAckReceived=-1

# Create Client Socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(0.1)

# Connect Socket to server
s.connect((host, port))

done = False

while not done:
    if(nextSeqNum < nextAckExpected + windowSize)and nextSeqNum <= lastPacket and not done:

        # Create Packet (Data is Packet Number here)
        pkt = str(nextSeqNum) + ',' + 'Custom Data Here'

        # Send Packet
        send_message(pkt)

        # Increment nextSeqNum
        nextSeqNum = nextSeqNum + 1

    try:
        packet = s.recvfrom(1024).decode().split(',')

        if packet[0] == nextAckExpected:
            nextAckExpected += 1
            lastAckReceived = time.time()
            if packet[0] == lastPacket:
                done = True

    except:
        if(time.time() - lastAckReceived > 0.01):
            for i in range(windowSize):
                pkt = str(i+nextAckExpected) + ',' + 'Custom Data Here'
                send_message(pkt)

send_message("hello there!")
# print('server sent:', s.recv(1024).decode())
s.close()
