from ccfcoef.constants import CPU_MANUFACTURING_EMISSIONS
from ccfcoef.embodied import Embodied


class AzureEmbodied(Embodied):
    def additional_cpu(self, cpu_name):
        cpus = self.cpus
        cpu = cpus.query(f'`Microarchitecture` == \"{cpu_name}\"')

        if int(cpu['CPU Sockets']) > 0:
            return float((int(cpu['CPU Sockets']) - 1) * CPU_MANUFACTURING_EMISSIONS)
        else:
            return 0.0
