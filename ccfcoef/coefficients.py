from abc import abstractmethod

import pandas as pd

from ccfcoef.constants import DRAM_THRESHOLD, DRAM_MANUFACTURING_EMISSIONS, SSD_MANUFACTURING_EMISSIONS, \
    HDD_MANUFACTURING_EMISSIONS, GPU_MANUFACTURING_EMISSIONS, CPU_MANUFACTURING_EMISSIONS
from ccfcoef.cpu_power import CPUPower


class Coefficients:

    def __init__(self, instances, filter_key='Microarchitecture'):
        self.instances = instances
        self.architectures = instances[filter_key].unique()
        self._cpus_power = []

    def add_cpu_power(self, name, power: CPUPower):
        self._cpus_power.append(
            cpu_power(name, power.min_watts, power.max_watts, power.gb_chip)
        )

    def use_coefficients(self, power):
        for architecture in self.architectures:
            if architecture in power:
                self.add_cpu_power(architecture, power[architecture])
            else:
                print('Missing: ' + architecture)

        return self._cpus_power


def cpu_power(architecture, min_watts, max_watts, gb_chip):
    return {
        'Architecture': architecture,
        'Min Watts': min_watts,
        'Max Watts': max_watts,
        'GB/Chip': gb_chip
    }


def additional_memory(platform_memory):
    """If the platform memory is greater than the baseline, calculate the
    additional emissions."""

    if float(platform_memory) > DRAM_THRESHOLD:
        additional_emissions = float(
            (float(platform_memory) - DRAM_THRESHOLD) * (
                    DRAM_MANUFACTURING_EMISSIONS / DRAM_THRESHOLD))
    else:
        additional_emissions = 0.0

    return additional_emissions


def load_instances(file):
    return pd.read_csv(file, na_values=['NC'])


def additional_cpu(cpus, cpu_name):
    cpu = cpus.query(f'`Microarchitecture` == \"{cpu_name}\"')
    sockets = int(cpu['CPU Sockets'].iloc[0])
    if sockets > 0:
        return float((sockets - 1) * CPU_MANUFACTURING_EMISSIONS)
    else:
        return 0.0


def additional_gpu(gpu_quantity):
    """Calculate additional emissions for any GPUs."""

    if gpu_quantity > 0:
        return float(gpu_quantity * GPU_MANUFACTURING_EMISSIONS)
    else:
        return 0.0


def additional_storage(storage_type, drive_quantity):
    """Calculate additional emissions for storage, depending on the storage
    type."""

    if drive_quantity <= 0:
        return 0.0

    if storage_type.lower() == 'ssd':
        factor = SSD_MANUFACTURING_EMISSIONS
    else:
        factor = HDD_MANUFACTURING_EMISSIONS

    return float(drive_quantity * factor)
