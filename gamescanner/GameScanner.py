import asyncio

from socket import AF_INET
from time import time
from math import ceil
from pprint import PrettyPrinter
from sys import exit

from SRCDSScanner import SRCDSScanner
from Quake3Scanner import Quake3Scanner
from NetworkIterator import NetworkIterator
from Database import Database
from WebServer import start_webserver
from PrometheusExporter import start_prometheus
try:
    from config import *
except ImportError:
    print("config.py not found. Create a config.py file. An example can "
            "be found as config-example.py in the gamescanner folder")
    exit(1)

pp = PrettyPrinter(indent=4)

async def dump_db(database, interval):
    while True:
        db = database.dump()
        pp.pprint("db length %d" % len(db))
        await asyncio.sleep(interval)


async def main():
    """
    main method of the scanner.
    #TODO improve the docstring
    """

    timestep = 0.2 # resolution for the packet rate limit
    database = Database(**database_settings)

    loop = asyncio.get_running_loop()

    # List containing all scanners
    scanners = list()

    # set up the scanners
    srcdstransport, srcdsprotocol = await loop.create_datagram_endpoint(
            lambda : SRCDSScanner(database), family = AF_INET)
    scanners.append(srcdsprotocol)

    q3transport, q3protocol = await loop.create_datagram_endpoint(
            lambda : Quake3Scanner(database), family = AF_INET)
    scanners.append(q3protocol)


    packets_per_ip = sum(s.packets_per_ip() for s in scanners)

    # make the rate limiting in 0.2s timesteps
    per_step_rate = rate*timestep
    num_ips = ceil(per_step_rate/packets_per_ip)

    print("scanning a maximum of %d ips per step" % num_ips)

    net_it = NetworkIterator(networks)

    # start the webserver
    loop.create_task(start_webserver(loop, database, webserver_address, webserver_port))
    #start the prometheus exporter
    loop.create_task(start_prometheus(loop, database, prometheus_address, prometheus_port))

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
