import socket
import time
from threading import *


def send_message(str):
   s.send(str.encode()) 
   data = ''
   data = s.recv(1024).decode()
   print (data)



s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "10.0.0.1"
port = 8000
print (host)
print (port)
s.connect((host,port))

send_message("hello there!")
# print('server sent:', s.recv(1024).decode())
s.close()