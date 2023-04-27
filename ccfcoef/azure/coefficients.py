from ccfcoef.coefficients import Coefficients
from ccfcoef.cpu_power import CPUPower


class AzureCoefficients(Coefficients):

    @staticmethod
    def instantiate(file):
        return AzureCoefficients(Coefficients.load_instances(file))
