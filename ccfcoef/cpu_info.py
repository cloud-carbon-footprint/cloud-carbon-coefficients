import csv


class CPUInfo:
    def __init__(self, cpus):
        self.cpus = cpus
        self.cpu_re = [rf'\b{string}$' for string in cpus]


def load_append_list(file_name):
    """Loads a CSV file then returns each row appended to a list."""
    with open(file_name, 'r') as csvfile:
        reader = csv.reader(csvfile)
        data = []
        for row in reader:
            data.append(row[0])
        return data
