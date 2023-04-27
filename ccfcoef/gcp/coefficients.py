from ccfcoef.coefficients import Coefficients


class GCPCoefficients(Coefficients):

    def add_cpu(self, name, power):
        """Add CPU for GCP differs from Azure and AWS because Max Watts is adjusted for GCP"""
        self._cpus_power.append({
            'Architecture': name,
            'Min Watts': power.min_watts,
            'Max Watts': power.max_watts_gcp_adjusted,
            'GB/chip': power.gb_chip
        })

    @staticmethod
    def instantiate(file):
        return GCPCoefficients(Coefficients.load_instances(file))
