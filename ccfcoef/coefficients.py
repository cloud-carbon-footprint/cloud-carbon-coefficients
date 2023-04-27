import pandas as pd

from ccfcoef.cpu_power import CPUPower


class Coefficients:

    def __init__(self, instances, filter_key='Microarchitecture'):
        self.instances = instances
        self.architectures = instances[filter_key].unique()
        self._cpus_power = []

    def add_cpu(self, name, power: CPUPower):
        self._cpus_power.append({
            'Architecture': name,
            'Min Watts': power.min_watts,
            'Max Watts': power.max_watts,
            'GB/chip': power.gb_chip
        })

    def create_coefficients(self, power):
        for architecture in self.architectures:
            if architecture in power:
                self.add_cpu(architecture, power[architecture])
            else:
                print('Missing: ' + architecture)

        return self._cpus_power

    @staticmethod
    def load_instances(file):
        return pd.read_csv(file, na_values=['NC'])
