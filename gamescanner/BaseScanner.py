class BaseScanner:
    """
    This class is a base class for Scanners.
    This class does only provide the method headers for a specific implementation.
    A child class scanner has to offer a functionality which adds the results of
    the scan into the database.
    """

    def __init__(self, database):
        """
        Constructs a BaseScanner with the given database
        """
        self.database = database

    @staticmethod
    def packets_per_ip():
        """
        Returns the number of packets the scanner sends per IP it scans.
        This is used for rate limiting purposes.
        """
        raise NotImplementedError

    def scan(self, ip, ports=None):
        """
        Scans the given ip.
        If ports is given only the ports in this list are scanned
        """
        raise NotImplementedError
