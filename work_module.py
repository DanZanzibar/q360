import csv

def partial_search(customer, search_string, percent):
    search_length = int(len(customer) * (percent / 100))
    return customer[1:search_length] in search_string

def make_file_from_list(file_name, list):
    with open(f'work-data/{file_name}.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        for row in list:
            writer.writerow(row)

def get_list_from_csv(file_name):
    with open(f'work-data/{file_name}.csv', 'r', newline='') as file:
        reader = csv.reader(file)
        output_list = []
        for row in reader:
            output_list.append(row)
    return output_list

def get_list_from_txt(file_name):
    with open(f'work-data/{file_name}.txt', 'r') as file:
        return [line.strip() for line in file]

def combine_lists(list1, *lists):
    combined_list = []
    for list in lists:
        temp_list = list.copy()
        temp_list.pop(0)
        combined_list += temp_list
    return list1 + combined_list

def alpha_sort_list(list, column_to_search, order='ascending'):
    temp_list = list.copy()
    header = temp_list.pop(0)
    output_list = [header]
    column_index = header.index(column_to_search)
    count = 0
    for row in temp_list:
        inserted = False
        if count == 0:
            output_list.append(row)
            count += 1
        else:
            for entry in output_list:
                if entry != output_list[0]:
                    if order == 'ascending':
                        if row[column_index].lower() <= entry[column_index].lower():
                            output_list.insert(output_list.index(entry), row)
                            inserted = True
                            break
                    elif order == 'descending':
                        if row[column_index].lower() >= entry[column_index].lower():
                            output_list.insert(output_list.index(entry), row)
                            inserted = True
                            break
            if not inserted:
                output_list.append(row)
    return output_list

def filter_customers(starting_list, column_to_search, values_to_match, matching=True, strict=False):
    temp_list = starting_list.copy()
    header = temp_list.pop(0)
    group1 = [header]
    group2 = [header]
    column_index = header.index(column_to_search)
    for row in temp_list:
        match_found = False
        for value in values_to_match:
            if strict:
                if value == row[column_index]:
                    group1.append(row)
                    match_found = True
                    break
            else:
                if value.lower() in row[column_index].lower():
                    group1.append(row)
                    match_found = True
                    break
        if match_found == False:
            group2.append(row)
    if matching:
        return group1
    else:
        return group2

def format_raw_customer_file(file_name, output_file_name):
    with open(f'work-data/{file_name}.csv', 'r', newline='') as raw_file:
        reader = csv.reader(raw_file)
        header = next(reader)
        new_header = ['Customer No.', 'Company', 'Address', 'Address 2', 'City', 'State', 'Sub Type', 'Bookings YTD', 'Previous Years Bookings']
        index_to_keep = [header.index(title) for title in new_header]
        polished_list = [new_header]
        for row in reader:
            new_row = []
            for entry in index_to_keep:
                new_row.append(row[entry].strip())
            polished_list.append(new_row)
    make_file_from_list(output_file_name, polished_list)

def format_raw_bookings_file(file_name, output_file_name):
    with open(f'work-data/{file_name}.csv', 'r', newline='') as raw_file:
        reader = csv.reader(raw_file)
        header = next(reader)
        new_header = ['CUSTOMER', 'AVERAGE', 'QUOTA']
        index_to_keep = [header.index(title) for title in new_header]
        polished_bookings = [new_header]
        for row in reader:
            new_row = []
            for entry in index_to_keep:
                new_row.append(row[entry].strip())
            polished_bookings.append(new_row)
    make_file_from_list(output_file_name, polished_bookings)

def add_bookings_data(customers_file_name, bookings_file_name, output_file_name):
    with open(f'work-data/{customers_file_name}.csv', 'r', newline='') as outside_customers_file:
        outside_reader = csv.reader(outside_customers_file)
        header = next(outside_reader)
        new_header = header + ['5Y Average']
        customers_with_no_matches = [new_header]
        customers_with_matches = [new_header]
        for row in outside_reader:
            with open(f'work-data/{bookings_file_name}.csv', 'r', newline='') as bookings_file:
                sales = []
                bookings_reader = csv.reader(bookings_file)
                for row2 in bookings_reader:
                    if (partial_search(row[1], row2[0], 80)):
                        sales.append(row2[1])
                if (sales == []):
                    customers_with_no_matches.append(row + ['no match'])
                else:
                    max_sales = max(sales)
                    customers_with_matches.append(row + [max_sales])
        make_file_from_list(output_file_name, alpha_sort_list(combine_lists(customers_with_matches, customers_with_no_matches), 'Company'))