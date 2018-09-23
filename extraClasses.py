from enum import Enum

class Event_type(Enum):
    frame_arrival =1
    cksum_err = 2
    timeout = 3
    network_layer_ready = 4

class Frame:
    def __init__(self,info,seq,ack):
        self.info = info
        self.seq = seq
        self.ack = ack
