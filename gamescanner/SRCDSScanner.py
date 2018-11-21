from time import time
from pprint import PrettyPrinter

from BaseScanner import BaseScanner

class SRCDSScanner(BaseScanner):
    """
    This class provides a scanner for SRCDS servers.
    """

    default_ports = [27015,27016,27017,27018,27019] #TODO add remaining ports
    query = b"\xFF\xFF\xFF\xFFTSource Engine Query\x00"

    def __init__(self, database):
        """
        Constructs a BaseScanner with the given database
        """
        self.database = database

    def connection_made(self, transport):
        self.transport = transport

    def connection_lost():
        pass

    def parse(self, data, addr):
        sender = addr
        data = data[4:]

        server_dict = dict()

        server_dict["ip"] = sender[0]
        server_dict["port"] = sender[1]
        server_dict["hostname"] = None
        server_dict["timestamp"] = time()
        server_dict["scanner"] = "SRCDSScanner"

        header                      = data[0] #Header
        # new srcds format
        if header == 0x49:
            server_dict["protocol_subversion"] = "srcds"
            payload                     = data[2:] # Name
            name_end                    = payload.find(b"\x00")
            server_dict["server_name"]  = payload[0:name_end].decode('utf-8', 'ignore')  # Name
            mapname_end                 = payload.find(b"\x00",name_end+1)
            server_dict["map"]          = payload[name_end+1:mapname_end].decode('utf-8', 'ignore') # Map
            folder_end                  = payload.find(b"\x00",mapname_end+1)
            server_dict["game"]         = payload[mapname_end + 1: folder_end].decode('utf-8', 'ignore') # Folder
            game_end                    = payload.find(b"\x00",folder_end+1)
            server_dict["game_type"]     = payload[folder_end + 1: game_end].decode('utf-8', 'ignore') # Game
            server_dict["steam_game_id"]= int.from_bytes(payload[game_end+1: game_end+3], byteorder='little') # Steam ID
            server_dict["players"]      = int.from_bytes(payload[game_end+3:game_end+4],byteorder='little') # Players
            server_dict["max_players"]  = int.from_bytes(payload[game_end+4:game_end+5], byteorder='little') # Max. Players
            server_dict["bot_count"]    = int.from_bytes(payload[game_end+5:game_end+6],byteorder='little') # Bots
            server_type = payload[game_end+6:game_end+7].decode("utf-8", "ignore") # Server Type
            server_dict["server_type"]  = "dedicated"
            if server_type == "l":
                server_dict["server_type"]  = "non-dedicated"
            elif server_type == "p":
                server_dict["server_type"]  = "proxy" # SourceTV relay
            # environment               = payload[game_end+7:game_end+8] # Environment
            password_protected = int.from_bytes(payload[game_end+8:game_end+9],byteorder='little') # Visibility
            server_dict["password_protected"] = True if password_protected != 0 else False
            # vac                       = payload[game_end+9:game_end+10] # VAC

            return server_dict


        # old goldsource format
        if header == 0x6D:
            server_dict["protocol_subversion"] = "goldsource"
            payload = data[1:]
            address_end = payload.find(b"\x00")
            name_end                    = payload.find(b"\x00", address_end+1)
            mapname_end                 = payload.find(b"\x00",name_end+1)
            folder_end                  = payload.find(b"\x00",mapname_end+1)
            game_end                    = payload.find(b"\x00",folder_end+1)
            server_dict["server_name"]  = payload[0:name_end].decode('utf-8', 'ignore')  # Name
            server_dict["map"]          = payload[name_end+1:mapname_end].decode('utf-8', 'ignore') # Map
            server_dict["game"]         = payload[mapname_end + 1: folder_end].decode('utf-8', 'ignore') # Folder
            server_dict["game_type"]     = payload[folder_end + 1: game_end].decode('utf-8', 'ignore') # Game
            server_dict["players"]      = int.from_bytes(payload[game_end+1:game_end+2],byteorder='little') # Players
            server_dict["max_players"]  = int.from_bytes(payload[game_end+2:game_end+3], byteorder='little') # Max. Players
            server_dict["protocol"]    = int.from_bytes(payload[game_end+3:game_end+4],byteorder='little') # Bots
            server_type = payload[game_end+4:game_end+5].decode("utf-8", "ignore") # Server Type
            server_dict["server_type"]  = "dedicated"
            if server_type == "L":
                server_dict["server_type"]  = "non-dedicated"
            elif server_type == "P":
                server_dict["server_type"]  = "proxy" # SourceTV relay
            environment               = payload[game_end+5:game_end+6] # Environment
            server_dict["environment"] = "Windows" if environment == "W" else "Linux"
            password_protected = int.from_bytes(payload[game_end+6:game_end+7],byteorder='little') # Visibility
            server_dict["password_protected"] = password_protected != 0
            mod = int.from_bytes(payload[game_end+7:game_end+8],byteorder='little') # is this server modded
            server_dict["mod"] = (mod != 0)
            mod_end = game_end + 8
            #special options if mod is true
            if mod != 0:
                # now 2 strings, 1 byte, 2 longs, 2 bytes
                mod_start = game_end+8
                modwebsite_end = payload.find(b"\x00", mod_start)
                moddownload_end = payload.find(b"\x00", modwebsite_end)
                server["mod_website"] = payload[mod_start:modwebsite_end]
                server["mod_download"] = payload[modwebsite_end:moddownload_end]
                server_dict["mod_version"]= int.from_bytes(
                        payload[moddownload_end+1:moddownload_end+5],byteorder='little') #mod version
                server_dict["mod_size"]= int.from_bytes(
                        payload[moddownload_end+5:moddownload_end+9],byteorder='little') #mod download size
                server_dict["mod_type"]= int.from_bytes(
                        payload[moddownload_end+9:moddownload_end+10],byteorder='little') #mod type (multiplayer or singleplayer)
                server_dict["mod_dll"]= int.from_bytes(
                        payload[moddownload_end+9:moddownload_end+10],byteorder='little') #mod dll (does the mod use a dll)
                mod_end = moddownload_end+10
            # VAC is skipped
            server_dict["bot_count"] = int.from_bytes(payload[mod_end:mod_end+1], byteorder='little')

            return server_dict


        return

    def datagram_received(self, data, addr):
        #print("received %s from %s" %(data[:min(40, len(data))], addr))
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
        return len(SRCDSScanner.default_ports)

    def scan(self, ip, ports=None):
        """
        Scans the given ip.
        If ports is given only the ports in this list are scanned
        """
        ports = SRCDSScanner.default_ports if ports is None else ports

        for port in ports:
            self.transport.sendto(SRCDSScanner.query, (ip,port))
