import Queue
import time
import socket
from threading import Thread

import sys

print('Initializing Variables')
data = Queue.Queue()
acks = Queue.Queue()
timer_start = time.time()
timeout = False


def network_layer():
    global data

    for i in range(500):
        time.sleep(0.002)
        data.put(i)


def physical_link_layer(socket_):
    global acks
    packetExpected = 0
    buffer = Queue.Queue()

        
    while 1:
        if not buffer.empty():
            packet_data = buffer.get()
            packet = packet_data.split(',')
            print('Received packet - ' + packet_data+'\n')
            if(packet[0] == 'DATA'):
                packet_num = packet[1]
                sending = 'ACK,'+str(packetExpected) + ':'
                print('Sending packet (from physical link layer) - '+sending+'\n')
                socket_.send(sending)
                if(packetExpected == packet_num):
                    packetExpected += 1

            elif(packet[0] == 'ACK'):
                acks.put(packet[1])
        else:
            complete_data = socket_.recv().decode()
            msgs = complete_data.split(':')
            for i in msgs:
                buffer.put(i)

def timeout_counter():
    global timer_start
    global timeout

    while 1:
        if(time.time() - timer_start > 0.1):
            timeout = True


def data_link_layer(socket_):
    global timer_start
    global timeout
    global data
    global acks

    windowSize = 7
    lastAckReceived = -1
    packet_to_send = 0

    while 1:
        if not data.empty() and packet_to_send < lastAckReceived + 1 + windowSize:
            data_copy = data.queue
            data_to_send = data_copy[0]
            packet = 'DATA,' + str(lastAckReceived+1+packet_to_send) + ',' + str(data_to_send) + ':'
            print('Sending packet (from network layer ready) - ' + packet + '\n')
            socket_.send(packet)
            packet_to_send += 1
            timer_start = time.time()
            # to_send = data.get()

        if not acks.empty():
            while not acks.empty():
                ack_num = acks.get()
                while (ack_num > lastAckReceived):
                    data.get()
                    lastAckReceived += 1

        if timeout:
            timeout = False
            # create copy
            data_copy = data.queue
            for i in range(windowSize):
                if(i >= len(data_copy)):
                    break
                data_to_send = data_copy[i]
                packet = 'DATA,'+str(lastAckReceived+1+i) + ',' + str(data_to_send) + ':'
                print('Sending Packet (timeout) - ' + packet + '\n')
                socket_.send(packet)
            timer_start = time.time()


# # # Initialize host and port
# host = "10.0.0.1"
host=sys.argv[1]  # server IP (127.0.0.1)
port =int(sys.argv[2]) # port

# # Create Server Socket (listener) 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.settimeout(0.1)

# # # Bind to port
s.bind((host, port))

# Que up to 2 request
s.listen(2)

# Accept connection
clientsocket, address = s.accept()

thread1 = Thread( target=network_layer, args=() )
thread2 = Thread( target=physical_link_layer, args=(clientsocket,) )
thread3 = Thread( target=timeout_counter, args=() )
thread4 = Thread( target=data_link_layer, args=(clientsocket,) )

thread1.daemon=True
thread2.daemon=True
thread3.daemon=True
thread4.daemon=True


thread1.start()
thread2.start()
thread3.start()
thread4.start()

# thread1.join()
# thread2.join()
# thread3.join()
# thread4.join()



while True:
    time.sleep(1)