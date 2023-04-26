import csv


def load_append_list(file_name):
    """Loads a CSV file then returns each row appended to a list."""
    with open(f'data/{file_name}', 'r') as csvfile:
        reader = csv.reader(csvfile)
        data = []
        for row in reader:
            data.append(row[0])
        return data
