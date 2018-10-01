import functools


from mininet.topo import Topo
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.node import OVSController,RemoteController

import time
from threading import Thread
import random

BANDWIDTH = 1
DELAY='0ms'
LOSS=2
# DELAY = str(random.randint(0,5))+'ms'
# print('Delay set to '+DELAY)

class LinearTopo(Topo):

    def __init__(self, **opts):
        """Init.
        k: number of switches (and hosts)
        hconf: host configuration options
        lconf: link configuration options"""

        super(LinearTopo, self).__init__(**opts)

        host1 = self.addHost('h1', ip='10.0.0.1')
        host2 = self.addHost('h2', ip='10.0.0.2')
        switch1 = self.addSwitch('s1')
        switch2 = self.addSwitch('s2')
        self.addLink(host1, switch1)
        self.addLink(host2, switch2)
        self.addLink(switch1, switch2, bw=BANDWIDTH, delay=DELAY, loss=LOSS)
        self.addLink(switch1,switch2)

def init_client1(hosts):
    print("Starting server program \n")    
    hosts[0].cmd('python client.py 0.0.0.0 9007 1 > server.log')

def init_client2(hosts):
    print("Starting client program \n")    
    hosts[1].cmd('python client.py 10.0.0.1 9007 0 > client.log')    




if __name__ == '__main__':
    # Create net consisting of 2 hosts
    topo = LinearTopo()
    net = Mininet(topo=topo, link=TCLink, controller=functools.partial(
        RemoteController, ip='172.17.0.1:32769'))
    net.start()

    hosts = net.hosts
    print(hosts[0].cmd('ping -c1 %s' % hosts[1].IP()))
    print(hosts[1].cmd('ping -c1 %s' % hosts[0].IP()))
    print(hosts[0].cmd('ifconfig'))
    # print("Starting server program")
    # print(hosts[0].cmd('python client.py 0.0.0.0 9007 1 &'))
    print(hosts[1].cmd('ifconfig'))    
    # time.sleep(2)
    # print("Starting client program")
    # print(hosts[1].cmd('python client.py 10.0.0.1 9007 0'))
    thread1 = Thread(target=init_client1, args=(hosts,))
    thread2 = Thread(target=init_client2, args=(hosts,))

    thread1.daemon = True
    thread2.daemon = True

    thread1.start()
    time.sleep(2)
    thread2.start()

    print("Started both threads\n")

    while True:
        time.sleep(1)
