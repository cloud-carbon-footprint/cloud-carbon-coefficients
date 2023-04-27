from ccfcoef.coefficients import *
from ccfcoef.constants import BASE_MANUFACTURING_EMISSIONS


class AzureCoefficients(Coefficients):

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
                'family': instance['Series'],
                'type': instance['Virtual Machine'],
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
    def instantiate(file):
        return AzureCoefficients(load_instances(file))
