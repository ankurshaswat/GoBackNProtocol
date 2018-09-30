import functools


from mininet.topo import Topo
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.node import OVSController,RemoteController


BANDWIDTH = 10
DELAY = '8ms'
LOSS = 2
MAX_QUEUE_SIZE = 1000


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
        self.addLink(switch1, switch2, bw=BANDWIDTH, delay=DELAY,
                     loss=LOSS, max_queue_size=MAX_QUEUE_SIZE)


if __name__ == '__main__':
    # Create net consisting of 2 hosts
    topo = LinearTopo()
    net = Mininet(topo=topo, link=TCLink, controller=functools.partial(
        RemoteController, ip='172.17.0.1:32769'))
    net.start()

    hosts = net.hosts
    print(hosts[0].cmd('ping -c1 %s' % hosts[1].IP()))
    print(hosts[1].cmd('ping -c1 %s' % hosts[0].IP()))
    hosts[0].cmd('python server.py &')
    print("Starting client program")
    print(hosts[1].cmd('python client.py'))
