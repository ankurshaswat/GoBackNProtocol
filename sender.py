'''
Go-back-n allows multiple outstanding frames. The sender may transmit up
to MAX_SEQ frames without waiting for an ack. In addition, unlike in the previous
protocolsm the network layer is not assumed to have a new packet all tje time. Instead,
the network layer causes a network_layer_ready revent when there is a packet to send.
'''

from extraClasses import Frame,Event_type

MAX_SEQ = 7

def between(a,b,c):
    ''' Return true if a<=b<c circularly; false otherwise. '''
    if (((a<=b) and (b<c)) or ((c<a) and (a<=b)) or ((b<c) and (c<a))):
        return True
    return False

def send_data(frame_nr , frame_expected , buffer):
    ''' Construct and send a data frame. '''
    s = new Frame(buffer[frame_nr],frame_nr,(frame_expected+MAX_SEQ) % (MAX_SEQ+1)) # insert packet , sequence number, piggyback ack into frame (scratch)
    to_physical_layer(s) # transmit the frame
    start_timer(frame_nr) # start the timer running

def protocol():
    next_frame_to_send # MAX_SEQ >1 ; used for outbound stream
    ack_expected # oldest frame as yet unacknowledged
    frame_expected # next frame expected on inbound stream
    frame r # scratch variable
    packet buffer[MAX_SEQ + 1] # buffers for the outbound stream
    seq_nr nbuffered # number of output buffers currently in use
    seq_nr i # used to index into the buffer array
    event_type event

    enable_network_layer() # allow network_layer_ready events
    ack_expected = 0 # next ack expected inbound
    next_frame_to_send = 0 # next frame going out
    frame_expected = 0 # number of frames expected inbound
    nbuffered = 0 # intitially no packets are buffered

    while(True):
        wait_for_event(&event) # four possibilities: see event_type above

        switch(event) {
            case network_layer_ready: # the network layer has a packet to send
                # Accept, save, and transmit a new frame
                from_netowrk_layer(&buffer[next_frame_to_send]) # fetch new packet
                nbuffered = nbuffered + 1 # expand the sender's window
                send_data(next_frame_to_send, frame_expected,buffer) # transmit the frame
                inc(next_frame_to_send) # advance sender's upper window edge
                break;
            case frame_arrival: # a data or control frame has arrived
                from_physical_layer(&r) # get incoming frame from physical layer

                if (r.seq == frame_expected):
                    # Frames are accepted only in order
                    to_network_layer(&r.info)   # pass packet to network layer
                    inc(frame_expected) # advance lower edge of receiver's window
                
                # Ack n implies n-1, n-2 etc. Check for this
                while(between(ack_expected,r.ack,next_frame_to_send)):
                    # Handle piggyback ack
                    nbuffered = nbuffered -1 # one frame fewer buffered
                    stop_timer(ack_expected)    # frame arrive intact; stop timer
                    inc(ack_expected)   # contract sender's window
                
                break;
            case cksum_err: break   # just ignore bad frames
            case timeout:   # trouble; retransmit all outstanding rames
                next_frame_to_send = ack_expected   # start retransmitting here
                for (i=1;i<=nbuffered;i++) {
                    send_data(next_frame_to_send,frame_expected,buffer) #resend frame
                    inc(next_frame_to_send) # prepare to send the next one
                }
        }

        if (nbuffered<MAX_SEQ):
            enable_network_layer()
        else:
            disable_network_layer()