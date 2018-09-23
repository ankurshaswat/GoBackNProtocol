def receiver():
    seq_nr frame_expected
    frame r,s
    event_type event

    frame_expected = 0
    while(True):
        wait_for_event(&event)  # possibilities: frame_arrival, cksum_err
        if (event == frame_arrival):    # a valid frame has arrived
            from_physical_layer(&r) # go get the newly arrived frame
            if(r.seq == frame_expected):    # this is what we have been waiting for
                to_network_layer(&r.info)   # pass the data to the network layer
                inc(frame_expected) # next time expect the other sequence
            s.ack = 1 - frame_expected  # tell which frame is being acked
            to_physical_layer(&s)   # send acknowledment