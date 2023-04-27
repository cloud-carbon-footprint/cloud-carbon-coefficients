from ccfcoef.coefficients import *
from ccfcoef.constants import BASE_MANUFACTURING_EMISSIONS


class GCPCoefficients(Coefficients):

    def embodied_coefficients(self, cpus):
        instances_embodied = []

        for key, instance in self.instances.iterrows():
            # Call our calculation methods for each of the additional components
            add_memory = additional_memory(
                instance['Platform Memory'])

            add_storage = additional_storage(
                instance['Platform Storage Type'],
                instance['Platform (largest instance) Storage Drive quantity'])

            additional_cpus = additional_cpu(cpus, instance['Microarchitecture'])

            additional_gpus = additional_gpu(instance['Platform GPU'])

            # Build a dictionary of the instance emissions
            instances_embodied.append({
                'family': instance['Machine Family'],
                'type': instance['Machine type'],
                'microarchitecture': instance['Microarchitecture'],
                'additional_memory': round(add_memory, 2),
                'additional_storage': round(add_storage, 2),
                'additional_cpus': round(additional_cpus, 2),
                'additional_gpus': round(additional_gpus, 2),
                'total': round(
                    BASE_MANUFACTURING_EMISSIONS + add_memory +
                    add_storage + additional_cpus + additional_gpus,
                    2)
            })
        return instances_embodied

    @staticmethod
    def embodied_coefficients_mean(embodied_coefficients):
        # Second iteration to aggregate by instance type and output the mean
        instance_types = embodied_coefficients.drop_duplicates(subset="type")

        embodied_mean = []
        for key, instance in instance_types.iterrows():
            instance_type = str(instance['type'])
            result = embodied_coefficients.query(f'`type` == "{instance_type}"')
            embodied_mean.append({
                'type': instance_type,
                'total_mean': result['total'].mean()})

        return embodied_mean

    def add_cpu_power(self, name, power):
        """Add CPU for GCP differs from Azure and AWS because Max Watts is adjusted for GCP"""
        self._cpus_power.append(
            cpu_power(name, power.min_watts, power.max_watts_gcp_adjusted, power.gb_chip)
        )

    @staticmethod
    def instantiate(file):
        return GCPCoefficients(load_instances(file))
