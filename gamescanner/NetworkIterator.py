from ipaddress import ip_network, ip_address

class NetworkIterator:
    """
    This class is an iterator which iterates over a given list of networs or ip
    addresses in a cyclic fashion.
    Therefore it never raises a StopIteration exception.
    Only IPv4 addresses and networks are supported.
    """

    def __init__(self, networks):
        """networks is a list if ip addresses or networks in CIDR notation"""
        self.networks = networks
        self.net_pos = 0
        self.current_net = SingleNetworkIterator(self.networks[self.net_pos])
        self.total_length = sum(2**(32-int(n.split("/")[1])) if "/" in n else 1 for n in self.networks)

    def __next__(self):
        while True:
            try:
                return next(self.current_net)
            except StopIteration:
                self.net_pos+=1
                self.net_pos = self.net_pos % len(self.networks)
                self.current_net = SingleNetworkIterator(self.networks[self.net_pos])

    def __len__(self):
        return self.total_length

class SingleNetworkIterator:

    def __init__(self, networkdesc):
        self.networkdesc = networkdesc
        if "/" not in self.networkdesc:
            self.networkdesc+= "/32"
        self.network = ip_network(self.networkdesc)
        self.pos = 0

    def __next__(self):
        if self.pos >= self.network.num_addresses:
            raise StopIteration
        ret = str(ip_address(self.network.network_address + self.pos))
        self.pos +=1
        return ret




