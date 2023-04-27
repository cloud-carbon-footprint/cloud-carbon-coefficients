from ccfcoef.coefficients import Coefficients
from ccfcoef.constants import BASE_MANUFACTURING_EMISSIONS


class AzureCoefficients(Coefficients):

    def embodied_coefficients(self, cpus):
        instances_embodied = []

        for key, instance in self.instances.iterrows():
            # Call our calculation methods for each of the additional components
            additional_memory = self.additional_memory(
                instance['Platform Memory'])

            additional_storage = self.additional_storage(
                instance['Platform Storage Type'],
                instance['Platform (largest instance) Storage Drive quantity'])

            additional_cpus = self.additional_cpu(cpus, instance['Microarchitecture'])

            additional_gpus = self.additional_gpu(instance['Platform GPU'])

            # Build a dictionary of the instance emissions
            instances_embodied.append({
                'family': instance['Series'],
                'type': instance['Virtual Machine'],
                'microarchitecture': instance['Microarchitecture'],
                'additional_memory': round(additional_memory, 2),
                'additional_storage': round(additional_storage, 2),
                'additional_cpus': round(additional_cpus, 2),
                'additional_gpus': round(additional_gpus, 2),
                'total': round(
                    BASE_MANUFACTURING_EMISSIONS + additional_memory +
                    additional_storage + additional_cpus + additional_gpus,
                    2)
            })

        return instances_embodied


    @staticmethod
    def instantiate(file):
        return AzureCoefficients(Coefficients.load_instances(file))
