from ccfcoef.coefficients import Coefficients
from ccfcoef.constants import CPU_MANUFACTURING_EMISSIONS, BASE_MANUFACTURING_EMISSIONS
from ccfcoef.cpu_power import CPUPower


class AWSCoefficients(Coefficients):

    def __init__(self, instances):
        """AWS uses a different header in its instances file"""
        super().__init__(instances, filter_key='Platform CPU Name')

    def use_coefficients(self, power):
        """
        AWS differs from Azure and GCP because it has a different CPU for Graviton and Graviton2
        and also the list we get from the aws_instances is filtered by the micro-architecture
        and not the families as the other providers. For this reason we need to find the family
        by looking at the CPU name list in CPUInfo.
        """
        for arch in self.architectures:

            arch = arch.replace('Xeon Platinum', '')
            arch = arch.replace('Xeon', '')
            arch = arch.strip()

            # This is another catch with AWS, we have the micro architecture but not the family so
            # we need to find it before asserting its power.
            arch = self.find_family_per_architecture(arch, power)

            if arch in power:
                self.add_cpu_power(arch, power[arch])
            elif arch in ['Graviton', 'Graviton2']:
                # We don't know the values for the Graviton chips so
                # assume they are the same spec as AMD EPYC Gen 2 but listed separately
                self.add_cpu_power(arch, power['EPYC 2nd Gen'])
            else:
                print('Missing: ' + arch)

        return self._cpus_power

    def additional_cpu(self, cpu_name):
        cpu = self.instances.query(f'`CPU Name` == \"{cpu_name}\"')
        sockets = int(cpu['Platform Number of CPU Socket(s)'].iloc[0])
        if sockets > 0:
            return float((sockets - 1) * CPU_MANUFACTURING_EMISSIONS)
        else:
            return 0.0

    @staticmethod
    def find_family_per_architecture(arch, power):
        for key, value in power.items():
            if arch in value.cpu_info.cpus:
                arch = key
                break
        return arch

    @staticmethod
    def instantiate(file):
        return AWSCoefficients(Coefficients.load_instances(file))
