#!/usr/bin/env python3

from time import time

class Database():

    def __init__(self, prune_time=300, prune_interval=30):
        """ Constructs a new Database.
        The prune_time parameters it the time after how many seconds a entry
        is removed from the database.
        The prune_interval parameter specifies how much time at least between
        prune steps."""
        self.db = list()
        self.prune_time = prune_time
        self.prune_interval = prune_interval
        self.last_prune = time()

    def add(self, data):
        """ add data to the database """
        for i in range(len(self.db)):
            server = self.db[i]
            if server["ip"] == data["ip"] and \
                    server["port"] == data["port"]:
                # server is in database
                # update the server
                self.db[i] = data
                return
        self.db.append(data)
        self._prune()

    def dump(self):
        """ returns the whole database content as a list"""
        self._prune()
        return self.db

    def _prune(self):
        """prunes the database"""
        current_time = time()
        if current_time - self.last_prune > self.prune_interval:
            print("time for pruning everything older than %d seconds" % self.prune_time)
            self.db = [x for x in self.db
                    if (x["timestamp"] - current_time) <= self.prune_time]
            self.last_prune = current_time
