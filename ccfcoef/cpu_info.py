class CPUInfo:
    def __init__(self, cpus):
        self.cpus = cpus
        self.cpu_re = [rf'\b{string}$' for string in self.cpus]

    def __iter__(self):
        return iter(self.cpus)

    @staticmethod
    def instantiate(file):
        with open(file, 'r') as f:
            cpus = [line.strip() for line in f.readlines()]
            return CPUInfo(cpus)
