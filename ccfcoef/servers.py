class Servers:
    def __init__(self, servers):
        if len(servers[servers['CPU Description'].str.contains('Ghz')]) > 0:
            raise ValueError('Data not clean, servers contains Ghz')
        self.servers = servers
