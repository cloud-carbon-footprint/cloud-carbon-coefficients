from abc import ABC, abstractmethod

import pandas as pd


class Coefficients(ABC):

    def __init__(self, instances):
        self.instances = instances
        self.architectures = instances['Microarchitecture'].unique()
        self._cpus_power = []

    @abstractmethod
    def _add_cpu(self, name, power):
        pass

    def create_coefficients(self, power):
        for architecture in self.architectures:
            if architecture in power:
                self._add_cpu(architecture, power[architecture])
            else:
                print('Missing: ' + architecture)

        return self._cpus_power

    @staticmethod
    def load_instances(file):
        return pd.read_csv(file, na_values=['NC'])
