import re

import pandas as pd

from ccfcoef.constants import MEMORY_COEFFICIENT
from ccfcoef.cpu_info import CPUInfo
from ccfcoef.family import Family


class SPECPower:
    def __init__(self, servers):
        cpu_desc_check = servers[servers['CPU Description'].str.contains(r'\bghz\b', case=False)]
        if len(cpu_desc_check) > 0:
            cpu_desc_check.to_csv('invalid_cpu_descriptions.csv')
            raise ValueError('Data not clean, servers contains Ghz, check: invalid_cpu_descriptions.csv')
        self.servers = servers

    def get_cpu_power(self, cpu: CPUInfo):
        return SPECPower.CPUPower(self.filter_by_cpu(cpu))

    def filter_by_cpu(self, cpu: CPUInfo):
        full_re = re.compile('|'.join(cpu.cpu_re), re.I)  # re changed in 3.11, globals need to be defined only once
        return self.servers[self.servers['CPU Description'].str.contains(full_re)]

    def tag_cpu_family(self, cpus: dict[Family, CPUInfo]):
        for family, info in cpus.items():
            self.servers.loc[self.filter_by_cpu(info).index, 'CPU Microarchitecture'] = family.name
        return self.servers

    class CPUPower:

        def __init__(self, servers):
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
    def instantiate(file_name):
        servers = pd.read_csv(file_name, na_values=['NC'])
        return SPECPower(servers)
