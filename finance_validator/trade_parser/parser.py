import csv
from datetime import datetime

def process_csv_file(csv_file) -> list[str]:
    trade_data = []
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        # next(reader, None)
        for row in reader:
            trade_data.append(row)
    return trade_data
            