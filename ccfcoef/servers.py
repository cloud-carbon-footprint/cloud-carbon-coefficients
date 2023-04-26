import re

import pandas as pd
from regex import regex

from ccfcoef.constants import MEMORY_COEFFICIENT


class Servers:
    def __init__(self, servers):
        if len(servers[servers['CPU Description'].str.contains('Ghz')]) > 0:
            raise ValueError('Data not clean, servers contains Ghz')
        self.servers = servers

    def idle_watts(self):
        return (self.servers['avg. watts @ active idle'].astype(float) / self.servers['Total Threads']).mean()

    def max_watts(self):
        return (self.servers['avg. watts @ 100%'].astype(float) / self.servers['Total Threads']).mean()

    def gb_chip(self):
        return (self.servers['Total Memory (GB)'] / self.servers['Chips']).mean()

    def total_memory(self):
        return self.servers['Total Memory (GB)']

    def max_watts_gcp_adjusted(self):
        return (self.max_watts() - (self.total_memory() * MEMORY_COEFFICIENT)).mean()


    @staticmethod
    def instantiate(file_name, re_list):
        servers = pd.read_csv(file_name, na_values=['NC'])
        full_re = re.compile('|'.join(re_list), re.I)  # re changed in 3.11, globals need to be defined only once
        filtered_servers = servers[servers['CPU Description'].str.contains(full_re)]
        return Servers(filtered_servers)
