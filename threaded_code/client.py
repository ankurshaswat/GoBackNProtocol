import Queue
import time
import socket
import sys
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
        data.put("____CUSTOM_DATA____-"+str(i))


def physical_link_layer(socket_):
    global acks
    packetExpected = 0
    # buffer = Queue.Queue()
    buffer = ""

    while 1:

        while ':' in buffer:
            packet_data, _, buffer = buffer.partition(':')
            packet = packet_data.split(',')
            print('Received packet - ' + packet_data+'\n')
            if(packet[0] == 'DATA'):
                packet_num = packet[1]
                if(packetExpected == int(packet_num)):
                    sending = 'ACK,'+str(packetExpected) + ':'
                    print('Sending packet (from physical link layer) - '+sending+'\n')
                    socket_.send(sending)
                    packetExpected += 1
                elif(packetExpected != 0):
                    sending = 'ACK,'+str(packetExpected-1) + ':'
                    print('Sending packet (from physical link layer) - '+sending+'\n')
                    socket_.send(sending)

            elif(packet[0] == 'ACK'):
                acks.put(packet[1])
        complete_data = socket_.recv(128).decode()
        # print('Received data - ' + complete_data + '\n')
        buffer += complete_data


def timeout_counter():
    global timer_start
    global timeout

    while 1:
        if(time.time() - timer_start > 0.5):
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
        if not data.empty() and packet_to_send < lastAckReceived + 1 + windowSize and (packet_to_send%(lastAckReceived+1)) < data.qsize():
            data_copy = data.queue
            data_to_send = data_copy[packet_to_send % (lastAckReceived+1)]
            packet = 'DATA,' + str(packet_to_send) + \
                ',NORMAL' + str(data_to_send) + ':'
            print('Sending packet (from network layer ready) - ' + packet + '\n')
            socket_.send(packet)
            packet_to_send += 1
            timer_start = time.time()
            # to_send = data.get()

        while not acks.empty():
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
                packet = 'DATA,'+str(lastAckReceived+1+i) + \
                    ',TIMEOUT_' + str(data_to_send) + ':'
                print('Sending Packet (timeout) - ' + packet + '\n')
                socket_.send(packet)
            timer_start = time.time()


# # # Initialize host and port
host = sys.argv[1]  # IP of other client(server)
port = int(sys.argv[2])  # port

# # Create Client Socket
socket_ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.settimeout(0.1)

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

thread1.daemon = True
thread2.daemon = True
thread3.daemon = True
thread4.daemon = True

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
