#!/usr/bin/python


from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import irange,dumpNodeConnections
from mininet.log import setLogLevel

from mininet.link import TCLink
from mininet.node import OVSController,RemoteController
from mininet.cli import CLI

import functools


BANDWIDTH=10
DELAY='8ms'
LOSS=2
MAX_QUEUE_SIZE=1000

class LinearTopo(Topo):
   "Linear topology of k switches, with one host per switch."

   def __init__(self, k=2, **opts):
       """Init.
           k: number of switches (and hosts)
           hconf: host configuration options
           lconf: link configuration options"""

       super(LinearTopo, self).__init__(**opts)

       self.k = k

       lastSwitch = None
       for i in irange(1, k):
           host = self.addHost('h%s' % i)
           switch = self.addSwitch('s%s' % i)
           self.addLink( host, switch)
           if lastSwitch:
               self.addLink( switch, lastSwitch ,bw=BANDWIDTH, delay=DELAY, loss=LOSS, max_queue_size=MAX_QUEUE_SIZE )
           lastSwitch = switch

def simpleTest():
    "Create and test a simple network"
    topo = LinearTopo(k=10)
    net= Mininet(topo=topo,link=TCLink,controller=functools.partial(RemoteController,ip='127.0.0.1:32775') )
    net.start()
    print "Dumping host connections"
    dumpNodeConnections(net.hosts)
    print "Testing network connectivity"
    switches = net.switches

    net.waitConnected()

    print("Testing network connectivity")
    net.pingAll()

    hosts = net.hosts

    print("Pinging h5 from h1")
    print(hosts[0].cmd('ping -c1 %s' % hosts[4].IP()))

    print("Running iperf between h1 and h5")
    print(net.iperf([hosts[0],hosts[4]]))

    print("Running iperf between h1 and h10")
    print(net.iperf([hosts[0],hosts[9]]))

    print("Running ifconfig on h1")
    print(hosts[0].cmd('ifconfig'))

    print("Running route on h1")
    print(hosts[0].cmd('route'))

    print("Running traceroute from h1 to h10")
    print(hosts[0].cmd('traceroute %s' % hosts[9].IP()))

    net.stop()

if __name__ == '__main__':
   # Tell mininet to print useful information
   setLogLevel('info')
   simpleTest()
