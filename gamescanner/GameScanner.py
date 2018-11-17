import asyncio

from socket import AF_INET
from time import time
from math import ceil
from pprint import PrettyPrinter

from SRCDSScanner import SRCDSScanner
from Quake3Scanner import Quake3Scanner
from NetworkIterator import NetworkIterator
from Database import Database
from WebServer import start_webserver

pp = PrettyPrinter(indent=4)

async def dump_db(database, interval):
    while True:
        db = database.dump()
        pp.pprint(len(db))
        pp.pprint(db)
        await asyncio.sleep(interval)


async def main():
    """
    main method of the scanner.
    #TODO improve the docstring
    """

    rate = 10; # Number of packets send per second. This rate does not apply to the refresher
    timestep = 0.2 # timeinterval in which the scanner tries to adjust the scans to

    database = Database(prune_interval=10, prune_time=30)

    loop = asyncio.get_running_loop()

    # List containing all scanners
    scanners = list()

    transport, protocol = await loop.create_datagram_endpoint(
            lambda : SRCDSScanner(database), family = AF_INET)
    scanners.append(protocol)

    q3transport, q3protocol = await loop.create_datagram_endpoint(
            lambda : Quake3Scanner(database), family = AF_INET)
    scanners.append(q3protocol)


    packets_per_ip = sum(s.packets_per_ip() for s in scanners)

    # make the rate limiting in 0.2s timesteps
    per_step_rate = rate*timestep
    num_ips = ceil(per_step_rate/packets_per_ip)

    print("scanning a maximum of %d ips per step" % num_ips)

    networks = [
            "216.52.148.47",
            #"89.163.189.0/24",
            "89.40.105.235",
            "193.19.119.197",
            "46.174.49.219",
            "45.76.94.34",
            "85.10.203.89"
        ]

    net_it = NetworkIterator(networks)

    loop.create_task(start_webserver(loop, database, "127.0.0.1", 9001))

    loop.create_task(dump_db(database, 3))
    print("created regular dump")

    while True:
        pre_scan_time = time()
        for _ in range(min(num_ips, len(net_it))):
            ip = next(net_it)
            for scanner in scanners:
                scanner.scan(ip)
        sleep_time = max(0,timestep - (time() - pre_scan_time))
        #print("sleeping for %f" % sleep_time)
        await asyncio.sleep(sleep_time)


if __name__ == "__main__":
    asyncio.run(main())
