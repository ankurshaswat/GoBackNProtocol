import Queue
import time
import socket
from threading import Thread

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

    while 1:
        packet = socket_.recv(1024).decode().split(',')

        if(packet[0] == 'DATA'):
            print('Received DATA - ', packet[2])
            packet_num = packet[1]
            socket_.send('ACK,'+packetExpected)
            if(packetExpected == packet_num):
                packetExpected += 1

        elif(packet[0] == 'ACK'):
            print('Received ACK - ',packet[1])
            acks.put(packet[1])


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
            packet = 'DATA,' + (lastAckReceived+1+packet_to_send) + ',' + data_to_send
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
                packet = 'DATA,'+(lastAckReceived+1+i) + ',' + data_to_send
                socket_.send(packet)


# # # Initialize host and port
host = "10.0.0.1"
port = 8000

# # Create Client Socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(0.1)

# # # Connect Socket to server
s.connect((host, port))

thread1 = Thread( target=network_layer, args=() )
thread2 = Thread( target=physical_link_layer, args=(s) )
thread3 = Thread( target=timeout_counter, args=() )
thread4 = Thread( target=data_link_layer, args=(s) )

thread1.start()
thread2.start()
thread3.start()
thread4.start()

thread1.join()
thread2.join()
thread3.join()
thread4.join()
