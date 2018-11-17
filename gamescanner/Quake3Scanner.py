from time import time

from BaseScanner import BaseScanner

class Quake3Scanner(BaseScanner):
    """
    This class provides a scanner for servers using the Quake3 Protocol.
    """

    default_ports = [27070, 27960, 27961, 27962, 27963,
            27992, 28960, 28961, 28962, 28963]
    query = b"\xFF\xFF\xFF\xFFgetstatus\x0A"
    #query = bytearray([0xFF, 0xFF, 0xFF,0xFF, 0x67, 0x65, 0x74, 0x73, 0x74, 0x61, 0x74, 0x75, 0x73, 0x0A])

    def __init__(self, database):
        """
        Constructs a Quake3Scanner with the given database
        """
        self.database = database

    def connection_made(self, transport):
        self.transport = transport

    def connection_lost():
        pass

    def parse(self, data, addr):
        sender = addr
        data = [m.split(b'\\') for m in data.splitlines(0x0A)]

        # check if the response is correct
        header = data[0][0]
        header_template = b"\xFF\xFF\xFF\xFFstatusResponse\n"
        if header != header_template:
            return

        response_dict = dict()

        # build a dict from the response
        # first entry in data[1] is empty, has to be skipped
        # then every 2 entries are a key value pair.
        i = 1
        while i < len(data[1]):
            key = data[1][i].decode().lower() #lowered because some servers reply with some fields not all lower case
            value = data[1][i+1].decode()
            response_dict[key] = value
            i+=2

        player_count = len(data[2:])

        server_dict = dict()
        server_dict["ip"] = sender[0]
        server_dict["hostname"] = None
        server_dict["port"] = sender[1]
        server_dict["server_name"] = response_dict["sv_hostname"]
        server_dict["map"] = response_dict["mapname"]
        server_dict["max_players"] = response_dict["sv_maxclients"]
        server_dict["players"] = player_count
        server_dict["game"] = response_dict["gamename"]
        server_dict["game_type"] = response_dict["g_gametype"]

        server_dict["timestamp"] = time()
        return server_dict

    def datagram_received(self, data, addr):
        print("received %s from %s" %(data[:min(40, len(data))], addr))
        try:
            server_dict = self.parse(data, addr)
            if server_dict is not None:
                self.database.add(server_dict)
        except:
            return

    @staticmethod
    def packets_per_ip():
        """
        Returns the number of packets the scanner sends per IP it scans.
        This is used for rate limiting purposes.
        """
        return len(Quake3Scanner.default_ports)

    def scan(self, ip, ports=None):
        """
        Scans the given ip.
        If ports is given only the ports in this list are scanned
        """
        ports = Quake3Scanner.default_ports if ports is None else ports

        print("scanning ip %s" % ip)

        for port in ports:
            self.transport.sendto(Quake3Scanner.query, (ip,port))
