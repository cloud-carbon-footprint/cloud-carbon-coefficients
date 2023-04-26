from ccfcoef.coefficients import Coefficients
from ccfcoef.cpu_power import CPUPower


class AzureCoefficients(Coefficients):

    def __init__(self, instances):
        super().__init__(instances)

    def _add_cpu(self, name, power: CPUPower):
        self._cpus_power.append({
            'Architecture': name,
            'Min Watts': power.min_watts,
            'Max Watts': power.max_watts,
            'GB/chip': power.gb_chip
        })

    @staticmethod
    def instantiate(file):
        return AzureCoefficients(Coefficients.load_instances(file))
