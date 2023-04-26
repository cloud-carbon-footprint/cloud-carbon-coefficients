from ccfcoef.constants import CPU_MANUFACTURING_EMISSIONS
from ccfcoef.emissions import Emissions


class AWSEmissions(Emissions):

    def additional_cpu(self, cpu_name):
        cpu = self.cpus.query(f'`CPU Name` == \"{cpu_name}\"')

        if int(cpu['Platform Number of CPU Socket(s)']) > 0:
            return float((int(cpu['Platform Number of CPU Socket(s)']) - 1) * CPU_MANUFACTURING_EMISSIONS)
        else:
            return 0.0
