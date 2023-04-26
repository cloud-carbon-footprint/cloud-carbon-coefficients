class CPUInfo:
    def __init__(self, cpus):
        self.cpus = cpus
        self.cpu_re = [rf'\b{string}$' for string in self.cpus]

    @staticmethod
    def instantiate(file_name):
        with open(file_name, 'r') as f:
            cpus = [line.strip() for line in f.readlines()]
            return CPUInfo(cpus)