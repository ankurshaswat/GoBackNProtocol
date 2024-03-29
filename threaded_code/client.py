import Queue
import time
import socket
import sys
import random
from threading import Thread
import random
import datetime

class Frame:
    def __init__(self, type, num, data):
        self.type = type
        self.num = str(num)
        self.data = data
        if (data == None):
            # if(type == 'ACK'):
            left_space = 32 - (3 + 2 + len(self.num)) - 1
            self.data = '_' * left_space
        else:
            left_space = 32 - (4 + 3 + len(self.num)) - 1
            self.data += ',' + ('_'*left_space)

    def toString(self):
        return (self.type+','+self.num+','+self.data+':')


print('Initializing Variables\n')
data = Queue.Queue()
acks = Queue.Queue()
timer_start = time.time()
timeout = False
total_packets_send = 500
total_packets_receive = 500
lastAckReceived = -1
packetExpected = 0

packetsSent = 0
packetsReceived = 0

START_TIME = time.time()
DATA_ERROR_PROB = 0.1
ACK_ERROR_PROB = 0.05


def network_layer():
    global data
    global total_packets_send

    for i in range(total_packets_send):
        data_size = random.randint(32, 222)
        data.put('_'*data_size)
        time.sleep(0.0025)
    print('Stopping Netowrk Layer - No more data to send to queue\n')


def checksum(packet):
    x = random.uniform(0, 1)
    if(packet[0] == 'DATA'):
        if(x < DATA_ERROR_PROB):
            return False
    else:
        if(x < ACK_ERROR_PROB):
            return False

    return True


def physical_link_layer(socket_):
    global acks
    global total_packets_receive
    global total_packets_send
    global packetExpected
    global lastAckReceived
    global packetsReceived
    buffer = ""

    while 1:
        while ':' in buffer:
            packet_data, _, buffer = buffer.partition(':')
            packet = packet_data.split(',')
            print('Received packet - ' + packet_data+'\n')

            if(packet[0] == 'DATA'):
                # Check for error
                if(not checksum(packet)):
                    continue
                packetsReceived += 1

                packet_num = packet[1]
                if(packetExpected == int(packet_num)):
                    sending = Frame('ACK', packetExpected, None)
                    print('Sending packet (from physical link layer) - ' +
                          sending.toString()+'\n')
                    dt = datetime.datetime.now()
                    print(dt.second*1000000 + dt.microsecond)
                    socket_.send(sending.toString())
                    # if(packetExpected == 100):
                        # print('Time for 100 packets- ' +
                            #   str(time.time()-START_TIME)+'\n')
                        # print('Total Packets Received Till Now - '+packetsReceived+'\n')
                    packetExpected += 1
                elif(packetExpected != 0):
                    sending = Frame('ACK', packetExpected-1, None)
                    print('Sending packet (from physical link layer) - ' +
                          sending.toString()+'\n')
                    socket_.send(sending.toString())

            elif(packet[0] == 'ACK'):
                # Check for error
                if(not checksum(packet)):
                    continue
                acks.put(packet[1])

        try:
            complete_data = socket_.recv(128).decode()
            buffer += complete_data
        except:
            if (packetExpected == total_packets_receive and lastAckReceived == total_packets_send - 1):
                print('Stopping Physical Link Layer\n')
                break


def timeout_counter():
    global timer_start
    global timeout
    global total_packets_send
    global lastAckReceived

    while 1:
        if(time.time() - timer_start > 0.5):
            timeout = True
        if(lastAckReceived == total_packets_send-1):
            print('Stopping Timeoout Counter\n')
            break


def data_link_layer(socket_):
    global timer_start
    global timeout
    global data
    global acks
    global lastAckReceived
    global total_packets_send
    global total_packets_receive
    global packetExpected
    global packetsSent

    windowSize = 7
    packet_to_send = 0
    flag=False

    while 1:
        if not data.empty() and packet_to_send < lastAckReceived + 1 + windowSize and (packet_to_send - lastAckReceived - 1) < data.qsize():
            data_copy = data.queue
            data_to_send = data_copy[packet_to_send - lastAckReceived - 1]
            packet = Frame('DATA', packet_to_send, data_to_send)
            print('Sending packet (from network layer ready) - ' +
                  packet.toString() +'\n')
            print('Lastack-',lastAckReceived)
            print('PacketsSent-',packetsSent)
            dt = datetime.datetime.now()
            print(dt.second*1000000 + dt.microsecond)            
            socket_.send(packet.toString())
            packetsSent += 1

            packet_to_send += 1
            timer_start = time.time()
            # to_send = data.get()

        while not acks.empty():
            # if(lastAckReceived == 100 and not flag):
                # print('Packets Sent to get this Ack - '+packetsSent+'\n')
                # flag=True
            ack_num = acks.get()
            while (lastAckReceived < int(ack_num)):
                dat = data.get()
                print('Removing acknowledged data' + dat + '\n')
                lastAckReceived += 1

        if timeout:
            timeout = False
            # create copy
            data_copy = data.queue
            for i in range(windowSize):
                if(i >= len(data_copy)):
                    break
                data_to_send = data_copy[i]
                packet = Frame('DATA', lastAckReceived+1+i, data_to_send)
                print('Sending Packet (timeout) - ' + packet.toString() + '\n')
                socket_.send(packet.toString())
                packetsSent+=1
            timer_start = time.time()

        if(packetExpected == total_packets_receive and lastAckReceived == total_packets_send - 1):
            print('Stopping Data Link Layer\n')
            break


# # # Initialize host and port
host = sys.argv[1]  # IP of other client(server)
port = int(sys.argv[2])  # port

# # Create Client Socket
socket_ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_.settimeout(10)

s = ''

if(sys.argv[3] == '0'):
    # # # Connect Socket to server
    print("Attempting to connect to", host)
    socket_.connect((host, port))
    s = socket_
else:
    # # # Bind to port
    socket_.bind((host, port))

    # Que up to 2 request
    socket_.listen(2)

    # Accept connection
    s, address = socket_.accept()

thread1 = Thread(target=network_layer, args=())
thread2 = Thread(target=physical_link_layer, args=(s,))
thread3 = Thread(target=timeout_counter, args=())
thread4 = Thread(target=data_link_layer, args=(s,))

# thread1.daemon = True
# thread2.daemon = True
# thread3.daemon = True
# thread4.daemon = True

thread1.start()
thread2.start()
thread3.start()
thread4.start()

thread1.join()
thread2.join()
thread3.join()
thread4.join()

socket_.close()

# while True:
#     time.sleep(1)
