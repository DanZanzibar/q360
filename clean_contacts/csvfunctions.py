import csv

def remove_entries(in_file: str, out_file: str, filter) -> None:
    with open(in_file, 'r', newline='') as file_read:
        reader = csv.reader(file_read)
        header = next(reader)
        with open(out_file, 'w', newline='') as file_write:
            writer = csv.writer(file_write)
            for row in reader:
                if filter(row): writer.writerow(row)

def column_is(row: list, col_index: int, col_value: str) -> bool:
    return row[col_index] == col_value

def column_is_not(row: list, col_index: int, col_value: str) -> bool:
    return row[col_index] != col_value

def column_starts_with(row: list[str], col_index: int, col_value: str) -> bool:
    return row[col_index].startswith(col_value)