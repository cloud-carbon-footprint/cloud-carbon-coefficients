from abc import ABC, abstractmethod

import ccfcoef.constants as const


class Embodied(ABC):

    def __init__(self, cpus):
        self.cpus = cpus

    @staticmethod
    def additional_memory(platform_memory):
        """If the platform memory is greater than the baseline, calculate the
        additional emissions."""

        if float(platform_memory) > const.DRAM_THRESHOLD:
            additional_emissions = float(
                (float(platform_memory) - const.DRAM_THRESHOLD) * (
                        const.DRAM_MANUFACTURING_EMISSIONS / const.DRAM_THRESHOLD))
        else:
            additional_emissions = 0.0

        return additional_emissions

    @staticmethod
    def additional_storage(storage_type, drive_quantity):
        """Calculate additional emissions for storage, depending on the storage
        type."""

        if drive_quantity <= 0:
            return 0.0

        if storage_type.lower() == 'ssd':
            factor = const.SSD_MANUFACTURING_EMISSIONS
        else:
            factor = const.HDD_MANUFACTURING_EMISSIONS

        return float(drive_quantity * factor)

    @staticmethod
    def additional_gpu(gpu_quantity):
        """Calculate additional emissions for any GPUs."""

        if gpu_quantity > 0:
            return float(gpu_quantity * const.GPU_MANUFACTURING_EMISSIONS)
        else:
            return 0.0

    @abstractmethod
    def additional_cpu(self, cpu_name):
        pass
