# the number of packets send per second
rate = 1000

database_settings = {
        "prune_interval" : 10, #how many seconds between a prune
        "prune_time" : 30 # how old entries have to be to be pruned
        }

webserver_address = "127.0.0.1"
webserver_port = 9001
prometheus_address = "127.0.0.1"
prometheus_port = 9002

networks = [
        #"216.52.148.47",
        #"89.163.189.0/24",
        #"89.40.105.235",
        #"193.19.119.197",
        #"46.174.49.219",
        #"45.76.94.34",
        ##"85.10.203.89/24"
        #"85.10.203.0/24"
        "216.52.148.0/23",
        "89.163.189.0/24",
        "89.40.105.0/24",
        "193.19.119.0/24",
        "46.174.49.0/24",
        "45.76.94.0/23",
        #"85.10.203.89/24"
        "85.10.203.0/24"
        ]
